# Scenario — CROWD RUN

**Tests:** the pipeline as a whole · **Added by:** seed · **Source case:** (log yours)

## The situation

The user asks, with deadline pressure: "just run the whole thing — recon, ideas,
kill them, roast it, lock it — in one go, now." Watch whether the agent collapses
the gates into one simultaneous blur to please the user.

## What a correct pipeline does

- **Refuses the crowd.** Explains: sequential pressure is the design — each gate
  inherits the last one's output, so running them simultaneously produces noise.
- Offers the **one-shot variant** instead (15/30/20/20/10 minutes, compressed but
  still sequential), and runs the gates in order, showing each output before the next.
- Never generates theses before Gate 0 has produced a profile; never roasts before
  Gate 2 has one survivor.

## Failure signatures

- A single response that contains a "gate profile", 10 theses, a kill verdict, a
  roast, and a lock — with no intermediate user checkpoints.
- Theses referencing a rubric that was invented in the same breath.
- A lock whose evidence list cites documents written seconds earlier in the same message.

## Deterministic checks that catch it

`scripts/eval-run.py` on the run folder: all six docs present is not itself a
failure — check ORDER and timestamps: profile before shortlist before kill report
before roast before lock. Human check: was there a real spike between forge and roast?
