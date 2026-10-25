#!/usr/bin/env python3
"""Read-only 10-carrier external witness packet validator; never executes participant code."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from independent_challenge import check_challenge, check_freeze, cross, CEILING

FILES = (
    "freeze.json", "challenge.json",
    "left-report.json", "left-record.json", "left-signature.json", "left-public.pem",
    "right-report.json", "right-record.json", "right-signature.json", "right-public.pem",
)
SCHEMA = "DEAGLE-EXTERNAL-CYCLE-1"
STATUS = "VALID_LOCAL_SYNTHETIC_CRYPTOGRAPHIC_PACKET__INDEPENDENCE_NOT_ESTABLISHED"


def read_packet(root):
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise ValueError("packet location must be a real directory")
    data, original_files = {}, {}
    for name in FILES:
        path = root / name
        if path.is_symlink() or not path.is_file() or path.resolve().parent != root.resolve():
            raise ValueError("missing, linked, or out-of-directory carrier: " + name)
        content = path.read_bytes()
        if not content or len(content) > (16384 if name.endswith(".pem") else 2 * 1024 * 1024):
            raise ValueError("empty or oversized carrier: " + name)
        original_files[name] = {"sha256": hashlib.sha256(content).hexdigest(), "bytes": len(content)}
        if name.endswith(".json"):
            try:
                value = json.loads(content.decode("utf-8"))
            except (UnicodeError, json.JSONDecodeError) as exc:
                raise ValueError("invalid JSON data: " + name) from exc
            if type(value) is not dict:
                raise ValueError("expected JSON object: " + name)
            data[name] = value
        else:
            if b"PRIVATE KEY" in content or b"BEGIN PUBLIC KEY" not in content:
                raise ValueError("invalid PEM or private key included: " + name)
            data[name] = str(path)
    return data, original_files


def admit(root):
    data, originals = read_packet(root)
    freeze, challenge = data["freeze.json"], data["challenge.json"]
    check_freeze(freeze)
    check_challenge(freeze, challenge)
    left = {"report": data["left-report.json"],
            "record": data["left-record.json"],
            "signature": data["left-signature.json"],
            "public_key": data["left-public.pem"]}
    right = {"report": data["right-report.json"],
             "record": data["right-record.json"],
             "signature": data["right-signature.json"],
             "public_key": data["right-public.pem"]}
    comparison = cross(freeze, challenge, left, right)
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "admission": "LOCAL_DATA_AND_SIGNATURE_VALID_ONLY",
        "frozen_artifact_sha256": freeze["artifact_sha256"],
        "frozen_artifact_bytes_included": False,
        "freeze_sha256": freeze["freeze_sha256"],
        "challenge_sha256": challenge["challenge_sha256"],
        "fixture_sha256": challenge["fixture_sha256"],
        "challenge_family": challenge["family"],
        "challenge_seed": challenge["seed"],
        "challenge_rounds": challenge["rounds"],
        "original_file_manifest": originals,
        "comparison_sha256": comparison["comparison_sha256"],
        "cases": comparison["case_count"],
        "matching_observations": comparison["matching_cases"],
        "differing_observations": comparison["differing_cases"],
        "examiner_left_declared": left["record"]["examiner"],
        "examiner_right_declared": right["record"]["examiner"],
        "signing_key_fingerprints": [comparison["left_key_sha256"], comparison["right_key_sha256"]],
        "independent_chronology_authenticated": False,
        "examiner_identity_authenticated": False,
        "separate_execution_environments_authenticated": False,
        "independent_witness_standing": "NOT ESTABLISHED",
        "native_VA_evidence": False,
        "physical_outcome_evidence": False,
        "public_release_cleared": False,
        "human_reviewer_required": True,
        "standing_ceiling": CEILING,
        "reproduction_note": (
            "The applicant source file is not included or independently checked here. "
            "Signatures prove control of signing keys, not examiner identity or independent execution. "
            "Hash-only records do not prove freeze chronology or real-world effects."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description="Read-only external packet verifier; JSON and public keys only")
    parser.add_argument("packet_dir")
    parser.add_argument("--out")
    args = parser.parse_args()
    try:
        result = admit(args.packet_dir)
        encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
        if args.out:
            Path(args.out).write_text(encoded, encoding="utf-8")
        print(encoded)
        return 0
    except (OSError, ValueError, TypeError, KeyError, AssertionError, OverflowError) as err:
        print("EXTERNAL WITNESS PACKET REFUSED: " + str(err), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
