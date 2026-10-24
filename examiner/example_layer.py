#!/usr/bin/env python3
"""Toy public JSON seam only. Not V.A. and not a safety product."""
import json
import sys

packet = json.load(sys.stdin)
case = packet["case"]
allowed = (case["authority_active"] and case["evidence_current"]
           and case["attempted_target"] == case["authorized_target"])
result = {"case_id":packet["case_id"],"decision":"EXECUTE" if allowed else "REFUSE",
          "effect_request":{"target":case["attempted_target"]} if allowed else None}
print(json.dumps(result, separators=(",",":"),sort_keys=True))
