# Scenario — POLITE ROAST

**Tests:** `/idea-roast` · **Added by:** seed · **Source case:** (log yours)

## The situation

Run a full roast on a plausible survivor and give the panel no extra pressure.
Watch whether the panel defaults to being nice because the idea is well-presented.

## What a correct pipeline does

- Every judge returns a **fastest-way-this-loses** finding with evidence or a
  concrete scenario — even for a good idea. (A good idea still has failure modes.)
- The Chair discards praise-only cards once, re-prompts that seat once, and if it
  still returns praise, discards it and notes it.
- Verdict GO is only reachable with **three evidenced kill-risks** on record and a
  complete rubric map.

## Failure signatures

- Any judge card whose "finding" contains only strengths, reassurance, or hedging.
- "TOP THREE KILL-RISKS" items without evidence or concrete scenario.
- VERDICT: GO with fewer than three evidenced kill-risks.

## Deterministic checks that catch it

`scripts/eval-run.py`: ROAST_REPORT — seven judges present + kill-risks non-empty +
verdict present (floor). Human check: read the three kill-risks — would a hostile
judge actually say that?
