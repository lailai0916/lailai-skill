# Preferences

lailai 的长期偏好与反感。稳定、可迁移的写这里；一次性的先进 `observations.md`。

## 语言与表达

- 简体中文。语言风格：简洁、自然、专业。
- 信息密度高，先结论后依据，能分点 / 对照 / 举例就不抒情。
- 中英之间留空格（`使用 React`，不是 `使用React`）。
- 术语首次出现用 `中文（English[, ACRONYM]）` 介绍。
- 数值、量、范围习惯精确化。

## 设计理念

- **统一 · 简约 · 现代**。
- 系统字体优先（SF Pro / system-ui，辅以 Inter）；主色干净（站点用 Twitter 蓝 `#1d9bf0`）。
- 动效克制：只在小元素上给清晰交互反馈（箭头轻移、图标轻微 `scale()`），**绝不给整卡 hover 上浮**——这是明确反感的 AI-tell。
- 现代 CSS（`grid`、`clamp()`、`color-mix()`、容器查询）优先于 JS 布局。
- 复用既有组件 / 原语优先于新造；新 UI 要和既有部分视觉与行为上看不出差别。

## 代码

- OI / 算法竞赛：C++17，`#include <bits/stdc++.h>`，`using namespace std;`，Tab 缩进，不写注释，不写防御性输入，优先 `cin` / `cout`，全局静态大数组，短变量名，`main` 结尾 `return 0;`，Allman 大括号。详见 [../references/cpp-oi-style.md](../references/cpp-oi-style.md)。
- 工程代码（站点）：严格 TypeScript，Prettier（`printWidth: 80`、`singleQuote: true`、`trailingComma: 'es5'`），CSS Modules，注释少而统一、只解释"为什么"。
- 编辑而非重写；一次一个连贯改动；不重排无关代码。

## 数学公式

- 统一用 `$...$`（行内）与 `$$...$$`（行间），所有场景一致（含 Docusaurus 站内）。不用 `\(...\)` / `\[...\]`。详见 [../references/markdown-style.md](../references/markdown-style.md) 与 [../references/docusaurus-style.md](../references/docusaurus-style.md)。

## 文档与排版

- Markdown 标题与正文之间保留一行空行。
- 中文 prose 用全角标点；引号用「」，书名用《》。
- README / 项目文档：徽章 + emoji 功能清单 + 树形结构 + 双语对等。

## 品味取向（语料校准）

- Apple 生态重度用户（16 寸 M3 Max MacBook Pro、iPhone、Watch、AirPods Max），熟悉型号与参数细节。
- 偏好高端、精工、龙头品牌叙事（Apple、德系精工、Sony Hi-Res、Leica 一类），把它们当参照标杆。
- 对"世界第一 / 最大 / 排名前十"类极值信息有持续兴趣，习惯量化与横向比较。
- Claude / Anthropic 的拥护者。
- 交付物偏轻量、可控、自己掌握的栈（HTML/CSS 手写转 PDF，不愿学 Figma/PS；用框架自带变量而非裸值）；能自动化 / 跟随系统就别加手动开关。

## AI 协作的交还方式（语料校准）

- 学新工具 / 排障时要 AI **一次只说一步**，做完确认再给下一步；一次抛十几条会被打断。
- 默认要 AI **只给建议、别动文件**（"告诉我怎么改就行"），落地也倾向自己在本地 VS Code 改，反感 agent 直接在 GitHub 新建 commit。
- 嫌啰嗦："别讲解别注释，直接告诉我做什么"——要动作清单，不要解说。

## 个人品牌与命名（语料校准）

- 把个人标识当长期资产经营：偏极简短域名（`lailai.one` 一类），会比价、研究重定向；站点求冗余（GitHub Pages + 自购服务器双押），强关注多搜索引擎收录与大陆可访问性。
- 取名重形式与味道：英文名爱要结构约束（等长字母、反义对）且"著名 / 好玩 / 有意义"；数字偏爱有趣的（质数、`23333`），嫌普通数字没意思。

## 强反感清单

- AI 腔（空话、抒情、营销、模板化首尾）。
- "希望本文对你有所帮助"式客套收尾、"本文将……"式开场。
- 整卡 hover 上浮等设计 AI-tell。
- 注水、为复杂而复杂、不一致、不落地。
- 把不确定说成确定；编造来源或数据。

## 维护提示

偏好会演化。新偏好先进 `observations.md`，确认稳定且可迁移后再写入。区分"长期偏好"与"特定项目的局部规则"——后者标明适用范围。
