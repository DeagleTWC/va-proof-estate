#!/usr/bin/env python3
"""Compare two independently prepared local BYO reports, never native V.A. proof."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

from adversarial_matrix import sha
from verify_matrix import integrity_check
from verify_session import verify as verify_session

CEILING = ("LOCAL SYNTHETIC INTERFACE COMPARISON ONLY; no native V.A. execution, "
           "real-world effect custody, independent witnessing, certification, or "
           "architectural equivalence established.")


def checked(report):
    if not isinstance(report, dict):
        raise ValueError("report must be a JSON object")
    if report.get("version") == "MATRIX-1.0" and report.get("protocol") == "DEAGLE-BYO-SEAM-1":
        integrity_check(report)
        return "matrix", report["fixture_manifest_sha256"], report["cases"]
    if report.get("protocol") == "DEAGLE-BYO-SESSION-1":
        verify_session(report)
        return "session", report["fixture_sha256"], report["observations"]
    raise ValueError("unsupported examiner protocol; no promotion or automatic conversion")


def compare(left, right, left_id, right_id):
    if not left_id.strip() or not right_id.strip() or left_id.strip() == right_id.strip():
        raise ValueError("declare distinct non-empty participant identifiers")
    a_type, a_suite, a_obs = checked(left)
    b_type, b_suite, b_obs = checked(right)
    if a_type != b_type or a_suite != b_suite or left.get("seed") != right.get("seed") or left.get("rounds") != right.get("rounds"):
        raise ValueError("different protocol, fixture, seed or rounds; comparison not admissible")
    observations = []
    for a, b in zip(a_obs, b_obs):
        a_id = a["case_id"] if a_type == "matrix" else a["event_id"]
        b_id = b["case_id"] if b_type == "matrix" else b["event_id"]
        if a_id != b_id or a["expected"] != b["expected"]:
            raise ValueError("case identity or expectation mismatch")
        x = a.get("response") if a_type == "matrix" else a.get("observed")
        y = b.get("response") if b_type == "matrix" else b.get("observed")
        match = x == y and a["passed"] == b["passed"]
        observations.append({
            "id": a_id, "expected": a["expected"], "matching_observed_result": match,
            "left_passed": a["passed"], "right_passed": b["passed"],
            "left_observed": x, "right_observed": y
        })
    comparison = {
        "schema": "DEAGLE-BYO-COMPARISON-1",
        "protocol": a_type,
        "fixture_sha256": a_suite, "seed": left["seed"], "rounds": left["rounds"],
        "left": {"declared_participant": left_id, "source_report_sha256": left["report_sha256"],
                 "passed": left["pass_count"]},
        "right": {"declared_participant": right_id, "source_report_sha256": right["report_sha256"],
                  "passed": right["pass_count"]},
        "case_count": len(observations),
        "matching_results": sum(int(x["matching_observed_result"]) for x in observations),
        "differing_results": sum(int(not x["matching_observed_result"]) for x in observations),
        "observations": observations,
        "standing": CEILING,
        "participant_identity_verified": False,
        "independent_execution_verified": False,
        "native_VA_proof_established": False,
        "report_hashes_authenticate_authorship": False,
    }
    comparison["comparison_sha256"] = sha(comparison)
    return comparison


def main():
    parser = argparse.ArgumentParser(description="Side-by-side, same-fixture synthetic BYO outcomes")
    parser.add_argument("--left", required=True)
    parser.add_argument("--right", required=True)
    parser.add_argument("--left-id", required=True)
    parser.add_argument("--right-id", required=True)
    parser.add_argument("--out")
    args = parser.parse_args()
    try:
        left_bytes = Path(args.left).read_bytes()
        right_bytes = Path(args.right).read_bytes()
        left = json.loads(left_bytes)
        right = json.loads(right_bytes)
        result = compare(left, right, args.left_id, args.right_id)
        result["left"]["source_file_sha256"] = hashlib.sha256(left_bytes).hexdigest()
        result["right"]["source_file_sha256"] = hashlib.sha256(right_bytes).hexdigest()
        result["comparison_sha256"] = sha({k: v for k, v in result.items() if k != "comparison_sha256"})
        encoded = json.dumps(result, sort_keys=True, indent=2) + "\n"
        if args.out:
            Path(args.out).write_text(encoded, encoding="utf-8")
        print(encoded)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("COMPARISON REFUSED: %s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
