# Reference: Docusaurus / MDX 风格

## 目标

让 Docusaurus 站点（`lailai0916.github.io`）的博客、文档、题解符合 lailai 既有规范。本文件提炼自站点 `.claude/rules/writing-style.md` 与 `.claude/CLAUDE.md`。

## 适用场景

- 在 `lailai0916.github.io` 仓库写 / 改 `blog/`、`docs/`、`i18n/zh-Hans/**` 下的 MDX。
- 写题解、数学文章、笔记、记录、旅行等博客。

> 这是**项目局部规则**，在站点范围内补充 [markdown-style.md](markdown-style.md) 的通用排版（数学分隔符两边一致，都是 `$...$` / `$$...$$`）。

## 核心规则

### 数学（KaTeX，局部覆盖）

- 行内用 `$...$`，行间 `$$...$$`（多步推导用 `\begin{aligned}`）。**不**用 `\(...\)` / `\[...\]`。这与全局规则一致（remark-math 原生语法）。
- 不给公式编号，用 prose 交叉引用。
- 罗马微分 `\mathrm{d}x`；划掉用 `\cancel{}`（非 `\sout`）；集合 `\set{...}`；取模 `\bmod`；单元格里强制大小用 `\displaystyle`。
- 任何数量都包进行内数学：`$30$ 分`、`$2$ 月 $26$ 日`。

### Frontmatter

- 博客字段顺序：`title`、`date`、`authors: lailai`（标量，不是数组）、`tags`（始终数组）。不用 `slug`（文件名即 slug）。
- 文档页只有 `title:`，无 date / authors / tags。
- 日期 `YYYY-MM-DDTHH:MM:SS+08:00`——**带秒，且带 Asia/Shanghai 时区偏移**（`+08:00` 必须；否则 CI 的 UTC 环境会把无偏移时间戳渲染偏 $8$ 小时）：`date: 2025-08-04T15:30:00+08:00`。普通文章秒位用 `:00`；**题解**用其**洛谷专栏对应版本的精确发布秒**（`<Solution>` 的 `aid`，洛谷记录到秒），两边保持一致。
- 标题格式 `<分类>：<名称>`，全角冒号。分类前缀固定：`题解：` / `数学：` / `项目：` / `资源：` / `个人：` / `旅行：` / `记录：` / `杂谈：`。
- tags 只能取自 `blog/tags.yml`。题解恒为 `[oi, solution, <oj>]`（`<oj>` ∈ luogu / codeforces / atcoder / spoj / uva）；数学 `[math]`。不自造 tag。

### 开头与 truncate

- 每篇博客一段简短 lead（通常 < 30 字，一句），空行，再 `{/* truncate */}`。lead 是列表页展示内容。无问候、无"本文将"。
- 题解用 `<Solution pid="..." aid="..." />` 替代 lead，再 `{/* truncate */}`，前面不放 prose。

### 标题

- 正文无 H1，frontmatter `title` 是唯一 H1，正文从 `##` 开始。
- 标题是短中文名词短语，结尾不加 `。？！`。复用既有词汇：`## 参考资料`、`## 题意简述`、`## 解题思路`、`## 参考代码`、`## 思想`、`## 化简`、`## 求解`、`## 例题`。
- `## 参考资料` 通常是引用来源的数学 / 杂谈文章的**第一个** `##`，放在正文前。

### 术语引入

- 技术概念首次出现：`**中文**（English[, ACRONYM]）`，缩写跟在全角逗号后：`**最大公约数**（Greatest Common Divisor，GCD）`。

### 代码块

- C++ 模板不变（见 [cpp-oi-style.md](cpp-oi-style.md)）。语言标签 `cpp`，不是 `c++`。
- C++ 内基本无注释。`title="main.cpp"` 仅在文件身份重要时加；题解省略。不用 `showLineNumbers` 和行高亮。

### MDX 组件

- `<Solution pid="..." aid="..." />`：每篇题解第一行（frontmatter 之后），恰两个属性。
- `<Problem id="..." />`：文档题目页 `## 例题` 末尾。
- `<Quote author="..." source="...">`：个人 / 记录文的题记，作者 / 来源须真实具体。
- `<Desmos id="..." />`、`<Notation>…</Notation>`（极少用）、`<GitHub repo="owner/repo" />`、`<Tabs>/<TabItem>`。

### Admonition

- 用：`:::tip`（澄清旁注）、`:::example`（站点自定义关键字，包 `<Tabs>` 例题）、`:::warning[版权声明]`（仅签名式长文）。
- `:::note` / `:::info` / `:::danger` 基本不用。

### 图片、链接

- 图片托管在 `https://cloud.lailai.one/f/<hash>/<name>.<ext>`，不放本地 `static/`，不用相对路径。`![](url)` 空 alt。明暗双图用 `#gh-light-mode-only` / `#gh-dark-mode-only` 锚点黏在一起、中间无空白。不设 `<img>` 宽高。
- 站内跨文链接用绝对站点路径：`[《……》](/blog/math/zjzk-2025-math-q24)`。
- `## 参考资料` 格式 `- [标题 - 来源](url)`，优先 OI Wiki、Wikipedia、OEIS。

### 题解模板（强制顺序）

1. frontmatter：`title: 题解：<PID> <name>`，`tags: [oi, solution, <oj>]`。
2. `<Solution pid="..." aid="..." />`
3. `{/* truncate */}`
4. 可选 `## 参考资料`。
5. `## 题意简述`（trivial CF / AT 可省）——一两句转述题目要求，**不含数据范围**（范围放思路 / 复杂度处）。
6. `## 解题思路`——**末尾必有复杂度行**：`时间复杂度为 $O(n\log n)$。`。
7. 可选中间推导（`## 基础知识` / `## 化简` / 命名引理）。
8. `## 参考代码`——单个 `cpp` 块，无 fence title、无注释。

无 `## 总结` / `## 结语`。代码结束即全文结束。

**题解美学（语料校准）**：追求**精简、优雅、"几句话说清"的高手感**，不长篇教学。能一两句讲透的思路绝不铺开；显然的题意 / 定义直接略过（"是个人都知道"）。判断标准是"像顶尖高手随手写的"，不是"面面俱到的讲义"。解题思路偏**连贯自然段**，少用 `**X**：` 加粗小标签罗列；简单转移行内 `$...$` 带过即可，多步推导才上 `$$` 公式块。

### 洛谷专栏版（同步拷贝）

每篇题解在洛谷专栏有一份**正文相同**的拷贝（`<Solution>` 的 `aid` 即其文章 id），与站内 mdx 只差结构性头部，正文骨架 / 数学 / 代码完全一致：

- **无 frontmatter、无 `<Solution>`、无 `{/* truncate */}`**。
- 开头放 **2 张 shields.io 徽章**（题目 + 博客），其后直接正文：

  ```md
  [![](https://img.shields.io/badge/Luogu-<PID>-blue?style=for-the-badge&logo=luogu)](https://www.luogu.com.cn/problem/<PID>)
  [![](https://img.shields.io/badge/Blog-Solution-blue?style=for-the-badge&logo=markdown)](https://lailai.one/blog/solution/<PID>)
  ```

  （已从 3 张减为 2 张，去掉「洛谷文章」那张。）

- **所有 OJ 题（含 CF / AT）都先发洛谷专栏拿到 `aid`**，站内 mdx 再用 `<Solution aid>` 引用；mdx 的 `date` 用洛谷专栏的精确发布秒，两边一致（见上「Frontmatter」）。

## lailai 排印约定（站点专属）

- **lailai 始终小写**，即使出现在句首、段落开头或标题中。
- **lailai 及含 lailai's 的名称为不翻译内容**，始终以英语排印，即使在非英语文本中。
- 资源 / 图片走 [lailai's Cloud](https://cloud.lailai.one)；未撰写或未完成的内容用 `[TODO]` 标记。
- 告示用 `:::` 加类型标签（`:::tip` / `:::example` / `:::warning[版权声明]`）。

## 不推荐做法

- 用 `\(...\)` / `\[...\]`；给公式编号；正文写 H1。
- 题解加"总结"或"希望对你有帮助"。
- 自造 tag、用数组写 `authors`、用本地图片路径。
- `:::note` / `:::info` 滥用。

## Self-review Checklist

- [ ] 数学用 `$...$` / `$$...$$`（站内覆盖）？数量都包进数学？
- [ ] frontmatter 字段、顺序、日期格式、分类前缀正确？
- [ ] lead 一句 + 空行 + `{/* truncate */}`（题解用 `<Solution>`）？
- [ ] 正文从 `##` 起，标题无句末标点，复用既有词汇？
- [ ] 引用文章 `## 参考资料` 在最前？
- [ ] 题解遵循强制模板，思路段以复杂度收尾，无"总结"？
- [ ] 图片走 cloud 域名、空 alt、无宽高？
- [ ] 组件属性、admonition 关键字合规？
