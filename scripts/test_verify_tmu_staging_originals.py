#!/usr/bin/env python3
"""Synthetic private TMU-source packet verification regressions.

No original archived TMU partner source is embedded in these fixtures.
"""
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from verify_tmu_staging_originals import inspect, NAMES, GATES

def sha(x):return hashlib.sha256(x).hexdigest()

def template():
    ids=("synthetic-execute-001","synthetic-refuse-001")
    hashes=("sha256:"+"a"*64,"sha256:"+"b"*64)
    bounds=("SYN-BIND-EXEC","SYN-BIND-REFUSE")
    rows=[
     {"receipt_id":ids[0],"decision_class":"EXECUTE","outcome":"EXECUTE",
      "state_hash":hashes[0],"commit_boundary":bounds[0],
      "runtime_identity":"synthetic-example-runtime","contract_identity":"TMU_Governed_Runtime_v8.3",
      "replayable":True},
     {"receipt_id":ids[1],"decision_class":"REFUSE","outcome":"REFUSE",
      "state_hash":hashes[1],"commit_boundary":bounds[1],
      "runtime_identity":"synthetic-example-runtime","contract_identity":"TMU_Governed_Runtime_v8.3",
      "replayable":True}
    ]
    metadata={"pack_id":"TMU_One_Path_Proof_Pack","pack_version":"v1.2_FULL_ENV",
              "environment":"staging_docker","runtime_identity":"synthetic-example-runtime",
              "gates":list(GATES),"gate_status_summary":dict.fromkeys(GATES,"PASS")}
    head=lambda key:"GATE: "+key+"\nSTATUS: PASS\nPACK_VERSION: v1.2_FULL_ENV\n"
    smoke=head("SMOKE")+"\n"+("\n".join(
        f"receipt_id: {row['receipt_id']}\nstate_hash: {row['state_hash']}\ncommit_boundary: {row['commit_boundary']}"
        for row in rows))+"\n"
    drift=head("RECEIPT_DRIFT")+"\nTotal receipts evaluated: 2\n"+ "\n".join(row["receipt_id"] for row in rows)
    replay=head("REPLAY")+"\n--- EXECUTE REPLAY ---\noriginal_decision_class: EXECUTE\nreplayed_decision_class: EXECUTE\n--- REFUSE REPLAY ---\noriginal_decision_class: REFUSE\nreplayed_decision_class: REFUSE\n--- NOTES ---\n"
    spans=head("SPAN_COMMIT_CONFORMANCE")+"\n--- EXECUTE SPAN ---\ntotal_span_ms: 50\ncommit_subspan_ms: 10\nevaluation_subspan_ms: 30\nseal_subspan_ms: 10\n--- REFUSE SPAN ---\ntotal_span_ms: 30\ncommit_subspan_ms: 5\nevaluation_subspan_ms: 20\nseal_subspan_ms: 5\n"
    f={
    "run_metadata.json":json.dumps(metadata).encode(),
    "smoke_output.txt":smoke.encode(),
    "conformance_output.txt":head("CONFORMANCE").encode(),
    "receipt_drift_output.txt":drift.encode(),
    "replay_gate_output.txt":replay.encode(),
    "span_commit_conformance_output.txt":spans.encode(),
    "receipt_bundle_20260413.ndjson":("\n".join(json.dumps(v) for v in rows)+"\n").encode()
    }
    return f

def fail(files,fn,reason):
    with tempfile.TemporaryDirectory(prefix="SYN_TMU_UNIT_") as tmp:
        root=Path(tmp)
        x=dict(files)
        fn(x)
        for name,raw in x.items():(root/name).write_bytes(raw)
        manifest={"schema":"va-private-tmu-staging-source-hash-manifest/1.0",
                 "classification":"PRIVATE_ORIGINAL_CUSTODY",
                 "historicalFreezeAuthenticated":False,
                 "files":{n:sha(raw) for n,raw in x.items()}}
        try:inspect(root,manifest)
        except (ValueError,TypeError,KeyError,UnicodeError):return
        raise AssertionError("False original source standing admitted: "+reason)

def main():
    original=template()
    with tempfile.TemporaryDirectory(prefix="SYN_TMU_POSITIVE_") as tmp:
        root=Path(tmp)
        for n,b in original.items():(root/n).write_bytes(b)
        d={"schema":"va-private-tmu-staging-source-hash-manifest/1.0",
           "classification":"PRIVATE_ORIGINAL_CUSTODY",
           "historicalFreezeAuthenticated":False,
           "files":{n:sha(data) for n,data in original.items()}}
        ok=inspect(root,d)
        assert ok["sourceFiles"]==7 and ok["originalSavedReceipts"]==2
        assert ok["originalArchivedCodeExecuted"] is False
        assert ok["actualLiveTMUDeploymentAuthenticated"] is False
        d["files"]["run_metadata.json"]="0"*64
        try:inspect(root,d)
        except ValueError:pass
        else:raise AssertionError("Mismatched original SHA accepted")
    def modjson(src,func):
        x=json.loads(src);func(x);return json.dumps(x).encode()
    edits=[
        ("wrong five-gate claimed status",lambda f:f.__setitem__("run_metadata.json",modjson(f["run_metadata.json"],lambda d:d["gate_status_summary"].update(smoke="FAIL")))),
        ("wrong staging source label",lambda f:f.__setitem__("run_metadata.json",modjson(f["run_metadata.json"],lambda d:d.update(environment="production")))),
        ("receipt class changed",lambda f:f.__setitem__("receipt_bundle_20260413.ndjson",f["receipt_bundle_20260413.ndjson"].replace(b'"REFUSE"',b'"EXECUTE"'))),
        ("receipt source identifier swapped",lambda f:f.__setitem__("receipt_bundle_20260413.ndjson",f["receipt_bundle_20260413.ndjson"].replace(b"synthetic-refuse-001",b"another-receipt"))),
        ("different commit condition",lambda f:f.__setitem__("receipt_bundle_20260413.ndjson",f["receipt_bundle_20260413.ndjson"].replace(b"SYN-BIND-REFUSE",b"SYN-OTHER"))),
        ("one saved original receipt dropped",lambda f:f.__setitem__("receipt_bundle_20260413.ndjson",f["receipt_bundle_20260413.ndjson"].splitlines(keepends=True)[0])),
        ("receipt source not replayable",lambda f:f.__setitem__("receipt_bundle_20260413.ndjson",f["receipt_bundle_20260413.ndjson"].replace(b'true',b'false'))),
        ("replay class contradicts receipt",lambda f:f.__setitem__("replay_gate_output.txt",f["replay_gate_output.txt"].replace(b"replayed_decision_class: REFUSE",b"replayed_decision_class: EXECUTE"))),
        ("gate FAIL",lambda f:f.__setitem__("smoke_output.txt",f["smoke_output.txt"].replace(b"STATUS: PASS",b"STATUS: FAIL"))),
        ("five-gate log absent",lambda f:f.pop("conformance_output.txt")),
        ("timing not arithmetically reconciled",lambda f:f.__setitem__("span_commit_conformance_output.txt",f["span_commit_conformance_output.txt"].replace(b"total_span_ms: 50",b"total_span_ms: 51"))),
        ("contract identity incorrect",lambda f:f.__setitem__("receipt_bundle_20260413.ndjson",f["receipt_bundle_20260413.ndjson"].replace(b"TMU_Governed_Runtime_v8.3",b"another-contract"))),
        ("original runtime label differs",lambda f:f.__setitem__("receipt_bundle_20260413.ndjson",f["receipt_bundle_20260413.ndjson"].replace(b"synthetic-example-runtime",b"another-runtime"))),
        ("drift source count missing",lambda f:f.__setitem__("receipt_drift_output.txt",f["receipt_drift_output.txt"].replace(b"Total receipts evaluated: 2",b"Total receipts evaluated: 0")))
    ]
    for desc,fn in edits:fail(original,fn,desc)
    print(f"PASS: {len(edits)+1} original-file hash, source role, receipt/replay and negative control tamper cases")
    print("PASS: tests use fabricated fixtures only; no actual customer outcome or independent witness implied")

if __name__=="__main__":main()
