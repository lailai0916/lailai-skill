# Test: README 与项目规范

## 测试目标

验证输出符合 lailai 的 README / 项目规范：一句话定位、多语言导航、统一结构、克制无形容词轰炸、Conventional Commits。

## 输入任务

虚构一个名为 `csv-diff` 的 TypeScript 命令行工具，用于对比两份 CSV 的差异。让被测 AI 编写英文 README 与对应的简体中文 README，并给出 GitHub description、topics 与三条示例提交信息。

## 期望输出特征

- 第一屏一句话定位，10 秒看懂「是什么」。
- 两份 README 的语言导航使用 ` · ` 分隔；当前语言加粗且不加链接，另一语言保留链接。
- 两份 README 均使用居中标题，并包含 last commit、top language、repo size 与 license 四个真实基础徽章。
- README 标题使用正式项目名 `CSV Diff`，仓库名仍为 `csv-diff`；仅明确的品牌写法可以例外（如 `lailai-template`、始终小写的 `laiism`）；所有新增路径使用英文 ASCII 名称。
- 结构：介绍 → 特性 → 快速开始 → 结构 → 其它 → 末尾 License 段。
- 特性区 emoji + 加粗小标题 + 一句说明；技术正文不用 emoji。
- 快速开始给可复制 `bash` 命令；结构树也使用 `bash` 块。
- 结构树不列 README、LICENSE、`.gitignore`、`.agents` 等通用条目；每一级文件夹优先，再按名称字典序排列。
- 每个项目结构条目的 `#` 均位于索引 $32$。
- 末尾 License 段使用 `lailai0916/tools` 的统一 MIT 链接。
- 提交信息为 `type(scope): description`。
- GitHub description 是一句克制的英文定位；topics 为 $3\sim8$ 个准确的小写 kebab-case 关键词。

## 评分标准（0～5）

- 0：长背景故事开场、形容词轰炸、求 star 收尾、提交写 `update`。
- 3：结构基本对，但缺一句话定位 / License 段，或有个别冗余。
- 5：定位 + 语言导航 + 结构 + 命令 + License + 克制 + 规范提交全部到位。

## 常见失败表现

- 「A powerful and elegant tool that revolutionizes…」形容词堆叠开场。
- 没有一句话定位，直接讲背景故事。
- 「如果觉得有用请给个 star ⭐」式收尾。
- 语言导航仍用 `|`，或没有加粗当前语言。
- 提交信息写 `update` / `fix bug`，无 type、无 scope。
- 标题直接写小写仓库名 `csv-diff`，或新增中文文件名。
- 项目结构使用 `text` 代码块，混列文件与文件夹，或用空格凭视觉对齐。
- 项目结构列出 README、LICENSE、`.gitignore`、`.agents` 等通用条目。
- License 链接当前仓库内的 `LICENSE`。

## 客观检查项（可机械判定，全过才算通过）

- [ ] 标题为 `CSV Diff`，新增路径均为英文 ASCII 名称；第一屏一句话说清项目定位；两份 README 的语言导航使用 ` · `，并分别加粗当前语言。
- [ ] 居中头部与四个基础徽章齐全，徽章路径指向实际 owner / repo。
- [ ] `## Features` 条目使用 emoji + 加粗标题 + 一句具体说明，无营销形容词或求 star 文案。
- [ ] 有可复制的 `bash` 安装 / 运行命令块。
- [ ] 项目结构为 `bash` 块，且不含通用仓库元数据。
- [ ] 项目结构逐级「文件夹在前、文件在后」，各组按名称字典序排列。
- [ ] 项目结构所有 `#` 均位于索引 $32$。
- [ ] 有末尾 `## License` 段，链接统一的 MIT License URL。
- [ ] 三条提交信息符合 Conventional Commits，无裸 `update` / `fix bug`。
- [ ] 给出合规的 GitHub description 与 $3\sim8$ 个 topics。

## 通过条件

主观评分 ≥ 4 分，**且**上述客观检查项全部通过。
