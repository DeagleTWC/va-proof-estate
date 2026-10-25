#!/usr/bin/env python3
"""Entirely synthetic historical-run packet tests. Never asserts actual pilot standing."""
import json
import tempfile
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from verify_historical_run_lineage import compare_records

CASES=("EXECUTE","REFUSE","ESCALATE")

def pack(path, root, files):
    with ZipFile(path,"w",ZIP_DEFLATED) as z:
        for name,item in files.items():
            z.writestr(root+"/"+name,json.dumps(item,sort_keys=True)+"\n")

def synthetic_records(connected,latency,run_id="SYNTHETIC_CASE_RUN_1"):
    cap=[]
    source={}
    for decision in CASES:
        canbind=(decision=="EXECUTE")
        cid="synthetic-receipt-"+decision.lower()
        rec={
            "receipt_id":cid,"decision":decision,
            "commit_boundary":"attending_signoff" if canbind else "not_reached",
            "bindability":{"commit_allowed":canbind},
            "constraints":{"latency_ms":latency[decision]},
            "receipt_sig":"NOT_A_SIGNATURE_syn_"+decision
        }
        if connected:
            rec.update(chain_valid=True,replay_result="held")
        source[decision.lower()+"_receipt_connected.json" if connected
               else decision.lower()+"_receipt_live.json"]=rec
        item={"case":decision,"outcome":decision,"receipt_id":cid,
              "latency_ms_observed":latency[decision],"commit_boundary_reached":canbind,
              "replay_result":"held"}
        if connected:
            item["chain_valid"]=True
        cap.append(item)
    if connected:
        source["capture_completed.json"]={"cases":cap,"run_id":run_id,"filled_by":"synthetic-examiner"}
        source["summary_completed.json"]={"result":"GO_WITH_CONSTRAINTS"}
    else:
        source["live_integration_capture_completed.json"]={
            "artifact_type":"live_integration_capture_sheet_v1_completed","cases":cap}
        source["live_integration_closeout_completed.json"]={"go_no_go_next":"GO_WITH_CONSTRAINTS"}
    return source

def expect_refusal(paths,label):
    try:
        compare_records(*paths)
    except (ValueError,KeyError,TypeError):
        return
    raise AssertionError("Fail-closed verifier admitted corrupted record: "+label)

def main():
    with tempfile.TemporaryDirectory(prefix="synthetic-historical-run-") as d:
        root=Path(d)
        paths=[root/x for x in ("integration.zip","connected-v1.zip","connected-v2.zip","readiness-v2.zip")]
        i=synthetic_records(False,dict(EXECUTE=410,REFUSE=255,ESCALATE=310))
        v1=synthetic_records(True,dict(EXECUTE=341,REFUSE=216,ESCALATE=287))
        v2=synthetic_records(True,dict(EXECUTE=312,REFUSE=198,ESCALATE=254))
        ready={"overview.json":{"status":"ready_for_lock","current_decision":"GO_WITH_CONSTRAINTS",
                                "based_on":"connected_environment_executed_v2"},
               "latency_gate.json":{"measured_ms":dict(EXECUTE=312,REFUSE=198,ESCALATE=254)}}
        def write_all():
            for p,tag,source in zip(paths,["synthetic-integration","synthetic-v1","synthetic-v2","synthetic-ready"],
                                    [i,v1,v2,ready]):
                pack(p,tag,source)
        write_all()
        got=compare_records(*paths)
        assert got["distinctConnectedRunIdentifiers"]==1
        assert got["v1AndV2AreSeparateIndependentRuns"] is False
        assert len(got["v1ToV2RecordedLatencyRevisions"])==3
        assert got["externalOriginalEffectsVerified"] is False
        assert got["humanWitnessIndependenceVerified"] is False
        assert got["archivedSignaturesCryptographicallyVerified"] is False
        tests=[
            ("forge bound REFUSE",v2,"refuse_receipt_connected.json",lambda x:x["bindability"].update(commit_allowed=True)),
            ("receipt mismatch",v2,"execute_receipt_connected.json",lambda x:x.update(decision="REFUSE")),
            ("replay flag overwritten",v2,"escalate_receipt_connected.json",lambda x:x.update(replay_result="failed")),
            ("wrong source latency",v2,"refuse_receipt_connected.json",lambda x:x["constraints"].update(latency_ms=999)),
            ("bad receipt ID",v2,"capture_completed.json",lambda x:x["cases"][0].update(receipt_id="unknown")),
            ("non-unique connected run",v2,"capture_completed.json",lambda x:x.update(run_id="NEW_RUN_ID")),
            ("v2 readiness divergence",ready,"latency_gate.json",lambda x:x["measured_ms"].update(EXECUTE=999)),
            ("closeout not constrained",v1,"summary_completed.json",lambda x:x.update(result="GO")),
            ("no REFUSE source",i,"refuse_receipt_live.json",lambda x:x.update(receipt_id="changed")),
            ("wrong original path",v1,"capture_completed.json",lambda x:x["cases"][0].update(commit_boundary_reached=False)),
        ]
        for label,where,item,mutate in tests:
            before=json.loads(json.dumps(where[item]))
            mutate(where[item]);write_all();expect_refusal(paths,label)
            where[item]=before
        write_all()
        assert len(compare_records(*paths)["sourceRecords"])==3
        print(f"PASS: synthetic three-case archived integration/connected v1/v2 and {len(tests)} tamper refusals")
        print("PASS: same connected run ID cannot become a second independent pilot")
        print("PASS: no real-world effect, native V12, cryptographic chain or witness standing assigned")

if __name__=="__main__":
    main()
