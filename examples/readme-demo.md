# Example: 把普通 README 改成 lailai 项目文档风格

## 输入（普通 / AI 腔 README）

> # My Cool Project
>
> This is a super powerful and amazing tool that will revolutionize the way you work! It's built with love and cutting-edge technology. We hope you enjoy using it as much as we enjoyed building it. Please give us a star if you like it! ⭐⭐⭐
>
> ## How to use
>
> Just install it and run. It's super easy!

## 处理原则

- 一句话定位放最前，删形容词轰炸和乞讨式收尾（[project-docs-style.md](../references/project-docs-style.md)）。
- 结构：介绍 → 特性 → 快速开始 → 结构。命令可复制（[markdown-style.md](../references/markdown-style.md)）。
- 专业、克制、信息密度高。

## 输出（lailai 风格）

```markdown
<div align="center">
  <h1>Task CLI</h1>
  <p><strong>English</strong> · <a href="README.zh-Hans.md">简体中文</a></p>
  <p>
    <img src="https://img.shields.io/github/last-commit/example/task-cli?style=flat-square" />
    <img src="https://img.shields.io/github/languages/top/example/task-cli?style=flat-square" />
    <img src="https://img.shields.io/github/repo-size/example/task-cli?style=flat-square" />
    <img src="https://img.shields.io/github/license/example/task-cli?style=flat-square" />
  </p>
</div>

## Project Introduction

> 一个极简的命令行待办工具，纯本地、零依赖、单文件存储。

## Features

📋 **Plain-Text Storage** — 任务存成单个 JSON 文件，可手改、可同步、可版本控制。

⚡ **Zero Dependencies** — 单文件脚本，无运行时依赖。

🔍 **Fast Filter** — 按状态 / 标签 / 关键词过滤，毫秒级。

## Getting Started

\`\`\`bash
npm install -g task-cli
task add "写周报" --tag work
task ls --tag work
\`\`\`

## Project Structure

\`\`\`bash
task-cli/
├── bin/                            # Executable entry
└── src/                            # Command and storage logic
\`\`\`

## License

This project's code is licensed under [MIT License](https://github.com/lailai0916/tools/blob/main/LICENSE).
```

## 为什么符合 lailai.skill

- 第一行一句话定位，10 秒看懂"是什么"。
- 居中标题、双语导航与四个基础徽章齐全；简体中文 README 必须完整镜像。
- 删掉"super powerful""revolutionize""give us a star"。
- 特性用 emoji + 加粗标题 + 一句说明，具体不空泛。
- 项目名使用正式大小写，仓库名仍为小写 kebab-case。
- 快速开始给可复制命令，结构树用 `bash` 代码块。
- 结构树仅列项目专属目录，文件夹按字典序排列，所有 `#` 均位于 `max(w+1,36)`；无更长条目时为索引 $36$。
- License 使用统一的 `lailai0916/tools` MIT 链接。
- GitHub About 另设一句英文 description 与 $3\sim8$ 个准确 topics，不留默认空白。
