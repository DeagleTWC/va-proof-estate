#!/usr/bin/env python3
"""VA-AD-001: bounded public-safe examiner fixture, NOT the native V.A. runtime.
Demonstrates a test METHOD: measure allowed effect, refused effect, and changed
standing independently of returned decision words. Standard library only.
"""
import hashlib
import json
from copy import deepcopy
from pathlib import Path

SPEC = "VA-AD-001/SPEC-1.0"
BUILD_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def run_case(case_id, authority, approved, evidence_valid, expected_effect):
    """One controlled mock effect route. No real tools, networks, or customer data."""
    state = {"protected_effects": []}
    before = deepcopy(state)
    candidate = {"kind": "append_mock_effect", "id": "demo-effect-1"}
    allowed = authority == "ACTIVE" and approved and evidence_valid
    decision = "ADMIT" if allowed else "REFUSE"
    if allowed:
        state["protected_effects"].append(candidate)
    after = deepcopy(state)
    actual_effect = len(after["protected_effects"]) > len(before["protected_effects"])
    assert actual_effect == expected_effect, f"{case_id}: observed effect mismatch"
    assert (before != after) == actual_effect, f"{case_id}: state measurement mismatch"
    condition = {"authority": authority, "approved": approved, "evidence_valid": evidence_valid}
    receipt = {
        "spec": SPEC, "fixture_build_sha256": BUILD_SHA256,
        "case": case_id, "condition": condition,
        "candidate": candidate, "decision": decision,
        "before_state_sha256": digest(before),
        "after_state_sha256": digest(after),
        "observed_mock_effect": actual_effect,
        "observer_scope": "same-process, one mock effect route"
    }
    receipt["receipt_sha256"] = digest(receipt)
    return receipt


def verify_receipt(receipt):
    claimed = receipt["receipt_sha256"]
    payload = {k: v for k, v in receipt.items() if k != "receipt_sha256"}
    return digest(payload) == claimed


def main():
    cases = [
        ("positive-authorized", "ACTIVE", True, True, True),
        ("negative-never-authorized", "MISSING", False, True, False),
        ("changed-condition-revoked", "REVOKED", True, True, False),
        ("negative-stale-evidence", "ACTIVE", True, False, False)
    ]
    first = [run_case(*case) for case in cases]
    second = [run_case(*case) for case in cases]
    assert first == second, "same-condition replay diverged"
    assert all(verify_receipt(r) for r in first), "receipt integrity check failed"
    # One changing material condition; same candidate, unchanged approval/evidence.
    assert first[0]["candidate"] == first[2]["candidate"]
    assert first[0]["condition"]["approved"] == first[2]["condition"]["approved"]
    assert first[0]["condition"]["evidence_valid"] == first[2]["condition"]["evidence_valid"]
    assert first[0]["observed_mock_effect"] and not first[2]["observed_mock_effect"]
    report = {
        "identity": SPEC, "artifact_sha256": BUILD_SHA256,
        "evidence_class": "LOCAL SYNTHETIC FIXTURE EXECUTION (NOT NATIVE V.A. RUN)",
        "scope": "one in-process mock effect route; no external effect",
        "cases": first, "same_condition_replay": "PASS",
        "receipt_integrity": "PASS", "overall": "PASS",
        "independent_reproduction": "NOT ATTESTED",
        "native_VA_execution": "NOT TESTED",
        "historical_pilot_data": "NOT INCLUDED"
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
