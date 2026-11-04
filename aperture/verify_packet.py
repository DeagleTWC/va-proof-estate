#!/usr/bin/env python3
"""V.A. Consequence Aperture public-safe data-only ORIGINAL-BYTE preflight.
Never executes an adapter, native URK, machine, command, or experiment.
Successful result establishes structure and exact source bytes, never scientific standing.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

SCHEMA = "VA-APERTURE-1"
KINDS = {"POSITIVE", "NEGATIVE", "CHANGED", "REPLAY"}
SHA = re.compile(r"^[0-9a-fA-F]{64}$")
NAME = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,158}$")
CEILING = "DECLARED_ONLY: STRUCTURE + SHA-256, NOT NATIVE EXECUTION, EFFECT PROOF OR INDEPENDENT REPRODUCTION"

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def timestamp(value):
    if not isinstance(value, str) or not value.endswith(("Z", "+00:00")):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

def fail_if(errors, condition, message):
    if not condition:
        errors.append(message)

def file_name(value):
    return isinstance(value, str) and value not in (".", "..") and NAME.fullmatch(value) is not None

def packet_structure(packet):
    errors = []
    if not isinstance(packet, dict):
        return ["Packet must be an object."], {}
    fail_if(errors, packet.get("schema") == SCHEMA, "Schema mismatch.")
    fail_if(errors, packet.get("standing") == "DECLARED_ONLY", "Self-submitted standing must be DECLARED_ONLY.")
    fail_if(errors, nonempty(packet.get("packet_id")), "Packet ID missing.")
    for flag in ("claimed_proven", "native_certified", "independent_reproduced"):
        fail_if(errors, packet.get(flag) is not True, "Self-certification forbidden: " + flag)
    freeze, challenge, boundary, witness = (packet.get(key) if isinstance(packet.get(key), dict) else {} for key in ("freeze", "challenge", "boundary", "witness"))
    fail_if(errors, nonempty(freeze.get("artifact_id")) and nonempty(freeze.get("owner_id")) and isinstance(freeze.get("artifact_sha256"), str) and SHA.fullmatch(freeze["artifact_sha256"]), "Freeze identity and 64-digit SHA-256 required.")
    a, b = timestamp(freeze.get("frozen_at")), timestamp(challenge.get("issued_at"))
    fail_if(errors, bool(a and b and a < b), "Declared freeze time must precede challenge issue time.")
    fail_if(errors, nonempty(freeze.get("anchor")) and freeze.get("anchor", "").startswith("https://"), "Separate HTTPS freeze anchor required; identity/chronology unverified.")
    fail_if(errors, all(nonempty(challenge.get(key)) for key in ("id", "examiner_id", "condition_summary")), "Challenge fields missing.")
    fail_if(errors, challenge.get("examiner_id") != freeze.get("owner_id"), "Issuer and applicant IDs must differ (not proof of independence).")
    routes = boundary.get("alternate_routes")
    fail_if(errors, nonempty(boundary.get("protected_effect")) and nonempty(boundary.get("observation_scope")) and isinstance(routes, list) and len(routes) > 0 and all(nonempty(x) for x in routes), "Protected effect, scope and alternate routes required.")
    fail_if(errors, nonempty(witness.get("id")) and witness.get("id") != freeze.get("owner_id") and file_name(witness.get("statement_file")), "Witness declaration and statement file required.")
    originals = packet.get("originals")
    fail_if(errors, isinstance(originals, list) and bool(originals), "Original manifest missing.")
    expected = {}
    if isinstance(originals, list):
        for i, item in enumerate(originals):
            if not isinstance(item, dict) or not file_name(item.get("file")) or not isinstance(item.get("sha256"), str) or not SHA.fullmatch(item["sha256"]):
                errors.append(f"Original {i} has unsafe name or invalid SHA-256.")
                continue
            name = item["file"]
            if name in expected:
                errors.append("Duplicate original filename: " + name)
            expected[name] = item["sha256"].lower()
    fail_if(errors, witness.get("statement_file") in expected, "Witness statement original absent.")
    controls = packet.get("controls")
    fail_if(errors, isinstance(controls, list) and len(controls) == 4, "Exactly four described control records required.")
    records = {}
    used = set()
    if isinstance(controls, list):
        for index, control in enumerate(controls):
            if not isinstance(control, dict) or control.get("kind") not in KINDS:
                errors.append(f"Invalid kind at control {index}.")
                continue
            kind = control["kind"]
            if kind in records:
                errors.append("Duplicate control: " + kind)
            records[kind] = control
            fail_if(errors, nonempty(control.get("condition_id")), kind + " condition ID missing.")
            fail_if(errors, type(control.get("measured_effect")) is bool, kind + " measured_effect must be an observed boolean claim, not an expected outcome.")
            for field in ("measurement_file", "receipt_file"):
                name = control.get(field)
                fail_if(errors, file_name(name) and name in expected, kind + " missing original for " + field)
                if file_name(name):
                    if name in used or name == witness.get("statement_file"):
                        errors.append("Original reused across roles: " + name)
                    used.add(name)
            fail_if(errors, control.get("measurement_file") != control.get("receipt_file"), kind + " receipt cannot be its own measurement.")
    fail_if(errors, set(records) == KINDS, "Positive, negative, changed, replay controls required.")
    if "POSITIVE" in records and "REPLAY" in records:
        fail_if(errors, records["POSITIVE"].get("condition_id") == records["REPLAY"].get("condition_id"), "Replay condition ID must match baseline.")
    if "POSITIVE" in records and "CHANGED" in records:
        fail_if(errors, records["POSITIVE"].get("condition_id") != records["CHANGED"].get("condition_id"), "Changed condition must differ from baseline.")
    return errors, expected

def hash_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for piece in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(piece)
    return digest.hexdigest()

def verify_packet(packet, originals_dir):
    errors, expected = packet_structure(packet)
    root = Path(originals_dir)
    if not root.is_dir():
        errors.append("Originals directory missing.")
    else:
        for name, digest in expected.items():
            target = root / name
            # Only a single flat directory of regular, unsymlinked original files.
            if not target.is_file() or target.is_symlink():
                errors.append("Missing or unsafe original file: " + name)
                continue
            if hash_file(target) != digest:
                errors.append("SHA-256 mismatch: " + name)
    return {"ok": not errors, "packet_id": packet.get("packet_id") if isinstance(packet, dict) else None,
            "original_count": len(expected), "errors": errors,
            "standing": "DECLARED_ONLY", "ceiling": CEILING}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    parser.add_argument("--originals", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.packet.stat().st_size > 1024 * 1024:
            raise ValueError("Packet exceeds 1 MB")
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
        result = verify_packet(packet, args.originals)
    except (OSError, ValueError, UnicodeError) as exc:
        result = {"ok": False, "standing": "DECLARED_ONLY", "ceiling": CEILING, "errors": [str(exc)]}
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 2

if __name__ == "__main__":
    sys.exit(main())
