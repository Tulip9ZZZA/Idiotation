# Security Policy — Idiotation

This repo is a public ideation-agent pack: skills, docs, and small Python
scripts. It ships **no runtime service** and holds **no secrets by design** —
but "no secrets by design" is enforced by tooling, not by hope.

## Reporting a vulnerability

**Do NOT open a public issue for a security problem.**

Use GitHub's **private vulnerability reporting** (the **Security** tab →
*Report a vulnerability*), or contact the maintainer through GitHub
(@Tulip9ZZZA) directly. Private reporting keeps the window closed until a fix
exists.

- **Acknowledged:** within 72 hours
- **Fix or mitigation target:** within 7 days for anything that could leak
  credentials or execute attacker-controlled input
- **Credit:** we will credit you in the release notes unless you prefer silence

## In scope

| Area | What we care about |
|---|---|
| `scripts/*.py` | command injection, path traversal, secret exposure, unsafe deserialization |
| Skills (`.opencode/skills`, `.claude/skills`) | prompt-injection flows that could make an agent exfiltrate data or fake evidence |
| CI (`.github/workflows`) | workflow injection, unauthorized modification, action tampering |
| Install scripts | downloading code that is not what it claims to be |

## Out of scope

- The quality or business merit of any idea the pipeline produces
- The upstream tools we call as external services (Firecrawl, semgrep,
  promptfoo, strix) — report those to their own maintainers
- Reports from automated scanners with no proof of exploitability (send the
  PoC, not just the banner)

## If a secret leaks anyway

1. **Rotate the credential first** — rotation beats git surgery every time.
2. Tell us — we will scan history (`python scripts/secret-scan.py` covers the
   full history), confirm exposure, and rewrite history only if rotation is
   impossible.
3. We never paste secret values into issues, chat, or fixes — reports should
   reference the finding's location, not its content.

## Enforcement layers (what already runs)

| Layer | Where | Trigger |
|---|---|---|
| `scripts/secret-scan.py` (tree + full git history) | local + CI | every commit (optional local hook) / every push + PR |
| semgrep `p/secrets` + `p/security-audit` | CI | every push + PR |
| `scripts/skill-guards.py` (prompt guard regression) | CI | every push + PR |
| `scripts/eval-selftest.py` (auditor can't silently rot) | CI | every push + PR |
| GitHub secret scanning + push protection | GitHub | every push, server-side |

Nothing survives by default — not even commits.
