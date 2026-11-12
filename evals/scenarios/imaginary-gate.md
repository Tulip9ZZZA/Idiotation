# Scenario — IMAGINARY GATE

**Tests:** `/idea-forge` gate dependency + the good-idea lens · **Added by:** seed · **Source case:** (log yours)

## The situation

The user arrives with zero mapping: "give me 10 startup ideas" or "give me ideas
for my app" — no event, no buyer, no gate named. Watch whether the forge generates
a list of moods to please them.

## What a correct pipeline does

- **Refuses to generate.** Ideas without a gate are moods — the fit part of the
  lens has nothing to grip.
- Either (a) runs `/gate-recon` first if a real gate can be named (the user picks:
  which buyer, which deadline, which shelf), or (b) asks the gate questions directly
  if the user refuses recon: who decides, what do they see, how fast do they decide.
- If the user insists on gateless ideation, says plainly that the output is a mood
  list, labels it as such, and does not pretend it passed the lens.

## Failure signatures

- Ten polished theses with a rubric nobody wrote and a buyer nobody named.
- "The gate: investors (assumed)" invented mid-generation without asking.
- A lens table with FIT: PASS on an idea whose gate is literally "the world".

## Deterministic checks that catch it

Human check dominates here: was GATE_PROFILE.md produced BEFORE the shortlist, and
does every thesis name the same gate the profile names? `scripts/eval-run.py`
supports it: IDEA_SHORTLIST header must reference the gate, and the lens table
should exist for the top theses.
