#!/usr/bin/env python3
"""Fail-closed PUBLIC proof status register check, not certification of physical measurements."""
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "kcd" / "KCD-PROOF-REGISTER.json"
EXPECTED = {"KCD-PH-01", "KCD-PH-02", "KCD-PH-03", "KCD-PH-04"}
STATUSES = {"FORMALIZED", "OBSERVED_BOUNDED", "INDEPENDENTLY_REPRODUCED"}

def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def guard(condition, message):
    if not condition:
        raise ValueError(message)

def evidence_path(record, claim_id):
    packet = record.get("evidencePacket")
    guard(isinstance(packet, dict), f"{claim_id}: missing released evidence packet")
    relative = packet.get("path", "")
    guard(isinstance(relative, str) and relative.startswith("kcd/evidence/") and ".." not in relative, f"{claim_id}: invalid evidence path")
    source = (ROOT / relative).resolve()
    guard(str(source).startswith(str((ROOT / "kcd/evidence").resolve()) + "/"), f"{claim_id}: path outside release area")
    guard(source.is_file(), f"{claim_id}: original public evidence packet does not exist")
    sha = packet.get("sha256", "")
    guard(isinstance(sha, str) and re.fullmatch(r"[a-f0-9]{64}", sha), f"{claim_id}: SHA missing or malformed")
    guard(sha256_file(source) == sha, f"{claim_id}: evidence SHA does not match source")
    data = json.loads(source.read_text(encoding="utf-8"))
    guard(data.get("claim_id") == claim_id, f"{claim_id}: wrong evidence claim identity")
    guard(data.get("custodian_publication_approved") is True, f"{claim_id}: no publication approval")
    guard(data.get("contains_protected_construction") is False, f"{claim_id}: protected construction declaration missing")
    for name in ("frozen_carrier", "calibrated_measurement_ref", "uncertainty_ref",
                 "positive_control_ref", "negative_control_ref",
                 "changed_condition_ref", "actual_effect_observation_ref",
                 "same_condition_replay_ref", "receipt_ref"):
        guard(isinstance(data.get(name), str) and bool(data[name].strip()), f"{claim_id}: {name} missing")
    return data

def main():
    obj = json.loads(REGISTER.read_text(encoding="utf-8"))
    guard(obj.get("schema") == "DEAGLE-KCD-PROOF-REGISTER-1", "Invalid KCD proof register schema")
    guard(obj.get("source") == "KCD Unified Mechanism and Application Architecture v2.0", "Corrected source changed")
    guard(obj.get("protectedConstructionReleased") is False, "Protected construction release state changed")
    guard(obj.get("programBInheritedStanding") is False, "Program B cannot inherit Program A proof")
    items = obj.get("claims")
    guard(isinstance(items, list) and {x.get("id") for x in items} == EXPECTED and len(items) == 4,
          "KCD PH identifiers are missing, repeated or renamed")
    measured = 0
    independent = 0
    for c in items:
        ident = c["id"]
        state = c.get("evidenceStatus")
        guard(state in STATUSES, f"{ident}: invalid evidence status")
        guard(c.get("sourceStage") == "FORMALIZED", f"{ident}: source formal identity changed")
        guard(c.get("fieldClasses") and isinstance(c.get("fieldClasses"), list), f"{ident}: carrier identity missing")
        guard("simulated" not in c["fieldClasses"], f"{ident}: synthetic carrier cannot qualify as physical witness")
        guard(c.get("physicalMeasurementAttached") is (state != "FORMALIZED"), f"{ident}: physical attachment mismatch")
        if state == "FORMALIZED":
            guard(c.get("evidencePacket") is None, f"{ident}: formal-only item cannot include promoted result")
            guard(c.get("independentWitnessAttached") is False, f"{ident}: independent witness without physical evidence")
        else:
            measured += 1
            packet = evidence_path(c, ident)
            if state == "INDEPENDENTLY_REPRODUCED":
                independent += 1
                guard(c.get("independentWitnessAttached") is True, f"{ident}: independent witness absent")
                guard(isinstance(packet.get("independent_reproduction_ref"), str)
                      and packet["independent_reproduction_ref"].strip(), f"{ident}: independent packet reference missing")
            else:
                guard(c.get("independentWitnessAttached") is False, f"{ident}: unearned independent witness label")
    guard(obj.get("observedPhysicalRunsAttached") == measured,
          "Published physical result count does not match released carriers")
    guard(obj.get("independentPhysicalRunsAttached") == independent,
          "Independent reproduction count does not match released carriers")
    print(json.dumps({"status":"KCD PUBLIC PROOF REGISTER STRUCTURALLY VALID",
                      "formalized_claims":len(items) - measured,"physical_packets":measured,
                      "independent_packets":independent,
                      "scope":"Evidence identity/required metadata only; no laboratory measurement authenticated."},sort_keys=True))
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("KCD REGISTER REJECTED: %s" % exc, file=sys.stderr)
        sys.exit(1)
