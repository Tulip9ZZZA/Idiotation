# Deep security layers — run locally, never committed

Two optional layers beyond `scripts/secret-scan.py` and semgrep. Both need an LLM
API key to run; keep keys in a local `.env` (gitignored) and NEVER in chat, docs,
or this repo.

## 1. promptfoo — prompt-injection / jailbreak redteam of the skills

What it tests: that the six SKILL.md prompts resist manipulation — e.g. the roast
staying hostile under a "be nice" injection, the kill gate refusing to accept a
head-spike as PASS.

Setup (from the promptfoo repo zip, or `npm i -g promptfoo`):

```bash
cd evals/prompt-security
# put your key in a local .env (gitignored):  OPENAI_API_KEY=sk-...  or ANTHROPIC_API_KEY=...
npx promptfoo eval -c promptfooconfig.yaml
npx promptfoo view
```

Config lives here: `promptfooconfig.yaml`. Extend `tests:` with real failure cases
logged in `evals/cases/`.

## 2. strix — agentic pentest of the repo + any web app you build

```bash
pip install strix-agent
# keys in .env: STRIX uses your LLM key(s) (e.g. OPENAI_API_KEY / ANTHROPIC_API_KEY)
strix .            # scans this repo's files, scripts, and any local services
strix http://localhost:3000   # when you have a running app to attack
```

Report artifacts land in local output folders (gitignored via `sessions/` if you
point them there).

## Rules

- Run both **before** pushing anything sensitive, and after any change that adds
  scripts that execute, fetch, or store credentials.
- These tools' outputs can contain findings with sensitive context — archive under
  `sessions/` (gitignored), not in committed docs.
- Licenses: promptfoo MIT, strix Apache-2.0, semgrep LGPL-2.1 — all used as
  external tools; nothing from them is vendored into this repo (see CREDITS.md).
