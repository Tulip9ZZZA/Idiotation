# ARCHITECTURE.md — why the kill-chain is sequential

## The mistake it avoids

The obvious build uses the five blocks as a crowd: Firecrawl scraping while the
council generates while Roast Room critiques, all at once. That produces noise —
everything is debated before anything is known, so nothing can be definitively
wrong, and a plan that can't be wrong can't be right either.

The Idiotation build is **sequential pressure**: five repos, five gates, six skills.
Each repo does the one job it does best, in sequence, so each gate inherits the last
one's output. The survivor hands off to Matt Pocock's spec workflow.

## The mapping — which block owns which gate

| Block | What it is | The one job it owns | Gates |
|---|---|---|---|
| Firecrawl | Scraper | Acquire the gate's evidence — winners, corpses, rubric, sponsor docs — as clean LLM-ready data | 0 Recon |
| Maxxing V2 Gauntlet | Five research lenses + hostile Terrain Gate | Run the lenses on the terrain, then try to invalidate the plan | 0 Recon + 2 Kill |
| Superpowers | Brainstorming + planning discipline | Draw out what you actually want; force a spike before implementation; write the plan | 1 Forge + 2 Kill + 4 Lock |
| LLM Council (idea) | Multi-model blind peer review + chairman synthesis | Generate and cross-review theses; surface non-obvious insights | 1 Forge |
| Roast Room | Adversarial council mechanics | Simulate the hostile judge; find where the submission loses first | 3 Roast |

And `good-idea` is **not a gate** — it is the **lens applied at every gate**:
structure, fit, surface, loop. It keeps the pipeline judging against your definition
of a good idea instead of the models' taste.

## The three hard rules

1. **LLM Council is for independent comparison, not proof of market demand.** A model
   majority is not evidence. The council surfaces; the lens ranks.
2. **Roast Room is adversarial review, not a substitute for users.** It exposes
   assumptions; it does not validate demand.
3. **Firecrawl gives facts; the models give structured disagreement; neither replaces
   a spike.** An idea you cannot falsify in 30 minutes cannot be proven in an 8-hour build.

## Design rationale (what the blocks force)

- **Facts before interpretation.** Gate 0 is evidence-only. No idea exists yet, so
  nothing can be defended yet — the models are forbidden from inventing.
- **Generation inherits evidence.** Gate 1 theses are generated FROM the gate
  profile, so fit is built in rather than checked later.
- **Falsification is mechanical in spirit.** Gate 2 borrows Maxxing's Terrain Gate:
  severity-mapped gaps, capped revise loop, blockers stated explicitly. Volume never
  passes a thesis — only closed gaps do.
- **The surface gets its own gate.** Gate 3 exists because structure without surface
  is invisible, and invisible ideas don't work. The cold-viewer judge owns this.
- **Locking is a contract, not a vibe.** Gate 4 produces a falsifiable promise plus a
  rubric→artifact map. If a rubric line has no artifact, the idea is not ready.
- **Nothing survives by default.** KILL is a clean exit. A precise KILL is more
  valuable than a vague PROCEED.

## Why the handoff works

Matt Pocock's spec workflow expects source-of-truth docs. The kill-chain produces
exactly them: `IDEA_LOCK.md` (the promise + acceptance criteria + non-goals),
`GATE_PROFILE.md` (the rubric), `TERRAIN_MAP.md` + `KILL_REPORT.md` (the evidence),
`ROAST_REPORT.md` (the known objections). `/grill-with-docs` grills the lock against
the evidence; `/to-spec` converts it; `/to-tickets` slices it into vertical tickets
whose "done" is visible in the demo; `/tdd` builds it test-first; `/code-review`
verifies it. Ideation ends where engineering begins — at a contract.
