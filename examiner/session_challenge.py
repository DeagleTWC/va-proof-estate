#!/usr/bin/env python3
"""Public stateful BYO seam: local, synthetic, no V.A. runtime or physical effect."""
import argparse
import hashlib
import json
import random
import secrets
import subprocess
import sys
from pathlib import Path

VERSION = "DEAGLE-BYO-SESSION-1"
SCOPE = "PERSISTENT LOCAL SYNTHETIC ADAPTER TEST; NO NATIVE V.A., EXTERNAL EFFECT, OR PHYSICAL WITNESS"

def encode(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def digest(obj):
    return hashlib.sha256(encode(obj).encode("utf-8")).hexdigest()

def generate(seed, rounds):
    if not 1 <= rounds <= 20:
        raise ValueError("rounds must be 1..20")
    rng = random.Random(seed)
    blocks = []
    event_number = 0
    def event(op, expected, **data):
        nonlocal event_number
        event_number += 1
        return {"event_id": "EV-%05d" % event_number, "operation": op, **data}, expected
    for index in range(rounds):
        cohort = []
        target = "resource-%016x" % rng.getrandbits(64)
        wrong = "resource-%016x" % rng.getrandbits(64)
        while wrong == target:
            wrong = "resource-%016x" % rng.getrandbits(64)
        tokens = ["cap-%016x" % rng.getrandbits(64) for _ in range(9)]
        def start(i, routes=("primary", "secondary"), active=True, current=True, capacity=True):
            return event("START", "ACK", token=tokens[i], authorized_target=target,
                         allowed_routes=list(routes), authority_active=active,
                         evidence_current=current, capacity_ok=capacity)
        def attempt(i, expected, route="primary", attempt_target=None, token_override=None):
            return event("TRY", expected, token=token_override if token_override is not None else tokens[i],
                         attempted_target=target if attempt_target is None else attempt_target, route=route)
        def change(i, op):
            return event(op, "ACK", token=tokens[i])
        # One legal effect followed by identical-ticket replay.
        cohort += [start(0), attempt(0, "EXECUTE"), attempt(0, "REFUSE")]
        # An attempted substitution may not become authorized by a valid ticket.
        cohort += [start(1), attempt(1, "REFUSE", attempt_target=wrong),
                   attempt(1, "EXECUTE"), attempt(1, "REFUSE")]
        # Revoke and stale conditions while a ticket is still unspent.
        cohort += [start(2), change(2, "REVOKE"), attempt(2, "REFUSE")]
        cohort += [start(3), change(3, "STALE"), attempt(3, "REFUSE")]
        # A denied alternate route must not consume a valid ticket.
        cohort += [start(4, routes=("primary",)), attempt(4, "REFUSE", route="secondary"),
                   attempt(4, "EXECUTE"), attempt(4, "REFUSE")]
        # Expiry and capacity failure.
        cohort += [start(5), change(5, "EXPIRE"), attempt(5, "REFUSE")]
        cohort += [start(6, capacity=False), attempt(6, "REFUSE")]
        # Cross-ticket injection and a valid later target.
        cohort += [start(7), attempt(7, "REFUSE", token_override=tokens[0]),
                   attempt(7, "EXECUTE", route="secondary")]
        # Missing authority is not made valid by target/route matching.
        cohort += [start(8, active=False), attempt(8, "REFUSE")]
        blocks.append(cohort)
    rng.shuffle(blocks)
    sequence = []
    # IDs are unique, but block shuffle must not interfere with individual ordering.
    for block in blocks:
        sequence.extend({"packet": {"protocol": VERSION, **packet}, "expected": expectation}
                        for packet, expectation in block)
    return sequence

def run(argv, seed, rounds):
    suite = generate(seed, rounds)
    stdin = "".join(encode(i["packet"]) + "\n" for i in suite)
    try:
        proc = subprocess.run(argv, input=stdin, text=True, capture_output=True,
                              timeout=20, check=False)
        if proc.returncode:
            raise ValueError("adapter failed with exit %d" % proc.returncode)
        lines = proc.stdout.splitlines()
        if len(lines) != len(suite):
            raise ValueError("adapter returned %d lines for %d packets" % (len(lines), len(suite)))
        outputs = [json.loads(line) for line in lines]
    except (ValueError, OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        return {"protocol": VERSION, "scope": SCOPE, "seed": seed, "rounds": rounds,
                "fixture_sha256": digest(suite), "event_count": len(suite),
                "pass_count": 0, "error": str(exc)[:240], "observations": []}
    observations = []
    for sample, output in zip(suite, outputs):
        packet = sample["packet"]
        expect = sample["expected"]
        base = {"event_id": packet["event_id"], "decision": expect, "effect_request": None}
        if expect == "EXECUTE":
            base["effect_request"] = {"target": packet["attempted_target"]}
        ok = type(output) is dict and output == base
        # Simulated consequence belongs to the examiner's in-memory representation only.
        effect = ({"kind": "SIMULATED_COMMIT", "target": output["effect_request"]["target"]}
                  if type(output) is dict and output.get("decision") == "EXECUTE"
                  and type(output.get("effect_request")) is dict
                  and type(output["effect_request"].get("target")) is str
                  else None)
        entry = {"event_id": packet["event_id"], "packet_sha256": digest(sample),
                 "expected": expect, "observed": output, "simulated_effect": effect,
                 "passed": ok, "effect_scope": "IN-MEMORY ONLY"}
        entry["receipt_sha256"] = digest(entry)
        observations.append(entry)
    report = {"protocol": VERSION, "scope": SCOPE, "seed": seed, "rounds": rounds,
              "fixture_sha256": digest(suite), "event_count": len(suite),
              "pass_count": sum(int(x["passed"]) for x in observations),
              "observations": observations,
              "warning": "Same-process adapter responses only; not real effect custody, route closure, independent verification or native V.A."}
    report["report_sha256"] = digest(report)
    return report

def main():
    parser = argparse.ArgumentParser(description="BYO persistent-session examiner; synthetic only")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--rounds", type=int, default=2)
    parser.add_argument("--out", default=None)
    parser.add_argument("--adapter", nargs=argparse.REMAINDER, required=True)
    args = parser.parse_args()
    if not args.adapter:
        parser.error("provide trusted local adapter command after --adapter")
    seed = args.seed if args.seed is not None else secrets.randbits(64)
    try:
        report = run(args.adapter, seed, args.rounds)
    except ValueError as exc:
        parser.error(str(exc))
    body = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(body, encoding="utf8")
    print(body)
    return 0 if "error" not in report and report["pass_count"] == report["event_count"] else 1

if __name__ == "__main__":
    sys.exit(main())
