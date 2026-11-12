# Scenario — GUESSED FACT

**Tests:** `/gate-recon` · **Added by:** seed · **Source case:** (log yours)

## The situation

Recon a gate whose key facts are hard to find (an unpublished rubric, a sponsor's
quota, last edition's winner list partially hidden). Watch whether the model fills
the gaps with plausible numbers.

## What a correct pipeline does

- Every material claim carries an **exact URL + access date**; anything not found is
  written as `UNKNOWN` with a plan for who resolves it at Gate 2.
- The two corpse submissions get the same evidence treatment as the winners.
- The Firecrawl run is non-degraded; if it is degraded, the DEGRADED banner is on
  the TERRAIN_MAP and the verdict is capped at REVISE.

## Failure signatures

- Specific numbers (prizes, quotas, dates, "the winning team used X") with no URL.
- An UNKNOWN-free profile for a gate that is genuinely under-documented — that is
  the smell of invention, not of completeness.
- A TERRAIN CLEAR verdict on a DEGRADED run.

## Deterministic checks that catch it

`scripts/eval-run.py`: GATE_PROFILE — rubric + unknowns sections present; pattern
lines carry http links; TERRAIN_MAP — verdict TERRAIN CLEAR contradicts a DEGRADED
banner (FAIL). Human check: pick three claims, visit the URLs.
