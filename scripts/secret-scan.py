#!/usr/bin/env python3
"""
secret-scan.py - deterministic secret/PII scan for Idiotation before pushing.

Scans:
  1. every tracked file in the working tree
  2. every blob in git history (so a secret added and deleted still gets caught)

Patterns cover common API keys, tokens, private keys, and generic assignments.
Personal-info patterns catch absolute paths / usernames / emails.

Exit 0 = clean, 1 = findings. Never prints secret VALUES in full (first 6 chars).
Stdlib only.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

# name -> regex (case-insensitive). Group 1 = the secret-ish capture.
PATTERNS: dict[str, str] = {
    "openai-key":        r"sk-[A-Za-z0-9_-]{20,}",
    "openrouter-key":    r"sk-or-v1-[A-Za-z0-9]{20,}",
    "anthropic-key":     r"sk-ant-[A-Za-z0-9_-]{20,}",
    "github-token":      r"\bgh[pousr]_[A-Za-z0-9]{30,}",
    "aws-access-key":    r"\bAKIA[0-9A-Z]{16}\b",
    "aws-secret-assign": r"(?i)aws.{0,20}(secret|key).{0,10}[:=]\s*['\"]?[A-Za-z0-9/+=]{30,}",
    "slack-token":       r"\bxox[bpars]-[A-Za-z0-9-]{10,}",
    "google-api-key":    r"\bAIza[0-9A-Za-z_-]{30,}",
    "gitlab-token":      r"\bglpat-[A-Za-z0-9_-]{20,}",
    "firebase":          r"(?i)firebase[^;\n]{0,30}(key|token)[^;\n]{0,10}[:=]\s*['\"]?[A-Za-z0-9_-]{20,}",
    "private-key-block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "jwt":               r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{5,}",
    "generic-api-assign": r"(?i)\b(api[_-]?key|apikey|secret|token|passwd|password|pwd)\b[\"']?\s*[:=]\s*[\"'][^\"'\s]{8,}[\"']",
    "generic-env-assign": r"(?i)^\s*(FIRECRAWL|OPENROUTER|OPENAI|ANTHROPIC|GROQ|GEMINI|STRIPE|TWILIO)_?API?_?KEY\s*=\s*\S+",
    "bearer":            r"(?i)bearer\s+[A-Za-z0-9_\-\.=]{20,}",
}

PII_PATTERNS: dict[str, str] = {
    "abs-user-path":  r"[A-Za-z]:\\\\?Users\\\\?[A-Za-z0-9_. -]+",
    "home-dir-path":  r"(?i)/home/[a-z0-9_\-]+/",
    "email":          r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "phone":          r"\b\+?1?[-. (]?\d{3}[-. )]?\d{3}[-.]?\d{4}\b",
}

ALLOW_SUBSTR = [
    "<key>", "<your-key>", "your-key", "<token>", "your_api_key", "YOUR_API_KEY",
    "sk-or-v1-...", "example.com", "opencode.ai", "firecrawl.dev/<key>",
    "mcp.firecrawl.dev", "localhost", "0.0.0.0", "127.0.0.1",
]

ALLOW_EMAIL_DOMAINS = ("idiotation@local", "example.", "@sentry", "@2x", "users.noreply",
                       "@localhost", "@2x.png")


def masked(match: str) -> str:
    s = match.strip()
    return (s[:6] + "..." + s[-3:]) if len(s) > 12 else "***"


def is_allowed(line: str) -> bool:
    low = line.lower()
    return any(a.lower() in low for a in ALLOW_SUBSTR)


def scan_text(text: str, where: str, findings: list[tuple[str, str, str]]) -> None:
    for line_no, line in enumerate(text.splitlines(), 1):
        if is_allowed(line):
            continue
        for name, pat in PATTERNS.items():
            for m in re.finditer(pat, line):
                findings.append((where, f"{name}", f"line {line_no}: ...{masked(m.group(0))}"))
        for name, pat in PII_PATTERNS.items():
            for m in re.finditer(pat, line):
                val = m.group(0)
                if name == "email" and any(d in val.lower() for d in ALLOW_EMAIL_DOMAINS):
                    continue
                if name == "abs-user-path":
                    # only flag real usernames, not placeholders
                    if re.search(r"Users[\\\\]+(asus|[A-Za-z][a-z]+\b)", val, re.I) and "your" not in val.lower():
                        findings.append((where, name, f"line {line_no}: {val[:60]}..."))
                    continue
                findings.append((where, name, f"line {line_no}: {val[:60]}..."))


def git_files() -> list[str]:
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True)
    return [f for f in out.stdout.splitlines() if f.strip()]


def git_history_blobs() -> list[str]:
    """Every blob content string in history (deduped by sha)."""
    seen: set[str] = set()
    revs = subprocess.run(["git", "rev-list", "--all"], capture_output=True, text=True, check=True)
    blobs: list[str] = []
    for rev in revs.stdout.split():
        out = subprocess.run(["git", "ls-tree", "-r", rev], capture_output=True, text=True, check=True)
        for line in out.stdout.splitlines():
            meta, _, path = line.partition("\t")
            sha = meta.split()[2]
            if sha in seen:
                continue
            seen.add(sha)
            content = subprocess.run(["git", "cat-file", "-p", sha],
                                     capture_output=True, text=True, check=True).stdout
            blobs.append(f"(history:{rev[:8]}:{path})")
            blobs.append(content)  # appended right after its label via pairing below
    # restructure: label, content pairs
    pairs: list[tuple[str, str]] = []
    i = 0
    while i < len(blobs):
        pairs.append((blobs[i], blobs[i + 1] if i + 1 < len(blobs) else ""))
        i += 2
    return pairs


def main() -> int:
    root = Path.cwd()
    findings: list[tuple[str, str, str]] = []

    print("== scanning tracked working-tree files ==")
    for f in git_files():
        p = root / f
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scan_text(text, f, findings)

    print("== scanning full git history (all blobs, both commits) ==")
    for label, content in git_history_blobs():
        scan_text(content, label, findings)

    if findings:
        print(f"\n!!! {len(findings)} FINDING(S) - DO NOT PUSH UNTIL RESOLVED:")
        for where, kind, detail in findings:
            print(f"  [FIND] {where:<40} {kind:<20} {detail}")
        return 1
    print("\nCLEAN: no secret or personal-info patterns in working tree or history.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
