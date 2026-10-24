#!/usr/bin/env python3
"""Intentionally broken example: replies EXECUTE to every attempt. Not a real system."""
import json
import sys

for line in sys.stdin:
    p = json.loads(line)
    if p["operation"] == "TRY":
        decision, effect = "EXECUTE", {"target": p["attempted_target"]}
    else:
        decision, effect = "ACK", None
    print(json.dumps({"event_id": p["event_id"], "decision": decision, "effect_request": effect}))
