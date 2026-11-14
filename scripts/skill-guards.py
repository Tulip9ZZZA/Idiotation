#!/usr/bin/env python3
"""
skill-guards.py - prompt-guard regression check for the Idiotation skills.

The six SKILL.md files are prompts. Their safety behavior lives in specific
guard phrases ("Firecrawl is REQUIRED", "NOT RUN", "Council majority is not
evidence"...). A well-meaning edit can silently delete a guard and change how
the agent behaves in the field. This script fails CI if any guard phrase goes
missing, so prompt drift is caught before a run does the damage.

Stdlib only. Exit 0 = all guards present, 1 = at least one missing.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# file (relative to repo root) -> guard phrases that MUST stay in the prompt
GUARDS: dict[str, list[str]] = {
    "AGENTS.md": [
        "The gate outranks the idea",
        "Nothing survives by default",
        "Log every run",
    ],
    ".opencode/skills/gate-recon/SKILL.md": [
        "Firecrawl is REQUIRED",
        "DEGRADED",
        "REVISE",
        "never invent",
    ],
    ".opencode/skills/good-idea/SKILL.md": [
        "structure, fit, surface, loop",
        "verdict PASS/FAIL",
        "GOOD / NICE / BAD / MOOD",
    ],
    ".opencode/skills/idea-forge/SKILL.md": [
        "Council majority is not evidence",
        "PRESERVED DISSENT",
    ],
    ".opencode/skills/idea-kill/SKILL.md": [
        "NOT RUN",
        "PASS / FAIL / NOT RUN",
    ],
    ".opencode/skills/idea-roast/SKILL.md": [
        "seven judges",
        "GO / RESHAPE / KILL",
        "cheapest change",
    ],
    ".opencode/skills/idea-lock/SKILL.md": [
        "one-line promise",
        "NON-GOALS",
        "PASS/FAIL/NOT RUN",
    ],
}


def main() -> int:
    missing: list[tuple[str, str]] = []
    absent_files: list[str] = []

    for rel, phrases in GUARDS.items():
        p = REPO / rel
        if not p.is_file():
            absent_files.append(rel)
            continue
        text = p.read_text(encoding="utf-8", errors="replace").lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                missing.append((rel, phrase))

    if absent_files:
        print(f"FAIL — guard target(s) missing from the repo: {', '.join(absent_files)}")
        return 1

    if missing:
        print(f"!!! {len(missing)} GUARD PHRASE(S) MISSING — a safety guard was edited out:\n")
        for rel, phrase in missing:
            print(f"  [MISSING] {rel:<45} '{phrase}'")
        print("\nRestore the phrase or, if the behavior genuinely changed, update")
        print("GUARDS in scripts/skill-guards.py in the same commit — never silently.")
        return 1

    total = sum(len(v) for v in GUARDS.values())
    print(f"OK — all {total} prompt guards present across {len(GUARDS)} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
