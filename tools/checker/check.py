#!/usr/bin/env python3
"""lailai-skill 风格 checker：把可机械判定的规则从「模型记得」变成「机器验」。

分两级：ERROR（确定性、近零误报，hook 会退出 2 打回）/ WARN（启发式，仅提示）。
规则溯源见同目录 README.md 的「规则 → reference」对照表。

用法：
    python3 check.py <file>...                # CLI，逐条打印，含 ERROR 则退出 1
    python3 check.py --hook                   # PostToolUse-compatible hook（读 stdin JSON）
    python3 check.py --commit <msgfile>       # 校验一条 commit message
    开关：--no-aitone --no-cjk-space --no-sentence --errors-only --quiet

忽略：文件内任一行含 `lailai-checker: disable` → 跳过整个文件；
      某行含 `checker-ignore` → 跳过该行的违规。
"""

import json
import os
import re
import subprocess
import sys

# ---------------------------------------------------------------------------
# 违规收集
# ---------------------------------------------------------------------------


class Issue:
    def __init__(self, path, line, level, rule, msg):
        self.path = path
        self.line = line
        self.level = level  # "ERROR" | "WARN"
        self.rule = rule
        self.msg = msg

    def format(self):
        return "{}:{}: [{} {}] {}".format(
            self.path, self.line, self.level, self.rule, self.msg
        )


CJK = r"一-鿿㐀-䶿"
CJK_RE = re.compile("[" + CJK + "]")


# ---------------------------------------------------------------------------
# Markdown / MDX 分区：把每一行标成 prose / mathspan / code，保留行号
# ---------------------------------------------------------------------------


def segment_markdown(lines):
    """返回三张表，元素均为 (lineno, text)：
    prose_spans   —— 散文片段（已剔除行内 code 与行内 math）
    math_spans    —— 数学内容（行内 $...$ 与行间 $$...$$）
    cpp_blocks    —— [(start_lineno, [代码行...])]，来自 ```cpp / ```c++ fence
    另外返回 has_frontmatter（首行 --- 判定）。
    """
    prose, math, cpp_blocks = [], [], []
    in_fence = False
    fence_lang = ""
    fence_buf = []
    fence_start = 0
    in_disp_math = False
    has_frontmatter = False

    # frontmatter：首行恰为 --- 到下一个 ---
    start = 0
    if lines and lines[0].strip() == "---":
        has_frontmatter = True
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break

    i = start
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        lineno = i + 1

        fence_open = re.match(r"^\s*(`{3,}|~{3,})\s*([A-Za-z0-9+#.-]*)", raw)
        if not in_fence and fence_open:
            in_fence = True
            fence_lang = fence_open.group(2).lower()
            fence_buf = []
            fence_start = lineno
            i += 1
            continue
        if in_fence:
            if re.match(r"^\s*(`{3,}|~{3,})\s*$", raw):
                if fence_lang in ("cpp", "c++", "cc", "cxx"):
                    cpp_blocks.append((fence_start + 1, fence_buf))
                in_fence = False
                fence_lang = ""
            else:
                fence_buf.append((lineno, raw))
            i += 1
            continue

        # 行间数学：单独成行的 $$
        if stripped == "$$":
            in_disp_math = not in_disp_math
            i += 1
            continue
        if in_disp_math:
            math.append((lineno, raw))
            i += 1
            continue

        # 普通散文行：抽出行内 code 与行内 math，其余归 prose
        prose_text, inline_math = split_inline(raw)
        for m in inline_math:
            math.append((lineno, m))
        prose.append((lineno, prose_text))
        i += 1

    return prose, math, cpp_blocks, has_frontmatter


def split_inline(text):
    """剔除行内 code（反引号）与行内 math（$...$），返回 (散文, [数学片段])。"""
    math_parts = []
    out = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == "`":
            j = i + 1
            while j < n and text[j] == "`":
                j += 1
            ticks = text[i:j]
            end = text.find(ticks, j)
            if end == -1:
                out.append(" " * (n - i))
                break
            out.append(" " * (end + len(ticks) - i))
            i = end + len(ticks)
            continue
        if c == "$":
            if i + 1 < n and text[i + 1] == "$":  # 行内 $$...$$（少见）
                end = text.find("$$", i + 2)
                if end != -1:
                    math_parts.append(text[i + 2 : end])
                    out.append(" " * (end + 2 - i))
                    i = end + 2
                    continue
            if i > 0 and text[i - 1] == "\\":  # 转义 \$
                out.append(c)
                i += 1
                continue
            end = text.find("$", i + 1)
            if end != -1 and end > i + 1:
                math_parts.append(text[i + 1 : end])
                out.append(" " * (end + 1 - i))
                i = end + 1
                continue
        out.append(c)
        i += 1
    return "".join(out), math_parts


# ---------------------------------------------------------------------------
# 数学检查（在 math span 内）
# ---------------------------------------------------------------------------

MATH_ERROR_PATTERNS = [
    (re.compile(r"\\dfrac"), "math-dfrac", r"用 \frac，不用 \dfrac"),
    (re.compile(r"\\emptyset"), "math-emptyset", r"空集用 \varnothing，不用 \emptyset"),
    (re.compile(r"\\cdots|\\ldots"), "math-dots", r"横向省略号用 \dots，不用 \cdots / \ldots"),
    (
        re.compile(r"\\(?:quad|qquad|,|;|:|!)(?![A-Za-z])|\\ "),
        "math-manual-space",
        r"禁用手动间距 \, \; \: \! \quad \qquad 与反斜杠空格，交给 KaTeX",
    ),
]

MATH_UNICODE = {
    "×": r"\times",
    "−": "-",
    "÷": r"\div",
    "°": r"^\circ",
    "～": r"\sim",
    "〜": r"\sim",
    "≤": r"\le",
    "≥": r"\ge",
    "≠": r"\ne",
}

TEXT_WRAP_RE = re.compile(r"\\(?:text|texttt|textbf|textit|operatorname|mathrm|mbox)\s*\{[^{}]*\}")
FRAC_BAD_RE = re.compile(r"\\frac\s*(?:[^{\s]|\{[^{}]*\}\s*[^{\s])")
STRUCTURAL_CJK_RE = re.compile(r"\\text\{[^{}]*(?:且|或|其余|否则)[^{}]*\}")


def check_math(path, math_spans, disabled_lines, issues):
    for lineno, text in math_spans:
        if lineno in disabled_lines:
            continue
        for rx, rule, msg in MATH_ERROR_PATTERNS:
            if rx.search(text):
                issues.append(Issue(path, lineno, "ERROR", rule, msg))
        for ch, repl in MATH_UNICODE.items():
            if ch in text:
                issues.append(
                    Issue(path, lineno, "ERROR", "math-unicode",
                          "公式内不用 Unicode 符号 '{}'，写 {}".format(ch, repl))
                )
        # 裸中文（剔除 \text{...} 等包裹后仍有 CJK）
        bare = TEXT_WRAP_RE.sub("", text)
        if CJK_RE.search(bare):
            issues.append(
                Issue(path, lineno, "WARN", "math-bare-cjk", r"公式内裸中文，套 \text{}")
            )
        # \frac 分子/分母未带花括号
        if FRAC_BAD_RE.search(text):
            issues.append(
                Issue(path, lineno, "WARN", "math-frac-brace",
                      r"\frac 分子分母都带花括号（\frac{a}{b}，非 \frac12 / \frac s2）")
            )
        if STRUCTURAL_CJK_RE.search(text):
            issues.append(
                Issue(path, lineno, "ERROR", "math-structural-cjk",
                      r"公式内结构标签用英文或逻辑符号，不写 \text{且/或/其余/否则}")
            )


# ---------------------------------------------------------------------------
# 数学分隔符（在原始行上：\( \) \[ \]）
# ---------------------------------------------------------------------------

DELIM_RE = re.compile(r"\\[\(\)\[\]]")


def check_math_delims(path, lines, code_line_set, disabled_lines, issues):
    for idx, raw in enumerate(lines):
        lineno = idx + 1
        if lineno in code_line_set or lineno in disabled_lines:
            continue
        prose, _ = split_inline(raw)
        if DELIM_RE.search(prose):
            issues.append(
                Issue(path, lineno, "ERROR", "math-delim",
                      r"数学分隔符统一用 $...$ / $$...$$，不用 \(...\) / \[...\]")
            )


MATH_TERMINAL_RE = re.compile(r"[.,，。;；:：]$")
MATH_ENV_RE = re.compile(r"\\(?:begin|end)\{[A-Za-z*]+\}")
MATH_ROW_BREAK_RE = re.compile(r" \\\\(?:\[[^]]+\])?$")


def check_display_math(path, lines, code_line_set, disabled_lines, issues):
    """检查行间公式及其上下文中完全由版面决定的硬规则。"""
    in_fence = False
    fence_mark = ""
    start = None
    for idx, raw in enumerate(lines):
        stripped = raw.strip()
        fence = re.match(r"^\s*(`{3,}|~{3,})", raw)
        if fence:
            mark = fence.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_mark = mark
            elif mark == fence_mark:
                in_fence = False
                fence_mark = ""
            continue
        if in_fence or stripped != "$$":
            continue
        if start is None:
            start = idx
            prev = idx - 1
            while prev >= 0 and not lines[prev].strip():
                prev -= 1
            if prev < 0 or not lines[prev].rstrip().endswith("："):
                issues.append(
                    Issue(path, idx + 1, "ERROR", "math-display-intro",
                          "行间公式前一行散文必须以全角冒号结尾")
                )
            continue

        body = [(line_idx, lines[line_idx]) for line_idx in range(start + 1, idx)]
        env_depth = 0
        env_rows = []
        for line_idx, line in body:
            if line_idx + 1 in disabled_lines or not line.strip():
                continue
            clean = line.strip()
            envs = MATH_ENV_RE.findall(clean)
            if envs and not (len(envs) == 1 and clean == envs[0]):
                issues.append(
                    Issue(path, line_idx + 1, "ERROR", "math-environment-line",
                          r"\begin / \end 必须各自单独成行")
                )
            if re.search(r"(?<!\s)&|&(?!\s)", line):
                issues.append(
                    Issue(path, line_idx + 1, "ERROR", "math-align-space",
                          "对齐符 & 两侧各留一个空格")
                )
            terminal = MATH_ROW_BREAK_RE.sub("", clean)
            if MATH_TERMINAL_RE.search(terminal) and not terminal.endswith(r"\right."):
                issues.append(
                    Issue(path, line_idx + 1, "ERROR", "math-display-terminal",
                          "行间公式内容与各分支末尾不加句读")
                )
            if clean.startswith(r"\begin{"):
                env_depth += 1
                env_rows = []
                continue
            if clean.startswith(r"\end{"):
                if env_rows:
                    for row_idx, (row_line_idx, row) in enumerate(env_rows):
                        has_break = bool(MATH_ROW_BREAK_RE.search(row.rstrip()))
                        if row_idx + 1 < len(env_rows) and not has_break:
                            issues.append(
                                Issue(path, row_line_idx + 1, "ERROR",
                                      "math-environment-break", r"多行公式的非末分支以空格加 \\ 结尾")
                            )
                        if row_idx + 1 == len(env_rows) and has_break:
                            issues.append(
                                Issue(path, row_line_idx + 1, "ERROR",
                                      "math-environment-break", "多行公式的末分支不写 \\")
                            )
                env_depth = max(0, env_depth - 1)
                env_rows = []
                continue
            if env_depth:
                if not line.startswith("  ") or line.startswith("   "):
                    issues.append(
                        Issue(path, line_idx + 1, "ERROR", "math-environment-indent",
                              "多行公式的每个分支严格缩进 2 个空格")
                    )
                env_rows.append((line_idx, line))
        start = None


# ---------------------------------------------------------------------------
# 散文 AI 腔 / 用词
# ---------------------------------------------------------------------------

AITONE_ERROR = [
    ("本文将", "套话预告，直接进入主题"),
    ("在本文中", "套话预告，直接进入主题"),
    ("众所周知", "空泛，给具体定义或事实"),
    ("让我们深入探讨", "综艺腔，直接展开"),
    ("一探究竟", "综艺腔，直接展开"),
    ("综上所述", "凑总结，技术内容自然收尾"),
    ("总而言之", "凑总结，技术内容自然收尾"),
    ("希望本文对你有所帮助", "模板化收尾，删掉"),
    ("希望对你有所帮助", "模板化收尾，删掉"),
    ("希望这篇", "模板化收尾，删掉"),
    ("作为一个 AI", "暴露模板，不自我指涉"),
    ("作为一个AI", "暴露模板，不自我指涉"),
    ("这是一个很好的问题", "套话开场，直接回答"),
    ("这是一个非常好的问题", "套话开场，直接回答"),
    ("显而易见", "空泛，给具体依据"),
    ("不难发现", "跳过推理，写清那一步或省去"),
    ("不难看出", "跳过推理，写清那一步或省去"),
    ("显然", "跳过推理，写清那一步或省去（lailai 明确禁用）"),
    ("易得", "跳过推理，写清那一步或省去（lailai 明确禁用）"),
]

AITONE_WARN = [
    ("值得注意的是", "填充词，直接说那件事"),
    ("需要指出的是", "填充词，直接说那件事"),
    ("需要注意的是", "填充词，直接说那件事"),
    ("在当今", "万能空话开头，删掉"),
    ("赋能", "营销黑话，用普通话说清"),
    ("抓手", "营销黑话，用普通话说清"),
    ("颗粒度", "营销黑话，用普通话说清"),
    ("闭环", "营销黑话，用普通话说清"),
    ("强大而优雅", "形容词堆叠，说具体好在哪"),
    ("简洁而现代", "形容词堆叠，说具体好在哪"),
]


def check_aitone(path, prose_spans, disabled_lines, issues):
    for lineno, text in prose_spans:
        if lineno in disabled_lines:
            continue
        for phrase, why in AITONE_ERROR:
            if phrase in text:
                issues.append(Issue(path, lineno, "ERROR", "aitone", "「{}」——{}".format(phrase, why)))
        for phrase, why in AITONE_WARN:
            if phrase in text:
                issues.append(Issue(path, lineno, "WARN", "aitone", "「{}」——{}".format(phrase, why)))


# ---------------------------------------------------------------------------
# 排版：弯引号 / emoji / 日期 / 中英空格 / 句长
# ---------------------------------------------------------------------------

CURLY = {"“": "「", "”": "」", "‘": "『", "’": "』"}
EMOJI_RE = re.compile(
    "[\U0001f000-\U0001faff\U00002600-\U000027bf\U0001f1e6-\U0001f1ff⬀-⯿️]"
)
DATE_SLASH_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}\s*/\s*\d{1,2}\s*/\s*\d{1,2}(?!\d)")
DATE_DOT_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}\.\d{1,2}\.\d{1,2}(?!\d)")
CLOCK_AMPM_RE = re.compile(r"\b\d{1,2}\s*[ap]\.?m\.?\b", re.IGNORECASE)
CJK_LATIN_RE = re.compile("[" + CJK + "][A-Za-z]|[A-Za-z][" + CJK + "]")
SENT_SPLIT_RE = re.compile(r"[。！？；]")


def check_typography(path, prose_spans, disabled_lines, opts, issues):
    is_readme = os.path.basename(path).lower().startswith("readme")
    for lineno, text in prose_spans:
        if lineno in disabled_lines:
            continue
        for ch, repl in CURLY.items():
            if ch in text:
                issues.append(
                    Issue(path, lineno, "WARN", "curly-quote",
                          "弯引号 '{}' → 直角引号 {}（强调用加粗）".format(ch, repl))
                )
                break
        if not is_readme and EMOJI_RE.search(text):
            issues.append(Issue(path, lineno, "WARN", "emoji", "正文避免 emoji（仅 README 特性区可用）"))
        if DATE_SLASH_RE.search(text) or DATE_DOT_RE.search(text):
            issues.append(
                Issue(path, lineno, "WARN", "date-format",
                      "日期用 2025-09-16 / 2025 年 9 月 16 日 / September 16, 2025，不用斜杠 / 点分")
            )
        if CLOCK_AMPM_RE.search(text):
            issues.append(Issue(path, lineno, "WARN", "time-format", "时间用 24h HH:MM:SS，不用 a.m./p.m."))
        if opts["cjk_space"]:
            m = CJK_LATIN_RE.search(text)
            if m:
                issues.append(
                    Issue(path, lineno, "WARN", "cjk-latin-space",
                          "中文与英文之间加空格（如 GitHub 项目）：…{}…".format(m.group(0)))
                )
        if opts["sentence"]:
            for seg in SENT_SPLIT_RE.split(text):
                seg = seg.strip()
                if not seg:
                    continue
                cjk = len(CJK_RE.findall(seg))
                if cjk >= len(seg) * 0.5 and len(seg) > 40:
                    issues.append(
                        Issue(path, lineno, "WARN", "sentence-length",
                              "句子 {} 字，超过 40 字建议值，可酌情拆短".format(len(seg)))
                    )
                    break


# ---------------------------------------------------------------------------
# Markdown 结构：标题空行 / 一级标题 / 行尾空格 / 连续空行
# ---------------------------------------------------------------------------

HEADING_RE = re.compile(r"^(#{1,6})\s+\S")


def check_md_structure(path, lines, has_frontmatter, code_line_set, disabled_lines, issues):
    blank_run = 0
    for idx, raw in enumerate(lines):
        lineno = idx + 1
        in_code = lineno in code_line_set
        if raw.rstrip("\n").rstrip() != raw.rstrip("\n") and not in_code:
            if lineno not in disabled_lines:
                issues.append(Issue(path, lineno, "WARN", "trailing-space", "行尾多余空格"))
        if raw.strip() == "":
            blank_run += 1
            if blank_run == 2 and not in_code and lineno not in disabled_lines:
                issues.append(Issue(path, lineno, "WARN", "blank-lines", "不连续用 2 个空行"))
        else:
            blank_run = 0
        if in_code:
            continue
        m = HEADING_RE.match(raw)
        if m and lineno not in disabled_lines:
            if has_frontmatter and len(m.group(1)) == 1:
                issues.append(Issue(path, lineno, "WARN", "h1", "站点正文不用一级标题，最高 ##"))
            nxt = lines[idx + 1] if idx + 1 < len(lines) else ""
            if nxt.strip() != "":
                issues.append(Issue(path, lineno, "ERROR", "heading-blank", "标题与正文之间需空一行"))
            if raw.rstrip().endswith(("。", "，", "；", "：", ".", ",", ";")):
                issues.append(Issue(path, lineno, "WARN", "heading-punct", "标题结尾不加标点"))


# ---------------------------------------------------------------------------
# README 项目规范：语言导航 / 正式项目名 / 结构树 / License
# ---------------------------------------------------------------------------

PROJECT_STRUCTURE_HEADINGS = {"## Project Structure", "## 项目结构"}
TREE_ENTRY_RE = re.compile(r"^(?P<prefix>(?:│   |    )*)(?:├── |└── )(?P<name>.+)$")
PROJECT_TITLE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROJECT_TITLE_EXCEPTIONS = {"lailai-template"}
MIT_LICENSE_URL = "https://github.com/lailai0916/tools/blob/main/LICENSE"
MIT_LICENSE_SENTENCE = (
    "This project's code is licensed under "
    "[MIT License]({}).".format(MIT_LICENSE_URL)
)
MIT_LICENSE_SENTENCE_ZH = "本项目代码采用 [MIT 许可协议]({})。".format(MIT_LICENSE_URL)
README_LANGUAGE_LINK_RE = re.compile(
    r'^<a href="README(?:\.[A-Za-z][A-Za-z0-9-]*)?\.md">[^<>]+</a>$'
)
README_LANGUAGE_CURRENT_RE = re.compile(r"^<strong>[^<>]+</strong>$")
README_CURRENT_LANGUAGES = {
    "README.md": "English",
    "README.zh-Hans.md": "简体中文",
    "README.zh-Hant.md": "繁體中文",
    "README.ja.md": "日本語",
    "README.ko.md": "한국어",
    "README.es.md": "Español",
    "README.fr.md": "Français",
    "README.ru.md": "русский",
}


def is_common_tree_entry(name):
    clean = name.split(" -> ", 1)[0].rstrip("/")
    base = clean.rsplit("/", 1)[-1]
    return (
        clean in (".agents", ".claude")
        or clean.startswith((".agents/", ".claude/"))
        or base.startswith(("README", "LICENSE"))
        or base in (
            ".gitignore",
            ".gitattributes",
            ".gitmodules",
            "AGENTS.md",
            "CLAUDE.md",
        )
    )


def check_project_tree(path, block, disabled_lines, issues):
    entries = []
    for lineno, raw in block:
        if not raw.strip():
            continue
        left = raw.split("#", 1)[0].rstrip()
        m = TREE_ENTRY_RE.match(left)
        if not m:
            continue
        name = m.group("name").strip()
        level = len(m.group("prefix")) // 4
        is_dir = name.split(" -> ", 1)[0].endswith("/")
        entries.append(
            {"line": lineno, "raw": raw, "name": name, "level": level, "is_dir": is_dir}
        )
        if "#" not in raw and lineno not in disabled_lines:
            issues.append(
                Issue(path, lineno, "ERROR", "project-tree-comment", "项目结构每个条目都要有行末注释")
            )
        if is_common_tree_entry(name) and lineno not in disabled_lines:
            issues.append(
                Issue(
                    path,
                    lineno,
                    "ERROR",
                    "project-tree-common",
                    "项目结构不列 README、LICENSE、.git*、.agents、.claude 等通用条目",
                )
            )
        entry_path = name.split(" -> ", 1)[0].rstrip("/")
        if any(ord(ch) > 127 for ch in entry_path) and lineno not in disabled_lines:
            issues.append(
                Issue(path, lineno, "ERROR", "project-tree-filename", "项目路径使用英文 ASCII 名称")
            )

    if entries:
        width = 32
        for entry in entries:
            if "#" not in entry["raw"] or entry["line"] in disabled_lines:
                continue
            actual = entry["raw"].index("#")
            if actual != width:
                issues.append(
                    Issue(
                        path,
                        entry["line"],
                        "ERROR",
                        "project-tree-align",
                        "# 必须位于索引 32，当前索引 {}".format(actual),
                    )
                )

    groups = {}
    stack = []
    for entry in entries:
        level = entry["level"]
        if level > len(stack):
            continue
        stack = stack[:level]
        parent = tuple(stack)
        groups.setdefault(parent, []).append(entry)
        if entry["is_dir"]:
            stack.append(entry["name"].split(" -> ", 1)[0].rstrip("/"))
    for group in groups.values():
        expected = sorted(
            group,
            key=lambda item: (0 if item["is_dir"] else 1, item["name"].casefold()),
        )
        if [item["name"] for item in group] != [item["name"] for item in expected]:
            issues.append(
                Issue(
                    path,
                    group[0]["line"],
                    "ERROR",
                    "project-tree-order",
                    "项目结构每一级先列文件夹、再列文件，同组按名称字典序排列",
                )
            )


def check_readme_language_nav(path, basename, lines, code_line_set, disabled_lines, issues):
    for idx, raw in enumerate(lines[:30]):
        lineno = idx + 1
        if lineno in code_line_set or lineno in disabled_lines:
            continue
        paragraph = re.search(r"<p>(.*?)</p>", raw)
        if not paragraph:
            continue
        content = paragraph.group(1)
        if "English" not in content or "简体中文" not in content:
            continue

        parts = content.split(" · ")
        separator_ok = len(parts) >= 2 and " | " not in content
        if not separator_ok:
            issues.append(
                Issue(
                    path,
                    lineno,
                    "ERROR",
                    "readme-language-separator",
                    "README 语言导航使用 ` · ` 分隔",
                )
            )

        current = [part for part in parts if README_LANGUAGE_CURRENT_RE.fullmatch(part)]
        expected = README_CURRENT_LANGUAGES.get(basename)
        if len(current) != 1 or (
            expected is not None and current[0] != "<strong>{}</strong>".format(expected)
        ):
            issues.append(
                Issue(
                    path,
                    lineno,
                    "ERROR",
                    "readme-language-current",
                    "README 仅加粗当前语言，且当前语言不加链接",
                )
            )

        if separator_ok and any(
            not README_LANGUAGE_CURRENT_RE.fullmatch(part)
            and not README_LANGUAGE_LINK_RE.fullmatch(part)
            for part in parts
        ):
            issues.append(
                Issue(
                    path,
                    lineno,
                    "ERROR",
                    "readme-language-links",
                    "README 除当前语言外的语言均保留链接",
                )
            )
        return


def check_readme_project_docs(path, lines, code_line_set, disabled_lines, issues):
    basename = os.path.basename(path)
    if not basename.lower().startswith("readme"):
        return

    check_readme_language_nav(path, basename, lines, code_line_set, disabled_lines, issues)

    head = "\n".join(lines[:40])
    if '<div align="center">' not in head:
        issues.append(
            Issue(path, 1, "ERROR", "readme-centered-header", "README 标题必须使用居中头部")
        )
    required_badges = {
        "last-commit": "last commit",
        "languages/top": "top language",
        "repo-size": "repo size",
        "license": "license",
    }
    missing_badges = [label for marker, label in required_badges.items() if marker not in head]
    if missing_badges:
        issues.append(
            Issue(
                path,
                1,
                "ERROR",
                "readme-required-badges",
                "README 缺少真实基础徽章：{}".format(", ".join(missing_badges)),
            )
        )

    for idx, raw in enumerate(lines[:30]):
        if idx + 1 in code_line_set:
            continue
        title_match = re.search(r"<h1>([^<]+)</h1>", raw)
        if not title_match:
            title_match = re.match(r"^#\s+(.+)$", raw)
        if not title_match:
            continue
        title = title_match.group(1).strip()
        if (
            PROJECT_TITLE_RE.fullmatch(title)
            and title not in PROJECT_TITLE_EXCEPTIONS
            and idx + 1 not in disabled_lines
        ):
            issues.append(
                Issue(
                    path,
                    idx + 1,
                    "ERROR",
                    "project-title-case",
                    "README 标题写正式项目名，不直接使用小写仓库名：{}".format(title),
                )
            )
        break

    for idx, raw in enumerate(lines):
        if idx + 1 in code_line_set:
            continue
        if raw.strip() not in PROJECT_STRUCTURE_HEADINGS:
            continue
        cursor = idx + 1
        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
        if cursor >= len(lines):
            issues.append(
                Issue(path, idx + 1, "ERROR", "project-tree-missing", "项目结构标题后缺少 bash 代码块")
            )
            continue
        fence = re.match(r"^\s*```([A-Za-z0-9+#.-]*)\s*$", lines[cursor])
        if not fence:
            issues.append(
                Issue(path, cursor + 1, "ERROR", "project-tree-missing", "项目结构标题后直接使用 bash 代码块")
            )
            continue
        if fence.group(1).lower() != "bash":
            issues.append(
                Issue(path, cursor + 1, "ERROR", "project-tree-language", "项目结构代码块语言必须是 bash")
            )
        end = cursor + 1
        while end < len(lines) and not re.match(r"^\s*```\s*$", lines[end]):
            end += 1
        check_project_tree(
            path,
            [(line_idx + 1, lines[line_idx]) for line_idx in range(cursor + 1, end)],
            disabled_lines,
            issues,
        )

    license_starts = [
        idx
        for idx, raw in enumerate(lines)
        if idx + 1 not in code_line_set and raw.strip() in ("## License", "## 许可协议")
    ]
    for start in license_starts:
        end = start + 1
        while end < len(lines) and not lines[end].startswith("## "):
            end += 1
        section = "\n".join(lines[start + 1 : end])
        if "MIT" not in section:
            continue
        if MIT_LICENSE_URL not in section:
            issues.append(
                Issue(
                    path,
                    start + 1,
                    "ERROR",
                    "license-link",
                    "MIT License 统一链接到 {}".format(MIT_LICENSE_URL),
                )
            )
        exact = MIT_LICENSE_SENTENCE_ZH if "zh-Hans" in basename else MIT_LICENSE_SENTENCE
        if exact not in section:
            issues.append(
                Issue(path, start + 1, "ERROR", "license-wording", "README 使用统一的 MIT License 文案")
            )


COMMAND_FILENAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.command$")


def check_path_name(path, issues):
    absolute = os.path.abspath(path)
    cursor = os.path.dirname(absolute)
    root = None
    while cursor != os.path.dirname(cursor):
        if os.path.exists(os.path.join(cursor, ".git")):
            root = cursor
            break
        cursor = os.path.dirname(cursor)
    relative = os.path.relpath(absolute, root) if root else os.path.basename(path)
    basename = os.path.basename(relative)
    if any(not part.isascii() for part in relative.split(os.sep)):
        issues.append(
            Issue(path, 1, "ERROR", "path-filename-ascii", "项目文件与目录使用英文 ASCII 名称")
        )
    if basename.endswith(".command") and not COMMAND_FILENAME_RE.fullmatch(basename):
        issues.append(
            Issue(path, 1, "ERROR", "command-filename", "Finder 启动脚本使用英文 kebab-case 文件名")
        )


# ---------------------------------------------------------------------------
# C++ OI 风格（.cpp 文件 与 ```cpp fence）
# ---------------------------------------------------------------------------

STRLIT_RE = re.compile(r'"(?:\\.|[^"\\])*"' + r"|'(?:\\.|[^'\\])*'")


def strip_cpp_literals(line):
    return STRLIT_RE.sub('""', line)


def strip_cpp_comments(line, in_block):
    out = []
    pos = 0
    while pos < len(line):
        if in_block:
            end = line.find("*/", pos)
            if end == -1:
                return "", True
            pos = end + 2
            in_block = False
            continue
        line_comment = line.find("//", pos)
        block_comment = line.find("/*", pos)
        if line_comment != -1 and (block_comment == -1 or line_comment < block_comment):
            out.append(line[pos:line_comment])
            break
        if block_comment != -1:
            out.append(line[pos:block_comment])
            pos = block_comment + 2
            in_block = True
            continue
        out.append(line[pos:])
        break
    return "".join(out), in_block


def has_top_level_comma(text):
    """忽略括号、数组初值与模板实参后，判断声明是否并列多个常量。"""
    depth = {"(": 0, "[": 0, "{": 0, "<": 0}
    close = {")": "(", "]": "[", "}": "{", ">": "<"}
    for char in text:
        if char in depth:
            depth[char] += 1
        elif char in close and depth[close[char]]:
            depth[close[char]] -= 1
        elif char == "," and not any(depth.values()):
            return True
    return False


def check_cpp(path, blocks, disabled_lines, issues):
    for start, buf in blocks:
        complete = any("#include <bits/stdc++.h>" in raw for _, raw in buf)
        namespaces = [
            idx for idx, (_, raw) in enumerate(buf)
            if re.match(r"^using namespace \w+;$", raw)
        ]
        if complete and namespaces:
            expected = namespaces[-1] + 1
            blanks = [idx for idx, (_, raw) in enumerate(buf) if not raw.strip()]
            if blanks != [expected]:
                lineno = buf[expected][0] if expected < len(buf) else buf[-1][0]
                issues.append(
                    Issue(path, lineno, "ERROR", "cpp-blank-layout",
                          "整份 OI 代码只能有 1 个空行，且只能紧跟 using namespace")
                )
        in_block_comment = False
        for offset, (lineno, raw) in enumerate(buf):
            code = strip_cpp_literals(raw)
            code_without_comments, in_block_comment = strip_cpp_comments(code, in_block_comment)
            if lineno in disabled_lines:
                continue
            if re.search(r"#include\s*<(iostream|cstdio|cstring|algorithm|vector|cmath|string|queue|stack|map|set|bitset|numeric|iomanip)>", raw):
                issues.append(Issue(path, lineno, "ERROR", "cpp-include", "用万能头 #include <bits/stdc++.h>"))
            if '" \\n"[' in raw or '" \\n"[' in raw.replace(" ", " "):
                issues.append(Issue(path, lineno, "ERROR", "cpp-space-newline", '不用 <<" \\n"[i==n] 技巧：输出空格、末尾无换行'))
            if re.search(r"\bstatic\b", code_without_comments):
                issues.append(Issue(path, lineno, "ERROR", "cpp-static", "OI 代码不使用 static 修饰符"))
            if any("\\n" in literal for literal in re.findall(r'"(?:\\.|[^"\\])*"', raw)):
                issues.append(Issue(path, lineno, "ERROR", "cpp-newline-in-str", "换行独立 <<'\\n'，字符串里不夹 \\n"))
            if re.search(r"\bendl\b", code):
                issues.append(Issue(path, lineno, "WARN", "cpp-endl", "换行用 '\\n' 不用 endl（交互题刷新除外）"))
            if re.search(r"\b(scanf|printf)\s*\(", code):
                issues.append(Issue(path, lineno, "WARN", "cpp-stdio", "读写用 cin/cout（固定格式分隔符除外）"))
            if re.search(r"\b(getchar|getchar_unlocked|putchar|putchar_unlocked|fread|fwrite)\s*\(", code):
                issues.append(Issue(path, lineno, "ERROR", "cpp-c-io", "OI 代码读写统一用 cin/cout，不使用底层 C I/O"))
            if re.search(r"\bstd::", code):
                issues.append(Issue(path, lineno, "ERROR", "cpp-std-prefix", "用 using namespace std;，不逐处 std::"))
            if re.search(r"//", code) or re.search(r"/\*", code):
                issues.append(Issue(path, lineno, "ERROR", "cpp-comment", "OI 代码不写注释"))
            if re.search(r"\b(true|false)\b", code) and "sync_with_stdio(false)" not in raw:
                issues.append(Issue(path, lineno, "ERROR", "cpp-bool", "bool 用 0/1，不用 true/false（sync_with_stdio 除外）"))
            if re.search(r"\bdp\b\s*\[", code):
                issues.append(Issue(path, lineno, "ERROR", "cpp-dp", "DP 数组用 f，不用 dp"))
            if re.search(r"\b(?:INF|MOD)\b", code_without_comments):
                issues.append(Issue(path, lineno, "ERROR", "cpp-constant-name", "无穷大与模数常量分别命名为 inf 与 mod"))
            if re.search(r"\b(?:qpow|quick_pow)\s*\(", code_without_comments):
                issues.append(Issue(path, lineno, "ERROR", "cpp-personal-idiom", "快速幂使用个人固定接口 Pow"))
            if re.search(r"\b(?:struct|class)\s+Fenwick\b", code_without_comments):
                issues.append(Issue(path, lineno, "ERROR", "cpp-personal-idiom", "树状数组使用个人固定接口 struct BIT"))
            if re.match(r"^ {2,}\S", raw) and not raw.lstrip().startswith(("*", "//")):
                issues.append(Issue(path, lineno, "ERROR", "cpp-indent", "用 1 个 Tab 缩进，不用空格"))
            if re.search(r"\b(register|inline)\b", code_without_comments):
                issues.append(Issue(path, lineno, "ERROR", "cpp-storage", "OI 代码不使用 register / inline"))
            declaration = code_without_comments.strip()
            if re.match(r"^const\b", declaration) and declaration.endswith(";"):
                if has_top_level_comma(declaration[:-1]):
                    issues.append(
                        Issue(path, lineno, "ERROR", "cpp-const-line",
                              "每个常量单独使用一行 const 声明")
                    )
            if re.search(r"\b[A-Za-z_]\w*\s*=\s*[^,;]+", declaration):
                nxt = offset + 1
                while nxt < len(buf) and not buf[nxt][1].strip():
                    nxt += 1
                if nxt < len(buf) and "cin>>" in buf[nxt][1]:
                    names = re.findall(r"\b([A-Za-z_]\w*)\s*=", declaration)
                    if names and not any(
                        re.search(r"\b{}\b".format(re.escape(name)), buf[nxt][1])
                        for name in names
                    ):
                        issues.append(
                            Issue(path, lineno, "ERROR", "cpp-declaration-order",
                                  "局部变量在完成前置输入后、首次使用前再定义")
                        )
            if re.search(r"\([ \t]*int[ \t]*\)[ \t]*[A-Za-z_]\w*(?:\[[^]]+\])?\.size\(\)", code):
                issues.append(Issue(path, lineno, "ERROR", "cpp-size-cast", ".size() 不就地强转 int；需要有符号运算时先存入 int"))
            if re.search(r"\b(?:auto|const[ \t]+[A-Za-z_]\w*|[A-Za-z_]\w*(?:<[^>]+>)?)&[ \t]*[A-Za-z_]\w*", code):
                issues.append(Issue(path, lineno, "ERROR", "cpp-reference-space", "引用符号贴变量名并留前空格：Type &x"))
            loop = re.search(r"\bfor\s*\(\s*int\s+([A-Za-z_]\w*)\s*=", code)
            if loop and loop.group(1) not in ("i", "j", "k"):
                issues.append(Issue(path, lineno, "ERROR", "cpp-loop-name", "经典 for 循环计数器只用 i / j / k"))
            if re.search(r"\b(if|for|while|switch)\s+\(", code):
                issues.append(Issue(path, lineno, "ERROR", "cpp-keyword-space", "控制关键字与左括号之间不加空格"))
            if re.search(r",[ \t]+", code_without_comments):
                issues.append(Issue(path, lineno, "ERROR", "cpp-comma-space", "逗号后不加多余空格"))
            if re.search(r"[ \t](?:==|!=|<=|>=|&&|\|\||[=+*/%<>-])[ \t]", code_without_comments):
                issues.append(Issue(path, lineno, "ERROR", "cpp-operator-space", "运算符两侧不加多余空格"))


# ---------------------------------------------------------------------------
# 工程代码：ASCII 分隔线 / banner / TODO（.ts .tsx .js .css .md）
# ---------------------------------------------------------------------------

ASCII_ART_RE = re.compile(r"[─-╿]{3,}|={5,}|-{5,}|#{5,}|\*{5,}")
TODO_RE = re.compile(r"\b(TODO|FIXME|XXX)\b")


def check_eng(path, lines, code_line_set, disabled_lines, issues):
    for idx, raw in enumerate(lines):
        lineno = idx + 1
        if lineno in disabled_lines:
            continue
        m = re.search(r"(?://|/\*|\*|#|<!--)\s*(.*)$", raw)
        comment = m.group(1) if m else raw
        if ASCII_ART_RE.search(comment) and "---" not in raw[:4]:
            # 排除 markdown 分隔线 --- 与表格；仅注释内的字符画
            if re.search(r"[─-╿]{3,}|={5,}", comment):
                issues.append(Issue(path, lineno, "WARN", "ascii-art", "注释里不用字符画分隔线，用纯名词标签"))
        if TODO_RE.search(strip_cpp_literals(raw)):
            issues.append(Issue(path, lineno, "WARN", "todo", "不留 TODO/FIXME，进任务清单"))


# ---------------------------------------------------------------------------
# Conventional Commits
# ---------------------------------------------------------------------------

COMMIT_RE = re.compile(r"^(feat|fix|docs|style|refactor|perf|test|chore|build|ci|revert)(\([^)]+\))?!?: .+")


def check_commit(path, text, issues):
    first = text.strip().splitlines()[0] if text.strip() else ""
    if first.startswith("Merge ") or first.startswith("Revert "):
        return
    if not COMMIT_RE.match(first):
        issues.append(
            Issue(path, 1, "ERROR", "commit-conventional",
                  "提交信息用 type(scope): description（如 feat(blog): …），当前：{!r}".format(first[:60]))
        )


# ---------------------------------------------------------------------------
# 单文件调度
# ---------------------------------------------------------------------------

MD_EXT = (".md", ".mdx")
CPP_EXT = (".cpp", ".cc", ".cxx", ".hpp", ".h")
ENG_EXT = (".ts", ".tsx", ".js", ".jsx", ".css", ".scss")


def collect_disabled(lines):
    """返回 (whole_file_disabled, set(禁用行号))。"""
    disabled = set()
    whole = False
    for idx, raw in enumerate(lines):
        if "lailai-checker: disable" in raw:
            whole = True
        if "checker-ignore" in raw:
            disabled.add(idx + 1)
    return whole, disabled


def check_file(path, opts):
    issues = []
    check_path_name(path, issues)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()
    except (OSError, UnicodeDecodeError):
        return issues
    lines = content.splitlines(keepends=False)
    whole_disabled, disabled = collect_disabled(lines)
    if whole_disabled:
        return issues

    ext = os.path.splitext(path)[1].lower()
    if ext in MD_EXT:
        prose, math, cpp_blocks, has_fm = segment_markdown(lines)
        code_line_set = set()
        for start, buf in cpp_blocks:
            for lineno, _ in buf:
                code_line_set.add(lineno)
        # fence 内所有行（含非 cpp）都不做散文/结构检查
        code_line_set |= fenced_line_set(lines)
        check_math(path, math, disabled, issues)
        check_math_delims(path, lines, code_line_set, disabled, issues)
        check_display_math(path, lines, code_line_set, disabled, issues)
        if opts["aitone"]:
            check_aitone(path, prose, disabled, issues)
        check_typography(path, prose, disabled, opts, issues)
        check_md_structure(path, lines, has_fm, code_line_set, disabled, issues)
        check_readme_project_docs(path, lines, code_line_set, disabled, issues)
        check_cpp(path, cpp_blocks, disabled, issues)
        check_eng(path, lines, code_line_set, disabled, issues)
    elif ext in CPP_EXT:
        blocks = [(1, [(i + 1, ln) for i, ln in enumerate(lines)])]
        check_cpp(path, blocks, disabled, issues)
    elif ext in ENG_EXT:
        check_eng(path, lines, set(), disabled, issues)

    issues.sort(key=lambda x: (x.line, 0 if x.level == "ERROR" else 1))
    return issues


def fenced_line_set(lines):
    s = set()
    in_fence = False
    for idx, raw in enumerate(lines):
        if re.match(r"^\s*(`{3,}|~{3,})", raw):
            if not in_fence:
                in_fence = True
            else:
                in_fence = False
            s.add(idx + 1)
            continue
        if in_fence:
            s.add(idx + 1)
    return s


# ---------------------------------------------------------------------------
# CLI / hook
# ---------------------------------------------------------------------------


def changed_line_set(path):
    """相对 HEAD 的新增/改动行号集合；无法判定或未跟踪（新文件）返回 None（=全查）。"""
    d = os.path.dirname(os.path.abspath(path)) or "."
    try:
        tracked = subprocess.run(
            ["git", "-C", d, "ls-files", "--error-unmatch", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        ).returncode == 0
        if not tracked:
            return None
        out = subprocess.run(
            ["git", "-C", d, "diff", "-U0", "--no-color", "HEAD", "--", path],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        ).stdout.decode("utf-8", "replace")
    except (OSError, subprocess.SubprocessError):
        return None
    changed = set()
    for line in out.splitlines():
        m = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
        if m:
            start = int(m.group(1))
            count = 1 if m.group(2) is None else int(m.group(2))
            changed.update(range(start, start + count))
    return changed


def run_paths(paths, opts):
    all_issues = []
    for p in paths:
        all_issues.extend(check_file(p, opts))
    return all_issues


def emit(issues, opts, stream):
    shown = [i for i in issues if not (opts["errors_only"] and i.level == "WARN")]
    for i in shown:
        stream.write(i.format() + "\n")
    return shown


def parse_opts(argv):
    opts = {
        "aitone": True,
        "cjk_space": True,
        "sentence": True,
        "errors_only": False,
        "quiet": False,
    }
    rest = []
    for a in argv:
        if a == "--no-aitone":
            opts["aitone"] = False
        elif a == "--no-cjk-space":
            opts["cjk_space"] = False
        elif a == "--no-sentence":
            opts["sentence"] = False
        elif a == "--errors-only":
            opts["errors_only"] = True
        elif a == "--quiet":
            opts["quiet"] = True
        else:
            rest.append(a)
    return opts, rest


def main(argv):
    if argv and argv[0] == "--hook":
        opts, _ = parse_opts(argv[1:])
        try:
            data = json.load(sys.stdin)
        except (ValueError, json.JSONDecodeError):
            return 0
        path = (data.get("tool_input") or {}).get("file_path")
        if not path or not os.path.isfile(path):
            return 0
        # skill 自身的 meta 文件合法含反面示例（显然 / \( / \dfrac），由 CLI 自查流程处理，hook 跳过
        norm = path.replace("\\", "/")
        if "/.agents/" in norm or "/.claude/" in norm:
            return 0
        issues = check_file(path, opts)
        if "--all-lines" not in argv:
            changed = changed_line_set(path)
            if changed is not None:
                issues = [i for i in issues if i.line in changed]
        errors = [i for i in issues if i.level == "ERROR"]
        warns = [i for i in issues if i.level == "WARN"]
        if errors:
            sys.stderr.write("lailai-checker 拦截（违反确定性规则，请修复）：\n")
            for i in errors:
                sys.stderr.write("  " + i.format() + "\n")
            for i in warns:
                sys.stderr.write("  " + i.format() + "\n")
            return 2
        if warns:
            sys.stderr.write("lailai-checker 提示（WARN，可自行判断）：\n")
            for i in warns:
                sys.stderr.write("  " + i.format() + "\n")
        return 0

    if argv and argv[0] == "--commit":
        path = argv[1]
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        issues = []
        check_commit(path, text, issues)
        for i in issues:
            sys.stderr.write(i.format() + "\n")
        return 1 if issues else 0

    opts, paths = parse_opts(argv)
    if not paths:
        sys.stderr.write(__doc__)
        return 0
    issues = run_paths(paths, opts)
    shown = emit(issues, opts, sys.stdout)
    errors = [i for i in shown if i.level == "ERROR"]
    if not opts["quiet"]:
        sys.stdout.write(
            "\n{} 个 ERROR，{} 个 WARN，检查 {} 个文件。\n".format(
                len(errors), len(shown) - len(errors), len(paths)
            )
        )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
