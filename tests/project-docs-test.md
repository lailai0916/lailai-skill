# Test: README 与项目规范

## 测试目标

验证输出符合 lailai 的 README / 项目规范：一句话定位、统一结构、克制无形容词轰炸、Conventional Commits。

## 输入任务

让被测 AI 为一个虚构小型开源工具（`csv-diff`，一个对比两份 CSV 差异的命令行工具，TypeScript）写英文 README，并给三条示例提交信息。

## 期望输出特征

- 第一屏一句话定位，10 秒看懂「是什么」。
- 结构：介绍 → 特性 → 快速开始 → 结构 → 其它 → 末尾 License 段。
- 特性区 emoji + 加粗小标题 + 一句说明；技术正文不用 emoji。
- 快速开始给可复制 `bash` 命令；结构树用 `text` 块、`#` 注释竖向对齐。
- 末尾有 License 段，代码项目默认 MIT。
- 提交信息为 `type(scope): description`。

## 评分标准（0～5）

- 0：长背景故事开场、形容词轰炸、求 star 收尾、提交写 `update`。
- 3：结构基本对，但缺一句话定位 / License 段，或有个别冗余。
- 5：定位 + 结构 + 命令 + License + 克制 + 规范提交全部到位。

## 常见失败表现

- 「A powerful and elegant tool that revolutionizes…」形容词堆叠开场。
- 没有一句话定位，直接讲背景故事。
- 「如果觉得有用请给个 star ⭐」式收尾。
- 提交信息写 `update` / `fix bug`，无 type、无 scope。

## 客观检查项（可机械判定，全过才算通过）

- [ ] 第一屏有一句话定位（介绍段首句即说清是什么）。
- [ ] 有 `## Features`（或等价）特性区，条目为 emoji + 加粗标题 + 一句说明。
- [ ] 有可复制的 `bash` 安装 / 运行命令块。
- [ ] 有末尾 `## License` 段，注明 MIT（代码项目）。
- [ ] 无「powerful」「revolutionary」「求 star / give it a star」等词。
- [ ] 三条提交信息均为 `type: …` 或 `type(scope): …`，无裸 `update` / `fix bug`。

## 通过条件

主观评分 ≥ 4 分，**且**上述客观检查项全部通过。
