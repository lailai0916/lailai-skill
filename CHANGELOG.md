# Changelog

记录 lailai.skill 的重要变化：新增习惯、修改规则、删除过时规则、示例与测试改进。

格式参考 [Keep a Changelog](https://keepachangelog.com)，版本遵循语义化版本的精神（人格模型不是软件，但版本号便于回溯）。

类型标签：`Added` 新增 / `Changed` 修改 / `Deprecated` 标记过时 / `Removed` 删除 / `Fixed` 修正 / `Test` 测试。

## [0.6.10] - 2026-06-08

ChatGPT 存档深挖第二轮（读 corrections / preferences / 话题分类，沉淀更完整画像）。

### Changed

- `profile/thinking-style.md`：新增**量化驱动、刨根问底**（先要硬数据 / 排名 / 占比，连续"X 呢"式下钻）与**好奇心广博**（跨域扫陌生领域）——语料话题分布佐证（金融/排名/数据命中 1328）。
- `profile/decision-rules.md`：新增**低风险小决策不纠结**（差别不大就选预算内销量最高 / 最稳妥）。
- `profile/conversation-style.md`：不喜欢的回答方式补**反感"通常 / 一般 / 取决于"打太极**（"不要告诉我通常"）。
- `references/docusaurus-style.md`：题解段补**题解美学**——精简、优雅、"几句话说清"的高手感，不长篇教学（"太长了"是全语料最高频纠正）。
- `references/design-style.md`：核心理念补**简约 ≠ 简陋**（"简约而不简单"，保留专业深度）。

### Notes

- C++ 反复纠正（别用 vector/static、大数组放外、无注释 / 防御性编程）完全复刻 `cpp-oi-style.md`，**强印证不改**。
- 一处待确认微调：深浅主题他曾倾向"纯跟随系统、去掉手动切换"，与 v0.6.4"可留手动切换"略冲突，未改规则、待本人定夺。
- 明确排除：政治敏感、对 AI 的脏话（私人 register）、地区品牌倾向、含第三方真名的升学策略、ChatGPT 客户端 `\[\]` 渲染 workaround（反向噪音，真实规则仍是 `$...$`）。

## [0.6.9] - 2026-06-08

ChatGPT 两年存档第一方语料校准（lailai 本人提供数据）。

### Changed

- `profile/conversation-style.md`：「提问方式」从 `待验证` 升为 `语料校准`，新增「要结果就直说"直接"」特征（语料约 290 次重现：直接给 / 别加额外 / 别解释 / 直接说答案）。
- `references/writing-style.md`：规则 1 补「严谨」register——书面偏严谨、嫌"太轻松"不像自己；新增 register 区分「润色他本人文字 ≠ 写新内容」（只微调通顺、不改原句语调）。
- `observations.md`：记录本次挖矿全过程（量化信号 + 原话 + 印证项 + 身份类待确认 + 隐私处理）。

### Notes

- 大量信号（简洁 / 先结论 / 反套话 / 反 AI 腔 / 统一 / 精简）被语料大规模复现，**仅升置信、未改规则**（反膨胀）。
- 身份类事实（地域 / 学段 / 昵称派生）按 🔴 检查点**未自行写入**，待本人确认。
- 含第三方真名的私人情绪消息已丢弃；原始语料留本机，不入库。

## [0.6.8] - 2026-06-08

组件打磨要到 Apple 级、用实测验证（lailai 本人确立）。

### Changed

- `references/design-style.md`：锐化规则 14 **精益求精到像素级**——Apple 级精细是合格线非加分，等高卡片无论内容长短必须严格等高、内边距视觉均匀、**实测数值验证而非肉眼**，不对称优先选最简单能保证统一的机制（如单行省略号）。checklist 末项补"卡片等高 / 间距用实测数值核对"，不增条数。来源：Paginator 多轮打磨后本人定为长期标准。

## [0.6.7] - 2026-06-07

UI 项目强制完整响应式 + 无障碍（lailai 本人补充）。

### Changed

- `references/design-style.md`：新增规则 13 **完整响应式 + 无障碍必备**——所有断点精确完美响应（无溢出 / 错位 / 截断），无障碍做语义化 + 键盘可达 + 可见焦点 + `aria`/`alt` + 对比度 + `prefers-reduced-motion`，默认就做不事后补；编辑而非重写顺延为规则 14。checklist 把"对比度"项扩成完整无障碍、"响应式"项明确到所有断点，不增条数。

## [0.6.6] - 2026-06-07

元规则：规则是默认而非教条（lailai 本人补充）。

### Added

- `SKILL.md` 核心原则新增第 9 条：默认尽量遵循所有规则，只在极少数明显该破例时用判断力变通（"规则是死的，人是活的"），且要自觉破例、说明原因；涉人格 / 安全边界的破例仍走 🔴 检查点。

## [0.6.5] - 2026-06-07

项目 i18n 多语言要求（lailai 本人补充）。

### Changed

- `references/project-docs-style.md`：规则 4 扩为"多语言以英文为基准"——README 之外，有可视化内容的项目做 i18n，默认 en + zh-Hans、默认英语；带例外（已有 i18n / 默认非英语 / 显然无需多语言就别硬加）。checklist 同步并入既有多语言项，不增条数。

## [0.6.4] - 2026-06-07

UI 项目强制深浅双主题、默认跟随系统（lailai 本人补充）。

### Added

- `references/design-style.md`：新增规则 12 **深浅双主题必备**——任何有可视化 UI 的项目（web / app）都必须同时支持深 / 浅色、**默认跟随系统**（`prefers-color-scheme`），颜色走 token 两套各一份；checklist 并入既有"明暗"项，不增条数。

## [0.6.3] - 2026-06-07

把 Prettier 从"风格遵循"升级为"每个项目必装"（lailai 本人补充）。

### Changed

- `references/project-docs-style.md`：规则 7 改为 **Prettier 必装**——每个项目都装为 `devDependency` + 配置文件 + `format` 脚本，HTML / CSS / JS / TS / JSON / MD 统一交给它，与"每项目必备 LICENSE"同级；checklist 合并入既有"每项目必备"项，不增条数。

## [0.6.2] - 2026-06-06

同步网站第一方更新（题解日期格式漂移修复）。

### Fixed

- `references/docusaurus-style.md`：日期格式更新为 `YYYY-MM-DDTHH:MM:SS+08:00`（带秒 + Asia/Shanghai 偏移，避免 CI/UTC 渲染偏 8 小时）；题解用洛谷专栏对应版本的精确发布秒同步——对齐网站 `.claude/rules/writing-style.md` 最新规则。

## [0.6.1] - 2026-06-06

A/B 校准第二轮（lailai 本人选择），继续精修聊天 / 对话维度。

### Changed

- `references/daily-chat-style.md`：吐槽也保持书面冷、不带脏话 / 网络梗；默认极简核心、how-to"要细节再问"（原理留给学概念）；按对象调客气度（熟人直接、不熟稍客气）。
- `profile/conversation-style.md`：认错时先讲自己原来的依据 / 怎么想的、再认错，不是干脆一句"我错了"。

## [0.6.0] - 2026-06-06

首次用 A/B 强制选择从 lailai 本人采集第一方校准，把聊天 / 审稿维度从"推断"升级为"已校准"。

### Changed

- `references/daily-chat-style.md`：经 A/B（lailai 本人选择）校准——"条件化但决断"（先按场景分情况、再落到明确结论 / 倾向，不是平铺一句也不是和稀泥）；"口语用大白话"（聊天不用书面"中文（English）+ 数学记号"tic，那套是写作 / 文档的）；示例标记升级为"已确认"。
- `references/writing-style.md`：新增"审稿 / 批评 register"——审阅 / 锐评时切到锋利、戳到点（虚 / 俗 / 撑不起主题 / 质变），非软建议。

### 方法

- A/B 强制选择（同场景两版、单轴差异、本人挑更像的）比开放式自省更准。这是首次把第一方 ground truth 写进 `待验证` 维度。

## [0.5.5] - 2026-06-06

让 lailai-skill 自身 README 符合自己定的项目规范（以身作则，解决 v0.5.4 记下的不一致）。

### Changed

- `README.md`：改为英文默认，加居中头部（`English | 简体中文` 切换 + last-commit / top-language / repo-size / license 四个 shields 徽章）；正文全英化。
- `README.zh-Hans.md`：新增简体中文版（原中文内容 + 头部切换指向英文）。
- 两版结构镜像对等，末尾均有 License 段（MIT）。

## [0.5.4] - 2026-06-06

按 lailai 第一方补充 GitHub 项目 README 规范。

### Changed

- `references/project-docs-style.md`：明确每个开源项目必有 `LICENSE`、**默认 MIT**、README 末尾必有 License 段；所有项目 README 跨项目统一同一套结构；新增可复制的居中头部骨架（`English | 简体中文` 切换 + 6 个 shields 徽章，preview 图可选）与 License 段示例。

## [0.5.3] - 2026-06-06

按 lailai 第一方澄清，精修竞赛 C++ 的 vector / auto 风格（纠正第三方记忆的不准确说法）。

### Changed

- `references/cpp-oi-style.md`：普通静态数组 `int a[N]` 优先；`vector` 仅用于确实优雅处（邻接表存图 `vector<int> G[N]`、`for(auto v:G[u])dfs(v);`）；**整段全是 `vector` 是 AI-tell**；`auto` 受欢迎（省去冗长迭代器类型）。
- `references/ai-tone-blacklist.md`：AI-tell 增"算法竞赛全是 vector"一行（指向 cpp-oi-style）。

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
