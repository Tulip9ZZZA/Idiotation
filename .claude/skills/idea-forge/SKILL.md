---
name: idea-forge
description: Generate wide and judge narrow — run Superpowers brainstorming to draw out what the user actually wants, then run a multi-model council (parallel theses, anonymized blind peer review, chairman synthesis; protocol inspired by karpathy/llm-council, re-implemented natively) to produce 10 candidate theses, then rank them with the good-idea lens. Produces IDEA_SHORTLIST.md. Use at T-5 after /gate-recon, or whenever the user wants many strong candidate ideas generated and ranked for a mapped gate. Does not kill, roast, or lock ideas.
---

# Idea Forge

Generate wide, judge narrow. Three moves inside one gate: **Superpowers draws out what
you actually want** (so the agent doesn't build what it merely believes you want),
**the council generates and blind-reviews 10 theses**, and **the good-idea lens ranks
them.** The council surfaces; the lens decides.

## Blocks used

| Block | Role in this skill | License | Where it lives |
|---|---|---|---|
| Superpowers (`obra/superpowers`) | Brainstorming discipline — context-aware questions before any generation | MIT | `blocks/superpowers` — `skills/brainstorming/SKILL.md` |
| LLM Council (concept, `karpathy/llm-council`) | 3-stage protocol: parallel first opinions → anonymized cross-review → chairman synthesis | **No license (all rights reserved) — we use only the published idea; the implementation below is original and runs natively in your harness. No code or text is copied.** | optional clone `blocks/llm-council` for the visual web app |
| good-idea (this pack) | The ranking lens | ours | `/good-idea` |

The council runs on whatever models your harness has. In OpenCode, spawn the stages as
sub-agents (any model available, at least 3 if possible). If only one model is
available, the council degrades to **one model playing three independent passes with
different review briefs** — say so in the output, never pretend it was multi-model.

## When to use / when not

- **Use:** after `/gate-recon` produced `GATE_PROFILE.md` + `TERRAIN_MAP.md`.
- **Use** when the user asks for "ideas for X" and a gate is already mapped.
- **Do not use** without a gate: ideas without a gate are moods. If no profile exists,
  send the user back to `/gate-recon` first — that is not bureaucracy, it is the fit part.
- **Does not:** kill (Gate 2), roast (Gate 3), or lock (Gate 4).

## Steps

### 1. Superpowers brainstorming (15–30 min)

Before generating ANYTHING, run the brainstorming discipline against `GATE_PROFILE.md`.
Load `blocks/superpowers/skills/brainstorming/SKILL.md` if present; otherwise follow
its core contract: **ask context-aware questions one message at a time, and do not
generate until the answers are concrete.** Never ask what the gate profile already
answers. The questions that matter for a gate:

- Who is the specific user, and have you seen this problem yourself?
- What is the current workaround, and what does it cost (time, money, risk)?
- What did the last edition's winners prove, and what did they leave on the table?
- What is the one demo moment a judge must see for this to win?
- What are you NOT willing to do (constraints, ethics, non-goals)?

Write the answers into the shortlist header. If the user says "just run it", record
their answers as stated assumptions and mark each `(assumed)`.

### 2. Council — Stage A: parallel first opinions (15–20 min)

Feed every councilor the same packet: the event theme, `GATE_PROFILE.md`,
`TERRAIN_MAP.md`, and the brainstorming answers. Prompt (verbatim):

> "Generate 10 candidate product theses for this gate. Each thesis MUST include:
> (a) the specific user, (b) the painful job, (c) the single demo moment a judge will
> see, and (d) the technical mechanism that makes that moment possible.
> Do not rank yet. Do not hedge. A thesis without a mechanism is a mood — do not submit moods."

Each councilor works alone. No model sees another's theses in this stage.

### 3. Council — Stage B: anonymized cross-review (15–20 min)

Swap theses so each councilor reviews another's set **with authorship anonymized**
(blind review exists so nobody plays favorites — including with itself). Each review:

> "Rank these theses in accuracy and insight. For the top 3: one line each on why the
> REASONING is strong. For the bottom 3: one line each on where the reasoning breaks.
> You are judging reasoning quality, not style. If two theses share a load-bearing
> assumption that looks false, flag it once with the flag shared by both."

### 4. Council — Stage C: chairman synthesis (10 min)

One model (the chairman) takes all theses + all blind reviews and produces:

- The **3 theses whose reasoning is strongest** — chosen by argument quality, not vote count.
- The **non-obvious insights** — claims that appeared in reviews that no thesis itself contained.
- The **preserved dissent** — disagreements between reviewers, written down verbatim
  in substance. Dissent is the raw material of Gate 2; do not iron it out.

### 5. Apply the good-idea lens (15 min)

Run `/good-idea` on each of the 10 theses against the gate. Rank by the lens: number
of failed parts first, then structure strength. **Council majority is not evidence** —
a model majority ranks nothing; it only surfaces what to look at.

### 6. Write IDEA_SHORTLIST.md

Template in `docs/templates/IDEA_SHORTLIST.template.md`.

## Output: IDEA_SHORTLIST.md

```text
BRAINSTORMING ANSWERS:      # from Step 1, marked (assumed) where applicable
  user:
  workaround & cost:
  winners proved / left on table:
  must-see demo moment:
  non-goals:

THESES (ranked by good-idea lens):
  1.
     user:
     job:
     demo moment:
     mechanism:
     insight:
     lens: structure / fit / surface / loop (pass-fail each)
     verdict: GOOD / NICE / BAD / MOOD
  2. ...
  10. ...

COUNCIL NON-OBVIOUS INSIGHTS:
  - ...
PRESERVED DISSENT:          # do NOT iron out; Gate 2 needs this
  - ...

TOP 3 FOR GATE 2:
  1. ...
  2. ...
  3. ...
```

## Rules

- Council majority is not evidence. The lens ranks; the council only surfaces.
- Do not force consensus. Preserve the dissent.
- Every thesis must have a demo moment and a mechanism. No mechanism → mood → discard.
- A thesis the user recognizes as "mine, but said better" outranks a novel thesis the
  user doesn't recognize. Ideation serves the builder, not the models.
- Never let generation start before Step 1's answers are concrete.
