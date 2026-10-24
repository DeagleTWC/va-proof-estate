#!/usr/bin/env python3
"""Verify local synthetic session report structure, digests, oracle and optional replay."""
import argparse
import json
import sys
from pathlib import Path

from session_challenge import digest, generate, run

def verify(report):
    if not isinstance(report, dict) or report.get("protocol") != "DEAGLE-BYO-SESSION-1":
        raise ValueError("wrong report protocol")
    if not isinstance(report.get("seed"), int) or not isinstance(report.get("rounds"), int):
        raise ValueError("invalid suite identity")
    suite = generate(report["seed"], report["rounds"])
    if report.get("fixture_sha256") != digest(suite):
        raise ValueError("fixture digest mismatch")
    if report.get("report_sha256") != digest({k:v for k,v in report.items() if k != "report_sha256"}):
        raise ValueError("report digest mismatch")
    observations = report.get("observations")
    if not isinstance(observations, list) or len(observations) != len(suite):
        raise ValueError("observation count does not match fixture")
    if report.get("event_count") != len(suite):
        raise ValueError("event count mismatch")
    passing = 0
    for i, (sample, obs) in enumerate(zip(suite, observations)):
        if not isinstance(obs, dict) or obs.get("event_id") != sample["packet"]["event_id"]:
            raise ValueError("observation identity mismatch for index %d" % i)
        if obs.get("packet_sha256") != digest(sample):
            raise ValueError("source packet mismatch for index %d" % i)
        if obs.get("expected") != sample["expected"]:
            raise ValueError("expected decision mismatch for index %d" % i)
        if obs.get("receipt_sha256") != digest({k:v for k,v in obs.items() if k != "receipt_sha256"}):
            raise ValueError("receipt hash mismatch for index %d" % i)
        pkt = sample["packet"]
        expected = {"event_id": pkt["event_id"], "decision": sample["expected"], "effect_request": None}
        if sample["expected"] == "EXECUTE":
            expected["effect_request"] = {"target": pkt["attempted_target"]}
        result = obs["observed"]
        valid = type(result) is dict and result == expected
        actual_effect = ({"kind":"SIMULATED_COMMIT","target":result["effect_request"]["target"]}
                         if type(result) is dict and result.get("decision") == "EXECUTE"
                         and type(result.get("effect_request")) is dict
                         and type(result["effect_request"].get("target")) is str
                         else None)
        if obs.get("simulated_effect") != actual_effect or obs.get("passed") is not valid:
            raise ValueError("simulated effect / pass mismatch for index %d" % i)
        passing += int(valid)
    if report.get("pass_count") != passing:
        raise ValueError("aggregate count mismatch")

def main():
    parser = argparse.ArgumentParser(description="Verify and optionally reproduce local stateful examiner packet")
    parser.add_argument("report")
    parser.add_argument("--adapter", nargs=argparse.REMAINDER,
                        help="optional trusted local adapter command for exact re-examination")
    args = parser.parse_args()
    try:
        original = json.loads(Path(args.report).read_text(encoding="utf8"))
        verify(original)
        if args.adapter:
            reproduction = run(args.adapter, original["seed"], original["rounds"])
            if reproduction != original:
                raise ValueError("adapter recreation differs from archived report")
        print(json.dumps({
            "result":"LOCAL_SYNTHETIC_REPORT_VALID",
            "events":original["event_count"],
            "passed":original["pass_count"],
            "reexecuted":bool(args.adapter),
            "standing":"NO NATIVE V.A., REAL EXTERNAL EFFECT, PHYSICAL WITNESS OR INDEPENDENT REPRODUCTION"
        }, sort_keys=True))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("FAIL: %s" % exc, file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
