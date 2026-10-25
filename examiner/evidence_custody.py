#!/usr/bin/env python3
"""Bind exact report bytes to a self-declared, non-authenticating custody envelope."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

from adversarial_matrix import sha
from compare_reports import checked, CEILING

SCHEMA = "DEAGLE-BYO-LOCAL-CUSTODY-1"


def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def make(report_path, participant, examiner, artifact_id, artifact_path=None, commit=None):
    if not all(isinstance(x, str) and x.strip() for x in (participant, examiner, artifact_id)):
        raise ValueError("participant, examiner, and artifact ID are required")
    if commit and not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
        raise ValueError("commit must be a 40-character Git SHA")
    report = json.loads(Path(report_path).read_bytes())
    kind, suite, _ = checked(report)
    envelope = {
        "schema": SCHEMA,
        "declared_participant": participant,
        "declared_examiner": examiner,
        "artifact_id": artifact_id,
        "artifact_source_file_sha256": file_sha(artifact_path) if artifact_path else None,
        "artifact_source_was_inspected": False,
        "examiner_commit_declared": commit,
        "protocol": kind,
        "fixture_sha256": suite,
        "source_report_byte_sha256": file_sha(report_path),
        "source_report_internal_sha256": report["report_sha256"],
        "source_report_case_count": len(report["cases"] if kind == "matrix" else report["observations"]),
        "standing": CEILING,
        "participant_identity_authenticated": False,
        "examiner_identity_authenticated": False,
        "independent_witness_authenticated": False,
        "native_VA_proof_established": False,
        "note": "SHA-256 detects bytes changing relative to this record, not who made them or whether real-world outcomes occurred. Do not publish private code or data."
    }
    envelope["envelope_sha256"] = sha(envelope)
    return envelope


def verify(envelope, report_path, artifact_path=None):
    if not isinstance(envelope, dict) or envelope.get("schema") != SCHEMA:
        raise ValueError("unknown custody schema")
    expected = sha({k: v for k, v in envelope.items() if k != "envelope_sha256"})
    if envelope.get("envelope_sha256") != expected:
        raise ValueError("custody envelope digest mismatch")
    report = json.loads(Path(report_path).read_bytes())
    kind, suite, observations = checked(report)
    if envelope.get("source_report_byte_sha256") != file_sha(report_path):
        raise ValueError("exact report bytes differ from frozen custody record")
    if (envelope.get("source_report_internal_sha256") != report["report_sha256"]
            or envelope.get("fixture_sha256") != suite
            or envelope.get("protocol") != kind
            or envelope.get("source_report_case_count") != len(observations)):
        raise ValueError("report identity differs from frozen custody record")
    if artifact_path:
        if not envelope.get("artifact_source_file_sha256"):
            raise ValueError("no artifact source file was bound to this envelope")
        if envelope["artifact_source_file_sha256"] != file_sha(artifact_path):
            raise ValueError("local artifact bytes differ from sealed artifact")
    if (envelope.get("native_VA_proof_established") is not False
            or envelope.get("independent_witness_authenticated") is not False
            or envelope.get("participant_identity_authenticated") is not False
            or envelope.get("examiner_identity_authenticated") is not False
            or envelope.get("standing") != CEILING):
        raise ValueError("unsupported evidence promotion or identity claim")
    return {
        "status": "LOCAL_REPORT_BYTES_AND_STRUCTURE_VERIFIED",
        "source_report_byte_sha256": envelope["source_report_byte_sha256"],
        "artifact_file_checked": bool(artifact_path),
        "identity_authenticated": False,
        "independent_witness_authenticated": False,
        "native_VA_proof_established": False,
        "standing": CEILING
    }


def main():
    parser = argparse.ArgumentParser(description="Local, public-safe BYO evidence custody")
    sub = parser.add_subparsers(dest="command", required=True)
    seal = sub.add_parser("seal", help="create local digest-binding envelope")
    seal.add_argument("--report", required=True)
    seal.add_argument("--participant", required=True)
    seal.add_argument("--examiner", required=True)
    seal.add_argument("--artifact-id", required=True)
    seal.add_argument("--artifact-file")
    seal.add_argument("--commit")
    seal.add_argument("--out", required=True)
    check = sub.add_parser("verify", help="check exact bytes and synthetic report structure")
    check.add_argument("--envelope", required=True)
    check.add_argument("--report", required=True)
    check.add_argument("--artifact-file")
    args = parser.parse_args()
    try:
        if args.command == "seal":
            result = make(args.report, args.participant, args.examiner, args.artifact_id,
                          args.artifact_file, args.commit)
            Path(args.out).write_text(json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        else:
            record = json.loads(Path(args.envelope).read_bytes())
            result = verify(record, args.report, args.artifact_file)
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("CUSTODY CHECK REFUSED: %s" % exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
