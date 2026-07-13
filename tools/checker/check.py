#!/usr/bin/env python3
"""lailai-skill 风格 checker：把可机械判定的规则从「模型记得」变成「机器验」。

分两级：ERROR（确定性、近零误报，hook 会退出 2 打回）/ WARN（启发式，仅提示）。
规则溯源见同目录 README.md 的「规则 → reference」对照表。

用法：
    python3 check.py <file>...                # CLI，逐条打印，含 ERROR 则退出 1
    python3 check.py --hook                   # Claude Code PostToolUse hook（读 stdin JSON）
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
        re.compile(r"\\(?:quad|qquad|,|;|:|!)(?![A-Za-z])"),
        "math-manual-space",
        r"禁用手动间距 \, \; \: \! \quad \qquad，交给 KaTeX",
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
                              "句子 {} 字，超 40 字（硬上限 60），拆短".format(len(seg)))
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
# C++ OI 风格（.cpp 文件 与 ```cpp fence）
# ---------------------------------------------------------------------------

STRLIT_RE = re.compile(r'"(?:\\.|[^"\\])*"' + r"|'(?:\\.|[^'\\])*'")


def strip_cpp_literals(line):
    return STRLIT_RE.sub('""', line)


def check_cpp(path, blocks, disabled_lines, issues):
    for start, buf in blocks:
        for offset, (lineno, raw) in enumerate(buf):
            if lineno in disabled_lines:
                continue
            code = strip_cpp_literals(raw)
            if re.search(r"#include\s*<(iostream|cstdio|cstring|algorithm|vector|cmath|string|queue|stack|map|set|bitset|numeric|iomanip)>", raw):
                issues.append(Issue(path, lineno, "ERROR", "cpp-include", "用万能头 #include <bits/stdc++.h>"))
            if '" \\n"[' in raw or '" \\n"[' in raw.replace(" ", " "):
                issues.append(Issue(path, lineno, "ERROR", "cpp-space-newline", '不用 <<" \\n"[i==n] 技巧：输出空格、末尾无换行'))
            if re.search(r'"[^"]*\\n', raw):
                issues.append(Issue(path, lineno, "WARN", "cpp-newline-in-str", "换行独立 <<'\\n'，字符串里不夹 \\n"))
            if re.search(r"\bendl\b", code):
                issues.append(Issue(path, lineno, "WARN", "cpp-endl", "换行用 '\\n' 不用 endl（交互题刷新除外）"))
            if re.search(r"\b(scanf|printf)\s*\(", code):
                issues.append(Issue(path, lineno, "WARN", "cpp-stdio", "读写用 cin/cout（固定格式分隔符除外）"))
            if re.search(r"\bstd::", code):
                issues.append(Issue(path, lineno, "WARN", "cpp-std-prefix", "用 using namespace std;，不逐处 std::"))
            if re.search(r"//", code) or re.search(r"/\*", code):
                issues.append(Issue(path, lineno, "WARN", "cpp-comment", "OI 代码不写注释"))
            if re.search(r"\b(true|false)\b", code) and "sync_with_stdio(false)" not in raw:
                issues.append(Issue(path, lineno, "WARN", "cpp-bool", "bool 用 0/1，不用 true/false（sync_with_stdio 除外）"))
            if re.search(r"\bdp\b\s*\[", code):
                issues.append(Issue(path, lineno, "WARN", "cpp-dp", "DP 数组用 f，不用 dp"))
            if re.match(r"^ {2,}\S", raw) and not raw.lstrip().startswith(("*", "//")):
                issues.append(Issue(path, lineno, "WARN", "cpp-indent", "用 1 个 Tab 缩进，不用空格"))


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
        if opts["aitone"]:
            check_aitone(path, prose, disabled, issues)
        check_typography(path, prose, disabled, opts, issues)
        check_md_structure(path, lines, has_fm, code_line_set, disabled, issues)
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
        if "/.claude/" in norm:
            return 0
        ext = os.path.splitext(path)[1].lower()
        if ext not in MD_EXT + CPP_EXT + ENG_EXT:
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
