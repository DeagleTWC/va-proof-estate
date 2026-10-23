#!/usr/bin/env python3
"""Fail closed on unsupported promotion of native V.A. V12 public proof standing.

This checks published artifact availability and integrity, not the scientific
validity of a native V.A. run. Protected/private materials must not be placed in
this repository to satisfy these checks.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE = ROOT / "proofs" / "V12-EVIDENCE-STATUS.json"
MANIFEST = ROOT / "proof-estate-manifest.json"
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ALLOWED = {
    "NOT_ATTACHED_HERE",
    "BOUNDED_NATIVE_OBSERVED",
    "INDEPENDENTLY_REPRODUCED",
}
PRIMARY = (
    "positiveEffectObservation",
    "negativeNonEffectObservation",
    "changedConditionObservation",
    "sameConditionReplay",
    "receiptRecord",
    "alternateRouteInventory",
)

def require(condition, why):
    if not condition:
        raise ValueError(why)

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def carrier_file(path):
    require(nonempty(path), "Missing relative carrier path")
    p = Path(path)
    require(not p.is_absolute() and ".." not in p.parts, "Unsafe carrier path")
    located = (ROOT / p).resolve()
    require(located.is_relative_to(ROOT), "Carrier escapes repository")
    require(located.is_file(), f"Attached carrier does not exist: {path}")
    return located

def validate_hashed_carrier(data, name):
    require(isinstance(data, dict), f"{name} must identify an actual carrier")
    f = carrier_file(data.get("carrier"))
    digest = data.get("sha256")
    require(isinstance(digest, str) and HEX64.fullmatch(digest), f"{name} missing SHA-256")
    computed = hashlib.sha256(f.read_bytes()).hexdigest()
    require(computed == digest, f"Wrong frozen SHA-256 for {name}")
    return f

def check(gate, manifest):
    require(gate.get("schema") == "va-native-v12-public/1.0", "Wrong evidence-gate schema")
    require(gate.get("system") == "V.A. / The Shift", "Wrong system identity")
    require(gate.get("systemVersion") == "V12", "Cannot register another system version as V12")
    version = manifest.get("systemVersionReference") or {}
    require(version.get("designation") == "V12", "Public manifest version disagrees with gate")
    require(gate.get("publicEvidenceStatus") in ALLOWED, "Unrecognized public evidence standing")
    require(gate.get("document") == "proofs/V12-REVIEW.md", "Wrong public examination route")
    carrier_file(gate["document"])
    status = gate["publicEvidenceStatus"]
    attached_fields = ("nativeCarrier", "nativeCarrierSHA256", "nativeRunIdentifier",
                       *PRIMARY, "releaseAuthorization")
    for name in ("examinerRecords", "independentReproductions"):
        require(isinstance(gate.get(name), list), name + " must be an array")
    if status == "NOT_ATTACHED_HERE":
        for name in attached_fields:
            require(gate.get(name) is None, f"{name}: no native V12 carrier publicly attached")
        require(not gate["examinerRecords"], "No attached examiner records at declared standing")
        require(not gate["independentReproductions"], "No witnessed reproductions at declared standing")
        require(manifest.get("nativeRuntimeReceiptsAttached") == 0, "Native receipt count promoted")
        require(manifest.get("independentlyReproducedRunsAttached") == 0, "Independent run count promoted")
        require(version.get("verifiedFrozenBuildAttached") is False, "Frozen build falsely announced")
        require(version.get("nativeV12ReceiptsAttached") is False, "Native V12 receipts falsely announced")
        require(version.get("independentV12ReproductionAttached") is False, "Reproduction falsely announced")
        return "NOT ATTACHED; public standing accurately bounded"

    native = {"carrier":gate.get("nativeCarrier"), "sha256":gate.get("nativeCarrierSHA256")}
    validate_hashed_carrier(native, "original frozen V12 native build")
    require(nonempty(gate.get("nativeRunIdentifier")), "Missing original V12 run ID")
    for item in PRIMARY:
        validate_hashed_carrier(gate.get(item), item)
    release = gate.get("releaseAuthorization")
    require(nonempty(release), "Release authorization needed for public materials")
    carrier_file(release)
    require(gate["examinerRecords"], "A native observed carrier needs an examiner record")
    for i, item in enumerate(gate["examinerRecords"]):
        validate_hashed_carrier(item, f"examinerRecords[{i}]")
    require(version.get("verifiedFrozenBuildAttached") is True, "Manifest frozen-build status not updated")
    require(version.get("nativeV12ReceiptsAttached") is True, "Manifest native receipts not updated")
    require(manifest.get("nativeRuntimeReceiptsAttached", 0) >= 1, "Manifest receipt count missing")
    if status == "BOUNDED_NATIVE_OBSERVED":
        require(not gate["independentReproductions"], "Cannot attach independent records without reviewing their standing")
        require(version.get("independentV12ReproductionAttached") is False, "False independent reproduction standing")
    else:
        records = gate["independentReproductions"]
        require(len(records) >= 2, "Two separately produced witness records are required")
        names = []
        for i, entry in enumerate(records):
            validate_hashed_carrier(entry, f"independentReproductions[{i}]")
            who = entry.get("examiner")
            require(nonempty(who), "Independent record missing examiner")
            require(nonempty(entry.get("disposition")), "Independent record missing review disposition")
            names.append(who.casefold().strip())
        require(len(names) == len(set(names)), "Witness identities must differ")
        require(version.get("independentV12ReproductionAttached") is True, "Manifest independent state not updated")
        require(manifest.get("independentlyReproducedRunsAttached", 0) >= 2, "Independent run count not established")
    return status

def selftest(gate, manifest):
    def must_fail(mutator):
        a, b = copy.deepcopy(gate), copy.deepcopy(manifest)
        mutator(a, b)
        try:
            check(a, b)
        except ValueError:
            return
        raise AssertionError("Invalid promotion incorrectly accepted")
    must_fail(lambda a,b: a.update(publicEvidenceStatus="BOUNDED_NATIVE_OBSERVED"))
    must_fail(lambda a,b: a.update(publicEvidenceStatus="INDEPENDENTLY_REPRODUCED"))
    must_fail(lambda a,b: b.update(nativeRuntimeReceiptsAttached=1))
    must_fail(lambda a,b: a.update(nativeCarrier="proofs/VA-AD-001/run.py"))
    must_fail(lambda a,b: a.update(systemVersion="V1.2"))
    print("PASS: five unsupported-promotion mutations rejected")

if __name__ == "__main__":
    current_gate = json.loads(GATE.read_text(encoding="utf-8"))
    current_manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    state = check(current_gate, current_manifest)
    print(f"PASS: native V12 public evidence state = {state}")
    selftest(current_gate, current_manifest)
