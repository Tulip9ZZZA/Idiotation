#!/usr/bin/env python3
"""
eval-selftest.py - meta-test: keeps the run auditor itself honest.

eval-run.py is the deterministic auditor for every Idiotation run. An auditor
that silently stops catching sabotage is worse than no auditor. This script
proves, on every push, that the auditor still:

  1. passes an honest, complete run fixture (exit 0), and
  2. fails a sabotaged fixture that seeds real violations (exit 1).

Stdlib only. Exit 0 = auditor verified, 1 = auditor regression.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUDITOR = REPO / "scripts" / "eval-run.py"
GOOD = REPO / "evals" / "fixtures" / "good"
BAD = REPO / "evals" / "fixtures" / "bad"


def run_audit(folder: Path) -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(AUDITOR), str(folder)],
                       capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def main() -> int:
    ok = True

    if not GOOD.is_dir() or not BAD.is_dir():
        print("FAIL — fixtures missing: evals/fixtures/{good,bad} must exist in the repo.")
        return 1

    good_rc, good_out = run_audit(GOOD)
    if good_rc != 0:
        print("FAIL — the HONEST fixture no longer passes. The auditor drifted:\n")
        print(good_out)
        ok = False
    else:
        passes = good_out.count("PASS")
        print(f"PASS — honest fixture accepted ({passes} checks, exit 0)")

    bad_rc, bad_out = run_audit(BAD)
    if bad_rc != 1:
        print("FAIL — the SABOTAGED fixture no longer fails. The auditor went blind:\n")
        print(bad_out)
        ok = False
    else:
        fails = bad_out.count("FAIL")
        print(f"PASS — sabotage caught ({fails} violations, exit 1)")

    if not ok:
        print("\nFix eval-run.py or the fixtures in the same commit. An auditor that")
        print("cannot catch seeded sabotage must not guard anything.")
        return 1

    print("\nSELFTEST OK — the auditor still passes honesty and still catches sabotage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
