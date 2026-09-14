# Reference: README 与项目规范

## 目标

写出像 lailai 的 README、项目文档，并遵循 lailai 的通用项目工程规范。本文件是这些规范的唯一维护位置；`lailai-template` 只提供可直接使用的实例。

## 适用场景

- 写或改 README、项目介绍、贡献指南、文档站首页。
- 审查项目结构、Git / 提交规范、文档风格。

## 项目工程规范

> **套用前先判档**，但新建公开 GitHub 仓库默认按完整标准交付：
>
> - **强制**：从 `lailai-template` 起步；`LICENSE`、Conventional Commits、`.gitignore`、居中双语 README、徽章、仓库描述与 topics；JS/TS 项目还含 Prettier。
> - **按项目决定**：对外发版才需 `CHANGELOG.md`；接受外部贡献才需 `CONTRIBUTING.md`。只有用户明确限定为私有内部脚本或单语内容时，才能省略 README i18n。

1. **Git 提交遵循 Conventional Commits**：`type(scope): description`（如 `feat: ...`、`fix(blog): ...`、`docs: ...`）。
2. **`.gitignore`** 用 Vite 默认模板。
3. **贡献指南（仅协作项目）**：有外部协作 / 会接受贡献的项目才写贡献指南，放 `.github/CONTRIBUTING.md`；单人小工具不必加。
4. **多语言以英文为基准**。英文使用 `README.md`。
   其他语言使用 `README.<language-tag>.md`，如 `README.zh-Hans.md`。
   新建公开仓库至少提供英语 + 简体中文两份完整 README，**默认英语**；有可视化内容时，产品本身也做 en + zh-Hans i18n。已有 i18n（其他语言 / 默认非英语）时沿用原配置。只有用户明确限定为私有内部脚本或单语内容时才省略。
5. **许可协议**：每个开源项目都要有 `LICENSE`，README 末尾必有 License 段。**代码项目默认 MIT**；README 的 MIT 链接统一指向 `https://github.com/lailai0916/tools/blob/main/LICENSE`，不链接当前仓库内的 `LICENSE`。英文固定写 `This project's code is licensed under [MIT License](https://github.com/lailai0916/tools/blob/main/LICENSE).`；中文对应写 `本项目代码采用 [MIT 许可协议](https://github.com/lailai0916/tools/blob/main/LICENSE)。`。**个人创作内容**（文章 / 设计 / 作品集等非代码）惯用 **CC BY-NC-SA**。
6. **版本与变更日志（仅发版项目）**：需要对外发布版本的项目才维护——版本遵循 Semantic Versioning，变更日志遵循 Keep a Changelog（`CHANGELOG.md`）。一次性脚本、小工具、单语内容项目不强加空骨架。
7. **Prettier 必装**：每个项目都装 Prettier 做格式化——`devDependency` + 配置文件（`printWidth: 100`、`singleQuote: true`、`trailingComma: "es5"`）+ `format` 脚本，HTML / CSS / JS / TS / JSON / MD 统一交给它，不手动对齐。C++ 见 [cpp-oi-style.md](cpp-oi-style.md)；文档文本遵循 [markdown-style.md](markdown-style.md) / [wording.md](wording.md)。
8. **仓库名、项目名、文件名分层**：GitHub 仓库名用小写 kebab-case；README `<h1>` 写正式项目名，不机械复制仓库名。单个英文单词的项目名首字母大写（仓库 `wordcloud` → 项目 `Wordcloud`）；多词项目按正式品牌分词与大小写。明确的品牌写法优先：`lailai-template` 显示名不变；`laiism-skill` 的显示名为 `laiism`，标题、句首与派生名称中的 `laiism` 始终小写。新文件与目录默认使用英文 ASCII 名称，遵循语言生态的命名习惯，禁止中文文件名；Finder 启动脚本写成 `start.command` 这类英文 kebab-case 名称。
9. **仓库 About 元数据是交付物**：description 用一句英文准确定位，不塞营销词；topics 使用 $3\sim8$ 个小写 kebab-case 关键词，覆盖领域、技术栈与用途；若有项目主页，同步 homepage。新建或重构仓库时必须核对 GitHub About 面板，不把它留作未说明的手工善后。

## README 文档风格

10. **一句话定位放最前**：用一句准确的话说清"这是什么"，10 秒看懂。
11. **结构清晰、跨项目统一**：介绍 → 特性 → 快速开始 → 结构 → 其它 → **末尾 License 段**。每节短、直给；**所有项目 README 用同一套结构与格式**。
12. **居中头部**：标题下放语言导航，下一行放 shields.io 徽章。
    语言间用 ` · ` 分隔。当前语言用 `<strong>` 加粗且不加链接。其他语言保留链接。
    徽章至少包括 last commit、top language、repo size 与 license；存在 CI、code style、coverage、release 等真实能力时必须同步展示，不放失效或虚构徽章。
13. **特性清单**：emoji + 加粗小标题 + 一句说明（`🎨 **Bespoke Home** — 一句话。`）。emoji 仅在 README 特性区用，技术正文不用。
14. **项目结构树严格统一**：只用 `bash` 代码块，根节点写 GitHub 仓库名。仅列帮助理解项目的专属核心目录与文件；不列 `README*`、`LICENSE*`、`.gitignore`、`.gitattributes`、`.gitmodules`、`.agents/`、`.claude/`、`AGENTS.md`、`CLAUDE.md` 等通用仓库元数据。每一级都先列文件夹、再列文件；同组按名称字典序排列。每个条目行末写一句必要注释；所有 `#` 必须位于索引 `max(w+1,36)`，其中 `w` 是结构树中最长条目左侧的字符数，默认索引为 $36$。**快速开始给可复制 `bash` 命令**。
15. **双语对等**：英文与中文各一份完整 README，互为镜像，不是翻译残桩。
16. **专业克制**：不堆形容词，不写"最强 / 革命性 / 颠覆"，不写"求 star"式收尾。

## 推荐做法

- 第一屏让人 10 秒看懂"是什么、解决什么、怎么跑"。
- 每个特性一句话，动词开头或名词短语。
- 命令块复制即用；中英文风格、结构、emoji 用法一致。
- 提交信息用 Conventional Commits，一次一个连贯改动。

## 不推荐做法

- 长篇背景故事、心路历程开场。
- 形容词轰炸（"强大、优雅、极致、丝滑"）。
- 中英文 README 一详一略、结构不对齐。
- "希望多多 star / 支持"式收尾。
- 提交信息写成 "update" / "fix bug" 这类无 type、无 scope 的模糊话。

## 示例

提交信息：

```text
feat(profile): add decision-rules and boundaries
docs: rewrite README intro to one-line positioning
fix(cpp): correct naming-table example
```

README 特性区：

```markdown
## Features

🎨 **Bespoke Home** — 自定义 bento 网格首页，带 Lorenz 吸引子动画。

📐 **Math & Live Code** — 自托管 KaTeX、Mermaid 图、可运行 React 代码块。
```

README 头部骨架（`<owner>` / `<repo>` 替换为实际值；preview 图可选，没有就删 `<picture>`）：

```html
<div align="center">
  <h1>project-name</h1>
  <p><strong>English</strong> · <a href="README.zh-Hans.md">简体中文</a></p>
  <p>
    <img
      src="https://img.shields.io/github/actions/workflow/status/<owner>/<repo>/deploy.yml?style=flat-square"
    />
    <img
      src="https://img.shields.io/github/last-commit/<owner>/<repo>?style=flat-square"
    />
    <img
      src="https://img.shields.io/github/languages/top/<owner>/<repo>?style=flat-square"
    />
    <img
      src="https://img.shields.io/github/repo-size/<owner>/<repo>?style=flat-square"
    />
    <img
      src="https://img.shields.io/badge/code_style-prettier-ff69b4?style=flat-square"
    />
    <img
      src="https://img.shields.io/github/license/<owner>/<repo>?style=flat-square"
    />
  </p>
</div>
```

`README.zh-Hans.md` 的语言行镜像为：

```html
<p><a href="README.md">English</a> · <strong>简体中文</strong></p>
```

合规的项目结构树：

```bash
task-cli/
├── bin/                            # Executable entry
└── src/                            # Command and storage logic
```

末尾 License 段：

```markdown
## License

This project's code is licensed under [MIT License](https://github.com/lailai0916/tools/blob/main/LICENSE).
```

## Self-review Checklist

- [ ] 提交信息是 Conventional Commits（`type(scope): description`）？
- [ ] 从 `lailai-template` 起步；README 使用正式项目名；第一屏一句话定位，10 秒看懂；新增路径无中文文件名？
- [ ] 结构：介绍 → 特性 → 快速开始 → 结构 → 其它，每节简短？
- [ ] 居中标题、语言导航与真实徽章齐全；特性区 emoji + 加粗标题 + 一句说明？
- [ ] 结构树为 `bash` 块，仅列项目专属内容；文件夹优先、各组字典序；所有 `#` 均位于 `max(w+1,36)`？
- [ ] 多语言以英文为基准，`README.md` / `README.zh-Hans.md` 中英对等？语言导航是否用 ` · ` 分隔，并仅加粗当前语言？有 UI 内容时，i18n 是否默认 en + zh-Hans、默认英语？
- [ ] 有 `LICENSE`（开源默认 MIT）+ README 末尾 License 段，MIT 链接指向 `lailai0916/tools`；装了 Prettier（config + format 脚本）？
- [ ] GitHub description、$3\sim8$ 个 topics 与 homepage 已核对；无形容词轰炸、无求 star 收尾、技术正文 emoji 克制？
