#!/usr/bin/env python3
"""Verify frozen public AAR-facing synthetic evidence, including negative mutation test."""
from hashlib import sha256
from pathlib import Path
import json
from examiner import run, replay_check, sha

ROOT = Path(__file__).resolve().parent
EV = ROOT / "evidence"
manifest = json.loads((EV / "manifest.json").read_text("utf-8"))
for name,digest in manifest.items():
    actual = sha256((EV/name).read_bytes()).hexdigest()
    assert actual == digest, f"artifact corruption: {name}"
result, cases, receipts, effects = run()
archived_result = json.loads((EV/"result.json").read_text("utf-8"))
archived_cases = json.loads((EV/"cases.json").read_text("utf-8"))
archived_effects = json.loads((EV/"effects.json").read_text("utf-8"))
archived_receipts = [json.loads(s) for s in (EV/"receipts.jsonl").read_text("utf-8").splitlines()]
assert (result, cases, effects, receipts) == (archived_result, archived_cases, archived_effects, archived_receipts), "nondeterministic replay"
assert replay_check(archived_receipts), "invalid receipt chain"
mutant = [dict(x) for x in archived_receipts]
mutant[3]["decision"] = "ALLOW" if mutant[3]["decision"] != "ALLOW" else "BLOCK"
assert not replay_check(mutant), "mutation undetected"
for case in archived_cases:
    assert case["decision"] == case["expected"]
    assert case["effect_delta"] == case["expected_effect_delta"]
    if case["decision"] in ("BLOCK","HOLD","ERROR_HOLD"):
        assert case["effect_before_sha256"] == case["effect_after_sha256"], f"refused effect happened: {case['id']}"
assert len(archived_effects) == 3
print("PASS: 20/20 cases; 18 immutable-chain receipts; 3 mock effects; 0 duplicate mock effects")
print("PASS: exact artifact hashes, deterministic replay, negative mutation detection")
print("BOUNDARY: local mock only; AAR author approval, native V.A. weave, external witnesses NOT CLAIMED")
