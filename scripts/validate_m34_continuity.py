#!/usr/bin/env python3
"""M34 public continuity index integrity check; no native execution claims."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "milestones/M33-EVIDENCE-CONTINUITY.json"

def validate(root=ROOT):
    data = json.loads((root / "milestones/M33-EVIDENCE-CONTINUITY.json").read_text(encoding="utf-8"))
    errors = []
    entries = data.get("progression", [])
    ids = [item.get("id") for item in entries]
    if ids != [f"M{i}" for i in range(27, 34)]:
        errors.append("Milestone progression must be contiguous M27-M33")
    for item in entries:
        path = item.get("path")
        if path and not (root / "milestones" / path).is_file():
            errors.append(f"Missing milestone carrier: {path}")
    for carrier in data.get("carriers", []):
        path = carrier.get("path")
        if not path or not (root / "milestones" / path).is_file():
            errors.append(f"Missing evidence navigation target: {path}")
    if data.get("history", {}).get("formalization") != "recorded_completed":
        errors.append("Completed formalization continuity changed")
    if data.get("history", {}).get("external_pilots") != "historical_external_pilots_recorded":
        errors.append("Historical pilot continuity changed")
    policy = data.get("evidence_policy", {})
    for key in ("preserve_original_classification", "do_not_infer_independent_reproduction", "do_not_invent_hold", "distinguish_historical_record_from_public_attachment"):
        if policy.get(key) is not True:
            errors.append(f"Continuity safeguard absent: {key}")
    if data.get("foundation", {}).get("invariant") != "The face may vary. The floor must not.":
        errors.append("Foundation invariant changed")
    return errors

if __name__ == "__main__":
    problems = validate()
    if problems:
        for problem in problems:
            print("FAIL:", problem)
        raise SystemExit(1)
    print("PASS: M34 public index structure, links and continuity safeguards")
