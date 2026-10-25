#!/usr/bin/env python3
"""Audit seven ORIGINAL private TMU-referenced staging evidence attachments.

Data-only: never runs preserved code, never publishes original receipt payloads,
and never authenticates a customer deployment, effect sensor or human examiner.
The manifest must carry separately recorded exact source-file digests.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

NAMES=("run_metadata.json","smoke_output.txt","conformance_output.txt",
       "receipt_drift_output.txt","replay_gate_output.txt",
       "span_commit_conformance_output.txt","receipt_bundle_20260413.ndjson")
GATES={
    "smoke":"smoke_output.txt",
    "conformance":"conformance_output.txt",
    "receipt_drift":"receipt_drift_output.txt",
    "replay":"replay_gate_output.txt",
    "span_commit_conformance":"span_commit_conformance_output.txt"
}
HEX=re.compile(r"^[0-9a-f]{64}$")
MAX_BYTES=100_000

def require(ok,why):
    if not ok:raise ValueError(why)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def original_file(root,name):
    p=root/name
    require(p.is_file() and not p.is_symlink(),"Original source missing or symlinked: "+name)
    before=p.stat()
    require(0<before.st_size<=MAX_BYTES,"Source size invalid")
    data=p.read_bytes()
    after=p.stat()
    require(before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns,
            "Source changed while inspected")
    return data

def inspect(root,manifest):
    require(isinstance(manifest,dict) and
            manifest.get("schema")=="va-private-tmu-staging-source-hash-manifest/1.0"
            and manifest.get("classification")=="PRIVATE_ORIGINAL_CUSTODY",
            "Expected a private original-file manifest")
    require(manifest.get("historicalFreezeAuthenticated") is False,
            "A modern file fingerprint is not a historic freeze")
    entries=manifest.get("files")
    require(isinstance(entries,dict) and set(entries)==set(NAMES),
            "All seven original source records must be distinctly enumerated")
    root=Path(root).absolute()
    require(root.is_dir() and not root.is_symlink(),"Source custody directory absent")
    source={}
    for name in NAMES:
        digest=entries[name]
        require(isinstance(digest,str) and HEX.fullmatch(digest),
                "Missing exact source SHA-256 for "+name)
        raw=original_file(root,name)
        require(sha(raw)==digest,"Exact source bytes differ from custody SHA-256: "+name)
        source[name]=raw
    meta=json.loads(source[NAMES[0]].decode("utf-8"))
    require(meta.get("pack_id")=="TMU_One_Path_Proof_Pack"
            and meta.get("pack_version")=="v1.2_FULL_ENV"
            and meta.get("environment")=="staging_docker",
            "Original pack category, version or staging scope substituted")
    require(meta.get("gates")==list(GATES) and
            meta.get("gate_status_summary")==dict.fromkeys(GATES,"PASS"),
            "Declared original five-gate summary incomplete")
    outputs={}
    for gate,name in GATES.items():
        content=source[name].decode("utf-8")
        require(re.search(r"^GATE:\s*"+gate.upper()+r"\s*$",content,re.M)
                and re.search(r"^STATUS:\s*PASS\s*$",content,re.M)
                and re.search(r"^PACK_VERSION:\s*v1\.2_FULL_ENV\s*$",content,re.M),
                "Saved gate result missing/misbound: "+gate)
        outputs[gate]=content
    try:
        lines=[json.loads(v) for v in source[NAMES[-1]].decode("utf-8").splitlines() if v.strip()]
    except (ValueError,UnicodeError) as e:
        raise ValueError("Original NDJSON receipt bundle not parseable") from e
    require(len(lines)==2 and [x.get("decision_class") for x in lines]==["EXECUTE","REFUSE"],
            "Original recorded positive/refusal controls incomplete")
    require(all(r.get("outcome")==r["decision_class"] and
                r.get("replayable") is True
                and r.get("contract_identity")=="TMU_Governed_Runtime_v8.3"
                for r in lines),"Receipt source class, contract and replay labels inconsistent")
    require(len(set(x.get("receipt_id") for x in lines))==2,
            "Duplicate recorded receipt identifiers")
    for receipt in lines:
        require(isinstance(receipt.get("receipt_id"),str)
                and receipt["receipt_id"] in outputs["smoke"]
                and receipt["receipt_id"] in outputs["receipt_drift"],
                "Receipt source ID not bound to smoke and drift files")
        require(receipt.get("state_hash") in outputs["smoke"]
                and receipt.get("commit_boundary") in outputs["smoke"],
                "Receipt source and recorded smoke state not linked")
        require(receipt.get("runtime_identity")==meta["runtime_identity"],
                "Actual saved receipt runtime label differs from source metadata")
    require("Total receipts evaluated: 2" in outputs["receipt_drift"],
            "Drift test did not enumerate exactly two original receipt records")
    for decision in ("EXECUTE","REFUSE"):
        replay=outputs["replay"]
        section=re.search(r"--- "+decision+r" REPLAY ---\s*(.*?)(?=---|\\Z)",replay,re.S)
        require(section is not None
                and "original_decision_class:" in section.group(1)
                and "replayed_decision_class:" in section.group(1)
                and re.search(r"original_decision_class:\s*"+decision+r"\b",section.group(1))
                and re.search(r"replayed_decision_class:\s*"+decision+r"\b",section.group(1)),
                "Recorded replay result missing/mismatched: "+decision)
    span=outputs["span_commit_conformance"]
    totals=[int(v) for v in re.findall(r"^total_span_ms:\s*(\d+)\s*$",span,re.M)]
    commits=[int(v) for v in re.findall(r"^commit_subspan_ms:\s*(\d+)\s*$",span,re.M)]
    evals=[int(v) for v in re.findall(r"^evaluation_subspan_ms:\s*(\d+)\s*$",span,re.M)]
    seals=[int(v) for v in re.findall(r"^seal_subspan_ms:\s*(\d+)\s*$",span,re.M)]
    require(len(totals)==len(commits)==len(evals)==len(seals)==2
            and all(a==b+c+d for a,b,c,d in zip(totals,commits,evals,seals)),
            "Source timing subspan values fail reported reconciliation")
    return {
        "schema":"va-private-tmu-original-source-data-audit/1.0",
        "outcome":"SEVEN_SAVED_STAGING_SOURCES_INTERNALLY_RECONCILED",
        "sourceFiles":7,
        "recordedPassGateFiles":5,
        "originalSavedReceipts":2,
        "recordedReplayClassComparisons":2,
        "recordedDecisions":["EXECUTE","REFUSE"],
        "reportedTotalSpansMilliseconds":totals,
        "reportedCommitSubspansMilliseconds":commits,
        "originalContemporaneousFreezeAuthenticated":False,
        "originalArchivedCodeExecuted":False,
        "independentExternalEffectMeasured":False,
        "actualLiveTMUDeploymentAuthenticated":False,
        "sourceDisclosureRightsVerified":False,
        "humanWitnessIndependenceAuthenticated":False,
        "sourceOnlyNotAutomaticRelease":True
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",required=True,help="Private folder of seven unchanged original attachments")
    p.add_argument("--manifest",required=True,help="Separately held private SHA-256 manifest")
    args=p.parse_args()
    try:
        root=Path(args.root).absolute()
        manifest=Path(args.manifest).absolute()
        require(manifest.is_file() and not manifest.is_symlink() and
                not manifest.resolve().is_relative_to(root.resolve()),
                "Manifest must be held separately from original source folder")
        d=json.loads(manifest.read_text(encoding="utf-8"))
        print(json.dumps(inspect(root,d),indent=2))
    except (ValueError,TypeError,KeyError,OSError,UnicodeError) as e:
        p.exit(2,"REFUSED: "+str(e)+"\n")

if __name__=="__main__":
    main()
