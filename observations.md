# Observations

这里记录尚未整理进正式规则的临时观察。

观察不等于规则。只有长期、稳定、可迁移、可执行的观察，才能进入 `profile/` 或 `references/`。

## 沉淀前的判断原则

- 临时情绪不等于长期人格。某天的烦躁、客气或随口一句，不是稳定特征。
- 一次性偏好不等于稳定规则。只出现过一次的选择，先观察，不要立刻成文。
- 私人隐私不应进入公开 skill。账号、密码、密钥、证件、精确住址等一律不记。
- 与他人有关的敏感信息不应进入公开 skill。
- 只有经过多次验证（至少 2～3 次不同场景重现）的习惯，才能进入正式规则。
- 沉淀时要能说清"为什么是稳定习惯"，而不只是"我觉得像"。

## 记录格式

每条观察用下面的结构（可复制 [prompts/add-observation.md](prompts/add-observation.md) 让 AI 代填）：

```text
### YYYY-MM-DD 一句话标题

- 现象：观察到什么（尽量带原话 / 具体例子）。
- 场景：在什么情境下出现。
- 推测：可能反映什么习惯或偏好（标明是推测）。
- 稳定性：首次出现 / 第 N 次重现。
- 处理：继续观察 / 待验证 / 建议沉淀到某文件。
- 隐私检查：是否含隐私或他人敏感信息（应为"否"才保留）。
```

## 沉淀流程

1. 在下方 Pending Observations 追加一条。
2. 同一习惯多次重现后，标注重现次数。
3. 稳定且可迁移 → 写入 `profile/` 或 `references/`，并在 `CHANGELOG.md` 记一笔。
4. 沉淀后，把这里的对应条目标 `已沉淀 → 文件名`，定期清理。
5. 涉及长期人格、价值判断、隐私边界、公开表达的变化，沉淀前需人工确认。

## Pending Observations

<!-- 在此追加新观察。示例（占位，可删）： -->

### 2026-06-03 初始化占位

- 现象：本文件由 v0.1.0 初始化，暂无真实待沉淀观察。
- 场景：项目创建。
- 推测：无。
- 稳定性：—
- 处理：等待真实使用中产生的观察。
- 隐私检查：否。

### 2026-06-04 第三方仓库画像报告（来源记录）

- 现象：lailai 提供了一份他人基于个人网站写的评价报告，含证据型观察。
- 场景：v0.3.1 校准。
- 已沉淀（与第一方证据互相印证，已写入 `profile/personality.md` / `thinking-style.md`）：
  - 体系化 / 立规矩、长期 / 产品心态、按场景用不同标准。
  - "张力与不一致"：自律分场景、标准后建旧产出未对齐、简约理念 vs 加法冲动。
- 待 lailai 确认（第三方推断，未沉淀为硬规则）：
  - "功能最大化"是否算需要克制的倾向，还是他认可的偏好。
  - "言行不一（旧题解仍用'不难发现'）"是否只是历史遗留、不代表当前标准。
- 明确不写入（报告也声明无法判断）：真实竞赛名次、团队协作能力、AI 使用占比、校内表现。
- 稳定性：报告与第一方证据多处吻合，但属第三方视角，解读性条目需本人确认。
- 处理：已折中处理（印证项沉淀，解读项待确认）。
- 隐私检查：否（报告与本条目均不含 PII）。

### 2026-06-07 题解双发布：洛谷专栏版 vs 个人站 mdx（补 references 空白）

- 现象：每篇题解发两处，格式不同。`docusaurus-style.md` 只覆盖了个人站 mdx，**洛谷专栏版是空白**。
  - 个人站 mdx（已有规则）：`blog/solution/<PID>.mdx`（保留大写 PID）；frontmatter（`title` 全角冒号 / `date` 带秒+时区 / `authors: lailai` 标量 / `tags: [oi, solution, <oj>]`）+ `<Solution pid="<PID>" aid="<洛谷文章id>" />` + `{/* truncate */}`；正文从 `##` 起、无 H1、无徽章。
  - 洛谷专栏版（缺口）：**无 frontmatter**；开头放 **2 张 shields.io 徽章**——题目 + 博客（已从 3 张减为 2 张，去掉「洛谷文章」那张）：
    - `[![](https://img.shields.io/badge/Luogu-<PID>-blue?style=for-the-badge&logo=luogu)](https://www.luogu.com.cn/problem/<PID>)`
    - `[![](https://img.shields.io/badge/Blog-Solution-blue?style=for-the-badge&logo=markdown)](https://lailai.one/blog/solution/<PID>)`
  - 共同点：骨架（可选 `## 参考资料` → `## 题意简述` → 推导分节 → `## 参考代码`，推导末句给复杂度，无总结）、数学 `$...$`、代码遵循 cpp-oi-style，两版一致。
  - 流程：**所有 OJ 题（含 CF/AT）都先发洛谷专栏拿 `aid`**（洛谷文章 id，记录到秒），个人站再用 `<Solution aid>` 引用，且 mdx 的 `date` 用洛谷专栏那一秒，两边一致。`oj` 随题号前缀（P/B→luogu、CF→codeforces、AT→atcoder、SP→spoj、UVA→uva）。
- 场景：用 lailai 的经验手册 + 109 篇真实题解（`lailai0916.github.io/blog/solution`）校准自动题解工具 `luogu-auto-writer` 时发现。
- 推测：洛谷专栏版从未进 references，因为站点规则仓库只管站内 mdx。
- 稳定性：109 篇 mdx 一致 + 手册明述，确定性高。
- 处理：建议沉淀为 `references/luogu-solution-style.md`，或在 `docusaurus-style.md` 增一节「洛谷专栏版」。
- 隐私检查：否。
