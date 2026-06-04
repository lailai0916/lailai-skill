# Reference: 工程代码风格（注释与约定）

## 目标

让工程代码（TS / React / CSS 等非竞赛代码）的注释与约定符合 lailai 习惯。提炼自站点 `.claude/rules/comments.md` 与 `CONTRIBUTING.md`。

## 适用场景

- 写或审查工程代码（前端 / 脚本 / 工具）。
- 与竞赛 C++ 区分：OI 代码见 [cpp-oi-style.md](cpp-oi-style.md)；提交 / Prettier / 项目规范见 [project-docs-style.md](project-docs-style.md)；CSS / 设计见 [design-style.md](design-style.md)。

## 注释规则

1. **注释解释"为什么"，不解释"是什么"**：写意图、非显然的约束、workaround、引用来源。绝不复述下一行明摆着做的事（`// increment i`、`// set state`）。
2. **少**：多数代码不需要注释。命名好的函数 / 变量胜过注释。只有"原因在代码里看不出来"时才写。复述代码的注释比没有更糟——拿不准就删。
3. **简洁**：尽量一行。去掉填充词（"basically""note that""we do this because"），直接陈述事实。
4. **英文、句首大写**：标识符保持原大小写（`sessionStorage`、`react-chrono`）。完整句子以句号结尾，短标签片段不加（`// Camera`、`// No solution available`）。

## 注释形式（只用这些）

- `//` 行注释 —— TS / TSX 默认形式。
- `/* … */` 块注释 —— CSS 里的说明或区段标签。
- JSDoc（`/** */`）—— 仅用于导出组件的 props、公开类型、导出函数；每行紧凑，能一行就一行。
- 工具指令（`// eslint-disable-…`、`// @ts-expect-error …`、`// prettier-…`）—— 是功能不是散文，按工具要求保留。

## 区段标签

长文件需要内部路标时，用**独占一行的纯标签**：TS 用 `// Variants`，CSS 用 `/* Variants */`。标签是短名词短语，不是句子。

- **禁止 ASCII 艺术分隔线**：绝不用 `── … ──`、`===== … =====`、`----- … -----` 或任何重复字符成行。这是视觉噪音。

## 禁止

- **不留注释掉的代码**：删掉，git 记得。唯一例外：明确标注的配置开关（作为可用选项的就地文档）。
- **不写 banner / 文件头注释**、作者标签、日期、变更记录。
- **不留 TODO / FIXME**：未完成的工作进真正的任务清单，不留在注释里。

## 其它约定

- 格式遵循 Prettier（`printWidth: 80`、`singleQuote: true`、`trailingComma: "es5"`），TypeScript `strict`（详见 [project-docs-style.md](project-docs-style.md)）。
- 编辑而非重写：最小、精准改动，一次一个连贯改动，不重排无关代码。
- 复用优先于新造；现代 CSS、CSS Modules 同目录（详见 [design-style.md](design-style.md)）。

## Self-review Checklist

- [ ] 注释只解释"为什么"，没有复述代码？
- [ ] 注释少而精，英文句首大写、形式合规？
- [ ] 区段标签是纯名词短语，没有 ASCII 分隔线？
- [ ] 没有注释掉的代码、banner、作者 / 日期、遗留 TODO / FIXME？
- [ ] 格式走 Prettier，改动最小、不重排无关代码？
