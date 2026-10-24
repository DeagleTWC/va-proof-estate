#!/usr/bin/env python3
"""Reconstruct public fixtures and check local report consistency. Not third-party attestation."""
import argparse
import json
import sys
from pathlib import Path

from adversarial_matrix import build_cases, run_matrix, sha

def integrity_check(report):
    if report.get("version") != "MATRIX-1.0":
        raise ValueError("wrong report version")
    signature = report.get("report_sha256")
    unsealed = {k: v for k, v in report.items() if k != "report_sha256"}
    if signature != sha(unsealed):
        raise ValueError("report digest mismatch")
    suite = build_cases(report["seed"], report["rounds"])
    if report.get("fixture_manifest_sha256") != sha(suite):
        raise ValueError("fixture manifest mismatch")
    results = report.get("cases", [])
    if len(results) != len(suite) or report["case_count"] != len(suite):
        raise ValueError("fixture count mismatch")
    if report["pass_count"] != sum(int(x.get("passed", False)) for x in results):
        raise ValueError("pass count mismatch")
    for index, (item, witnessed) in enumerate(zip(suite, results)):
        if witnessed.get("packet") != item["packet"]:
            raise ValueError("input mismatch at index %d" % index)
        if witnessed.get("expected") != item["expected"]:
            raise ValueError("expected status mismatch at index %d" % index)
        if witnessed.get("fixture_sha256") != sha(item):
            raise ValueError("fixture hash mismatch at index %d" % index)
        envelope = {k: v for k, v in witnessed.items() if k != "receipt_sha256"}
        if witnessed.get("receipt_sha256") != sha(envelope):
            raise ValueError("receipt mismatch at index %d" % index)
    return suite

def main():
    parser = argparse.ArgumentParser(description="Verify local synthetic BYO evidence packet")
    parser.add_argument("report", help="previously saved JSON report")
    parser.add_argument("--adapter", nargs=argparse.REMAINDER,
                        help="optional trusted local executable to reproduce results")
    args = parser.parse_args()
    try:
        original = json.loads(Path(args.report).read_text(encoding="utf-8"))
        integrity_check(original)
        if args.adapter:
            repeated = run_matrix(args.adapter, original["seed"], original["rounds"])
            if repeated != original:
                raise ValueError("reproduction mismatch: current adapter outputs differ from preserved report")
        print(json.dumps({
            "status": "LOCAL REPORT INTEGRITY VALID",
            "source": str(args.report),
            "adapter_reproduced": bool(args.adapter),
            "case_count": original["case_count"],
            "pass_count": original["pass_count"],
            "standing": "SELF-CONTAINED LOCAL SYNTHETIC CHECK ONLY; NOT INDEPENDENT OR NATIVE V.A.",
        }, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print("VERIFICATION FAILED: %s" % exc, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
