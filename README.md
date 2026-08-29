<div align="center">
  <h1>lailai.skill</h1>
  <p><strong>English</strong> · <a href="README.zh-Hans.md">简体中文</a></p>
  <p>
    <img src="https://img.shields.io/github/last-commit/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/languages/top/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/repo-size/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/license/lailai0916/lailai-skill?style=flat-square" />
  </p>
</div>

## Project Introduction

> A continuously evolving personal cyber-twin system for lailai — replicating lailai's expression, thinking, aesthetics, working habits, and everyday communication style as faithfully as possible.

A personal skill for AI agents (Claude Code / Codex / Cursor / OpenClaw, etc.). Not a one-line "act as lailai," but a structured, maintainable, verifiable, and continuously evolving personal model.

## Project Goals

Make AI as much like lailai as possible in writing, docs, code, design, chat, judgment, and project maintenance — and more so over time: consistent style, high information density, no AI tone, and actionable output.

## Non-Goals

- Not a persona-roleplay prompt, nor "act as lailai."
- Not a static persona fixed after a single generation.
- Not a tool to impersonate lailai and deceive others.
- Not a work-only template — it also covers everyday chat, learning, and long-term self-modeling.

## Safety Boundaries

- Does not impersonate lailai in public statements, promises, identity claims, or authorization.
- Does not store accounts, passwords, keys, IDs, precise addresses, or other sensitive data.
- Does not expose private chats, others' privacy, or unvetted sensitive material.
- If output might be mistaken for lailai's real words, it flags the need for human review.
- Major changes to long-term personality, value judgments, privacy boundaries, or public expression must be confirmed by lailai.

See [profile/boundaries.md](profile/boundaries.md) for the full boundaries.

## Use Cases

- Writing / polishing Chinese content, removing AI tone.
- Writing or reviewing READMEs, project intros, and GitHub docs.
- Writing Markdown / MDX notes, problem solutions, and math articles under the target repo's local rules.
- Writing or reviewing OI competitive-programming C++17 code.
- Routing Luogu workflows to `luogu-solution` and new repositories to `lailai-template`.
- "Unity · Simplicity · Modernity" UI / design review.
- Simulating lailai's everyday chat and questioning style.
- Decision support, learning companion, long-term self-modeling and updates.

See [SKILL.md](SKILL.md) for out-of-scope cases and triggers.

## Project Structure

```bash
lailai-skill/
├── evolution/                  # Evaluation rubric and evolution log
├── examples/                   # Representative input and output pairs
├── profile/                    # Long-term identity, preferences, and boundaries
├── prompts/                    # Maintenance prompts
├── references/                 # Executable style and workflow rules
├── tests/                      # Verifiable behavior tests
├── tools/                      # Checkers and supporting utilities
├── observations.md             # Pending observations
├── SKILL.md                    # Skill entry point
└── test-prompts.json           # Prompt-level regression cases
```

## Getting Started

This repo is a standard Agent Skill (`SKILL.md` + frontmatter `name: lailai-skill`), usable in any skills-compatible runtime — Claude Code, Codex, Cursor, OpenClaw, Gemini CLI, and more.

### Where it goes (a hard requirement)

A skill **must** live in a configured skills directory. Placing it at an arbitrary repository
root does not make every runtime discover it.

The canonical user installation is `~/.agents/skills/lailai-skill/`. Install it once and let
projects reference it textually by Skill name or canonical repository URL. Do not vendor,
submodule, or copy it into each project; that creates stale parallel sources. If a runtime does
not discover `~/.agents/skills` natively, add one constant-size directory adapter.

### User level (clone once)

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/lailai0916/lailai-skill ~/.agents/skills/lailai-skill
# Update: cd ~/.agents/skills/lailai-skill && git pull
```

### After installing

1. The entry is its `SKILL.md`; the agent reads it first, then the relevant `profile/` and `references/` by task type (all links are relative, so they survive moving the whole folder).
2. Triggering: describe a chat / writing / code / design / decision task to match the description automatically, or say explicitly "use lailai's style," "do it my way," or "make it more like me."
3. Target-repo Agent rules take priority within that project. Luogu work routes to
   [`luogu-solution`](https://github.com/lailai0916/luogu-solution); new GitHub repositories
   start from [`lailai-template`](https://github.com/lailai0916/lailai-template).

## Habit Recording

When you notice a new expression, preference, dislike, or habit, **record it first in [observations.md](observations.md)** — don't edit the rules directly.

> An observation is not a rule. Only long-term, stable, transferable, executable observations earn their way into `profile/` or `references/`.

Copy [prompts/add-observation.md](prompts/add-observation.md) to have the AI record it.

## Skill Evolution

1. Observe: new habits go into `observations.md` first.
2. Stability check: separate transient moods, one-off preferences, and long-term habits.
3. Sediment: verified observations are organized into `profile/` or `references/`.
4. Examples / tests: when a rule changes, update `examples/` and `tests/`.
5. Darwin-style optimization: evaluate → improve → test → keep or roll back ([prompts/evolve-skill.md](prompts/evolve-skill.md)).
6. Versioning & logs: notable changes go into `CHANGELOG.md` and `evolution/evolution-log.md`.
7. Human confirmation: changes to long-term personality, value judgments, privacy boundaries, or public expression are confirmed by lailai.

## Skill Maintenance

Maintenance is long-term work, not a one-off. See [references/maintenance-guide.md](references/maintenance-guide.md) for details, and score with [evolution/evaluation-rubric.md](evolution/evaluation-rubric.md). Principles:

- Observation ≠ rule; transient mood ≠ long-term personality; one-off preference ≠ stable habit.
- Rules must be executable and checkable. Every change can explain "why."
- If a new rule makes output less like lailai, roll it back; if an old rule conflicts with the current lailai, update or retire it.

## License

This project's code is licensed under [MIT License](https://github.com/lailai0916/tools/blob/main/LICENSE). Its original documentation and skill content are licensed under [CC BY 4.0](LICENSE-docs).
