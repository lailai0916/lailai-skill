# Reference: 风格 checker

把 lailai-skill 里**可机械判定**的规则从「模型记得」变成「机器验」。定位见 [maintenance-guide.md](../../references/maintenance-guide.md) 的「遵循率」一节：prose 规则天花板是「90% + 自觉」，想要 99% 必须把可判定的部分交给确定性校验。

## 两级严格度

- **ERROR**：确定性、近零误报。Hook 模式命中即退出 2，可由支持命令 hook 的 runtime
  直接拦截。
- **WARN**：启发式（句长、中英空格、日期、emoji 等），只提示不拦截。

分级是命门——**宁可漏报，不可错报**。错报会训练人无视 checker，比没有更糟。拿不准的规则一律放 WARN，永不进 ERROR。

## 用法

```bash
# CLI：逐条打印，含 ERROR 退出 1（用于审计、CI）
python3 check.py <file>...
python3 check.py --errors-only --quiet blog/**/*.mdx   # 只看 ERROR

# 兼容 Claude Code PostToolUse JSON 的 hook 模式（diff-aware，只查本次改动行）
python3 check.py --hook

# 一条 commit message
python3 check.py --commit .git/COMMIT_EDITMSG

# 开关
--no-aitone --no-cjk-space --no-sentence   # 关某类
--errors-only                              # 只报 ERROR
--all-lines                                # hook 下改为全量（默认只查改动行）
```

**diff-aware（关键）**：`--hook` 默认用 `git diff HEAD` 只校验本次改动的行。存量违规（旧数学笔记里的 `\dfrac`、老题解里的「显然」）不会挡你改无关内容——只有你新写 / 碰过的行才拦。新文件（未跟踪）全查。契合「新规则对新产出生效，不回溯翻新」。

## 忽略

- 文件内任一行含 `lailai-checker: disable` → 跳过整个文件。
- 某行含 `checker-ignore` → 跳过该行的违规。
- `--hook` 自动跳过 `/.agents/` 与 `/.claude/` 下的路径（skill 自身 meta 文件合法含
  反面示例，走 CLI 自查）。

## 规则 → reference 对照

| 规则 id | 级别 | 出处 |
| :-- | :-: | :-- |
| `math-delim`（`\(...\)` / `\[...\]`） | ERROR | [latex-math-style](../../references/latex-math-style.md) 规则 1 |
| `math-dfrac` / `math-dots` / `math-emptyset` | ERROR | latex 规则 12、16、17 |
| `math-manual-space`（`\,` `\quad` 等） | ERROR | latex 规则 4 |
| `math-display-intro` / `math-display-terminal` | ERROR | latex 规则 2 |
| `math-environment-line` / `math-environment-indent` / `math-environment-break` / `math-align-space` | ERROR | latex 规则 28 |
| `math-structural-cjk` | ERROR | latex 规则 31 |
| `math-unicode`（`×` `−` `°` `～` 等） | ERROR | latex 规则 31 |
| `math-bare-cjk` / `math-frac-brace` | WARN | latex 规则 31、21 |
| `aitone`（本文将 / 显然 / 不难发现 / 易得…） | ERROR/WARN | [ai-tone-blacklist](../../references/ai-tone-blacklist.md) |
| `heading-blank` | ERROR | [writing-style](../../references/writing-style.md)、[markdown-style](../../references/markdown-style.md) |
| `h1` / `heading-punct` | WARN | markdown 规则 5、7 |
| `curly-quote` | WARN | markdown 规则 13 |
| `emoji` / `date-format` / `time-format` | WARN | writing 规则 12、20、21 |
| `cjk-latin-space` / `sentence-length` | WARN | markdown 规则 17；writing 规则 6（建议项） |
| `trailing-space` / `blank-lines` | WARN | markdown 规则 3 |
| `cpp-include` / `cpp-space-newline` / `cpp-static` | ERROR | [cpp-oi-style](../../references/cpp-oi-style.md) 规则 6、12、16 |
| `cpp-blank-layout` / `cpp-const-line` / `cpp-declaration-order` | ERROR | cpp 规则 3、16、17 |
| `cpp-constant-name` / `cpp-c-io` | ERROR | cpp 规则 11、21 |
| `cpp-personal-idiom` | ERROR | [cpp-oi-idioms](../../references/cpp-oi-idioms.md) 的固定 `Pow` 与 `BIT` 接口 |
| `cpp-endl` / `cpp-stdio` / `cpp-comment` / `cpp-bool` / `cpp-dp` / `cpp-std-prefix` / `cpp-indent` | ERROR/WARN | cpp 规则 11、4、14、24、7、3 |
| `ascii-art` / `todo` | WARN | [engineering-code-style](../../references/engineering-code-style.md) |
| `commit-conventional` | ERROR | [project-docs-style](../../references/project-docs-style.md) 规则 1 |
| `project-title-case` / `project-brand-case` / `path-filename-ascii` / `command-filename` | ERROR | project-docs-style 规则 8；品牌大小写同时检查正文 |
| `readme-language-*` | ERROR | project-docs-style 规则 11 |
| `project-tree-*` | ERROR | project-docs-style 规则 14 |
| `readme-centered-header` / `readme-required-badges` | ERROR | project-docs-style 规则 12 |
| `license-link` / `license-wording` | ERROR | project-docs-style 规则 5 |

## 故意不查什么（判断类，留给 reviewer / 人）

checker 只碰能确定判定的。下列**不进 checker**，靠 reviewer agent 或人工把关：

- 语气是否「克制、干、专业」、register 是否贴场景、是否先结论后依据——语义判断。
- 形容词堆叠、注水、假结构（首先其次然后）——需理解语义。
- C++ 是否「整段全 vector」的 AI-tell、变量名是否达意、能否再抠一层复杂度——需读懂代码。
- 设计审美、一致性、是否有整卡 hover 上浮——需看渲染。
- 题解 / 文档结构是否合理、信息密度够不够——需通读。

规则边界随 reference 演进；改规则时同步改本 checker 与 [tests/](../../tests/)，让「规则 ↔ 校验」共同进化（闭环见 maintenance-guide）。

## 自测

`tests/` 下的通用与 README 回归夹具覆盖各类 ERROR。`good` 必须零 ERROR 零 WARN，`bad` 必须命中预期规则。改 checker 后跑：

```bash
python3 check.py tests/good.mdx   # 期望：0 ERROR，0 WARN
python3 check.py tests/bad.mdx    # 期望：各类 ERROR 齐全
python3 check.py tests/readme-good.md
python3 check.py tests/readme-bad.md
python3 -m unittest test_checker.py
```
