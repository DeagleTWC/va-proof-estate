#!/usr/bin/env python3
"""Verify the public VA-AD-001 fixture, not native V.A. or pilot outcomes."""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNNER = HERE / "run.py"
ARCHIVE = HERE / "local-fixture-report.json"
CASES = {
    "positive-authorized": ("ADMIT", True),
    "negative-never-authorized": ("REFUSE", False),
    "changed-condition-revoked": ("REFUSE", False),
    "negative-stale-evidence": ("REFUSE", False),
}

def digest(value):
    return hashlib.sha256(json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()

def execute():
    result = subprocess.run(
        [sys.executable, str(RUNNER)], capture_output=True, text=True,
        check=True, cwd=HERE, timeout=20
    )
    return json.loads(result.stdout)

def verify():
    runner_sha = hashlib.sha256(RUNNER.read_bytes()).hexdigest()
    baseline = json.loads(ARCHIVE.read_text(encoding="utf-8"))
    observed, replay = execute(), execute()
    assert observed == replay, "Same-condition replay diverges"
    assert observed["artifact_sha256"] == runner_sha
    assert baseline["artifact_sha256"] == runner_sha
    assert observed["overall"] == "PASS"
    assert observed["native_VA_execution"] == "NOT TESTED"
    assert observed["independent_reproduction"] == "NOT ATTESTED"
    fresh = {r["case"]: r for r in observed["cases"]}
    stored = {r["case"]: r for r in baseline["cases"]}
    assert set(fresh) == set(stored) == set(CASES)
    empty = digest({"protected_effects": []})
    effected = digest({"protected_effects": [
        {"kind": "append_mock_effect", "id": "demo-effect-1"}
    ]})
    for name, (decision, effect) in CASES.items():
        r = fresh[name]
        assert r["decision"] == decision
        assert r["observed_mock_effect"] is effect
        assert r["before_state_sha256"] == empty
        assert r["after_state_sha256"] == (effected if effect else empty)
        assert r["fixture_build_sha256"] == runner_sha
        payload = {k: v for k, v in r.items() if k != "receipt_sha256"}
        assert digest(payload) == r["receipt_sha256"]
        for field, value in stored[name].items():
            assert r[field] == value, f"Archived mismatch: {name}/{field}"
        assert digest(dict(payload, decision="TAMPERED")) != r["receipt_sha256"]
    admitted, revoked = fresh["positive-authorized"], fresh["changed-condition-revoked"]
    assert admitted["candidate"] == revoked["candidate"]
    for field in ("approved", "evidence_valid"):
        assert admitted["condition"][field] == revoked["condition"][field]
    assert admitted["condition"]["authority"] != revoked["condition"]["authority"]
    print("PASS: fixture output, archived report, receipt hashes, mutation detection and replay")
    print("SCOPE: synthetic local fixture; native V.A. and pilot outcomes NOT TESTED")

if __name__ == "__main__":
    verify()
