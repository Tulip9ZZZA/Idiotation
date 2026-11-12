# CASE — <short slug>

```text
DATE: <YYYY-MM-DD>
GATE(S) RUN: <recon / forge / kill / roast / lock / spec-handoff>
HARNESS: <OpenCode / Claude Code / other>
MODELS AVAILABLE: <list; if one model only, say so>
BLOCKS PRESENT: <firecrawl? maxxing? superpowers? roast-room? llm-council?>
FIRECRAWL: <configured / DEGRADED run>
RUN FOLDER: <sessions/YYYY-MM-DD-<slug>/ or repo root>

INPUT (the brief you gave, verbatim):
  <...>

WHAT HAPPENED (timeline, one line per step):
  1.
  2.

RUN VERDICT: <final survivor / GO / RESHAPE / KILL / TERRAIN BLOCKED / ...>

KIND: GOOD / FAIL / EXAMPLE       # mark per gate if mixed, e.g. "recon GOOD, roast FAIL"

FAILURES (the gold - be merciless):
  - <gate>: <rule violated> — what the agent did vs what it should have done.
    What you had to correct by hand:
    <...>

WHAT WORKED (do not skip - protect what survives):
  - <...>

TEACHING (the one-line lesson):
  <lesson>
  patch target: <which SKILL.md + which section>

STATUS: logged
```

## Scorecard (paste output of `python scripts/eval-run.py <run-folder>`)

```text
<paste here>
```
