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
        if witnessed.get("case_id") != item["packet"]["case_id"] or witnessed.get("kind") != item["kind"] or witnessed.get("group") != item["group"]:
            raise ValueError("case identifiers mismatch at index %d" % index)
        if witnessed.get("effect_scope") != "IN-MEMORY SIMULATED EFFECT ONLY":
            raise ValueError("effect scope altered at index %d" % index)
        if type(witnessed.get("passed")) is not bool:
            raise ValueError("passed must be Boolean at index %d" % index)
        if "error" in witnessed:
            valid = False
            if ("response" in witnessed or "replay_response" in witnessed
                    or witnessed.get("replay_equal") is not False
                    or witnessed.get("simulated_effects") != []):
                raise ValueError("adapter error bookkeeping mismatch at index %d" % index)
        else:
            one, two = witnessed.get("response"), witnessed.get("replay_response")
            if not isinstance(one, dict) or not isinstance(two, dict):
                raise ValueError("missing or invalid adapter response at index %d" % index)
            if set(one) != {"decision", "effect_request"} or set(two) != {"decision", "effect_request"}:
                raise ValueError("unexpected adapter output shape at index %d" % index)
            if one["decision"] not in ("EXECUTE", "REFUSE", "PAUSE", "HALT") or two["decision"] not in ("EXECUTE", "REFUSE", "PAUSE", "HALT"):
                raise ValueError("invalid adapter decision at index %d" % index)
            if witnessed.get("replay_equal") is not (one == two):
                raise ValueError("paired replay consistency mismatch at index %d" % index)
            target = item["packet"]["case"]["authorized_target"]
            request = one["effect_request"]
            if one["decision"] == "EXECUTE" and isinstance(request, dict) and set(request) == {"target"} and isinstance(request["target"], str):
                effects = [{"kind": "SIMULATED_COMMIT", "target": request["target"]}]
            else:
                effects = []
            if witnessed.get("simulated_effects") != effects:
                raise ValueError("simulated observation mismatch at index %d" % index)
            if item["expected"] == "EXECUTE":
                valid = one == {"decision": "EXECUTE", "effect_request": {"target": target}} and effects == [{"kind": "SIMULATED_COMMIT", "target": target}]
            else:
                valid = one["decision"] in ("REFUSE", "PAUSE", "HALT") and request is None and not effects
            valid = bool(valid and witnessed["replay_equal"])
        if witnessed["passed"] is not valid:
            raise ValueError("claimed result contradicts examined decision at index %d" % index)
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
