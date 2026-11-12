#!/usr/bin/env python3
"""
eval-run.py - deterministic audit of an Idiotation run.

Same philosophy as the Terrain Gate itself: volume never enters the verdict;
only closed checks do. Reads the six run documents and mechanically checks the
invariants this repo demands. A run can pass every check and still be shallow -
the human case notes in evals/cases/ are the higher court.

Usage:
    python scripts/eval-run.py <run-folder-or-repo-root>

Exit codes: 0 = all hard checks passed, 1 = at least one FAIL, 2 = nothing to audit.
Stdlib only. Works on Windows/macOS/Linux.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = [
    "GATE_PROFILE.md",
    "TERRAIN_MAP.md",
    "IDEA_SHORTLIST.md",
    "KILL_REPORT.md",
    "ROAST_REPORT.md",
    "IDEA_LOCK.md",
]

JUDGES = ["Investor", "Customer", "Technical Critic", "Competitor",
          "Operator", "Contrarian", "Board Member"]

HEDGES = [
    r"\bprobably fine\b", r"\bshould be fine\b", r"\bseems solid\b",
    r"\bprobably works\b", r"\bI think it'?s fine\b",
]


def find_doc(root: Path, name: str) -> Path | None:
    """Find name at root, one level down (sessions runs), or via walk (depth<=3)."""
    direct = root / name
    if direct.is_file():
        return direct
    for child in sorted(root.iterdir()) if root.is_dir() else []:
        if child.is_dir():
            cand = child / name
            if cand.is_file():
                return cand
    hits = [p for p in root.rglob(name) if len(p.relative_to(root).parts) <= 3]
    return hits[0] if hits else None


class Audit:
    def __init__(self) -> None:
        self.lines: list[tuple[str, str, str]] = []  # status, check, detail

    def add(self, status: str, check: str, detail: str = "") -> None:
        self.lines.append((status, check, detail))

    def hard(self, ok: bool, check: str, ok_detail: str = "", bad_detail: str = "") -> bool:
        self.add("PASS" if ok else "FAIL", check, ok_detail if ok else bad_detail)
        return ok

    def soft(self, ok: bool, check: str, ok_detail: str = "", bad_detail: str = "") -> None:
        self.add("PASS" if ok else "WARN", check, ok_detail if ok else bad_detail)


def section(text: str, start_pat: str, end_pat: str) -> str:
    m = re.search(start_pat, text, re.I)
    if not m:
        return ""
    rest = text[m.end():]
    e = re.search(end_pat, rest, re.I)
    return rest[: e.start()] if e else rest


def audit_gate_profile(a: Audit, p: Path | None) -> None:
    if p is None:
        a.add("SKIP", "GATE_PROFILE.md", "not found (no recon run)")
        return
    t = p.read_text(encoding="utf-8", errors="replace")
    a.hard(re.search(r"who decides:[ \t]*\S", t, re.I) is not None,
           "gate decider named",
           bad_detail="'who decides:' is empty - the gate is not mapped")
    a.hard("UNKNOWNS" in t.upper(), "honest UNKNOWNS section present",
           bad_detail="no UNKNOWNS section - smells like invention, not completeness")
    a.soft("RUBRIC" in t.upper(), "rubric recorded (published or default)")
    pat = section(t, r"PATTERNS", r"RUBRIC|UNKNOWNS")
    urls = len(re.findall(r"https?://", pat))
    a.soft(urls >= 2, f"patterns carry URLs ({urls} found)",
           bad_detail="winner/corpse patterns without URLs - the corpses need receipts too")


def audit_terrain_map(a: Audit, p: Path | None) -> None:
    if p is None:
        a.add("SKIP", "TERRAIN_MAP.md", "not found")
        return
    t = p.read_text(encoding="utf-8", errors="replace")
    missing = [f"LENS {i}" for i in range(1, 6) if f"LENS {i}" not in t]
    a.hard(not missing, "all five lens reports present",
           bad_detail=f"missing: {', '.join(missing)} - silent scouting")
    a.hard("TERRAIN GATE" in t.upper(), "terrain gate section present")
    m = re.search(r"VERDICT:\s*(.*)", t)
    verdict = m.group(1).strip() if m else ""
    a.hard(bool(verdict), "terrain verdict stated",
           bad_detail="no VERDICT line - recon without a verdict is a mood")
    degraded = "DEGRADED RUN" in t or "DEGRADED" in t.upper()
    if "TERRAIN CLEAR" in verdict.upper():
        a.hard(not degraded, "TERRAIN CLEAR on a non-degraded run",
               bad_detail="TERRAIN CLEAR contradicts the DEGRADED banner - degraded runs cap at REVISE")
    else:
        a.soft(bool(re.search(r"REVISE|TERRAIN BLOCKED", verdict, re.I)),
               f"verdict in vocabulary (TERRAIN CLEAR/REVISE/TERRAIN BLOCKED): got '{verdict[:40]}'")


def audit_shortlist(a: Audit, p: Path | None) -> None:
    if p is None:
        a.add("SKIP", "IDEA_SHORTLIST.md", "not found (no forge run)")
        return
    t = p.read_text(encoding="utf-8", errors="replace")
    verdicts = len(re.findall(r"verdict:\s*(GOOD|NICE|BAD|MOOD)", t, re.I))
    a.hard(verdicts >= 1, f"lens verdicts present ({verdicts})",
           bad_detail="theses were never judged through the lens")
    a.soft(verdicts >= 5, f"wide generation ({verdicts} theses judged)",
           bad_detail="generate wide, judge narrow - fewer than 5 judged theses")
    a.hard("PRESERVED DISSENT" in t.upper(), "council dissent preserved",
           bad_detail="no PRESERVED DISSENT section - consensus cop-out; dissent is Gate 2's raw material")
    a.hard(re.search(r"TOP\s*3", t, re.I) is not None, "top 3 promoted to Gate 2")
    a.soft("mechanism" in t.lower(), "theses carry mechanisms",
           bad_detail="theses without mechanisms are moods")


def audit_kill_report(a: Audit, p: Path | None) -> None:
    if p is None:
        a.add("SKIP", "KILL_REPORT.md", "not found (no kill run)")
        return
    t = p.read_text(encoding="utf-8", errors="replace")
    survivors = len(re.findall(r"SURVIVOR:", t))
    a.hard(survivors == 1, f"exactly one survivor (found {survivors})",
           bad_detail="the kill gate produces ONE survivor")
    verdicts = re.findall(r"verdict:\s*(\S+)", t, re.I)
    bad = [v for v in verdicts if v.upper().rstrip(":") not in {"KILL", "REFINE", "PROCEED"}]
    a.hard(not bad, f"verdicts in vocabulary KILL/REFINE/PROCEED ({len(verdicts)} theses)",
           bad_detail=f"off-vocabulary verdicts: {bad}")
    if survivors == 1:
        s_idx = t.upper().find("SURVIVOR:")
        block = t[s_idx:]
        block = block[: block.upper().find("TO GATE 3")] if "TO GATE 3" in block.upper() else block
        evidence = re.findall(r"(https?://|command:|screenshot|\.png|\.jpg|output:)", block, re.I)
        a.hard(len(evidence) >= 1, "survivor has captured spike evidence",
               bad_detail="survivor declared with zero captured commands/URLs/screenshots - a head spike")
    not_run = len(re.findall(r"NOT RUN", t, re.I))
    a.soft(True, f"'NOT RUN' honesty markers present: {not_run}",
           ok_detail="untested spikes are recorded, never converted to passed" if not_run
           else "no untested spikes claimed - ok if all spikes ran")


def audit_roast_report(a: Audit, p: Path | None) -> None:
    if p is None:
        a.add("SKIP", "ROAST_REPORT.md", "not found (no roast run)")
        return
    t = p.read_text(encoding="utf-8", errors="replace")
    missing = [j for j in JUDGES if j.lower() not in t.lower()]
    a.hard(not missing, "all seven judges sat",
           bad_detail=f"missing judges: {', '.join(missing)}")
    risks = section(t, r"TOP THREE KILL-RISKS", r"RUBRIC MAP|VERDICT")
    numbered = len(re.findall(r"^\s*\d+\.", risks, re.M))
    a.hard(numbered >= 3, f"three evidenced kill-risks ({numbered} numbered)",
           bad_detail="GO is unreachable without three evidenced kill-risks on record")
    a.hard("RUBRIC MAP" in t.upper(), "rubric map present",
           bad_detail="criteria without visible artifacts = idea not ready")
    m = re.search(r"VERDICT:\s*(GO|RESHAPE|KILL)", t, re.I)
    a.hard(m is not None, "roast verdict stated (GO/RESHAPE/KILL)",
           bad_detail="no roast verdict - a polite non-verdict is a failed roast")
    if m and m.group(1).upper() == "RESHAPE":
        a.hard(re.search(r"cheapest change:\s*\S", t, re.I) is not None,
               "RESHAPE names the cheapest change",
               bad_detail="RESHAPE without a named change is a deferred kill")


def audit_idea_lock(a: Audit, p: Path | None) -> None:
    if p is None:
        a.add("SKIP", "IDEA_LOCK.md", "not found (no lock run)")
        return
    t = p.read_text(encoding="utf-8", errors="replace")
    for header, name in [
        ("ONE-LINE PROMISE", "one-line promise"),
        ("RUBRIC MAP", "rubric->artifact map"),
        ("LOAD-BEARING ASSUMPTIONS", "load-bearing assumptions"),
        ("NON-GOALS", "non-goals"),
        ("EVIDENCE", "evidence list"),
    ]:
        a.hard(header in t.upper(), f"{name} present", bad_detail=f"IDEA_LOCK missing '{header}'")
    if "EVIDENCE" in t.upper():
        linked = sum(1 for d in DOCS if d in t)
        a.soft(linked >= 5, f"evidence list references the five docs ({linked}/5)",
               bad_detail="the lock must cite the full chain: profile, terrain, shortlist, kill, roast")


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"[error] not a folder: {root}")
        return 2

    found = {name: find_doc(root, name) for name in DOCS}
    if not any(found.values()):
        print("NOTHING TO AUDIT (exit 2)")
        print(f"No run documents ({', '.join(DOCS)}) found under: {root}")
        print("Run the gates first, then audit. Logs belong in evals/cases/.")
        return 2

    a = Audit()
    audit_gate_profile(a, found["GATE_PROFILE.md"])
    audit_terrain_map(a, found["TERRAIN_MAP.md"])
    audit_shortlist(a, found["IDEA_SHORTLIST.md"])
    audit_kill_report(a, found["KILL_REPORT.md"])
    audit_roast_report(a, found["ROAST_REPORT.md"])
    audit_idea_lock(a, found["IDEA_LOCK.md"])

    # hedge scan across all present docs
    all_text = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                         for p in found.values() if p is not None)
    hits = [h for h in HEDGES if re.search(h, all_text, re.I)]
    a.soft(not hits, "no hedged verdict language",
           bad_detail=f"hedging found: {hits}")

    w = max(len(c) for _, c, _ in a.lines)
    for status, check, detail in a.lines:
        print(f"{status:<5} {check:<{w}}  {detail}")
    fails = sum(1 for s, _, _ in a.lines if s == "FAIL")
    warns = sum(1 for s, _, _ in a.lines if s == "WARN")
    passes = sum(1 for s, _, _ in a.lines if s == "PASS")
    skips = sum(1 for s, _, _ in a.lines if s == "SKIP")
    print("-" * 78)
    print(f"RESULT: {'FAIL' if fails else 'PASS'}   "
          f"checks: {passes} pass / {fails} fail / {warns} warn / {skips} skipped")
    if fails:
        print("A FAIL is a floor violation - log the run in evals/cases/ with the failures.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
