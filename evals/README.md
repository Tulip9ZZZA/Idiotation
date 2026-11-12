# evals/ — the pipeline improves only from logged use

Idiotation is an agent, and agents get better the same way ideas do in this very
repo: **a claim has to survive contact with reality.** Every time you run the
kill-chain — a hackathon, a launch, a client pitch, or just one gate on some idea —
the run is either a **GOOD**, a **FAIL**, or an instructive **EXAMPLE**. All three
are gold. The fails are the most valuable thing this repo will ever own.

## What counts as a case

| Kind | Meaning | Example |
|---|---|---|
| **GOOD** | The pipeline behaved; the outputs were clean; the verdict was right for the right reasons | A thesis died in Gate 2 because a real spike failed — and dying early was correct |
| **FAIL** | An agent violated a rule of this repo | The roast came back polite; the spike was "run" in the model's head; a fact was guessed; the council consensus ironed out dissent |
| **EXAMPLE** | Neither broken nor clean — a novel situation worth teaching | A sponsor changed the rubric mid-week; the gate closed while you were building |

A single run can be GOOD at one gate and FAIL at another — log the whole run once,
mark per-gate kinds in the case file.

## How to log a run (2 minutes after the run)

1. Copy `templates/case.template.md` → `cases/YYYY-MM-DD-<slug>.md`.
2. Fill it **honestly** — especially the FAILURES section. A case without a named
   failure is a brochure, not an eval.
3. Point `evidence:` at the archived run docs in `sessions/<date>-<gate>/`.
4. Paste the scorecard from `python scripts/eval-run.py <run-folder>` at the bottom.
5. Set `STATUS: logged`.

## How a case becomes an eval

1. Extract the failure's **shape** (not its content) into
   `scenarios/<failure-slug>.md`: the situation brief, what a correct pipeline does,
   and the failure signatures to watch for. Six seed scenarios already exist —
   `polite-roast`, `head-spike`, `guessed-fact`, `crowd-run`, `hedged-proceed`,
   `imaginary-gate`.
2. **Re-test:** run the pipeline on the scenario brief (fresh session, or ask the
   agent to self-test against the scenario) and check the failure signatures.
3. If it still fails, patch the offending SKILL.md section named in the case's
   `TEACHING` field, sync (`scripts/sync-skills.ps1`), and re-test.
4. Update the case's `STATUS: logged → patched → re-tested(passed)`.

## The deterministic audit — `scripts/eval-run.py`

Same philosophy as the Terrain Gate itself: **volume never enters the verdict; only
closed checks do.** The script reads the six output documents and mechanically
checks the invariants this repo demands (real spike evidence, seven judges present,
dissent preserved, rubric map, falsifiable promise, no DEGRADED CLEAR contradictions).

```bash
python scripts/eval-run.py .                 # audit the current run at repo root
python scripts/eval-run.py sessions/2026-11-12-demo   # audit an archived run
```

Exit code 0 = all hard checks passed; 1 = at least one FAIL. It is a floor, not a
judge: a run can pass every check and still be a shallow run — the case file's
human notes are the higher court.

## Directory map

```text
evals/
├── README.md            # this file
├── templates/
│   └── case.template.md # the run report
├── scenarios/           # reusable test situations + failure signatures
├── cases/               # YOUR logged runs (one md per run)
└── (scorecards are pasted into each case)
```
