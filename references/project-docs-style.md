# Reference: README 与项目规范

## 目标

写出像 lailai 的 README、项目文档，并遵循 lailai 的项目工程规范。提炼自站点 `docs/project/guides/project.mdx`（lailai 的《项目规范指南》）、`README.md` / `README.zh-Hans.md`、`.claude/CLAUDE.md`。

## 适用场景

- 写或改 README、项目介绍、贡献指南、文档站首页。
- 审查项目结构、Git / 提交规范、文档风格。

## 项目工程规范（来自《项目规范指南》）

1. **Git 提交遵循 Conventional Commits**：`type(scope): description`（如 `feat: ...`、`fix(blog): ...`、`docs: ...`）。
2. **`.gitignore`** 用 Vite 默认模板。
3. **贡献指南**放 `.github/CONTRIBUTING.md`。
4. **README** 用 `README.md`；多语言以英文为基准，其它语言用 `README.<language-tag>.md`（如 `README.zh-Hans.md`）。
5. **许可协议**：每个开源项目都要有 `LICENSE`，**默认 MIT**。README 末尾必有 License 段说明。
6. **版本**遵循 Semantic Versioning；**变更日志**遵循 Keep a Changelog。
7. **Prettier 必装**：每个项目都装 Prettier 做格式化——`devDependency` + 配置文件（`printWidth: 80`、`singleQuote: true`、`trailingComma: "es5"`）+ `format` 脚本，HTML / CSS / JS / TS / JSON / MD 统一交给它，不手动对齐。C++ 见 [cpp-oi-style.md](cpp-oi-style.md)；文档文本遵循 [markdown-style.md](markdown-style.md) / [wording.md](wording.md)。

## README 文档风格

8. **一句话定位放最前**：用一句准确的话说清"这是什么"，10 秒看懂。
9. **结构清晰、跨项目统一**：介绍 → 特性 → 快速开始 → 结构 → 其它 → **末尾 License 段**。每节短、直给；**所有项目 README 用同一套结构与格式**。
10. **居中头部 + 徽章**（展示型项目）：标题、双语切换链接、一排 shields.io 徽章（CI、last commit、top language、repo size、code style、license）。
11. **特性清单**：emoji + 加粗小标题 + 一句说明（`🎨 **Bespoke Home** — 一句话。`）。emoji 仅在 README 特性区用，技术正文不用。
12. **结构树用 `text` 代码块**画目录，关键目录后跟注释；**快速开始给可复制 `bash` 命令**。
13. **双语对等**：英文与中文各一份完整 README，互为镜像，不是翻译残桩。
14. **专业克制**：不堆形容词，不写"最强 / 革命性 / 颠覆"，不写"求 star"式收尾。

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
  <p>English | <a href="README.zh-Hans.md">简体中文</a></p>
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

末尾 License 段：

```markdown
## License

Licensed under the [MIT License](LICENSE).
```

## Self-review Checklist

- [ ] 提交信息是 Conventional Commits（`type(scope): description`）？
- [ ] README 第一屏一句话定位，10 秒看懂？
- [ ] 结构：介绍 → 特性 → 快速开始 → 结构 → 其它，每节简短？
- [ ] 展示型项目有徽章；特性区 emoji + 加粗标题 + 一句说明？
- [ ] 结构树 `text` 块、命令 `bash` 块且可复制？
- [ ] 多语言以英文为基准（`README.md` / `README.zh-Hans.md`）、中英对等？
- [ ] 有 `LICENSE`（开源默认 MIT）+ README 末尾 License 段；装了 Prettier（config + format 脚本）？
- [ ] 无形容词轰炸、无求 star 收尾、技术正文 emoji 克制？
