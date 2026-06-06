# Changelog

记录 lailai.skill 的重要变化：新增习惯、修改规则、删除过时规则、示例与测试改进。

格式参考 [Keep a Changelog](https://keepachangelog.com)，版本遵循语义化版本的精神（人格模型不是软件，但版本号便于回溯）。

类型标签：`Added` 新增 / `Changed` 修改 / `Deprecated` 标记过时 / `Removed` 删除 / `Fixed` 修正 / `Test` 测试。

## [0.5.2] - 2026-06-06

把"跨项目记录观察"的指令放进 skill 本身，使其随 GitHub 源可移植（替代不可移植的 `~/.claude/CLAUDE.md`）。

### Changed

- `SKILL.md`：description 增加触发词（"这不像我""记一笔""记进 lailai-skill"）；进化机制入口新增"跨项目记录（写回 GitHub 源）"——任何项目里触发即把观察追加进源仓库 `observations.md` 并 push，只改 observations、身份级先确认。

### 说明

- 指令现随 skill（GitHub 源）走，单一源、可移植。每台机器一次性把 skill 装到 `~/.claude/skills/lailai-skill` 即生效，不再依赖各机器手写的 `~/.claude/CLAUDE.md`。

## [0.5.1] - 2026-06-05

加入反膨胀机制，防止"素材越喂越多、文件越滚越大"。

### Added

- `references/maintenance-guide.md`：新增"反膨胀：收敛而非累积"铁律（判重优先、净增趋零、文件软上限、合并 > 新增、observations 是缓冲）+ 定期复查清单的合并剪枝项。
- `evolution/evaluation-rubric.md`：新增"膨胀负分项"（重复 / 超软上限 / 净增持续为正 / observations 堆积）。

## [0.5.0] - 2026-06-05

接入 lailai's Home 项目：lailai-skill 作为 submodule，并把 Home `.claude/` 的通用规则归到 skill。

### Added

- `references/engineering-code-style.md`：工程代码（TS / React / CSS）注释与约定——注释解释"为什么"、少而精、禁 ASCII 分隔线、不留注释代码 / banner / TODO，提炼自站点 `.claude/rules/comments.md`。
- `SKILL.md` / `README.md`：索引与结构树登记新 reference。

### 跨仓库整理

- lailai-skill 提交并推送，作为 submodule 接入 `lailai0916.github.io/.claude/skills/lailai-skill`。
- Home 侧通用规则去重、指向本 skill；站点专属规则（i18n、laikit 组件、Docusaurus 站点写作）保留在 Home。详见该仓库变更。

## [0.4.0] - 2026-06-04

用达尔文.skill（9 维 100 分 rubric + 独立 judge 盲评 + 棘轮机制）优化 SKILL.md。独立 judge 评分 **57.6 → 81.8（Δ +24.2）**。

### Added

- `evolution/darwin-results.tsv`：达尔文棘轮日志（基线 / 各轮 / 保留与否 / eval_mode）。
- `SKILL.md`：新增"失败模式与兜底"if-then 表（dim3：无 reference 命中、规则冲突、自检不过、`待验证` 维度、跨场景、风格无关、信息不确定的兜底）。
- `SKILL.md`：新增"🔴 检查点"视觉标记停机条款（dim4：命中即 🛑 STOP 等人工确认）。

### Changed

- `SKILL.md` 工作流：6 步全部标「输入 → 输出」，第 5 步自检不过显式回退（dim2）。
- `SKILL.md` 安全边界：去除与"🔴 检查点"的逐字重复，安全边界=常设禁令、检查点=停机触发（dim7 去冗余）。
- `README.md`：安装章节由"在 Claude Code 项目中使用"改为 runtime 中立的"安装与使用"，清除达尔文 runtime gate 红灯（支持 Claude Code / Codex / Cursor / OpenClaw 等）。

### 达尔文评分变化（独立 judge）

| 维度                 |   改前   |   改后   |
| :------------------- | :------: | :------: |
| dim2 工作流清晰度    |    5     |    9     |
| dim3 失败模式编码    |    2     |    9     |
| dim4 检查点设计      |    4     |    9     |
| dim8 实测（dry-run） |    6     |    8     |
| **总分 / 100**       | **57.6** | **81.8** |

方法纪律：独立子代理盲评（非自评自改）；棘轮只保留涨分；HL-4 见好就收，未为凑分注水；SKILL.md 体积 8130 → 约 10.1KB，未超 150% 上限。

## [0.3.1] - 2026-06-04

参考第三方仓库画像报告，补入与第一方证据互相印证的人格特质。

### Changed

- `profile/personality.md`：核心特征补"体系化 / 立规矩""长期 / 产品心态""分场景用不同标准"；新增"张力与不一致（真实的一面）"——自律分场景、标准后建旧产出未对齐、简约理念 vs 加法冲动，用于让模拟更真实，不假装永远完美一致。
- `profile/thinking-style.md`：取舍逻辑补"按场景选标准"。
- `observations.md`：记录该第三方报告为来源，区分"已沉淀（与第一方印证）"与"待 lailai 确认（第三方推断）"。

### 来源说明

- 该报告为第三方基于公开网站的评价，非第一方。已沉淀项均与第一方证据（CONTRIBUTING、guides、提交记录）吻合；解读性条目留在 observations 待本人确认，未硬化为规则。

## [0.3.0] - 2026-06-04

一轮严格校准：强化进化闭环、测试可验证性与边界表述，确认可公开、可作为 Claude Code skill 直接使用。

### Added

- `references/maintenance-guide.md`：新增"核心闭环"——observation → rule → example → test → evolution log →（回到）observation，明确每条规则都要有对应示例与测试。
- 8 个 `tests/*` 各增"客观检查项（可机械判定）"，把"像不像 lailai"从主观打分细化为可逐条判定（如句长 ≤ 40、无「显然」、snake_case、`$...$`、必抓整卡 hover 上浮等）。
- `examples/{chat-style,thinking,decision}-demo.md` 各增 ❌ 反例 + ✓ 正例对照。

### Changed

- `SKILL.md`：进化机制入口点明核心闭环；自检补"用词 + 句长"项。
- `README.md`：安装说明改以 `.claude/skills/lailai-skill/` 为主路径，确认相对链接迁移后仍有效。
- `profile/identity.md`：去掉生日推断式措辞，仅保留公开用户名，更贴合 boundaries。

### 校准结论

- 定位已是"持续进化型赛博分身系统"，非窄工作流 skill；覆盖聊天 / 思维 / 决策 / 写作 / 代码 / 设计 / 维护 / 学习。
- 无 PII 泄漏（电话 / 邮箱 / QQ / 微信均未写入）；冒充类表述全部为预防性否定语境；无玄学人设。
- 适合公开到 GitHub。

## [0.2.0] - 2026-06-04

从个人网站 `lailai0916.github.io` 系统蒸馏，大幅提升 profile 与 references 的真实性与精度。

### Added

- `references/wording.md`：用词规范（你 / 仅 / 若、错别字、禁用「显然 / 易得 / 不难发现」），提炼自站点《用词规范表》。
- `references/latex-math-style.md`：LaTeX 数学公式风格（`$...$`、`\frac` 非 `\dfrac`、`\dots`、单字母变量、复杂度不带常数…），提炼自站点《文本格式指南》与《LaTeX 指南》。
- 新增结构理由：镜像 lailai 自己的指南分法（他把用词、LaTeX 作为独立指南维护）。

### Changed

- `profile/identity.md`：补入公开身份（杭州第二中学高中生、OIer）、OI 获奖（NOIP 2025 / CSP 2025 一等奖、USACO Platinum）、自述（独立学习 / 系统思考 / 理论与实践）、兴趣（跑步 / 旅行 / AI 重度用户）、长期项目清单。**刻意排除**联系方式等 PII。
- `profile/personality.md`：补入务实目标导向、谦逊自知、跨学科好奇、重积累回顾等价值信号。
- `references/writing-style.md`：补入《文本格式指南》规则——简洁 / 自然 / 专业、每句 ≤ 40（最多 60）字、主动语态、避免多余形容词 / 虚词 / Emoji、术语与人名格式、GenAI 须人工审核。
- `references/markdown-style.md`：补入完整排版规则——kebab-case 文件名、2 空格缩进、H2–H4、列表标点、直角引号、连接号区分、空格规则、ISO 8601 时间等。
- `references/cpp-oi-style.md`：按《代码风格指南》修正——snake_case 而非泛指"短变量名"，`N`=max+5，能 `int` 不 `long long`，避免 `static` / `register` / `inline`，小变量局部 + 大数组全局，补入命名表与常量约定。
- `references/design-style.md`：补入《设计风格指南》——统一优先于美观、层级用视觉强度、柔和中性色、不用渐变 / 半透明、对比度 4.5:1 / 3:1、不孤字成行、"基于直觉"的谦逊。
- `references/project-docs-style.md`：补入《项目规范指南》——Conventional Commits、`README.<lang>.md`、`.github/CONTRIBUTING.md`、Semantic Versioning、Keep a Changelog、Prettier 配置。
- `references/docusaurus-style.md`：补入站点排印约定（lailai 始终小写且不翻译、`[TODO]`、cloud 资源）。
- `references/ai-tone-blacklist.md`：新增「显然 / 易得 / 不难发现」禁用行。
- `SKILL.md`：索引新增 wording 与 latex-math-style，自检补入用词与句长检查。

### 资料来源

本轮全部来自 `lailai0916.github.io` 的第一方公开内容：`docs/project/guides/{wording,text,code,design,project,latex,markdown}.mdx`、`src/pages/about/index.mdx`、`docs/contest/index.mdx`、`.claude/rules/` 与 `CLAUDE.md`、`CONTRIBUTING.md`、`README*.md`。已确认事实，非推断。

### 安全

- 个人网站公开列出的联系方式（电话 / 邮箱 / QQ / 微信等）与精确生日**未写入** skill，遵循 boundaries。

## [0.1.0] - 2026-06-03

初始化 lailai.skill 的赛博分身结构。

### Added

- 入口 `SKILL.md`：定位、适用 / 不适用场景、核心原则、安全边界、profile / reference 索引、工作流、自检流程、进化机制入口。
- `README.md`：项目介绍、边界、结构、使用与进化说明。
- `profile/`：identity、personality、thinking-style、conversation-style、preferences、decision-rules、boundaries。
- `references/`：daily-chat-style、writing-style、markdown-style、docusaurus-style、cpp-oi-style、design-style、project-docs-style、learning-style、ai-tone-blacklist、maintenance-guide，每个含 Self-review Checklist。
- `examples/`：聊天、思维、文章改写、README、Docusaurus、C++、设计审查、决策共 8 个示例。
- `tests/`：8 个风格测试，含评分标准与通过条件。
- `prompts/`：analyze-source-materials、generate-skill-v0、review-style、update-skill、evolve-skill、add-observation。
- `evolution/`：evaluation-rubric（12 维 0–5 分）、evolution-log（模板 + 首条记录）。
- `observations.md`：临时观察的记录结构与稳定性判断说明。
- `LICENSE`（MIT）。

### 资料来源

- **基于真实资料提炼**（高可信）：写作风格、Markdown / Docusaurus 规范、OI C++17 风格、设计审查标准、README / 项目文档风格、部分反感项与 AI 腔黑名单——提炼自 `lailai0916.github.io` 仓库的 `.claude/rules/writing-style.md`、`.claude/CLAUDE.md`、`.github/CONTRIBUTING.md`、真实题解与博客、`src/` 设计系统 `laikit`，以及公开 README 与个人网站 <https://www.lailai.one>。
- **基于已知偏好初始化**（待验证）：日常聊天风格、提问方式、思考方式细节、决策规则、学习方式、性格反应、长期偏好——来自本次任务说明中 lailai 自述的偏好，尚缺真实聊天 / 决策样例佐证，已在对应文件标注 `待验证`。

### 待办

- 补充真实日常聊天样例、决策样例、反例，以替换 `待验证` 内容。
- 用真实任务（个人网站、README、文档、代码、设计审查、聊天模拟）跑 `tests/` 验证。
- 跑一轮达尔文式优化，记入 `evolution/evolution-log.md`。

### 已确认

- 数学公式分隔符：所有场景统一用 `$...$` / `$$...$$`（含 Docusaurus 站内），不用 `\(...\)` / `\[...\]`。由 lailai 于 2026-06-03 确认。
