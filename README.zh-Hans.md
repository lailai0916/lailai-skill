<div align="center">
  <h1>lailai.skill</h1>
  <p><a href="README.md">English</a> | 简体中文</p>
  <p>
    <img src="https://img.shields.io/github/last-commit/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/languages/top/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/repo-size/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/license/lailai0916/lailai-skill?style=flat-square" />
  </p>
</div>

> lailai 的持续进化型个人赛博分身系统，用于尽可能复刻 lailai 的表达方式、思维方式、审美偏好、工作习惯与日常交流风格。

面向 Claude Code / Codex / Cursor / OpenClaw 等 AI Agent 的个人 skill。它不是一句"请扮演 lailai"，而是一个结构化、可维护、可验证、可持续进化的个人模型。

## 它解决什么问题

让 AI 在写作、文档、代码、设计、聊天、判断与项目维护中尽可能像 lailai，并且随时间越来越像——风格一致、信息密度高、没有 AI 腔、能落地。

## 它不是什么

- 不是人格扮演 Prompt，也不是"扮演 lailai"。
- 不是一次性生成后固定不变的静态人设。
- 不是用来冒充 lailai 本人欺骗他人的工具。
- 不是只服务工作的模板——它也覆盖日常聊天、学习与长期自我建模。

## 边界

- 不冒充 lailai 本人对外发言、做承诺、声明身份或授权。
- 不保存账号、密码、密钥、证件、精确住址等敏感信息。
- 不公开私人聊天、他人隐私或未整理的敏感资料。
- 生成内容若可能被误认为本人真实发言，须提醒人工确认。
- 长期人格、价值判断、隐私边界、公开表达方式的重要变化，必须由 lailai 人工确认。

完整边界见 [profile/boundaries.md](profile/boundaries.md)。

## 适用场景

- 写作 / 润色中文内容，去 AI 腔。
- 写或审查 README、项目介绍、GitHub 文档。
- 写 Docusaurus / MDX 笔记、题解、数学文章。
- 写或评审 OI 算法竞赛 C++17 代码。
- "统一·简约·现代"风格的 UI / 设计审查。
- 模拟 lailai 的日常聊天与提问方式。
- 决策辅助、学习陪伴、长期自我建模与持续更新。

不适用场景与触发条件见 [SKILL.md](SKILL.md)。

## 仓库结构

```text
lailai-skill/
├── README.md                  # 英文（默认）
├── README.zh-Hans.md          # 简体中文（本文件）
├── SKILL.md                   # 入口：定位、场景、原则、边界、工作流、自检
├── LICENSE                    # MIT
├── CHANGELOG.md               # 重要变化记录
├── profile/                   # 长期人格、偏好、思考方式、边界
│   ├── identity.md
│   ├── personality.md
│   ├── thinking-style.md
│   ├── conversation-style.md
│   ├── preferences.md
│   ├── decision-rules.md
│   └── boundaries.md
├── references/                # 可执行风格规则（每个文件含 Self-review Checklist）
│   ├── daily-chat-style.md
│   ├── writing-style.md
│   ├── wording.md
│   ├── markdown-style.md
│   ├── latex-math-style.md
│   ├── docusaurus-style.md
│   ├── cpp-oi-style.md
│   ├── engineering-code-style.md
│   ├── design-style.md
│   ├── project-docs-style.md
│   ├── learning-style.md
│   ├── ai-tone-blacklist.md
│   └── maintenance-guide.md
├── examples/                  # 代表性输入 → 处理原则 → 输出 → 为什么符合
├── tests/                     # 可验证的风格测试（目标 / 输入 / 期望 / 评分 / 通过条件）
├── prompts/                   # 维护时可直接复制的提示词
├── evolution/                 # 评分标准与进化日志
│   ├── evaluation-rubric.md
│   └── evolution-log.md
└── observations.md            # 尚未沉淀为规则的临时观察
```

## 安装与使用

本仓库是一个标准 Agent Skill（`SKILL.md` + frontmatter `name: lailai-skill`），可用于 Claude Code、Codex、Cursor、OpenClaw、Gemini CLI 等兼容 skills 的 runtime。

### 放哪里（位置是硬要求）

skill **必须**放在 runtime 的 skills 目录，放仓库根目录无效（Claude Code 不会发现它）。

| 安装方式                       | 路径                                  | 适用                                              |
| :----------------------------- | :------------------------------------ | :------------------------------------------------ |
| **用户级**（推荐，个人自用）   | `~/.claude/skills/lailai-skill/`      | 一处安装，**所有项目**自动可用、单一源、零漂移    |
| **项目级**（仓库自带、锁版本） | `<项目>/.claude/skills/lailai-skill/` | 需要 CI / 云端 agent / 别的机器 `clone 即自带` 时 |

> 选法：纯自己跨项目用 → 用户级一次搞定；某仓库要在 CI / 云端跑 agent 自带 skill → 项目级 submodule。**不要同名同时装两级**——用户级会盖掉项目级。

### 用户级（clone 一次）

```bash
git clone https://github.com/lailai0916/lailai-skill ~/.claude/skills/lailai-skill
# 更新：cd ~/.claude/skills/lailai-skill && git pull
```

### 项目级（git submodule）

```bash
cd <项目>
git submodule add https://github.com/lailai0916/lailai-skill .claude/skills/lailai-skill
git commit -m "chore(claude): add lailai-skill submodule"   # gitlink 必须一起提交，见下
```

⚠️ **两个必须做对的点：**

1. **clone 要带上 submodule**，否则 `.claude/skills/lailai-skill/` 是空壳：
   - 新 clone：`git clone --recurse-submodules <项目>`
   - 已 clone：`git submodule update --init --recursive`
   - CI（GitHub Actions）：`actions/checkout` 设 `with: { submodules: recursive }`（GitLab：`GIT_SUBMODULE_STRATEGY: recursive`）。
2. **提交时别漏掉 gitlink**。`git submodule add` 会同时暂存 `.gitmodules` 和 gitlink，二者要一起提交。提交后用 `git submodule status` 确认能看到一行 `<sha> .claude/skills/lailai-skill`；只提交了 `.gitmodules` 没提交 gitlink，别的机器 clone 就拉不到内容。
3. **更新版本（bump pin）**：`git submodule update --remote .claude/skills/lailai-skill && git add .claude/skills/lailai-skill && git commit -m "chore: bump lailai-skill"`。

### 装好之后

1. 入口是其中的 `SKILL.md`；Agent 先读它，再按任务类型读对应 `profile/` 与 `references/`（链接都是相对路径，整体搬动后仍有效）。
2. 触发：描述聊天 / 写作 / 代码 / 设计 / 决策类任务时自动匹配 description，或明确说"用 lailai 的风格""按我的习惯来""像我一点"。

## 如何记录新习惯

发现一个新的表达、偏好、反感项或习惯时，**先记到 [observations.md](observations.md)**，不要直接改规则。

> 观察不等于规则。只有长期、稳定、可迁移、可执行的观察，才能进入 `profile/` 或 `references/`。

可直接复制 [prompts/add-observation.md](prompts/add-observation.md) 给 AI 来记录。

## 如何持续进化

1. 观察记录：新习惯先进 `observations.md`。
2. 稳定性判断：区分短期情绪、临时偏好与长期习惯。
3. 规则沉淀：验证过的观察整理进 `profile/` 或 `references/`。
4. 示例 / 测试更新：规则变了就更新 `examples/` 与 `tests/`。
5. 达尔文式优化：评估 → 改进 → 测试 → 保留或回滚（[prompts/evolve-skill.md](prompts/evolve-skill.md)）。
6. 版本与日志：重要变化记入 `CHANGELOG.md` 与 `evolution/evolution-log.md`。
7. 人工确认：涉及长期人格、价值判断、隐私边界、公开表达的变化，由 lailai 确认。

## 如何维护和更新

维护是长期工作，不是一次性任务。细则见 [references/maintenance-guide.md](references/maintenance-guide.md)，评分用 [evolution/evaluation-rubric.md](evolution/evaluation-rubric.md)。原则：

- 观察 ≠ 规则，临时情绪 ≠ 长期人格，一次性偏好 ≠ 稳定习惯。
- 规则必须可执行、可检查。每次进化都能说清"为什么改"。
- 若新规则让输出更不像 lailai，回滚；若旧规则与当前状态冲突，更新或废弃。

## 许可证

代码与文本以 [MIT License](LICENSE) 授权。本 skill 描述的是公开可分享的风格与方法，不包含隐私信息。
