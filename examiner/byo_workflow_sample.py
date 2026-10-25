#!/usr/bin/env python3
"""Generate synthetic BYO workflow evidence packet for local training only."""
import argparse
import hashlib
import json
import os
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def add(root, relative, data):
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8")
    with target.open("xb") as f:
        f.write(raw)
    return {"path": relative, "sha256": sha(raw)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", required=True, help="New, nonexistent folder for synthetic example")
    a = p.parse_args()
    root = Path(a.out).absolute()
    if root.exists():
        p.exit(2, "REFUSED: example directory already exists; do not overwrite\n")
    root.mkdir(parents=True)
    workflow_id = "SYNTHETIC-DEMO-ONLY"
    workflow = add(root, "workflow.json", {
        "workflowId": workflow_id,
        "protectedConsequence": "Dummy local counter increment; no real-world effect",
        "declaredRoutes": ["main-route", "alternate-route"],
        "note": "This is a deliberately synthetic training sample, not a customer pilot."
    })
    sources = []
    saved = {}
    for kind, cid, decision, effect, condition, route, extra in [
        ("ALLOW", "allowed-case", "EXECUTE", True, "normal", "main-route", {}),
        ("REFUSE", "denied-case", "REFUSE", False, "invalid-authority", "alternate-route", {}),
        ("CHANGED", "changed-case", "REFUSE", False, "revoked", "main-route", {"changedFrom": "allowed-case"}),
        ("REPLAY", "replay-case", "EXECUTE", True, "normal", "main-route", {"replayOf": "allowed-case"})
    ]:
        rec = add(root, f"evidence/{cid}-receipt.json", {
            "schema": "deagle-byo-boundary-receipt/1.0",
            "workflowId": workflow_id, "caseId": cid, "decision": decision,
            "sourceType": "SYNTHETIC_NOT_REAL_EVIDENCE"
        })
        obs = add(root, f"evidence/{cid}-observer.json", {
            "schema": "deagle-byo-effect-observer/1.0",
            "workflowId": workflow_id, "caseId": cid,
            "route": route, "effectObserved": effect, "method": "SIMULATED_EFFECT",
            "observationDescription": "Dummy in-memory count, not independently instrumented."
        })
        extra = dict(extra)
        if kind == "REPLAY":
            extra["originalReceiptSHA256"] = saved["allowed-case"]["receipt"]["sha256"]
        event = {
            "schema": "deagle-byo-observation/1.0",
            "workflowId": workflow_id, "caseId": cid, "kind": kind,
            "candidateId": "test-candidate-01",
            "conditionDigest": sha(condition.encode("utf-8")),
            "route": route, "decision": decision, "effectObserved": effect,
            "measurement": obs, "receipt": rec, **extra
        }
        saved[cid] = event
        sources.append(add(root, f"cases/{cid}.json", event))
    manifest = {
        "schema": "deagle-byo-workflow-evidence/1.0",
        "packetCustody": "PARTICIPANT_OWNED_LOCAL",
        "releaseAuthorized": False, "externalEffectStanding": "UNVERIFIED",
        "workflowId": workflow_id, "workflow": workflow, "cases": sources,
        "warning": "Entirely synthetic reference. Passing only shows local record consistency."
    }
    add(root, "manifest.json", manifest)
    print("CREATED SYNTHETIC DATA-ONLY PACKET:", root)
    print("Run: python examiner/byo_workflow_evidence.py --packet \"" + str(root) + "\"")
    print("Never publish or portray this as actual third-party or native V.A. evidence.")


if __name__ == "__main__":
    main()
