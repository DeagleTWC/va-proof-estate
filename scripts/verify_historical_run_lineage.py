#!/usr/bin/env python3
"""Offline data-only historical run records and revision checker. Never executes an archive."""
import argparse
import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, BadZipFile

DECISIONS=("EXECUTE", "REFUSE", "ESCALATE")
MAX_MEMBERS=30
MAX_BYTES=2_000_000

def require(ok, why):
    if not ok:
        raise ValueError(why)

def inspect_zip(p):
    p=Path(p)
    with ZipFile(p) as z:
        members=z.infolist()
        require(1 <= len(members) <= MAX_MEMBERS, "Unexpected number of archive objects")
        require(len(set(x.filename for x in members))==len(members), "Duplicate archive member")
        origins=set()
        contents={}
        total=0
        for info in members:
            name=info.filename
            path=PurePosixPath(name)
            require(not path.is_absolute() and ".." not in path.parts and
                    "\\" not in name and len(path.parts)>1, "Unsafe archive member path")
            require(info.flag_bits & 1 == 0, "Encrypted archive member refused")
            require(stat.S_IFMT(info.external_attr >> 16) != stat.S_IFLNK,
                    "Symlinked archive member refused")
            require(info.file_size <= MAX_BYTES, "Member too large")
            total += info.file_size
            require(total <= MAX_BYTES, "Archive expanded size over bound")
            origins.add(path.parts[0])
            if not info.is_dir():
                short="/".join(path.parts[1:])
                require(short not in contents, "Repeated path in archive")
                require(short.endswith((".json", ".md", ".txt")), "Unexpected member type")
                contents[short]=z.read(info)
        require(len(origins)==1, "More than one archive source root")
    return contents

def parsed(data, name):
    require(name in data, "Missing original source object: "+name)
    return json.loads(data[name].decode("utf-8"))

def inspect_record(path, capture, closeout):
    records=inspect_zip(path)
    data=parsed(records,capture)
    rows=data.get("cases")
    require(isinstance(rows,list) and len(rows)==3, "Incomplete three-case capture")
    require([r.get("case") for r in rows]==list(DECISIONS), "Outcome classes missing/duplicated")
    receipt_files=[name for name in records if "receipt_" in name and name.endswith(".json")]
    require(len(receipt_files)==3, "Three distinct original receipt records required")
    receipts=[json.loads(records[name]) for name in receipt_files]
    require(len(set(x.get("receipt_id") for x in receipts))==3,
            "Duplicate original receipt identifiers")
    requires_connected=(capture=="capture_completed.json")
    run_id=data.get("run_id")
    if requires_connected:
        require(isinstance(run_id,str) and run_id.strip(), "Connected run identity absent")
        require(data.get("filled_by") not in (None, ""), "Source author field missing")
    else:
        require(data.get("artifact_type")=="live_integration_capture_sheet_v1_completed",
                "Real integration source classification mismatch")
    original_report=parsed(records,closeout)
    if requires_connected:
        require(original_report.get("result")=="GO_WITH_CONSTRAINTS",
                "Bounded historical recorded outcome changed")
    else:
        require(original_report.get("go_no_go_next")=="GO_WITH_CONSTRAINTS",
                "Original integration closeout changed")
    latencies={}
    for row in rows:
        kind=row["case"]
        same=[r for r in receipts if r.get("receipt_id")==row.get("receipt_id")]
        require(len(same)==1, "Missing matching receipt for recorded case")
        rec=same[0]
        expected_commit=(kind=="EXECUTE")
        require(row.get("outcome")==kind and rec.get("decision")==kind,
                "Case outcome and original receipt disagree")
        require(type(row.get("commit_boundary_reached")) is bool and
                row["commit_boundary_reached"] == expected_commit,
                "Recorded protected commit violates bounded outcome")
        require(rec.get("commit_boundary")==("attending_signoff" if expected_commit else "not_reached"),
                "Original receipt commit boundary contradicts recorded case")
        require(rec.get("bindability",{}).get("commit_allowed") is expected_commit,
                "Receipt binding flag contradicts source boundary outcome")
        ms=row.get("latency_ms_observed")
        require(type(ms) is int and 0 < ms < 120_000 and
                rec.get("constraints",{}).get("latency_ms")==ms,
                "Source-record latency and receipt disagree")
        require(row.get("replay_result")=="held" and
                (not requires_connected or (row.get("chain_valid") is True and
                 rec.get("chain_valid") is True and rec.get("replay_result")=="held")),
                "Source claims replay/chain mismatch")
        require(isinstance(rec.get("receipt_sig"),str) and rec["receipt_sig"],
                "Archived unverified signature-label absent")
        # A textual 'sig_*' label is not a cryptographic signature check.
        latencies[kind]=ms
    return {
        "kind": "CONNECTED_ENVIRONMENT" if requires_connected else "INTEGRATION_SIMULATION",
        "runId": run_id if requires_connected else None,
        "outcomeClasses": list(DECISIONS),
        "caseCount": 3,
        "sourceOutcome": "GO_WITH_CONSTRAINTS",
        "originalArchiveSHA256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        "latencyReportedMs": latencies,
        "originalStoredReceiptsCrossChecked": True,
        "receiptCryptographicSignaturesVerified": False,
        "receiptChainRecomputed": False,
        "replayIndependentlyExecuted": False,
        "actualExternalEffectInstrumented": False,
        "qualifiedIndependentHumanWitnessAuthenticated": False,
    }

def compare_records(integration, connected_v1, connected_v2, readiness):
    intg=inspect_record(integration,"live_integration_capture_completed.json",
                        "live_integration_closeout_completed.json")
    one=inspect_record(connected_v1,"capture_completed.json","summary_completed.json")
    two=inspect_record(connected_v2,"capture_completed.json","summary_completed.json")
    require(one["runId"] == two["runId"], "Different connected runs; no same-run revision comparison possible")
    require(one["originalArchiveSHA256"] != two["originalArchiveSHA256"],
            "Connected versions must preserve distinct original bytes")
    # Revisions must not be counted as independent runs, even when their latencies differ.
    differences={kind:{"v1":one["latencyReportedMs"][kind], "v2":two["latencyReportedMs"][kind]}
                 for kind in DECISIONS if one["latencyReportedMs"][kind]!=two["latencyReportedMs"][kind]}
    require(differences, "Version differences not present: do not falsely report revised latency")
    z=inspect_zip(readiness)
    latency=parsed(z,"latency_gate.json")
    overview=parsed(z,"overview.json")
    require(overview.get("status")=="ready_for_lock" and
            overview.get("current_decision")=="GO_WITH_CONSTRAINTS" and
            overview.get("based_on")=="connected_environment_executed_v2",
            "Readiness does not actually bind to connected v2")
    require(latency.get("measured_ms")==two["latencyReportedMs"],
            "Later readiness numbers disagree with v2 source")
    return {
        "schema":"va-private-historical-run-source-reconciliation/1.0",
        "classification":"PRIVATE_LOCAL_SOURCE_AUDIT_NOT_FOR_PUBLIC_UPLOAD",
        "publicSummaryClass":"ORIGINAL_RECORDED_CASE_AND_RECEIPT_CROSSCHECK",
        "sourceArchiveCount":4,
        "recordedCaseFilesCountAcrossThreeArchives":9,
        "distinctConnectedRunIdentifiers":1,
        "v1AndV2AreSeparateIndependentRuns":False,
        "integrationSourceSaysSimulation":True,
        "v1ToV2RecordedLatencyRevisions":differences,
        "readinessConsistentWithConnectedV2":True,
        "sourceRecords":[intg,one,two],
        "externalOriginalEffectsVerified":False,
        "humanWitnessIndependenceVerified":False,
        "archivedSignaturesCryptographicallyVerified":False,
        "signedOriginalFreezeAndOriginalReleaseRightsVerified":False,
        "note":"The source archive calls the first integration simulation. The v1/v2 connected-environment versions carry the same run identifier and recorded latency changes. Stored receipt strings/chain flags and 'replay held' reports are not independent cryptographic replay, external effect observation, hospital deployment, or qualified third-party evidence."
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--integration",required=True)
    p.add_argument("--connected-v1",required=True)
    p.add_argument("--connected-v2",required=True)
    p.add_argument("--readiness-v2",required=True)
    p.add_argument("--out",help="PRIVATE result path outside original input directories")
    a=p.parse_args()
    try:
        data=compare_records(a.integration,a.connected_v1,a.connected_v2,a.readiness_v2)
        if a.out:
            targets=[Path(getattr(a,key.replace("-","_"))).absolute().resolve() for key in
                     ("integration","connected-v1","connected-v2","readiness-v2")]
            output=Path(a.out).absolute()
            require(not output.is_symlink() and not output.exists(), "Never overwrite previous private audit")
            require(output.resolve() not in targets, "Result cannot overwrite input originals")
            fd=os.open(str(output),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,"w",encoding="utf-8") as fp:
                json.dump(data,fp,indent=2)
                fp.write("\n")
        print("PASS: recorded three-class source and receipt consistency across historical archives")
        print("SAME CONNECTED RUN ID: v1/v2 are revisions, NOT two independent runs")
        print("PASS: v2 source latency agrees with separately archived readiness source")
        print("Not established: external effect, independently verified signatures, native V12, third-party witnesses")
    except (ValueError,KeyError,TypeError,BadZipFile,OSError,UnicodeError) as exc:
        p.exit(2,"REFUSED: "+str(exc)+"\n")

if __name__=="__main__":
    main()
