#!/usr/bin/env python3
"""Synthetic BYO workflow evidence proof of fail-closed behavior. Never a live-world pilot."""
import copy
import hashlib
import json
import tempfile
from pathlib import Path

from byo_workflow_evidence import run_packet


def digest(b):
    return hashlib.sha256(b).hexdigest()


def save(root, path, content):
    raw = (json.dumps(content, sort_keys=True, indent=2) + "\n").encode("utf-8")
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    return {"path": path, "sha256": digest(raw)}


def reject(root, name):
    try:
        run_packet(root)
    except (ValueError, KeyError, TypeError, OSError):
        return
    raise AssertionError("Validator wrongly admitted: " + name)


def main():
    with tempfile.TemporaryDirectory(prefix="deagle-byo-synthetic-") as tmp:
        root = Path(tmp)
        workflow = save(root, "workflow.json",
                        {"workflowId": "TEST-OWN-WORKFLOW",
                         "protectedConsequence": "Synthetic local counter",
                         "declaredRoutes": ["route-A", "route-B"]})
        cases = []
        def make(cid, kind, decision, effect, route, condition, extra=None):
            receipt = save(root, f"evidence/{cid}-receipt.json",
                           {"schema": "deagle-byo-boundary-receipt/1.0",
                            "caseId": cid, "workflowId": "TEST-OWN-WORKFLOW", "decision": decision})
            observer = save(root, f"evidence/{cid}-observer.json",
                            {"schema": "deagle-byo-effect-observer/1.0",
                             "caseId": cid, "workflowId": "TEST-OWN-WORKFLOW",
                             "effectObserved": effect, "route": route,
                             "method": "SIMULATED_EFFECT", "observationDescription": "Synthetic locally counted effects"})
            payload = {"schema": "deagle-byo-observation/1.0",
                       "caseId": cid, "kind": kind, "workflowId": "TEST-OWN-WORKFLOW",
                       "candidateId": "candidate-1", "route": route,
                       "conditionDigest": digest(condition.encode()),
                       "decision": decision, "effectObserved": effect,
                       "measurement": observer, "receipt": receipt}
            if extra:
                payload.update(extra)
            c = save(root, f"cases/{cid}.json", payload)
            cases.append(c)
            return payload
        positive = make("positive-1", "ALLOW", "EXECUTE", True, "route-A", "valid")
        refuse = make("refusal-1", "REFUSE", "REFUSE", False, "route-B", "no authority")
        changed = make("changed-1", "CHANGED", "REFUSE", False, "route-A", "revoked",
                       {"changedFrom": "positive-1"})
        replay = make("replay-1", "REPLAY", "EXECUTE", True, "route-A", "valid",
                      {"replayOf": "positive-1", "originalReceiptSHA256": positive["receipt"]["sha256"]})
        manifest = {
            "schema": "deagle-byo-workflow-evidence/1.0", "packetCustody": "PARTICIPANT_OWNED_LOCAL",
            "releaseAuthorized": False, "externalEffectStanding": "UNVERIFIED",
            "workflowId": "TEST-OWN-WORKFLOW", "workflow": workflow, "cases": cases}
        def put(obj):
            (root / "manifest.json").write_text(json.dumps(obj, indent=2), encoding="utf-8")
        put(manifest)
        result = run_packet(root)
        assert result["result"] == "LOCAL_DATA_CONSISTENCY_ONLY"
        assert result["casesStructurallyMatched"] == 4
        assert result["allDeclaredRoutesMeasured"] is True
        assert result["effectRealityVerifiedByThisTool"] is False
        assert result["publicationAuthorized"] is False
        tests = 0
        def bad_payload(cid, mutator, label):
            nonlocal tests
            original = root / "cases" / (cid+".json")
            raw = original.read_bytes()
            doc = json.loads(raw)
            mutator(doc)
            new = save(root, f"cases/{cid}.json", doc)
            patched = copy.deepcopy(manifest)
            for carrier in patched["cases"]:
                if carrier["path"] == f"cases/{cid}.json":
                    carrier.update(new)
            put(patched)
            reject(root, label)
            original.write_bytes(raw)
            put(manifest)
            tests += 1
        bad_payload("refusal-1", lambda d:d.update(effectObserved=True), "negative observation contradicted")
        bad_payload("refusal-1", lambda d:d.update(decision="EXECUTE"), "refusal executability")
        bad_payload("changed-1", lambda d:d.update(conditionDigest=positive["conditionDigest"]), "unchanged conditions")
        bad_payload("changed-1", lambda d:d.update(changedFrom="missing"), "changed source absent")
        bad_payload("replay-1", lambda d:d.update(originalReceiptSHA256="0"*64), "false preserved receipt")
        bad_payload("replay-1", lambda d:d.update(candidateId="different"), "replay different candidate")
        bad_payload("positive-1", lambda d:d.update(route="secret-route"), "undeclared consequence route")
        tampered=copy.deepcopy(manifest)
        tampered["cases"][0]["sha256"]="0"*64
        put(tampered);reject(root,"altered case hash");put(manifest);tests+=1
        missing=copy.deepcopy(manifest)
        missing["cases"]=[c for c in missing["cases"] if c["path"]!="cases/refusal-1.json"]
        put(missing);reject(root,"no negative control");put(manifest);tests+=1
        escaped=copy.deepcopy(manifest)
        escaped["workflow"]={"path":"../secret.json","sha256":workflow["sha256"]}
        put(escaped);reject(root,"path traversal");put(manifest);tests+=1
        false_release=copy.deepcopy(manifest)
        false_release["releaseAuthorized"]=True
        put(false_release);reject(root,"false release switch");put(manifest);tests+=1
        measurement=root/"evidence/refusal-1-observer.json"
        original_measurement=measurement.read_bytes()
        measurement.write_bytes(b"{}")
        reject(root,"original measurement tampered")
        measurement.write_bytes(original_measurement)
        tests+=1
        outside=root/"different-file.json"
        outside.symlink_to(root/"workflow.json")
        symlink=copy.deepcopy(manifest)
        symlink["workflow"]={"path":"different-file.json","sha256":workflow["sha256"]}
        put(symlink);reject(root,"symlink source");put(manifest);tests+=1
        assert run_packet(root)["casesStructurallyMatched"]==4
        print(f"PASS: 4 synthetic data-only BYO workflow cases and {tests} fail-closed negative controls")
        print("PASS: no code execution, no claim of authentic independent or native V.A. evidence")


if __name__ == "__main__":
    main()
