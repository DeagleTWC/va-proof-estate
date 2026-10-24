#!/usr/bin/env python3
"""Public-safe physical witness metadata preflight. Never validates physical truth."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

CLASSES = {"PH-01":"Protected interior and exterior relations",
           "PH-02":"Independent actuator termination",
           "PH-03":"Acoustic and vibration propagation",
           "PH-04":"Thermal and composite burden"}
REQUIRED_CARRIERS = (
    "pre_state_ref", "post_state_ref", "independent_sensor_ref",
    "calibration_ref", "uncertainty_ref", "negative_control_ref",
    "changed_condition_ref", "same_condition_replay_ref", "receipt_ref",
)
PLACEHOLDERS = {"", "tbd", "unknown", "none", "n/a", "placeholder", "example", "pending"}

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(value):
    return hashlib.sha256(canonical(value).encode("utf8")).hexdigest()

def usable(value):
    return isinstance(value, str) and value.strip().lower() not in PLACEHOLDERS \
        and not any(p in value.lower() for p in ("example.com", "localhost", "<insert", "replace-me"))

def check(packet):
    issues = []
    if not isinstance(packet, dict):
        return {"status":"INCOMPLETE","issues":["packet must be a JSON object"]}
    if packet.get("schema") != "DEAGLE-PHYSICAL-REVIEW-1":
        issues.append("Unknown or missing schema")
    class_id = packet.get("physical_class")
    if class_id not in CLASSES:
        issues.append("Select exactly one PH-01..PH-04 carrier")
    release = packet.get("release", {})
    if not isinstance(release, dict) or release.get("custodian_approved") is not True:
        issues.append("Custodian publication approval not established")
    if not isinstance(release, dict) or release.get("contains_protected_construction") is not False:
        issues.append("Protected construction must not appear in a public packet")
    if not isinstance(release, dict) or release.get("contains_confidential_customer_data") is not False:
        issues.append("Confidential customer data must not appear in a public packet")
    blocked = any("approval" in x or "Protected construction" in x or "Confidential" in x for x in issues)
    artifact = packet.get("artifact", {})
    if not isinstance(artifact, dict):
        artifact = {}
    for key in ("id", "version", "scope"):
        if not usable(artifact.get(key)):
            issues.append("Missing fixed artifact "+key)
    digest_id = artifact.get("sha256")
    if not isinstance(digest_id, str) or re.fullmatch(r"[a-fA-F0-9]{64}", digest_id) is None:
        issues.append("Invalid or absent fixed-artifact SHA-256")
    if artifact.get("frozen") is not True:
        issues.append("Artifact freeze not established")
    evidence = packet.get("evidence", {})
    if not isinstance(evidence, dict):
        evidence = {}
    for field in REQUIRED_CARRIERS:
        if not usable(evidence.get(field)):
            issues.append("Missing or placeholder evidence reference: "+field)
    if class_id in ("PH-03", "PH-04") and not usable(evidence.get("domain_specific_accounting_ref")):
        issues.append("Missing carrier-specific propagation / energy accounting")
    if packet.get("asserted_independent_reproduction") is True:
        if not usable(evidence.get("independent_reproduction_ref")):
            issues.append("Independent reproduction asserted without a separate examination reference")
    result = {
        "schema":"DEAGLE-PHYSICAL-PREFLIGHT-1",
        "record_sha256":digest(packet),
        "physical_class":class_id if class_id in CLASSES else None,
        "class_name":CLASSES.get(class_id),
        "status":("WITHHOLD_PUBLICATION" if blocked else
                  "METADATA_INCOMPLETE" if issues else
                  "METADATA_PRESENT_UNVERIFIED"),
        "issues":issues,
        "metadata_only":True,
        "native_VA_proof_established":False,
        "physical_outcome_verified":False,
        "independent_reproduction_verified":False,
        "reviewer_note":("Fields and references are checked for presence and release declarations only. "
                         "There is no authentication of witnesses, measurements, calibration, claims or their truth. "
                         "A structurally complete packet does not establish observed physical behavior.")
    }
    return result

def main():
    parser = argparse.ArgumentParser(description="Check physical witness evidence metadata; no hardware tests")
    parser.add_argument("packet")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    try:
        raw = Path(args.packet).read_text(encoding="utf8")
        data = json.loads(raw)
        report = check(data)
        encoded = json.dumps(report, indent=2, sort_keys=True)+"\n"
        if args.out:
            Path(args.out).write_text(encoded, encoding="utf8")
        print(encoded)
        return 0 if report["status"] == "METADATA_PRESENT_UNVERIFIED" else 1
    except (OSError, ValueError) as exc:
        print("PACKET ERROR: %s" % exc, file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
