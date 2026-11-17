#!/usr/bin/env python3
"""Independent AAR-facing, public-safe synthetic examination; NOT AAR or V.A. runtime.

No protected AAR implementation, original RULE-COST-001 thresholds, NEW K,
network connection, or real-world effect is used. Python standard library only.
All numeric limits and operations in this file are examiner-invented fixtures.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path

RULE = "EXAMINER-ILLUSTRATIVE-001/1.0"  # not an AAR normative rule
ZERO = "0" * 64

def canon(value):
    return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")

def sha(value):
    return hashlib.sha256(canon(value)).hexdigest()

def valid(case):
    """Public, self-authored example. BLOCK has precedence over HOLD."""
    block, hold = [], []
    if case["authority"] not in ("VALID", "LIMITED", "MISSING", "REVOKED"):
        block.append("unknown_authority")
    if case["authority"] in ("MISSING", "REVOKED"):
        block.append("authority_absent_or_revoked")
    if not case["evidence_valid"]:
        block.append("evidence_invalid")
    if case["route"] != "declared":
        block.append("alternate_route_not_authorized")
    if any(not isinstance(case[k], int) or isinstance(case[k], bool) for k in ("units", "cost_cents", "capacity")):
        block.append("invalid_numeric_evidence")
    else:
        if any(case[k] < 0 for k in ("units", "cost_cents", "capacity")):
            block.append("negative_operating_condition")
        if case["capacity"] < case["units"]:
            hold.append("insufficient_capacity")
    if case["authority"] == "LIMITED" or case["scope"] != "continuation":
        hold.append("mandate_insufficient")
    if case["contradictory_capacity"]:
        hold.append("capacity_conflict")
    if case["cost_cents"] > 90:
        hold.append("illustrative_cost_ceiling")
    if case["exploratory"]:
        hold.append("illustrative_exploratory_pattern")
    if block:
        return "BLOCK", block + hold
    if hold:
        return "HOLD", hold
    return "ALLOW", []

BASE = {
    "authority": "VALID", "scope": "continuation", "units": 10,
    "capacity": 20, "cost_cents": 50, "exploratory": False,
    "evidence_valid": True, "contradictory_capacity": False,
    "route": "declared", "effect_key": "A", "evidence": "SYNTHETIC-A",
}

def samples():
    # 20 falsifiable propositions. The numbers are independently invented.
    specs = [
        ("01-authorized", {}, "ALLOW", 1),
        ("02-retry-no-double-effect", {}, "ALLOW", 0),
        ("03-revoked", {"authority": "REVOKED", "effect_key": "B"}, "BLOCK", 0),
        ("04-absent-authority", {"authority": "MISSING", "effect_key": "B"}, "BLOCK", 0),
        ("05-corrupt-evidence", {"evidence_valid": False, "effect_key": "B"}, "BLOCK", 0),
        ("06-empty-evidence", {"evidence_valid": False, "evidence": "", "effect_key": "B"}, "BLOCK", 0),
        ("07-alternate-route", {"route": "unregistered", "effect_key": "B"}, "BLOCK", 0),
        ("08-over-capacity", {"capacity": 3, "effect_key": "B"}, "HOLD", 0),
        ("09-over-cost", {"cost_cents": 91, "effect_key": "B"}, "HOLD", 0),
        ("10-exploratory", {"exploratory": True, "effect_key": "B"}, "HOLD", 0),
        ("11-limited-mandate", {"authority": "LIMITED", "effect_key": "B"}, "HOLD", 0),
        ("12-wrong-scope", {"scope": "review_only", "effect_key": "B"}, "HOLD", 0),
        ("13-changed-condition-authorized", {"effect_key": "B", "evidence": "REPAIRED-B"}, "ALLOW", 1),
        ("14-same-condition-replay", {"capacity": 3, "effect_key": "B"}, "HOLD", 0),
        ("15-revoked-after-allow", {"authority": "REVOKED", "effect_key": "B"}, "BLOCK", 0),
        ("16-independent-valid", {"effect_key": "C", "evidence": "SYNTHETIC-C"}, "ALLOW", 1),
        ("17-receipt-write-fault", {"effect_key": "D", "failure": "receipt"}, "ERROR_HOLD", 0),
        ("18-effect-commit-fault", {"effect_key": "E", "failure": "effect"}, "ERROR_HOLD", 0),
        ("19-conflicting-capacity", {"contradictory_capacity": True, "effect_key": "F"}, "HOLD", 0),
        ("20-unknown-authority", {"authority": "UNKNOWN", "effect_key": "G"}, "BLOCK", 0),
    ]
    for ident, updates, expected, delta in specs:
        case = dict(BASE)
        case.update(updates)
        case["id"] = ident
        yield case, expected, delta

def replay_check(receipts):
    previous = ZERO
    for number, receipt in enumerate(receipts, 1):
        data = {k:v for k,v in receipt.items() if k != "receipt_sha256"}
        if receipt["sequence"] != number or receipt["previous_sha256"] != previous:
            return False
        if receipt["receipt_sha256"] != sha(data):
            return False
        previous = receipt["receipt_sha256"]
    return True

def run():
    effects = {}
    receipts = []
    cases = []
    for candidate, expected, delta in samples():
        before = copy.deepcopy(effects)
        conditions = {k:v for k,v in candidate.items() if k != "failure"}
        fingerprint = sha(conditions)
        decision, reasons = valid(candidate)
        fault = candidate.get("failure")
        if fault:
            decision, reasons = "ERROR_HOLD", ["injected_" + fault + "_failure"]
            # Deliberately before local atomic assignment: nothing is committed.
        else:
            staged = copy.deepcopy(effects)
            if decision == "ALLOW" and candidate["effect_key"] not in staged:
                staged[candidate["effect_key"]] = {
                    "effect_key": candidate["effect_key"], "condition_sha256": fingerprint,
                    "evidence": candidate["evidence"]}
            receipt_body = {
                "schema": "aar-facing-public-fixture/1", "rule": RULE,
                "sequence": len(receipts) + 1,
                "receipt_id": f'PUB-RCP-{len(receipts)+1:04d}',
                "case_id": candidate["id"],
                "decision": decision, "reasons": reasons,
                "condition_sha256": fingerprint,
                "before_sha256": sha(before), "after_sha256": sha(staged),
                "effect_delta": len(staged) - len(before),
                "previous_sha256": receipts[-1]["receipt_sha256"] if receipts else ZERO,
                "mock_only": True,
            }
            receipt = {**receipt_body, "receipt_sha256": sha(receipt_body)}
            # Only a single in-memory staging seam; not a durable / distributed transaction.
            effects, receipts = staged, [*receipts, receipt]
        observed_delta = len(effects) - len(before)
        passed = decision == expected and observed_delta == delta and replay_check(receipts)
        cases.append({
            "id": candidate["id"], "expected": expected, "decision": decision,
            "expected_effect_delta": delta, "effect_delta": observed_delta,
            "effect_before_sha256": sha(before), "effect_after_sha256": sha(effects),
            "condition_sha256": fingerprint, "receipt_id": receipts[-1]["receipt_id"] if not fault else None,
            "reasons": reasons, "pass": passed,
            "mock": True,
        })
    result = {
        "schema": "aar-facing-public-fixture/1", "run_id": "AAR-FACING-2026-11-17-SYN-001",
        "rule": RULE, "origin": "independent public examiner, not AAR source code",
        "case_count": len(cases), "passed": sum(c["pass"] for c in cases),
        "failed": sum(not c["pass"] for c in cases),
        "receipts": len(receipts), "mock_effects": len(effects),
        "duplicate_effects": len([c for c in cases if c["id"].startswith("02-") and c["effect_delta"]]),
        "receipt_chain_verified": replay_check(receipts),
        "status": "PASS / SYNTHETIC EXAMINER ONLY" if all(c["pass"] for c in cases) else "FAIL",
        "native_va_weave": False, "aar_owner_reviewed": False,
        "third_party_reproduced": False, "production_system": False,
        "route_scope": "one in-process declared route + one synthetic attempted bypass",
        "external_effects": False, "real_timebase": False,
    }
    assert result["case_count"] == 20 and result["passed"] == 20
    assert result["receipts"] == 18 and result["mock_effects"] == 3
    assert result["duplicate_effects"] == 0 and result["receipt_chain_verified"]
    return result, cases, receipts, effects

def write(out: Path):
    result, cases, receipts, effects = run()
    out.mkdir(parents=True, exist_ok=True)
    paths = {
        "result.json": json.dumps(result, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        "cases.json": json.dumps(cases, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
        "receipts.jsonl": "".join(json.dumps(r, sort_keys=True, ensure_ascii=True) + "\n" for r in receipts),
        "effects.json": json.dumps(effects, sort_keys=True, indent=2, ensure_ascii=True) + "\n",
    }
    for name, body in paths.items(): (out/name).write_text(body, encoding="utf-8")
    manifest = {name: hashlib.sha256(body.encode("utf-8")).hexdigest() for name,body in paths.items()}
    (out/"manifest.json").write_text(json.dumps(manifest, sort_keys=True, indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="evidence", help="Synthetic output directory")
    args = parser.parse_args()
    write(Path(args.out))
