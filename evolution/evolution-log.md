# Evolution Log

记录每次重要进化。新记录追加在最上方（倒序）。模板在文件末尾。

每条含：日期、版本、触发原因、新观察、修改文件、修改内容、测试结果、是否保留、是否需人工确认、后续行动。

---

## 2026-06-06 · v0.5.3 · C++ vector/auto 第一方澄清

- **触发原因**：lailai 直接澄清——竞赛里整段全是 vector = AI-tell；普通数组 `int a[N]` 优先；vector 仅用于存图（`for(auto v:G[u])`）；auto 喜欢（省冗长类型）。纠正 ChatGPT 记忆里"不喜欢 vector / auto"的错误。
- **处理**：第一方 + 稳定 + 真实仓库可佐证 → 直接精修 `cpp-oi-style.md` 既有规则（非新增大段），`ai-tone-blacklist.md` 加一行指针。
- **反膨胀**：自检清单已满 8 项 → 折进现有项不新增；净增约 4 行。
- **方法示范**：第三方（ChatGPT 总结）"不喜欢 vector/auto"与第一方冲突 → 不照收，以第一方为准。
- **是否保留**：保留（v0.5.3）。

## 2026-06-06 · v0.5.2 · 自维护指令随 skill 可移植（方案 A）

- **触发原因**：lailai 指出"记一笔"指令放 `~/.claude/CLAUDE.md` 不可移植（换机器失效），违背"GitHub 为唯一源"。
- **决策**：方案 A——把指令放进 skill 本身（随 GitHub 源走），而非每机器手写全局配置。
- **修改文件**：`SKILL.md`（触发词 + 跨项目记录小节）、`CHANGELOG.md`。
- **配套动作**：commit + push 源仓库；本机 `git clone` 装 skill 到 `~/.claude/skills/lailai-skill`；删除 `~/.claude/CLAUDE.md`。
- **每机器一次性成本**：把 skill 装到用户级一次即生效（本来用 skill 就要做）。
- **是否保留**：保留（v0.5.2）。

## 2026-06-05 · v0.5.1 · 反膨胀机制

- **触发原因**：lailai 担心"每天喂素材 → 不断追加 → 文件越滚越大"。这是这类累积系统的头号失败模式。
- **修改文件**：`references/maintenance-guide.md`（反膨胀铁律 + 合并剪枝复查项）、`evolution/evaluation-rubric.md`（膨胀负分项）。
- **核心约束**：判重优先、净增趋零、文件软上限（reference ≤150 行 / profile ≤80 行）、合并 > 新增、observations 是缓冲。素材越多规则应**收敛**而非线性增长。
- **自我节制**：本次为防膨胀而加的内容也刻意从简（约 20 行），不破坏自身约束。
- **是否保留**：保留（v0.5.1）。
- **后续行动**：下次大维护跑一轮合并剪枝，核净增行数。

## 2026-06-05 · v0.5.0 · 接入 lailai's Home（submodule + 去重）

- **触发原因**：lailai 要求整理两仓库的 Claude 配置——skill 作为 submodule 接入 Home，通用规则归 skill，Home 只留项目专属 + 调用入口。
- **决策（人工确认）**：lailai-skill 本地 commit + push；Home `.claude/rules` 平衡整理（保留路径作用域的站点专属，去重通用部分 + 指针）。
- **修改文件**：新增 `references/engineering-code-style.md`（迁自 Home `comments.md` 通用精华）；`SKILL.md` / `README.md` 登记；首次提交并推送全部 skill 内容；Home 侧加 submodule、精简 rules、CLAUDE.md 加调用入口。
- **架构结论**：skill = 跨项目通用个人风格（触发式 / 显式引用加载）；Home `.claude` = 站点专属 + 路径作用域自动加载（i18n / laikit / 站点写作）+ 指向 skill 的入口。两套加载机制互补，不重复存同一套规则。
- **是否保留**：保留（v0.5.0）。
- **是否需人工确认**：Home 的 commit 由 lailai 决定（本轮只 stage，给出建议 message）。
- **后续行动**：lailai 确认 Home commit；其它机器 / CI clone 时记得 `git submodule update --init`。

## 2026-06-04 · v0.4.0 · 达尔文.skill 优化 SKILL.md

- **触发原因**：lailai 要求用达尔文.skill 优化 lailai.skill。
- **方法**：读取已安装的 darwin-skill（9 维 100 分 rubric + runtime gate + 独立 judge 盲评 + 棘轮 + 人在回路），忠实执行 Phase 0–3。
- **基线（独立 judge 盲评）**：57.6 / 100。最低维 dim3 失败模式编码（2）、dim4 检查点设计（4），同属 dim2/3/4 相关簇；外加 P0 runtime 红灯（README）。
- **改动**：
  - P0：README 安装章节改 runtime 中立，清除红灯。
  - Round 1（相关簇）：SKILL.md 加"失败模式与兜底"if-then 表、"🔴 检查点"视觉停机条款、工作流 6 步标「输入→输出」。
  - Round 2（去冗余）：去除安全边界与检查点的逐字重复。
- **复评（另一独立 judge 盲评）**：81.8 / 100，Δ +24.2。dim2 5→9、dim3 2→9、dim4 4→9、dim8 6→8。
- **棘轮决策**：81.8 > 57.6 → 保留。HL-4 见好就收，未追加凑分轮次。
- **是否保留**：保留（v0.4.0）。日志见 `evolution/darwin-results.tsv`。
- **是否需人工确认**：🔴 现在等 lailai 看改动摘要确认（达尔文人在回路检查点）。eval_mode 全为 dry_run（judge 用推演评 dim8，未跑 with/without 子代理对比），属已知局限。
- **后续行动**：lailai 确认后，可考虑用真实 with/without 子代理跑一次 full_test 复核 dim8；继续补聊天 / 决策真实样例。

## 2026-06-04 · v0.3.1 · 吸收第三方画像报告

- **触发原因**：lailai 提供他人基于网站写的评价报告，要求参考并写入信息。
- **新观察**：报告与第一方证据多处吻合（完美主义、体系化、长期主义、克制审美、自知），并指出几处诚实的张力（自律分场景、标准后建未回溯、简约 vs 加法）。
- **修改文件**：`profile/personality.md`、`profile/thinking-style.md`、`observations.md`、`CHANGELOG.md`。
- **修改内容**：把与第一方印证的特质沉淀进 profile（含"张力与不一致"小节，提升模拟真实度）；第三方推断条目记入 observations 待确认，不硬化。
- **方法纪律**：遵守"观察 ≠ 规则"——第三方推断不直接成规则，先与第一方证据交叉验证，再决定沉淀或挂起。
- **测试结果**：无新增可机械测试项（人格类）；不影响既有 tests。
- **是否保留**：保留（v0.3.1）。
- **是否需人工确认**：是——observations 中"功能最大化是否需克制""言行不一是否仅历史遗留"两条待 lailai 表态。
- **后续行动**：等 lailai 确认那两条；继续补真实聊天 / 决策样例。

## 2026-06-04 · v0.3.0 · 严格校准

- **触发原因**：lailai 要求按 17 项检查做一轮严格校准（定位、维度覆盖、进化闭环、冒充 / 隐私 / 玄学风险、可触发性、tests 可验证性等）。
- **新观察**：tests 偏主观、进化闭环未显式串联、安装路径未对齐 `.claude/skills/`。隐私与冒充风险经扫描确认无实际问题。
- **修改文件**：`references/maintenance-guide.md`（核心闭环）、`tests/*`（8 个客观检查项）、`examples/{chat-style,thinking,decision}-demo.md`（❌/✓ 反例）、`SKILL.md`、`README.md`、`profile/identity.md`、`CHANGELOG.md`。
- **修改内容**：见 CHANGELOG v0.3.0。核心是把"像不像 lailai"可机械判定化，并显式化 observation→rule→example→test→log 闭环。
- **测试结果**：用新客观检查项回测既有 `examples/`：C++ demo、Docusaurus demo、写作 / 改写 demo 均通过对应客观项；反例均被对应检查项判负（符合预期）。
- **是否保留**：保留（v0.3.0）。
- **是否需人工确认**：(1) 是否要把某些公开联系方式纳入（当前默认全部排除）；(2) 聊天 / 决策维度仍需真实样例最终校准。
- **后续行动**：补真实聊天 / 决策样例；跑一次端到端真实任务实测打分。

## 2026-06-04 · v0.2.0 · 从个人网站系统蒸馏

- **触发原因**：lailai 要求详细查看个人网站 `lailai0916.github.io`，把各方面信息维护进 skill。
- **新观察**：发现站点已有 lailai 自订的成套风格指南 `docs/project/guides/*`（用词、文本、代码、设计、项目、LaTeX、Markdown），以及 About 页、竞赛获奖、个人写作中的价值信号。这些是第一方权威资料，远比 v0.1.0 的推断精确。
- **修改文件**：新增 `references/wording.md`、`references/latex-math-style.md`；改写 `references/{writing-style,markdown-style,cpp-oi-style,design-style,project-docs-style,docusaurus-style,ai-tone-blacklist}.md`；改写 `profile/{identity,personality}.md`；更新 `SKILL.md`、`CHANGELOG.md`。
- **修改内容**：把指南规则落成可执行条目；修正 v0.1.0 的 C++ 风格偏差（snake_case、N+5、int 优先、无 static 等）；统一数学为 `$...$`；补入身份与价值信号；提交规范改为 Conventional Commits。
- **测试结果**：未跑自动测试；以 `examples/` 与 `tests/` 的期望对照人工核对，新规则与之一致（C++ demo、数学分隔符、写作示例均符合）。
- **是否保留**：保留（v0.2.0 基线）。质量明显提升：多数维度从"推断"升级为"第一方确认"。
- **是否需人工确认**：(1) 已确认：数学统一 `$...$`、PII 排除策略；(2) 待确认：聊天 / 决策 / 学习等 `待验证` 维度仍缺真实样例；identity 是否还要补 / 删。
- **后续行动**：
  1. 仍需真实聊天 / 决策样例校准剩余 `待验证` 维度。
  2. 跑一轮 `tests/` 实测打分。
  3. 考虑把 learning-style、thinking-style 与站点笔记组织习惯再对齐一次。

## 2026-06-03 · v0.1.0 · 初始化

- **触发原因**：从空仓库构建 lailai.skill 赛博分身系统。
- **新观察**：首次系统提炼，无"新"观察；基线来自真实资料 + 自述偏好。
- **修改文件**：全部新建——`SKILL.md`、`README.md`、`LICENSE`、`CHANGELOG.md`、`observations.md`、`profile/*`（7）、`references/*`（10）、`examples/*`（8）、`tests/*`（8）、`prompts/*`（6）、`evolution/*`（2）。
- **修改内容**：建立结构、入口、profile、可执行 references、示例、测试、维护 prompts、评分标准。写作 / Markdown / Docusaurus / C++ / 设计 / README 维度基于 `lailai0916.github.io` 仓库的 `.claude/rules/`、`CLAUDE.md`、`CONTRIBUTING.md`、真实题解与 `laikit` 提炼；聊天 / 思考 / 决策 / 学习 / 性格维度基于本人自述偏好初始化，标 `待验证`。
- **测试结果**：尚未在真实任务上跑 `tests/`（待办）。`examples/` 作为正例自检通过。
- **是否保留**：保留（作为 v0.1.0 基线）。
- **是否需人工确认**：(1) 数学分隔符——已确认：所有场景统一 `$...$` / `$$...$$`（2026-06-03，覆盖初始的分场景方案）；(2) 待确认：全部 `待验证` 维度需真实样例校准；(3) 待确认：identity 公开粒度。
- **后续行动**：
  1. 补真实聊天 / 决策 / 反例样例，校准 `待验证` 内容。
  2. 用真实任务跑 `tests/`，记录得分。
  3. 跑首轮达尔文式优化（`prompts/evolve-skill.md`），定位最弱维度。

---

## 记录模板

```text
## YYYY-MM-DD · vX.Y.Z · 一句话标题

- 触发原因：……
- 新观察：……（来自 observations.md 的哪条 / 哪次真实使用）
- 修改文件：……
- 修改内容：……（最小、可解释）
- 测试结果：……（用了哪些 tests，前后得分，对照 evaluation-rubric.md）
- 是否保留：保留 / 回滚（回滚则记失败假设）
- 是否需人工确认：是 / 否（涉及人格 / 价值 / 隐私 / 公开表达则必为是）
- 后续行动：……
```
