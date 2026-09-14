#!/usr/bin/env python3

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    errors = []

    required = {
        "SKILL.md": (
            "github.com/lailai0916/luogu-solution",
            "github.com/lailai0916/lailai-template",
            "github.com/lailai0916/laiism-skill",
            "目标项目内部规则优先",
            "prompts/review-style.md",
        ),
        "README.md": ("~/.agents/skills/luogu-solution",),
        "README.zh-Hans.md": ("~/.agents/skills/luogu-solution",),
        "prompts/review-style.md": ("不复制、改写或封装本文件正文",),
        "profile/personality.md": ("ai-and-skills", "rules-and-risk", "interests-and-ethics"),
    }
    for rel, needles in required.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing required architecture marker: {needle}")

    forbidden = {
        "references/cpp-oi-style.md": ("docs/contest/personal/common-templates.mdx",),
        "prompts/review-style.md": (".agents/skills/lailai-reviewer",),
    }
    for rel, needles in forbidden.items():
        text = (ROOT / rel).read_text(encoding="utf-8")
        for needle in needles:
            if needle in text:
                errors.append(f"{rel}: forbidden downstream implementation path: {needle}")

    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1

    print("Architecture routes and ownership boundaries are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
