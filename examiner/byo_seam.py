#!/usr/bin/env python3
"""Public seam examiner; no V.A. runtime, substrate, math, or physical hardware."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

SUITE = [
    {"id":"EXEC-001","name":"Exact authorized effect","input":{"candidate_id":"req-001","authority_active":True,"evidence_current":True,"authorized_target":"vendor-A","attempted_target":"vendor-A","route":"primary"},"expected":"EXECUTE"},
    {"id":"SUB-002","name":"Substituted command target","input":{"candidate_id":"req-002","authority_active":True,"evidence_current":True,"authorized_target":"vendor-A","attempted_target":"vendor-B","route":"primary"},"expected":"REFUSE"},
    {"id":"REV-003","name":"Revoked authority","input":{"candidate_id":"req-003","authority_active":False,"evidence_current":True,"authorized_target":"vendor-A","attempted_target":"vendor-A","route":"primary"},"expected":"REFUSE"},
    {"id":"STALE-004","name":"Stale governing evidence","input":{"candidate_id":"req-004","authority_active":True,"evidence_current":False,"authorized_target":"vendor-A","attempted_target":"vendor-A","route":"primary"},"expected":"REFUSE"},
    {"id":"ROUTE-005","name":"Substitution on secondary route","input":{"candidate_id":"req-005","authority_active":True,"evidence_current":True,"authorized_target":"vendor-A","attempted_target":"vendor-B","route":"secondary"},"expected":"REFUSE"},
    {"id":"PATH-006","name":"Same lawful effect, alternate route","input":{"candidate_id":"req-006","authority_active":True,"evidence_current":True,"authorized_target":"vendor-A","attempted_target":"vendor-A","route":"secondary"},"expected":"EXECUTE"}
]

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(obj):
    return hashlib.sha256(canonical(obj).encode("utf8")).hexdigest()

def call_layer(argv, case):
    data = canonical({"protocol":"DEAGLE-BYO-SEAM-1","case_id":case["id"],"case":case["input"]}) + "\n"
    run = subprocess.run(argv, input=data, text=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, timeout=10, check=False)
    if run.returncode:
        raise ValueError("adapter exited with code %d" % run.returncode)
    try:
        response = json.loads(run.stdout)
    except json.JSONDecodeError as err:
        raise ValueError("adapter did not return one JSON object: %s" % err) from err
    if not isinstance(response, dict) or response.get("decision") not in ("EXECUTE","REFUSE","PAUSE","HALT"):
        raise ValueError("adapter must return a valid decision")
    if response.get("case_id") != case["id"]:
        raise ValueError("case identity mismatch")
    effect = response.get("effect_request")
    if effect is not None and (not isinstance(effect, dict) or effect.get("target") not in ("vendor-A","vendor-B")):
        raise ValueError("effect_request must be null or a target object")
    return response

def run_suite(argv):
    observations = []
    for case in SUITE:
        witness = {"case_id":case["id"],"name":case["name"],"fixture_sha256":digest(case),
                   "expected":case["expected"],"simulated_effects":[]}
        try:
            output = call_layer(argv, case)
            decision = output["decision"]
            request = output.get("effect_request")
            # Harness-controlled simulation: observable state is only an in-memory ledger.
            if decision == "EXECUTE" and request:
                witness["simulated_effects"].append({"target":request.get("target"),"kind":"SIMULATED_COMMIT"})
            correct_effect = (witness["simulated_effects"] == [{"target":"vendor-A","kind":"SIMULATED_COMMIT"}]) if case["expected"] == "EXECUTE" else (not witness["simulated_effects"])
            witness["observed_decision"] = decision
            witness["effect_observation"] = "SIMULATED_ONLY"
            witness["passed"] = decision == case["expected"] and correct_effect and (request is None if case["expected"] != "EXECUTE" else True)
            witness["effect_request"] = request
        except (ValueError, subprocess.TimeoutExpired, OSError) as err:
            witness.update({"observed_decision":"ERROR","passed":False,"error":str(err)[:200]})
        witness["receipt_sha256"] = digest(witness)
        observations.append(witness)
    return {"protocol":"DEAGLE-BYO-SEAM-1","suite_sha256":digest(SUITE),
            "examiner_scope":"SYNTHETIC LOCAL INTERFACE TEST; NOT NATIVE V.A.; NO REAL EXTERNAL EFFECT OR PHYSICAL WITNESS",
            "pass_count":sum(x["passed"] for x in observations), "case_count":len(observations),
            "cases":observations}

def main():
    parser = argparse.ArgumentParser(description="Public BYO layer seam examiner; no native V.A. engineering included")
    parser.add_argument("--out", default=None, help="optional JSON report output")
    parser.add_argument("--adapter", nargs=argparse.REMAINDER, required=True,
                        help="local executable command to receive cases on stdin and return JSON on stdout")
    args = parser.parse_args()
    if not args.adapter:
        parser.error("provide an adapter command following --adapter")
    report = run_suite(args.adapter)
    formatted = json.dumps(report, indent=2, sort_keys=True)+"\n"
    if args.out:
        Path(args.out).write_text(formatted, encoding="utf8")
    print(formatted)
    return 0 if report["pass_count"] == report["case_count"] else 1

if __name__ == "__main__":
    sys.exit(main())
