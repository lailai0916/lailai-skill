# Repository instructions

This repository is the canonical source for the runtime-neutral `lailai-skill` Agent Skill.
Read `SKILL.md` before changing behavior, then read the affected files under `profile/`,
`references/`, `prompts/`, `tools/`, and `tests/`.

## Rules

- Keep `SKILL.md` and all active guidance runtime-neutral. Describe capabilities, not one
  vendor's tool names or private directories.
- `~/.agents/skills/lailai-skill` is the documented user-level installation path.
  Runtime-specific paths are compatibility adapters, never additional sources of truth.
- An observation is not yet a stable rule. New habits enter `observations.md`; promote them
  only through the maintenance workflow and required human checkpoints.
- When a rule changes, update the relevant examples/tests and record the change in
  `CHANGELOG.md` and `evolution/evolution-log.md` when appropriate.
- Preserve the privacy, impersonation, and human-confirmation boundaries in
  `profile/boundaries.md`.
- Keep cross-repository guidance single-source: this repository owns personal and reusable
  style; downstream repositories keep only a route plus their local deltas, never mirrored rules.
- Keep English and Simplified-Chinese README installation guidance aligned.

## Validation

```bash
python3 tools/checker/check.py tools/checker/tests/good.mdx
python3 tools/checker/check.py tools/checker/tests/bad.mdx # expected to fail with ERROR findings
python3 -m py_compile tools/checker/check.py
python3 tools/checker/check_architecture.py
```

`AGENTS.md` is the canonical repository instruction file. `CLAUDE.md` is only a compatibility
import; do not duplicate these rules in runtime-specific files.
