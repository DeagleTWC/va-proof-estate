#!/usr/bin/env python3
"""Generated, local-only BYO seam stress cases. Not native V.A. or a physical witness."""
import argparse
import hashlib
import json
import random
import secrets
import subprocess
import sys
from pathlib import Path

PROTOCOL = "DEAGLE-BYO-SEAM-1"
SCOPE = ("GENERATED LOCAL SYNTHETIC SEAM TEST; NOT NATIVE V.A.; "
         "NO EXTERNAL OR PHYSICAL CONSEQUENCE OBSERVED")
NONEXECUTE = {"REFUSE", "PAUSE", "HALT"}
KINDS = (
    ("PERMIT_PRIMARY", "EXECUTE", "primary", True, True, False),
    ("SUBSTITUTE_PRIMARY", "NONEXECUTE", "primary", True, True, True),
    ("REVOKE_PRIMARY", "NONEXECUTE", "primary", False, True, False),
    ("STALE_PRIMARY", "NONEXECUTE", "primary", True, False, False),
    ("PERMIT_SECONDARY", "EXECUTE", "secondary", True, True, False),
    ("SUBSTITUTE_SECONDARY", "NONEXECUTE", "secondary", True, True, True),
    ("REVOKE_SECONDARY", "NONEXECUTE", "secondary", False, True, False),
    ("STALE_SECONDARY", "NONEXECUTE", "secondary", True, False, False),
    ("MULTI_FAIL_SECONDARY", "NONEXECUTE", "secondary", False, False, True),
)

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def sha(obj):
    return hashlib.sha256(canonical(obj).encode("utf-8")).hexdigest()

def build_cases(seed, rounds):
    if rounds < 1 or rounds > 40:
        raise ValueError("rounds must be between 1 and 40")
    rng = random.Random(seed)
    cases = []
    for cohort in range(rounds):
        a = "party-" + format(rng.getrandbits(64), "016x")
        b = "party-" + format(rng.getrandbits(64), "016x")
        while b == a:
            b = "party-" + format(rng.getrandbits(64), "016x")
        candidate_id = "movement-" + format(rng.getrandbits(64), "016x")
        for kind, expectation, route, active, current, substituted in KINDS:
            case_id = "M%02d-%s" % (cohort + 1, kind)
            packet = {
                "protocol": PROTOCOL,
                "case_id": case_id,
                "case": {
                    "candidate_id": candidate_id,
                    "authority_active": active,
                    "evidence_current": current,
                    "authorized_target": a,
                    "attempted_target": b if substituted else a,
                    "route": route,
                },
            }
            cases.append({"packet": packet, "expected": expectation, "group": cohort + 1, "kind": kind})
    rng.shuffle(cases)
    return cases

def invoke(argv, packet):
    proc = subprocess.run(
        argv, input=canonical(packet) + "\n",
        capture_output=True, text=True, timeout=10, check=False,
    )
    if proc.returncode:
        raise ValueError("adapter exit code %d" % proc.returncode)
    try:
        output = json.loads(proc.stdout)
    except (ValueError, TypeError) as exc:
        raise ValueError("expected one JSON object on stdout") from exc
    if not isinstance(output, dict):
        raise ValueError("adapter output must be a JSON object")
    if output.get("case_id") != packet["case_id"]:
        raise ValueError("case_id mismatch")
    if output.get("decision") not in ("EXECUTE", "REFUSE", "PAUSE", "HALT"):
        raise ValueError("unsupported decision")
    request = output.get("effect_request")
    if request is not None:
        if not isinstance(request, dict) or set(request) != {"target"} or not isinstance(request["target"], str):
            raise ValueError("effect_request must be null or an exact {'target': string} object")
    return {"decision": output["decision"], "effect_request": request}

def observe(argv, item):
    packet = item["packet"]
    expected = item["expected"]
    result = {
        "case_id": packet["case_id"],
        "kind": item["kind"],
        "group": item["group"],
        "packet": packet,
        "fixture_sha256": sha(item),
        "expected": expected,
        "effect_scope": "IN-MEMORY SIMULATED EFFECT ONLY",
    }
    try:
        one = invoke(argv, packet)
        two = invoke(argv, packet)
        result["response"] = one
        result["replay_response"] = two
        result["replay_equal"] = (one == two)
        # The examiner records only a local symbolic consequence request.
        effect = (
            [{"kind": "SIMULATED_COMMIT", "target": one["effect_request"]["target"]}]
            if one["decision"] == "EXECUTE" and one["effect_request"] is not None
            else []
        )
        result["simulated_effects"] = effect
        target = packet["case"]["authorized_target"]
        if expected == "EXECUTE":
            valid = one == {"decision": "EXECUTE", "effect_request": {"target": target}}
            valid = valid and effect == [{"kind": "SIMULATED_COMMIT", "target": target}]
        else:
            valid = one["decision"] in NONEXECUTE and one["effect_request"] is None and not effect
        result["passed"] = bool(valid and result["replay_equal"])
    except (ValueError, subprocess.TimeoutExpired, OSError) as exc:
        result["passed"] = False
        result["error"] = str(exc)[:180]
        result["replay_equal"] = False
        result["simulated_effects"] = []
    result["receipt_sha256"] = sha(result)
    return result

def run_matrix(argv, seed, rounds):
    suite = build_cases(seed, rounds)
    cases = [observe(argv, item) for item in suite]
    report = {
        "protocol": PROTOCOL, "version": "MATRIX-1.0",
        "examiner_scope": SCOPE,
        "seed": seed, "rounds": rounds,
        "fixture_manifest_sha256": sha(suite),
        "case_count": len(cases), "pass_count": sum(int(x["passed"]) for x in cases),
        "cases": cases,
        "warning": ("Replays are separate local adapter invocations. "
                    "This does not establish persistent-state custody, deployment route "
                    "closure, independent witnessing, or real-world non-formation."),
    }
    report["report_sha256"] = sha(report)
    return report

def main():
    parser = argparse.ArgumentParser(description="Synthetic, generated, BYO seam matrix; no native V.A. runtime")
    parser.add_argument("--seed", type=int, default=None, help="decimal seed for identical fixture reconstruction")
    parser.add_argument("--rounds", type=int, default=4, help="cohorts, 1-40; each yields nine transformations")
    parser.add_argument("--out", default=None, help="optional local JSON report destination")
    parser.add_argument("--adapter", nargs=argparse.REMAINDER, required=True,
                        help="trusted local executable command, for example python examiner/example_layer.py")
    opts = parser.parse_args()
    if not opts.adapter:
        parser.error("adapter command required after --adapter")
    seed = opts.seed if opts.seed is not None else secrets.randbits(64)
    try:
        result = run_matrix(opts.adapter, seed, opts.rounds)
    except ValueError as exc:
        parser.error(str(exc))
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if opts.out:
        Path(opts.out).write_text(encoded, encoding="utf-8")
    print(encoded)
    return 0 if result["pass_count"] == result["case_count"] else 1

if __name__ == "__main__":
    sys.exit(main())
