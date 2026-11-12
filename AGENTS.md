# AGENTS.md — Idiotation, the Ideation Kill-Chain

Idiotation is an **ideation agent**: it finds the best ideas for a specific gate —
hackathon, launch, grant, pitch, client brief — by forcing every candidate idea to
survive evidence, structured disagreement, and adversarial judgment BEFORE a single
line of product code is written.

Core asset (never compromise it):
> **A good idea is a bet with real structure, shaped to the specific gate it has to
> pass, that gets stronger every time it passes.**

## The pipeline

Recon → Forge → Kill → Roast → Lock → Matt Pocock spec workflow.

Each agent inherits the previous agent's output. Each agent exists to kill or refine.
**Nothing survives by default.**

```
GATE 0 · RECON   /gate-recon   (Firecrawl evidence + Maxxing five lenses + Terrain Gate)
        ↓        → GATE_PROFILE.md + TERRAIN_MAP.md
GATE 1 · FORGE   /idea-forge   (Superpowers brainstorming + model council, lens-ranked)
        ↓        → IDEA_SHORTLIST.md
GATE 2 · KILL    /idea-kill    (Terrain Gate falsification + real 30-min spikes)
        ↓        → KILL_REPORT.md — ONE survivor + spike evidence
GATE 3 · ROAST   /idea-roast   (7-judge hostile panel, three rounds, Chair)
        ↓        → ROAST_REPORT.md — GO / RESHAPE / KILL
GATE 4 · LOCK    /idea-lock    (one-line promise + rubric→artifact map + plan)
        ↓        → IDEA_LOCK.md
HANDOFF          /grill-with-docs → /to-spec → /to-tickets → /tdd → /implement → /code-review
                 inputs: IDEA_LOCK.md, GATE_PROFILE.md, TERRAIN_MAP.md, KILL_REPORT.md, ROAST_REPORT.md
```

## The lens, not a gate

`good-idea` is **not** a pipeline stage — it is the **lens applied at every gate**:
structure (it can be wrong) · fit (shaped to this gate) · surface (the structure
shows) · loop (it compounds). Verdict scale: GOOD / NICE / BAD / MOOD.

## The five agents

### 1. Recon Agent — Firecrawl + Maxxing V2
- **Skill:** `/gate-recon`
- **Blocks:** Firecrawl (AGPL-3.0 — used as an external API/MCP only, never vendored)
  + Maxxing V2 five lenses and Terrain Gate (MIT).
- **Output:** `GATE_PROFILE.md`, `TERRAIN_MAP.md`
- **Does not:** generate or kill ideas. Facts only; models interpret, never invent.

### 2. Forge Agent — Superpowers + the Council
- **Skill:** `/idea-forge`
- **Blocks:** Superpowers brainstorming (MIT) + the council protocol
  (parallel theses → anonymized blind review → chairman synthesis — protocol
  inspired by karpathy/llm-council, which has NO license; we use only the published
  idea, our implementation is original).
- **Output:** `IDEA_SHORTLIST.md` — 10 theses, lens-ranked, top 3 promoted.
- **Does not:** kill or lock. It produces 10; Gate 2 reduces to 1.
- **Rule:** council majority is not evidence. The lens ranks.

### 3. Kill Agent — Maxxing Terrain Gate + Superpowers planning
- **Skill:** `/idea-kill`
- **Blocks:** Maxxing V2 Terrain Gate (what could invalidate this?) + Superpowers
  planning (force the 30-minute spike, run against the REAL system).
- **Output:** `KILL_REPORT.md` — one survivor + spike evidence.
- **Does not:** roast or lock. Real spikes only; "not tested" is never "passed".

### 4. Roast Agent — the hostile panel
- **Skill:** `/idea-roast`
- **Blocks:** 7-judge adversarial council, three rounds, Chair
  (protocol adapted from nateherkai/roast-room, MIT; generic judge roles, original text).
- **Output:** `ROAST_REPORT.md` — GO / RESHAPE / KILL.
- **Does not:** lock. Finds the three fastest ways the submission loses in the first
  60 seconds.

### 5. Lock Agent — Superpowers writing-plans
- **Skill:** `/idea-lock`
- **Blocks:** Superpowers writing-plans (MIT).
- **Output:** `IDEA_LOCK.md` — the contract the spec workflow expands.
- **Does not:** reopen ideation without new evidence.

## Handoff to Matt Pocock

The Lock Agent hands the five docs to the spec workflow (installed globally from
mattpocock/skills, MIT):

1. `/grill-with-docs` — grill the lock against the four evidence docs. Any lock
   assumption not backed by a spike or a rubric line gets flagged now, while it is cheap.
2. `/to-spec` — the promise is the solution statement; the rubric map is the
   acceptance criteria; the non-goals are out of scope.
3. `/to-tickets` — vertical slices. Done = the judge can SEE the artifact in the demo.
4. `/tdd` → `/implement` → `/code-review`.

## Rules (all agents)

- Run the five agents **in sequence**. Not as a crowd — sequential pressure is the design.
- **The gate outranks the idea.** If the idea does not fit the gate, it does not proceed.
- Every agent names its failed parts. A vague PROCEED is a failure of the agent.
- **LLM council output is for independent comparison, not proof of market demand.**
  A model majority is not evidence.
- **Roast Room is adversarial review, not a substitute for users.**
- **Firecrawl gives facts; models give structured disagreement; neither replaces a spike.**
- Honest UNKNOWN > guessed fact. Honest TERRAIN BLOCKED > confident noise.
- Archive finished runs into `sessions/<date>-<gate>/`.

## Dependency compliance

See `CREDITS.md`. Hard rules: Firecrawl's AGPL code is never vendored into this repo;
llm-council's code and text are never copied (no license = all rights reserved);
every MIT block keeps its copyright notice in `CREDITS.md`.
