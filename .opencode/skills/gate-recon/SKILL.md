---
name: gate-recon
description: Acquire the gate's evidence (Firecrawl discipline), then run Maxxing V2's five research lenses and the hostile Terrain Gate on the terrain. Produces GATE_PROFILE.md and TERRAIN_MAP.md. Use at T-7 to T-5, BEFORE any ideation, whenever the user names a gate — a hackathon, Devpost event, grant, launch, investor meeting, client brief — or asks to map a competitive/problem terrain before generating ideas. Do not use for generating or judging ideas (that is idea-forge / good-idea).
---

# Gate Recon

You do not find good ideas. **You choose the mechanism, and the mechanism tells you
what counts as good.** This skill chooses the mechanism and maps the terrain before a
single idea is generated. It runs in two halves: **Evidence** (facts from the real
world) and **Terrain** (five lenses + a hostile gate over those facts).

## Blocks used

| Block | Role in this skill | License | Where it lives |
|---|---|---|---|
| Firecrawl | Scrape the gate's evidence into clean, LLM-ready data | AGPL-3.0 — used as an external service/API only; its code is never vendored into this repo | hosted: firecrawl.dev · MCP: `opencode mcp add firecrawl --global --url https://mcp.firecrawl.dev/<key>/v2.0/mcp` · optional clone under `blocks/firecrawl` |
| Maxxing V2 Gauntlet | The five lenses + the Terrain Gate protocol | MIT | `blocks/maxxing-itout` (branch `v2-gauntlet`) — `docs/TERRAIN_GATE.md`, `skills/terrain-scout` |

**Fallback rule:** if Firecrawl is not configured, use webfetch/websearch but keep the
same evidence discipline below (URL + date for every material claim). If the Maxxing
repo is not cloned, run the lens and gate protocol manually — this file contains the
full protocol — and note in TERRAIN_MAP.md that the mechanical checks did not run.

## When to use / when not

- **Use:** a gate exists or is coming (hackathon, Devpost, incubator demo day, grant
  deadline, product launch, investor pitch, client RFP) and nothing is mapped yet.
- **Do not use:** to generate or judge ideas — that is `/idea-forge` with `/good-idea`.
- **Do not use** to prove market demand. Recon maps the gate; it never validates a thesis.

## Steps

### 1. Frame the gate (10 min)

Write one paragraph before scraping anything:

- **What is the gate?** (event, sponsor track, launch venue, investor, buyer)
- **Who decides?** (sponsors' engineers? a panel of VCs? an algorithm? judges given a rubric?)
- **What do they see?** (a Devpost page? a 3-min demo? a 10-slide deck? the product itself?)
- **How fast do they decide?** (30 seconds on a shelf, 3 minutes on stage, a week of review)
- **State:** open / closed / coming — with dates.

If any of these is unknown after framing, it becomes a target for Step 2, not a guess.

### 2. Firecrawl the gate (15–45 min)

Acquire evidence. Scrape, in this order:

1. **The winners.** The gallery of the gate's last edition — top 5–10 winning projects.
   For each: the problem they picked, the demo moment, the sponsor API used, submission
   quality (README, video, devpost polish).
2. **The rejects.** At least one ordinary or abandoned submission. The corpses matter as
   much as the trophies — learn what the gate rejects, not only what it rewards.
3. **The rubric.** The official judging criteria page and its weights. If none is
   published, record that fact and plan for default weights.
4. **The sponsors.** If a sponsor API is mandatory: its docs, free-tier limits, quota,
   latency, and whether it needs a verified account.
5. **The competition.** Competitor and alternative pages if the domain is known: docs,
   pricing, comparison pages, changelogs.

Evidence discipline (this is the part that makes recon real instead of vibes):

- Record **exact URL + access date** for every material claim.
- **Never invent** pricing, customer counts, quotas, or competitor weaknesses.
- Mark everything not found as `UNKNOWN` — an honest UNKNOWN is an asset; a guessed
  fact is a landmine at Gate 2.
- Save raw scrapes under `sessions/<date>-<gate>/evidence/` and reference them.

### 3. Run the five lenses (30–60 min)

Feed the evidence to the lenses (run them in parallel as sub-agents if your harness
allows it — they are independent intelligence lenses). Each lens reads ALL the
evidence and writes findings with: claim, source URL, confidence (0–1), and a
**declared blind spot** (what this lens knows it did not check).

1. **Elite performance** — What do the strongest teams/products in this domain
   actually do? Their real workflow, not their marketing.
2. **Reverse engineering** — What did the winning projects prove, and why did the
   weak ones fail? Corpses over trophies: closed issues, abandoned repos, postmortems.
3. **Fundamentals** — What must exist for this workflow to work at all? (APIs, data,
   accounts, money, time.) List the dependency inventory.
4. **First principles** — Which assumptions here are causal truths and which are
   borrowed hype? Argue against the experts, the sponsors, and yourself.
5. **Pro vs amateur** — What observable standard separates a credible result from a
   superficial prototype? (Real data vs mock data; working end-to-end vs screenshot;
   error handling vs happy path.)

### 4. Run the hostile Terrain Gate (20–30 min)

The gate is not a peer of the lenses — **it owns them.** Anything the lenses produced
survives only if it clears the gate. Ask the nine questions (from Maxxing V2's
`TERRAIN_GATE.md`):

1. What did we overlook?
2. Which assumptions remain unverified?
3. What important information is missing?
4. Which dependencies, tools, resources, or constraints did we fail to investigate?
5. What contradicts our current understanding?
6. Did we reverse-engineer the right examples?
7. Did we neglect something fundamental?
8. Did we mistake an impressive demonstration for a proven implementation?
9. What could make this entire plan fail when it meets reality?

Then run the spirit of the deterministic checks even without the mechanical tool:

- Every lens produced a report with findings (no silent scouting).
- Every declared blind spot is either covered by an explicit UNKNOWN or researched.
- The dependency inventory is not empty.
- Evidence count meets the floor (rule of thumb: ≥ 3 independent facts per material claim).
- No material claim cites UNKNOWN evidence or evidence with confidence < 0.4.

### 5. Verdict and write-out

Verdicts: **TERRAIN CLEAR** (no material gap open) / **REVISE** (material gaps:
route each gap back to its owning lens with a targeted question, capped at 2 rounds)
/ **TERRAIN BLOCKED** (a blocker: ineligible, deadline impossible, dependency
unobtainable — say so explicitly, never fake it).

Write `GATE_PROFILE.md` and `TERRAIN_MAP.md` (templates in `docs/templates/`).

## Output: GATE_PROFILE.md

```text
GATE:
  name:
  who decides:
  what they see:
  how fast they decide:
  what makes them say yes:
  what makes them say no:
  state: open / closed / coming

PATTERNS WE CAN APPLY:      # from the winners, with URLs
  - ...
PATTERNS WE WILL NOT COPY:  # from the corpses, with URLs
  - ...
RUBRIC (published or default weights):
  - criterion: weight
UNKNOWNS:                   # every UNKNOWN becomes Gate 2's job
  - ...
```

## Output: TERRAIN_MAP.md

```text
LENS 1 — ELITE PERFORMANCE:   findings + blind spot
LENS 2 — REVERSE ENGINEERING: findings + blind spot
LENS 3 — FUNDAMENTALS:        findings + blind spot
LENS 4 — FIRST PRINCIPLES:    findings + blind spot
LENS 5 — PRO VS AMATEUR:      findings + blind spot

TERRAIN GATE:
  evidence gaps:
  contradictions:
  dependencies:
  failure modes:
  eligibility risks:

VERDICT: TERRAIN CLEAR / REVISE / TERRAIN BLOCKED
  if BLOCKED: what evidence would clear it
```

## Rules

- **Firecrawl (or your fetch tools) are the only source of facts. The models interpret;
  they do not invent.**
- Do not proceed to Gate 1 while a material rule or dependency remains UNKNOWN.
- Cite the exact URL and date for every material claim.
- Never mark research complete because the report looks long. **Volume never enters
  the verdict — only closed gaps do.**
- A blocker is a gift: an honest TERRAIN BLOCKED saves a weekend.
