<div align="center">
  <h1>lailai.skill</h1>
  <p><a href="README.md">English</a> · <strong>简体中文</strong></p>
  <p>
    <img src="https://img.shields.io/github/actions/workflow/status/lailai0916/lailai-skill/ci.yml?branch=main&style=flat-square" />
    <img src="https://img.shields.io/github/last-commit/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/languages/top/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/repo-size/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/license/lailai0916/lailai-skill?style=flat-square" />
  </p>
</div>

## 项目简介

> lailai 的持续进化型个人赛博分身系统。它尽可能复刻 lailai 的表达、思维、审美、工作习惯与日常交流风格。

这是面向各类 AI Agent 的个人 Skill。它不是一句「请扮演 lailai」。这是结构化、可维护、可验证、可持续进化的个人模型。

## 项目目标

让 AI 在写作、文档、代码、设计、聊天、判断与项目维护中尽可能像 lailai。模型会持续进化，同时保持风格一致、密度高、无 AI 腔且能落地。

## 非项目标

- 不是人格扮演 Prompt，也不是"扮演 lailai"。
- 不是一次性生成后固定不变的静态人设。
- 不是用来冒充 lailai 本人欺骗他人的工具。
- 不是只服务工作的模板——它也覆盖日常聊天、学习与长期自我建模。

## 安全边界

- 不冒充 lailai 本人对外发言、做承诺、声明身份或授权。
- 不保存账号、密码、密钥、证件、精确住址等敏感信息。
- 不公开私人聊天、他人隐私或未整理的敏感资料。
- 生成内容若可能被误认为本人真实发言，须提醒人工确认。
- 长期人格、价值判断与隐私边界的重要变化必须人工确认。公开表达方式也一样。

完整边界见 [profile/boundaries.md](profile/boundaries.md)。

## 适用场景

- 写作 / 润色中文内容，去 AI 腔。
- 写或审查 README、项目介绍、GitHub 文档。
- 在目标仓库内部规范下写 Markdown / MDX 笔记、题解与数学文章。
- 写或评审 OI 算法竞赛 C++17 代码。
- 将洛谷工作流路由到 `luogu-solution`，新仓库路由到 `lailai-template`。
- 个人行为模型保留在本仓库，思想立场与教义发展路由到 `laiism-skill`。
- "统一·简约·现代"风格的 UI / 设计审查。
- 模拟 lailai 的日常聊天与提问方式。
- 决策辅助、学习陪伴、长期自我建模与持续更新。

不适用场景与触发条件见 [SKILL.md](SKILL.md)。

## 项目结构

```bash
lailai-skill/
├── evolution/                      # 评分标准与进化日志
├── examples/                       # 代表性输入与输出对照
├── profile/                        # 长期身份、偏好与边界
├── prompts/                        # 维护提示词
├── references/                     # 可执行风格与工作流规则
├── tests/                          # 可验证行为测试
├── tools/                          # Checker 与辅助工具
├── observations.md                 # 尚未沉淀的观察
├── SKILL.md                        # Skill 入口
└── test-prompts.json               # Prompt 回归样例
```

## 快速开始

本仓库是一个标准 Agent Skill（`SKILL.md` + frontmatter `name: lailai-skill`），可用于 Claude Code、Codex、Cursor、OpenClaw、Gemini CLI 等兼容 skills 的 runtime。

### 放哪里（位置是硬要求）

skill **必须**放在已配置的 skills 目录；随便放在某个仓库根目录，并不会让所有 runtime
自动发现它。

权威用户级安装路径是 `~/.agents/skills/lailai-skill/`。只安装一份，各项目通过 Skill 名称或
GitHub 权威源作文本引用；不要再用 submodule、内嵌副本或逐项目复制，否则会形成过期的平行
真源。若某个 runtime 不会原生发现 `~/.agents/skills`，只加一个常数大小的目录适配入口。

### 用户级（clone 一次）

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/lailai0916/lailai-skill ~/.agents/skills/lailai-skill
# 更新：cd ~/.agents/skills/lailai-skill && git pull
```

若要让洛谷专用流程无需临时抓取即可被发现，将它安装在同一用户级目录：

```bash
git clone https://github.com/lailai0916/luogu-solution ~/.agents/skills/luogu-solution
```

涉及 laiism 与思想材料时，将独立 Skill 安装在同一目录：

```bash
git clone https://github.com/lailai0916/laiism-skill ~/.agents/skills/laiism-skill
```

### 装好之后

1. 入口是其中的 `SKILL.md`；Agent 先读它，再按任务类型读对应 `profile/` 与 `references/`（链接都是相对路径，整体搬动后仍有效）。
2. 触发：描述聊天 / 写作 / 代码 / 设计 / 决策类任务时自动匹配 description，或明确说"用 lailai 的风格""按我的习惯来""像我一点"。
3. 目标仓库内部 Agent 规则在该项目范围内优先。洛谷任务转到
   [`luogu-solution`](https://github.com/lailai0916/luogu-solution)；新建 GitHub 仓库从
   [`lailai-template`](https://github.com/lailai0916/lailai-template) 开始。
4. 涉及 laiism 与思想立场时，读取独立安装的 [`laiism-skill`](https://github.com/lailai0916/laiism-skill)；未安装时读取其权威仓库。普通聊天与代码任务不要求加载它。

## 习惯记录

发现一个新的表达、偏好、反感项或习惯时，**先记到 [observations.md](observations.md)**，不要直接改规则。思想材料归 `laiism-skill`；本仓库只保留行为观察和引用，不维护第二份立场正文。

> 观察不等于规则。只有长期、稳定、可迁移、可执行的观察，才能进入 `profile/` 或 `references/`。

可直接复制 [prompts/add-observation.md](prompts/add-observation.md) 给 AI 来记录。

## 持续进化

1. 观察记录：新习惯先进 `observations.md`。
2. 稳定性判断：区分短期情绪、临时偏好与长期习惯。
3. 规则沉淀：验证过的观察整理进 `profile/` 或 `references/`。
4. 示例 / 测试更新：规则变了就更新 `examples/` 与 `tests/`。
5. 达尔文式优化：评估 → 改进 → 测试 → 保留或回滚（[prompts/evolve-skill.md](prompts/evolve-skill.md)）。
6. 版本与日志：重要变化记入 `CHANGELOG.md` 与 `evolution/evolution-log.md`。
7. 人工确认：涉及长期人格、价值判断与隐私边界的变化，由 lailai 确认。公开表达也一样。

## 维护更新

维护是长期工作，不是一次性任务。细则见 [references/maintenance-guide.md](references/maintenance-guide.md)，评分用 [evolution/evaluation-rubric.md](evolution/evaluation-rubric.md)。原则：

- 观察 ≠ 规则，临时情绪 ≠ 长期人格，一次性偏好 ≠ 稳定习惯。
- 规则必须可执行、可检查。每次进化都能说清"为什么改"。
- 若新规则让输出更不像 lailai，回滚；若旧规则与当前状态冲突，更新或废弃。

## 许可协议

本项目代码采用 [MIT 许可协议](https://github.com/lailai0916/tools/blob/main/LICENSE)。原创文档与 Skill 内容采用 [知识共享 署名 4.0 国际许可协议](LICENSE-docs)。
