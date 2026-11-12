---
name: idea-kill
description: Try to KILL the top three theses — articulate load-bearing assumptions, run Maxxing V2's hostile Terrain Gate against each, and run a real 30-minute spike against the riskiest assumption (Superpowers planning discipline: spike before implementation, never simulate the spike in the model's head). Produces KILL_REPORT.md with exactly one survivor. Use at T-4 after /idea-forge, or when the user wants an idea stress-tested/falsified before building. An idea that cannot be falsified in 30 minutes cannot be proven in an 8-hour build.
---

# Idea Kill

**An idea you cannot falsify in a 30-minute spike is an idea you cannot prove in an
8-hour hackathon.** This skill exists to be wrong cheaply and loudly. KILL is a clean
exit, not a failure — a precise KILL is more valuable than a vague PROCEED.

## Blocks used

| Block | Role in this skill | License | Where it lives |
|---|---|---|---|
| Maxxing V2 Terrain Gate | The falsification engine — what unknown, contradiction, dependency, or failure mode could invalidate this? | MIT | `blocks/maxxing-itout` (v2-gauntlet) — `docs/TERRAIN_GATE.md`, `eval/scenarios/` |
| Superpowers planning | Forces a spike before implementation; prevents the agent jumping to product code | MIT | `blocks/superpowers` — `skills/writing-plans/SKILL.md` |

**Fallback:** without the Maxxing clone, run the gate questions from Step 2 manually
(the full protocol is embedded here) and say in the report that the mechanical checks
did not run.

## When to use / when not

- **Use:** after `/idea-forge` produced a top 3. Takes the top 3 as input, one survivor out.
- **Use** when the user asks "is this idea actually buildable / will it actually work".
- **Do not use** to judge pitch quality — that is `/idea-roast`. Kill tests the
  structure; roast tests the surface.

## Steps

### 1. For each of the top 3 theses: articulate the load-bearing assumptions (15 min)

List 3–5 assumptions per thesis. For each assumption, name:

- The **strongest counterargument** (steel-man the case against your own idea).
- The **evidence that would prove it false** (what would you see in the world?).
- A **30-minute test** that could falsify it (a real API call, a real query, a real
  model output, a real search of the competition).

If you cannot name the assumptions, you do not understand the idea well enough to
build it — say so and drop it to REFINE.

### 2. Run the Terrain Gate on each thesis (15 min)

Ask the gate questions directly (from Maxxing V2 `TERRAIN_GATE.md`):

- What unknown could invalidate this?
- What contradiction exists between the thesis and the terrain (`TERRAIN_MAP.md`)?
- What dependency is unavailable, rate-limited, or fragile?
- What failure mode would kill the demo in the room?
- Did we mistake an impressive demonstration for a proven implementation?

Map every gap to severity: **blocker / material / minor.** A blocker = the thesis
cannot proceed at all (ineligible, impossible deadline, unobtainable dependency).

### 3. Run the 30-minute spike on the riskiest assumption (30 min per surviving thesis)

Use the Superpowers planning discipline: **the agent plans the spike in one paragraph
(command to run, expected output, what result kills the assumption), the user approves,
THEN the spike runs.** Hard rules:

- Run the spike against the **real system**: real API call, real database query, real
  model output, real hardware. Capture the command, URL, screenshot, or output.
- **Do not simulate the spike in the model's head.** A spike that happened only in
  the model's imagination is recorded as NOT RUN.
- If the spike cannot run (no key, no network, no hardware), record why, mark the
  thesis REFINE, and name the residual risk. **Never convert "not tested" into "passed."**

### 4. Verdict per thesis

- **KILL** — a load-bearing assumption is false, or a blocker gap stands. Clean exit.
- **REFINE** — one assumption shaky: name the smallest change that de-risks it, and
  the one spike that would settle it.
- **PROCEED** — spikes passed, no material gap open. Build with conviction.

If all three die: say it plainly, and either re-run `/idea-forge` with the next 3 from
the shortlist or return to `/gate-recon` — the terrain may have changed.

### 5. Write KILL_REPORT.md — one survivor only

Template in `docs/templates/KILL_REPORT.template.md`.

## Output: KILL_REPORT.md

```text
THESIS 1:
  one-line promise:
  assumptions:
    1. counterargument: / falsifying evidence: / 30-min test:
    2. ...
  terrain gate:
    unknowns:
    contradictions:
    dependencies:
    failure modes:
  spike result: PASS / FAIL / NOT RUN
  verdict: KILL / REFINE / PROCEED

THESIS 2: ...
THESIS 3: ...

SURVIVOR: thesis N
  why it survived:
  spike evidence (commands / URLs / screenshots):
  residual risks:

TO GATE 3:
  survivor one-line promise:
```

## Rules

- Do not hedge. A precise KILL is more valuable than a vague PROCEED.
- Run real spikes. Not-tested is a verdict; record it as one.
- Never convert "not tested" into "passed."
- If everything survives, suspect the spikes were too easy — the riskiest assumption
  was not actually tested. Re-run the hardest one.
- One survivor. If two survive on equal evidence, the user — not the model — picks.
