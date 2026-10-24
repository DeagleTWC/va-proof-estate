#!/usr/bin/env python3
"""Minimal teaching reference for the public JSONL test seam. NOT native V.A."""
import json
import sys

grants = {}
for line in sys.stdin:
    try:
        p = json.loads(line)
        op = p["operation"]
        eid = p["event_id"]
        decision = "REFUSE"
        effect = None
        if p.get("protocol") == "DEAGLE-BYO-SESSION-1":
            token = p.get("token")
            if op == "START":
                grants[token] = {
                    "target": p["authorized_target"],
                    "routes": p["allowed_routes"],
                    "active": p["authority_active"],
                    "current": p["evidence_current"],
                    "capacity": p["capacity_ok"],
                    "expired": False,
                    "used": False,
                }
                decision = "ACK"
            elif op in {"REVOKE", "STALE", "EXPIRE"}:
                if token in grants:
                    change = {"REVOKE":"active", "STALE":"current", "EXPIRE":"expired"}[op]
                    grants[token][change] = (change == "expired")
                    decision = "ACK"
            elif op == "TRY":
                g = grants.get(token)
                if g and not g["used"] and g["active"] and g["current"] and g["capacity"] and not g["expired"] and p["attempted_target"] == g["target"] and p["route"] in g["routes"]:
                    decision = "EXECUTE"
                    effect = {"target": p["attempted_target"]}
                    g["used"] = True
        print(json.dumps({"event_id": eid, "decision": decision, "effect_request": effect},
                         sort_keys=True, separators=(",", ":")), flush=True)
    except (KeyError, ValueError, TypeError):
        print(json.dumps({"event_id": "ERROR", "decision": "REFUSE", "effect_request": None}), flush=True)
