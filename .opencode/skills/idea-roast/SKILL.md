---
name: idea-roast
description: Simulate a hostile judging panel against the single surviving idea — a 7-judge adversarial board (investor, customer, technical critic, competitor, operator, contrarian, board member) arguing over three rounds (open positions, debate, verdict), Chaired so it finds the three fastest ways the submission LOSES points in the first 60 seconds of a demo. Protocol adapted from nateherkai/roast-room's council mechanics (MIT). Produces ROAST_REPORT.md with GO / RESHAPE / KILL. Use at T-3 after /idea-kill, or whenever the user wants an idea attacked before a real judge, investor, or audience sees it. Not feedback — a roast.
---

# Idea Roast

**This is not feedback. This is a hostile panel finding reasons the idea loses.**
The real judge will not be polite; neither is this room. The output that matters is
not praise — it is the three fastest ways this loses points in the first 60 seconds.

## Blocks used

| Block | Role in this skill | License | Where it lives |
|---|---|---|---|
| Roast Room (`nateherkai/roast-room`) | Council mechanics: seats argue in rounds, a Chair keeps score and writes the verdict | MIT — protocol adapted here with original text and generic judge roles; the original repo additionally offers expert-persona "brains" (Bezos, Graham, Hormozi, …) worth cloning for the full experience | `blocks/roast-room` — `.claude/skills/roast-room/SKILL.md` |

**Fallback:** runs natively in any harness via sub-agents (one per judge, run in
parallel in the same message). If the Roast Room clone exists and you are in Claude
Code, prefer `/roast-room` with its real expert brains, then map its verdict into
ROAST_REPORT.md.

## When to use / when not

- **Use:** after `/idea-kill` returns one survivor with spike evidence.
- **Use** when the user says "roast this", "break this", "what would a judge hate".
- **Do not use** to replace users. Adversarial review exposes assumptions; it does
  not validate demand. If a claim needs a user to prove it, it goes back to a spike.

## The judges

Seven seats, one voice each, run as parallel sub-agents:

| Seat | The question they own |
|---|---|
| **Investor** | Would I fund/bet on this? Where is the leverage, where is the trap? |
| **Customer** (the cold viewer) | Would I understand and want this in 10 seconds without context? |
| **Technical Critic** | Where does this break — API limits, edge cases, error states, the demo-gods? |
| **Competitor** | How would I copy, undercut, or already-do-this better? |
| **Operator** | Can this ship on time? What's the hidden cost in hours/money/people? |
| **Contrarian** | What does everyone believe here that is false? Why is the obvious read wrong? |
| **Board Member** | Against the rubric, where do the points actually go to zero? |

The **Customer seat is the most important**: if a cold viewer is confused, the demo is
broken — that is a finding about the artifact, not the idea.

## Steps

### 1. Build the brief (10 min)

Input: the survivor from `KILL_REPORT.md`, `GATE_PROFILE.md` (rubric + weights), and
the one-line promise. Brief under 300 words, every assumption marked `(assumed)`.
**Do not ask "Is this a good idea?"** Ask instead, verbatim to the panel:

> "You are a judging panel at [GATE]. Your rubric weights are [from GATE_PROFILE].
> Find the **three fastest ways this submission loses points in the first 60 seconds
> of a demo**. Be brutal. Do not hedge. Every finding needs evidence or a concrete
> scenario. Praise is noise; tell me where the points go to zero."

### 2. Round 1 — opening positions (10 min)

Spawn all seven judges in ONE message, in parallel. Each judge returns a card:

- **Fastest way this loses** (one sentence).
- **Evidence or scenario** (rubric line, API limit, user confusion moment, competitor move).
- **Stance:** KILL / RESHAPE / PASS.
- **Severity:** 1–3 on rubric impact.

The Chair (you) never argues a seat, never adds a finding of your own — if you see a
hole no judge raised, hand it to the closest seat as a debate question instead.

### 3. Round 2 — debate (10 min)

Each judge sees the other six cards (anonymized if run as models that could play
favorites). Each must: defend their card if attacked, concede if beaten, and name the
**crux** — the underlying disagreement (a factual question, a numbers question, or a
values trade like speed vs safety) that explains why seats split. Weigh arguments, not
headcount: one seat with a decisive fact beats three seats with vibes.

### 4. Rubric map (5 min)

Every rubric criterion must map to an **artifact visible in the demo or submission**.
If a criterion has no artifact, the idea is not ready — that is a finding, not a note.

### 5. Round 3 — verdict (5 min)

Chair scores: per-seat stance, argument-weighted. Overrides: a **blocker-severity
technical or eligibility finding = KILL regardless of score**; unanimity in Round 1 is
a warning, not a win (make the strongest unargued alternative a crux). Verdicts:

- **GO** — survives the roast. Advance to Gate 4.
- **RESHAPE** — one cheapest change de-risks it. Name the change. Then re-roast or
  proceed with the change locked.
- **KILL** — fatal flaw found. Return to Gate 2 with a new thesis (or Gate 1 if the
  shortlist is exhausted).

### 6. Write ROAST_REPORT.md

Template in `docs/templates/ROAST_REPORT.template.md`.

## Output: ROAST_REPORT.md

```text
SURVIVOR:
  one-line promise:

PERSONA FINDINGS (round 1, verbatim-in-substance):
  Investor:
  Customer:
  Technical Critic:
  Competitor:
  Operator:
  Contrarian:
  Board Member:

CRUXES (from round 2):
  - crux: / seats on each side: / how it resolved:

TOP THREE KILL-RISKS:
  1. ...
  2. ...
  3. ...

RUBRIC MAP:
  [criterion] → [visible artifact] (or: NO ARTIFACT)

VERDICT: GO / RESHAPE / KILL
  if RESHAPE: cheapest change:

TO GATE 4:
  what to lock:
```

## Rules

- Do not be polite. The judge will not be.
- A finding without evidence or a concrete scenario is a mood, not a finding — return
  it to the seat once; if it comes back empty, discard it and note that.
- The Customer seat outranks the others on "is the demo readable in 10 seconds".
- Quote seats faithfully; never put words in a seat's mouth.
- Treat unanimity as a warning, not a win.
- Roast Room is adversarial review, not a substitute for users. It exposes
  assumptions; it does not validate demand.
