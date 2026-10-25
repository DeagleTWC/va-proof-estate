#!/usr/bin/env python3
"""Read-only, data-only BYO workflow evidence audit; never executes supplied code."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

SCHEMA = "deagle-byo-workflow-evidence/1.0"
OBS_SCHEMA = "deagle-byo-observation/1.0"
MEASURE_SCHEMA = "deagle-byo-effect-observer/1.0"
RECEIPT_SCHEMA = "deagle-byo-boundary-receipt/1.0"
HEX = re.compile(r"^[0-9a-f]{64}$")
LABEL = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]{1,80}$")
REQUIRED = {"ALLOW", "REFUSE", "CHANGED"}
ALLOWED = REQUIRED | {"REPLAY"}
ALLOWED_SUFFIXES = {".json", ".jsonl", ".txt", ".csv"}
MAX_BYTES = 2_000_000


def need(check, why):
    if not check:
        raise ValueError(why)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":")).encode("utf-8")


def file_with_hash(root, relative, expected, description):
    need(isinstance(relative, str) and relative and len(relative) < 240,
         f"Missing path for {description}")
    rel = Path(relative)
    need(not rel.is_absolute() and ".." not in rel.parts and
         "\\" not in relative and rel.as_posix() == relative,
         f"Unsafe path: {description}")
    need(rel.suffix.lower() in ALLOWED_SUFFIXES, "No executable or archive sources admitted")
    root = root.resolve()
    current = root
    for piece in rel.parts:
        current /= piece
        need(not current.is_symlink(), f"Symlink refused: {description}")
    resolved = current.resolve()
    need(resolved.is_relative_to(root) and resolved.is_file(), f"File missing: {description}")
    size = resolved.stat().st_size
    need(size <= MAX_BYTES, f"File too large: {description}")
    need(isinstance(expected, str) and HEX.fullmatch(expected), f"Invalid SHA-256: {description}")
    actual = hashlib.sha256(resolved.read_bytes()).hexdigest()
    need(actual == expected, f"Changed or mismatched original bytes: {description}")
    return resolved


def load_json(path, what):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError(f"Invalid JSON in {what}") from exc


def bound_file(root, identity, label):
    need(isinstance(identity, dict), "Missing carrier identity: " + label)
    return file_with_hash(root, identity.get("path"), identity.get("sha256"), label)


def run_packet(root):
    root = Path(root).absolute()
    need(root.is_dir() and not root.is_symlink(), "Select a real local packet directory")
    manifest = load_json(root / "manifest.json", "manifest")
    need(manifest.get("schema") == SCHEMA, "Unknown packet schema")
    need(manifest.get("packetCustody") == "PARTICIPANT_OWNED_LOCAL",
         "Participant custody declaration missing")
    need(manifest.get("releaseAuthorized") is False,
         "Public release is a separate human review, not a local switch")
    need(manifest.get("externalEffectStanding") == "UNVERIFIED",
         "Cannot self-promote real-world effect status")
    name = manifest.get("workflowId")
    need(isinstance(name, str) and LABEL.fullmatch(name), "Invalid workflow identity")
    work = load_json(bound_file(root, manifest.get("workflow"), "workflow"), "workflow")
    need(isinstance(work, dict) and work.get("workflowId") == name,
         "Workflow carrier identity mismatch")
    need(isinstance(work.get("protectedConsequence"), str) and work["protectedConsequence"].strip(),
         "Protected consequence not named")
    routes = work.get("declaredRoutes")
    need(isinstance(routes, list) and routes and all(isinstance(x, str) and x for x in routes)
         and len(set(routes)) == len(routes), "Missing or duplicate declared routes")
    entries = manifest.get("cases")
    need(isinstance(entries, list) and 3 <= len(entries) <= 40,
         "Packet must contain 3-40 original case sources")
    ids = set()
    kinds = set()
    observations = {}
    files = set()
    for source in entries:
        need(isinstance(source, dict), "Invalid case carrier")
        case_path = bound_file(root, source, "case")
        need(str(case_path) not in files, "Reused case carrier")
        files.add(str(case_path))
        case = load_json(case_path, "case")
        need(isinstance(case, dict) and case.get("schema") == OBS_SCHEMA,
             "Invalid observation schema")
        cid, kind = case.get("caseId"), case.get("kind")
        need(isinstance(cid, str) and LABEL.fullmatch(cid) and cid not in ids,
             "Missing or duplicate case ID")
        need(kind in ALLOWED, "Unknown case class")
        need(case.get("workflowId") == name, "Cross-workflow result injected")
        need(isinstance(case.get("candidateId"), str) and case["candidateId"].strip(),
             "Missing candidate identity")
        need(isinstance(case.get("conditionDigest"), str) and HEX.fullmatch(case["conditionDigest"]),
             "Invalid governing condition digest")
        need(case.get("route") in routes, "Observation references undeclared effect route")
        need(case.get("decision") in ("EXECUTE", "REFUSE", "HALT"), "Unknown consequence decision")
        need(type(case.get("effectObserved")) is bool, "No actual observation value given")
        measurement = load_json(bound_file(root, case.get("measurement"), "effect measurement"), "effect measurement")
        receipt = load_json(bound_file(root, case.get("receipt"), "decision receipt"), "decision receipt")
        need(isinstance(measurement, dict) and measurement.get("schema") == MEASURE_SCHEMA,
             "Invalid independent observation record format")
        need(isinstance(receipt, dict) and receipt.get("schema") == RECEIPT_SCHEMA,
             "Invalid boundary receipt format")
        for item, label in [(receipt, "receipt"), (measurement, "measurement")]:
            need(item.get("caseId") == cid, label + " case ID mismatch")
            need(item.get("workflowId") == name, label + " workflow ID mismatch")
        need(receipt.get("decision") == case["decision"], "Original receipt and case outcome disagree")
        need(measurement.get("effectObserved") is case["effectObserved"],
             "Effect claim contradicted by supplied observer record")
        need(measurement.get("route") == case["route"], "Different effect path was measured")
        need(measurement.get("method") in ("LOCAL_MEASUREMENT", "DECLARED_INDEPENDENT_MEASUREMENT",
                                           "SIMULATED_EFFECT"),
             "Measurement method not disclosed")
        need(isinstance(measurement.get("observationDescription"), str)
             and measurement["observationDescription"].strip(), "Effect observation details missing")
        need(kind != "ALLOW" or (case["decision"] == "EXECUTE" and case["effectObserved"]),
             "Positive control does not show declared effect")
        if kind in ("REFUSE", "CHANGED"):
            need(case["decision"] in ("REFUSE", "HALT") and case["effectObserved"] is False,
                 "Non-effect claimed despite execution or observed consequence")
        ids.add(cid)
        kinds.add(kind)
        observations[cid] = case
    need(REQUIRED.issubset(kinds), "Missing positive, negative or changed-condition case")
    base = [x for x in observations.values() if x["kind"] == "ALLOW"]
    for case in observations.values():
        if case["kind"] == "CHANGED":
            previous = observations.get(case.get("changedFrom"))
            need(previous is not None and previous["kind"] == "ALLOW",
                 "Changed-condition source case missing")
            need(case["candidateId"] == previous["candidateId"],
                 "Changed-condition case replaced candidate instead of condition")
            need(case["conditionDigest"] != previous["conditionDigest"],
                 "Changed-condition case did not change governing conditions")
        if case["kind"] == "REPLAY":
            previous = observations.get(case.get("replayOf"))
            need(previous is not None and previous["kind"] == "ALLOW",
                 "Replay must point to an existing permitted original")
            need(case["candidateId"] == previous["candidateId"] and
                 case["conditionDigest"] == previous["conditionDigest"], "Replay conditions drifted")
            need(case["decision"] == previous["decision"] and
                 case["effectObserved"] == previous["effectObserved"], "Same-condition replay disagrees")
            need(case.get("originalReceiptSHA256") == previous["receipt"]["sha256"],
                 "Replay lacks preserved original receipt hash")
    return {"workflowId": name,
            "result": "LOCAL_DATA_CONSISTENCY_ONLY",
            "casesStructurallyMatched": len(observations),
            "caseKinds": sorted(kinds),
            "declaredRoutes": routes,
            "measuredRoutes": sorted(set(x["route"] for x in observations.values())),
            "allDeclaredRoutesMeasured": set(routes).issubset({x["route"] for x in observations.values()}),
            "effectRealityVerifiedByThisTool": False,
            "humanWitnessIndependenceVerified": False,
            "nativeVAReproductionVerified": False,
            "publicationAuthorized": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--packet", required=True)
    p.add_argument("--out", help="Private result file OUTSIDE the packet; never uploaded by this tool")
    a = p.parse_args()
    try:
        result = run_packet(a.packet)
        if a.out:
            root = Path(a.packet).resolve()
            dest = Path(a.out).absolute()
            need(not dest.resolve().is_relative_to(root), "Report output must be outside input packet")
            encoded = (json.dumps(result, indent=2) + "\n").encode("utf-8")
            fd = os.open(str(dest), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, "wb") as f:
                f.write(encoded)
        print(json.dumps(result, indent=2))
    except (ValueError, FileNotFoundError, OSError, TypeError, KeyError, StopIteration) as ex:
        p.exit(2, "REFUSED: " + str(ex) + "\n")


if __name__ == "__main__":
    main()
