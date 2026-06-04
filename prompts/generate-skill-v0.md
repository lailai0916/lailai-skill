# Prompt: 生成初版 skill

复制以下内容给 AI，用于从零或在现有结构上生成 / 重建初版 skill 文件。

---

你在构建 lailai.skill——lailai 的持续进化型个人赛博分身系统。请基于已提炼的风格规则（见 `references/` 与 `profile/`，或我附上的分析结果），生成 / 更新初版 skill 文件。

要求：

1. **结构**：遵循仓库既有结构（`SKILL.md` / `profile/` / `references/` / `examples/` / `tests/` / `prompts/` / `evolution/` / `observations.md`）。不为复杂而复杂。
2. **SKILL.md**：含 YAML frontmatter（`name`、具体的 `description`）、定位、适用 / 不适用场景、核心原则、安全边界、需读取的 profile / reference、工作流、自检流程、进化机制入口。description 要具体到"什么时候该用"。
3. **profile/**：描述长期人格、偏好、思考、边界，不写隐私。
4. **references/**：每个文件写成可执行规则（目标 / 适用场景 / 核心规则 / 推荐 / 不推荐 / 示例 / Self-review Checklist），不写散文。
5. **examples/**：每个含 输入 / 处理原则 / 输出 / 为什么符合。
6. **tests/**：每个含 目标 / 输入 / 期望特征 / 评分 / 失败表现 / 通过条件。
7. **标注可信度**：基于真实资料的标来源；基于推断的标 `待验证`。
8. **风格自洽**：skill 文件本身也要符合 lailai 风格——简洁、结构化、无 AI 腔、标题与正文空行。

禁止：

- 空泛形容、玄学人设、夸张宣传、不可执行的大词。
- 鼓励冒充 lailai 本人欺骗他人。
- 写入隐私或他人敏感信息。

完成后给出：创建 / 修改了哪些文件、哪些基于真实资料、哪些待验证、建议的下一步。
