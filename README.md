<div align="center">
  <h1>lailai.skill</h1>
  <p>English | <a href="README.zh-Hans.md">简体中文</a></p>
  <p>
    <img src="https://img.shields.io/github/last-commit/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/languages/top/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/repo-size/lailai0916/lailai-skill?style=flat-square" />
    <img src="https://img.shields.io/github/license/lailai0916/lailai-skill?style=flat-square" />
  </p>
</div>

> A continuously evolving personal cyber-twin system for lailai — replicating lailai's expression, thinking, aesthetics, working habits, and everyday communication style as faithfully as possible.

A personal skill for AI agents (Claude Code / Codex / Cursor / OpenClaw, etc.). Not a one-line "act as lailai," but a structured, maintainable, verifiable, and continuously evolving personal model.

## What It Solves

Make AI as much like lailai as possible in writing, docs, code, design, chat, judgment, and project maintenance — and more so over time: consistent style, high information density, no AI tone, and actionable output.

## What It Is Not

- Not a persona-roleplay prompt, nor "act as lailai."
- Not a static persona fixed after a single generation.
- Not a tool to impersonate lailai and deceive others.
- Not a work-only template — it also covers everyday chat, learning, and long-term self-modeling.

## Boundaries

- Does not impersonate lailai in public statements, promises, identity claims, or authorization.
- Does not store accounts, passwords, keys, IDs, precise addresses, or other sensitive data.
- Does not expose private chats, others' privacy, or unvetted sensitive material.
- If output might be mistaken for lailai's real words, it flags the need for human review.
- Major changes to long-term personality, value judgments, privacy boundaries, or public expression must be confirmed by lailai.

See [profile/boundaries.md](profile/boundaries.md) for the full boundaries.

## Use Cases

- Writing / polishing Chinese content, removing AI tone.
- Writing or reviewing READMEs, project intros, and GitHub docs.
- Writing Docusaurus / MDX notes, problem solutions, and math articles.
- Writing or reviewing OI competitive-programming C++17 code.
- "Unity · Simplicity · Modernity" UI / design review.
- Simulating lailai's everyday chat and questioning style.
- Decision support, learning companion, long-term self-modeling and updates.

See [SKILL.md](SKILL.md) for out-of-scope cases and triggers.

## Repository Structure

```text
lailai-skill/
├── README.md                       # English (this file)
├── README.zh-Hans.md               # 简体中文
├── SKILL.md                        # Entry: positioning, scope, principles, boundaries, workflow, self-check
├── LICENSE                         # MIT
├── CHANGELOG.md                    # Notable changes
├── profile/                        # Long-term personality, preferences, thinking, boundaries
│   ├── identity.md
│   ├── personality.md
│   ├── thinking-style.md
│   ├── conversation-style.md
│   ├── preferences.md
│   ├── decision-rules.md
│   └── boundaries.md
├── references/                     # Executable style rules (each with a Self-review Checklist)
│   ├── daily-chat-style.md
│   ├── writing-style.md
│   ├── wording.md
│   ├── markdown-style.md
│   ├── latex-math-style.md
│   ├── docusaurus-style.md
│   ├── cpp-oi-style.md
│   ├── engineering-code-style.md
│   ├── design-style.md
│   ├── project-docs-style.md
│   ├── learning-style.md
│   ├── ai-tone-blacklist.md
│   └── maintenance-guide.md
├── examples/                       # Representative input → handling → output → why it fits
├── tests/                          # Verifiable style tests (goal / input / expectations / scoring / pass criteria)
├── prompts/                        # Copy-paste prompts for maintenance
├── evolution/                      # Scoring rubric and evolution log
│   ├── evaluation-rubric.md
│   └── evolution-log.md
└── observations.md                 # Temporary observations not yet sedimented into rules
```

## Installation & Usage

This repo is a standard Agent Skill (`SKILL.md` + frontmatter `name: lailai-skill`), usable in any skills-compatible runtime — Claude Code, Codex, Cursor, OpenClaw, Gemini CLI, and more.

### Where it goes (a hard requirement)

A skill **must** live in the runtime's skills directory. Placing it at the repo root does nothing (Claude Code won't discover it).

| Method                                        | Path                                     | When                                                                   |
| :-------------------------------------------- | :--------------------------------------- | :--------------------------------------------------------------------- |
| **User level** (recommended for personal use) | `~/.claude/skills/lailai-skill/`         | Install once, available in **all** projects; single source, zero drift |
| **Project level** (vendored, version-pinned)  | `<project>/.claude/skills/lailai-skill/` | When CI / cloud agents / other machines need `clone-and-it's-there`    |

> Rule of thumb: personal cross-project use → user level, done once; a repo that runs agents in CI / the cloud → project-level submodule. **Don't install both levels under the same name** — the user level shadows the project level.

### User level (clone once)

```bash
git clone https://github.com/lailai0916/lailai-skill ~/.claude/skills/lailai-skill
# Update: cd ~/.claude/skills/lailai-skill && git pull
```

### Project level (git submodule)

```bash
cd <project>
git submodule add https://github.com/lailai0916/lailai-skill .claude/skills/lailai-skill
git commit -m "chore(claude): add lailai-skill submodule"   # commit the gitlink too — see below
```

⚠️ **Two things to get right:**

1. **Clone with submodules**, or `.claude/skills/lailai-skill/` is an empty shell:
   - Fresh clone: `git clone --recurse-submodules <project>`
   - Existing clone: `git submodule update --init --recursive`
   - CI (GitHub Actions): set `actions/checkout` with `submodules: recursive` (GitLab: `GIT_SUBMODULE_STRATEGY: recursive`).
2. **Don't drop the gitlink when committing.** `git submodule add` stages both `.gitmodules` and the gitlink — commit them together. Afterward, `git submodule status` should show one line `<sha> .claude/skills/lailai-skill`; committing only `.gitmodules` without the gitlink leaves a fresh clone with no content.
3. **Bump the pinned version**: `git submodule update --remote .claude/skills/lailai-skill && git add .claude/skills/lailai-skill && git commit -m "chore: bump lailai-skill"`.

### After installing

1. The entry is its `SKILL.md`; the agent reads it first, then the relevant `profile/` and `references/` by task type (all links are relative, so they survive moving the whole folder).
2. Triggering: describe a chat / writing / code / design / decision task to match the description automatically, or say explicitly "use lailai's style," "do it my way," or "make it more like me."

## Recording New Habits

When you notice a new expression, preference, dislike, or habit, **record it first in [observations.md](observations.md)** — don't edit the rules directly.

> An observation is not a rule. Only long-term, stable, transferable, executable observations earn their way into `profile/` or `references/`.

Copy [prompts/add-observation.md](prompts/add-observation.md) to have the AI record it.

## How It Evolves

1. Observe: new habits go into `observations.md` first.
2. Stability check: separate transient moods, one-off preferences, and long-term habits.
3. Sediment: verified observations are organized into `profile/` or `references/`.
4. Examples / tests: when a rule changes, update `examples/` and `tests/`.
5. Darwin-style optimization: evaluate → improve → test → keep or roll back ([prompts/evolve-skill.md](prompts/evolve-skill.md)).
6. Versioning & logs: notable changes go into `CHANGELOG.md` and `evolution/evolution-log.md`.
7. Human confirmation: changes to long-term personality, value judgments, privacy boundaries, or public expression are confirmed by lailai.

## Maintenance & Updates

Maintenance is long-term work, not a one-off. See [references/maintenance-guide.md](references/maintenance-guide.md) for details, and score with [evolution/evaluation-rubric.md](evolution/evaluation-rubric.md). Principles:

- Observation ≠ rule; transient mood ≠ long-term personality; one-off preference ≠ stable habit.
- Rules must be executable and checkable. Every change can explain "why."
- If a new rule makes output less like lailai, roll it back; if an old rule conflicts with the current lailai, update or retire it.

## License

Licensed under the [MIT License](LICENSE). This skill describes publicly shareable style and methods, and contains no private information.
