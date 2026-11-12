---
name: idea-lock
description: Lock the surviving idea into IDEA_LOCK.md — the one-line promise (user, job, obstacle, cost, outcome, insight), the rubric→artifact map, load-bearing assumptions, loop, and non-goals — written with Superpowers writing-plans discipline, then hand off the five evidence docs to Matt Pocock's spec workflow (/grill-with-docs → /to-spec → /to-tickets → /tdd → /implement → /code-review). Use at T-3 after /idea-roast returns GO or RESHAPE, or when the user decides to commit to an idea. Once locked, ideation does NOT reopen without new evidence.
---

# Idea Lock

**Once you lock, you do not reopen ideation without new evidence that invalidates the
original choice. The kill-chain WAS the evidence.** Locking converts a survivor into a
contract: one promise, one rubric map, one plan skeleton — short enough that
`/to-spec` can expand it without inventing anything.

## Blocks used

| Block | Role in this skill | License | Where it lives |
|---|---|---|---|
| Superpowers writing-plans | Written plan before implementation; bite-sized testable tasks; no drift into code | MIT | `blocks/superpowers` — `skills/writing-plans/SKILL.md` |
| Matt Pocock skills (handoff target) | `/grill-with-docs`, `/to-spec`, `/to-tickets`, `/tdd`, `/implement`, `/code-review` | MIT | installed globally (or `blocks/matt-pocock-skills`) — `skills-main/skills/engineering/` |

## When to use / when not

- **Use:** after `/idea-roast` returns **GO** (or RESHAPE with the change locked in).
- **Use** when the user says "lock it", "let's commit to this", "write it up".
- **Do not use** while a rubric line has no artifact or a promise cannot be falsified.
  Fix those first — the lock is only as strong as its weakest artifact.

## Steps

### 1. Write the one-line promise (10 min)

Compress the idea to one sentence, gate-shaped. It must contain all six parts:

> **[User]** struggles to **[job]** because **[obstacle]**, which causes **[cost]**.
> We change that by **[outcome]**, and what makes it different is **[insight]**.

Test it against the lens: it must be **falsifiable** (structure), **gate-shaped**
(fit), **glance-readable** (surface). If it cannot be wrong, it is not locked — it is
a slogan. Rewrite until a skeptic could bet against it.

### 2. Map the rubric to artifacts (10 min)

Every criterion from `GATE_PROFILE.md` gets a named artifact BEFORE the build starts:

| Criterion | What the judge sees | The artifact that proves it |
|---|---|---|
| Problem / Relevance | the 10-second pain statement | the assumption list from KILL_REPORT |
| Execution / does it work | the 60-second live transformation | the spike evidence in KILL_REPORT |
| Innovation | the "I haven't seen that" moment | the non-obvious insight from IDEA_SHORTLIST |
| Design / Pitch | a coherent identity | the Customer finding in ROAST_REPORT |

**If a line has no artifact, the idea is not ready.** Go back one gate; do not pad.

### 3. Write IDEA_LOCK.md (15 min)

Follow the writing-plans discipline: document what a fresh engineer cannot know (the
decided names, values, artifacts, and the test that proves each), keep it short —
`/to-spec` will expand it. Include the plan skeleton as bite-sized, testable tasks
where each task's "done" is something a judge can SEE in the demo.

### 4. Hand off to Matt Pocock

Run the spec workflow with the five docs as source of truth:

```
IDEA_LOCK.md, GATE_PROFILE.md, TERRAIN_MAP.md, KILL_REPORT.md, ROAST_REPORT.md
```

1. `/grill-with-docs` — grill every assumption in IDEA_LOCK against the evidence in
   the other four. Any lock assumption not backed by a spike in KILL_REPORT or a
   rubric line in GATE_PROFILE gets flagged here, while it is still cheap.
2. `/to-spec` — the one-line promise becomes the solution statement; the rubric map
   becomes the acceptance criteria; the non-goals become out-of-scope.
3. `/to-tickets` — vertical slices; a ticket is done when the judge can see the
   artifact it produces in the demo.
4. `/tdd` → `/implement` → `/code-review`.

## Output: IDEA_LOCK.md

```text
ONE-LINE PROMISE:
  [user] struggles to [job] because [obstacle], which causes [cost].
  We change that by [outcome], and what makes it different is [insight].

GATE:
  name:
  state: open / closed / coming

RUBRIC MAP:
  criterion → visible artifact
  ...

LOAD-BEARING ASSUMPTIONS:    # from KILL_REPORT, each with its spike status
  [assumption] — spike: PASS/FAIL/NOT RUN
  ...

WHAT IS DIFFERENT:           # from GATE_PROFILE patterns we can apply
  ...

LOOP:
  what compounds: [or "no loop — accepted, one-time demo"]

NON-GOALS:
  ...

EVIDENCE:
  GATE_PROFILE.md
  TERRAIN_MAP.md
  IDEA_SHORTLIST.md
  KILL_REPORT.md
  ROAST_REPORT.md
```

## Rules

- The one-line promise must be falsifiable. If it cannot be wrong, it is not locked.
- Every rubric line gets an artifact. No artifact → not ready → back one gate.
- Do not reopen the decision without new evidence. "I have another idea" during the
  build is a note for the next run, not a reopen.
- Keep the lock short. Density of decisions, not volume of prose.
- Archive finished runs: move the five evidence docs into
  `sessions/<date>-<gate>/` so the next run starts clean.
