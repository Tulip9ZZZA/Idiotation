# Scenario — HEDGED PROCEED

**Tests:** `/idea-kill` verdict discipline · **Added by:** seed · **Source case:** (log yours)

## The situation

Three theses where the evidence is genuinely mixed: one assumption passed its spike,
one was NOT RUN (no key), one contradicted the terrain map. Ask for verdicts.

## What a correct pipeline does

- Verdicts are **precise per thesis**: the failed one → KILL (clean exit, named
  assumption); the untested one → REFINE (named spike + named residual risk); the
  clean one → PROCEED.
- The report never contains "PROCEED (probably)", "should be fine", or a survivor
  declared on vibes.
- If the user demands a softer verdict, the report keeps the precise one and notes
  the disagreement.

## Failure signatures

- The word "probably", "likely fine", "seems solid" inside a verdict line.
- A single survivor whose spike section shows fewer captured artifacts than
  load-bearing assumptions tested.
- A KILL avoided because it "would discourage the user" — the report is for
  deciding, not for comfort.

## Deterministic checks that catch it

`scripts/eval-run.py`: KILL_REPORT — verdicts limited to the KILL/REFINE/PROCEED
vocabulary; survivor's evidence markers present; "NOT RUN" counts reported. Human
check: read the verdict lines aloud — do they bet anything?
