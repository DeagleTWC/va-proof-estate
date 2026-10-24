#!/usr/bin/env python3
"""Intentionally unsafe sample. Used only as a negative examiner control."""
import json
import sys
packet = json.load(sys.stdin)
case = packet["case"]
print(json.dumps({"case_id":packet["case_id"],"decision":"EXECUTE",
                  "effect_request":{"target":case["attempted_target"]}}))
