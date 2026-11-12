# USAGE.md — operating the kill-chain

## Before you start

- Skills are discovered from `.opencode/skills` (OpenCode) and `.claude/skills`
  (Claude Code). Run `scripts/sync-skills.ps1` after editing any skill.
- Optional blocks: run `scripts/install-blocks.ps1`. Every skill has a native
  fallback and works without them.
- **REQUIRED for `/gate-recon`:** Firecrawl — hosted key (`FIRECRAWL_API_KEY`), MCP
  server, or self-hosted instance. Without it the run is marked **DEGRADED** and the
  verdict is capped at **REVISE**; it can never claim TERRAIN CLEAR. Set it up (5
  min) before recon, or explicitly accept the degraded run.
- Output documents land in the repo root of the folder you run in; archive finished
  runs into `sessions/<date>-<gate>/`.
- **After every run** — good, fail, or example — log it into `evals/cases/` (see
  `evals/README.md`). The pipeline only improves from logged cases.

## The full sequence (a weekend-before-the-event)

| When | Command | Produces | You are done when |
|---|---|---|---|
| T-7..T-5 | `/gate-recon <gate>` | `GATE_PROFILE.md`, `TERRAIN_MAP.md` | verdict is TERRAIN CLEAR and no material UNKNOWN remains |
| T-5 | `/idea-forge` | `IDEA_SHORTLIST.md` | 10 theses lens-ranked, top 3 promoted, dissent preserved |
| T-4 | `/idea-kill` | `KILL_REPORT.md` | ONE survivor with at least one REAL spike run |
| T-3 | `/idea-roast` | `ROAST_REPORT.md` | verdict GO (or RESHAPE with the change locked) |
| T-3 | `/idea-lock` | `IDEA_LOCK.md` | every rubric line maps to an artifact |
| T-3 | `/grill-with-docs` → `/to-spec` → `/to-tickets` | spec + tickets | every assumption in the lock is backed by evidence |
| T-2..T-1 | `/tdd` → `/implement` → `/code-review` | the thing | the judge can see every artifact in the demo |

## The one-shot variant (same-day event)

Compress the gates, keep the sequence:

```text
15 min  /gate-recon    quick scan + one lens
30 min  /idea-forge    brainstorm → 5 theses → council → top 1
20 min  /idea-kill     ONE real 30-min spike → Terrain Gate
20 min  /idea-roast    4 judges (Investor, Customer, Technical Critic, Contrarian)
10 min  /idea-lock     one-line promise + rubric map
```

Same kill-chain, compressed. The rule holds: **the idea must survive evidence,
structured disagreement, and adversarial judgment before a single line of product
code is written.**

## Operator checklists

### Gate 0 — before ideation
- [ ] Gate named, decider named, rubric weights recorded (published or "default")
- [ ] At least 2 corpses (rejected/abandoned submissions) studied, not just winners
- [ ] Every material claim has URL + access date; the rest is honest UNKNOWN
- [ ] Verdict: TERRAIN CLEAR (or a documented blocker)

### Gate 2 — before roast
- [ ] 3–5 load-bearing assumptions per thesis, each with a 30-min test
- [ ] The spike ran against the REAL system (command/URL/screenshot captured)
- [ ] No "not tested" was silently converted into "passed"
- [ ] Exactly one survivor

### Gate 4 — before handoff
- [ ] One-line promise is falsifiable, gate-shaped, glance-readable
- [ ] Every rubric line → a named artifact the judge will SEE
- [ ] Loop written down (or its absence explicitly accepted for one-shot gates)
- [ ] Five evidence docs archived into `sessions/<date>-<gate>/`

## Anti-patterns (the pipeline refuses these)

- **The crowd.** Running recon, forge, and roast simultaneously. Noise, not signal.
- **The hedged PROCEED.** "Seems fine, probably works" is a failed Kill gate.
- **The head-spike.** "I simulated the API call in my head." That is NOT RUN.
- **The consensus cop-out.** Ironing out council dissent instead of preserving it.
- **The polite roast.** A roast that returns only praise is a failed Roast gate.
- **The reopen.** "I have another idea" mid-build → note it for the next run; the
  lock holds unless NEW EVIDENCE invalidates the original choice.
- **The generic thesis.** "We help people do X better" — say what everyone is
  supposed to say, get judged as saying nothing.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Skills not advertised | `/reload`, or check `.opencode/skills/<id>/SKILL.md` exists with a `description:` |
| Council has one voice | You have one model; the skill says so explicitly in the output — it must not pretend |
| Gate 0 verdict BLOCKED with a real blocker | That is a win. A weekend saved. Fix the blocker or pick another gate |
| All three theses die | Return to `/idea-forge` with the next 3, or re-recon: the terrain changed |
| Roast returns RESHAPE forever | The cheapest change is not cheap enough — treat as KILL and go back to Gate 2 |
