#!/usr/bin/env python3
"""Offline, private historical reviewer-PDF source-byte audit. Never grants release or independent standing."""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

SCHEMA="va-private-original-review-document-check/1.0"
CLASSES=("CARRIER_QUALIFICATION_HOLD","SAME_OBJECT_DIFFERENTIAL_REVIEW_PARTIAL")
IDS=("IQR-ITR-001-v1.0","ITR-PYJWT-2130-INDEPENDENT-v1.0")
HEX=re.compile(r"^[0-9a-f]{64}$")
MAX_BYTES=5_000_000

def need(test,reason):
    if not test: raise ValueError(reason)

def safe_source(root,path,digest):
    need(isinstance(path,str) and path and len(path)<230 and "\\" not in path,
         "Bad original source path")
    p=Path(path)
    need(not p.is_absolute() and ".." not in p.parts and p.as_posix()==path,
         "Untrusted source path")
    need(p.suffix.lower()==".pdf","Original report is not a PDF")
    candidate=root
    for component in p.parts:
        candidate=candidate/component
        need(not candidate.is_symlink(),"Source symlinks are not admissible")
    candidate=candidate.resolve()
    need(candidate.is_relative_to(root) and candidate.is_file(),"Original report not present")
    need(isinstance(digest,str) and HEX.fullmatch(digest),"Bad original SHA-256")
    before=candidate.stat()
    need(100<before.st_size<=MAX_BYTES,"Suspicious original PDF size")
    raw=candidate.read_bytes()
    after=candidate.stat()
    need(before.st_size==after.st_size and before.st_mtime_ns==after.st_mtime_ns,
         "Source changed while being fingerprinted")
    need(raw.startswith(b"%PDF-") and b"%%EOF" in raw[-2048:],
         "Original carrier has invalid PDF framing")
    h=hashlib.sha256(raw).hexdigest()
    need(h==digest,"Original report bytes do not match original source digest")
    return len(raw)

def verify_manifest(data,root):
    need(isinstance(data,dict) and data.get("schema")==SCHEMA,
         "Original review manifest schema mismatch")
    need(data.get("classification")=="PRIVATE_DO_NOT_PUBLISH",
         "Missing private original source custody")
    need(data.get("releaseAuthorization") is False,
         "Private original release cannot be granted by this verifier")
    need(data.get("independentNativeVAWitnessAuthenticated") is False,
         "External reviewer of PyJWT is not an independently qualified V.A. witness")
    need(data.get("independentDifferentialHarnessReproducedInThisAudit") is False,
         "The original PyJWT test harness was not rerun by this source-byte audit")
    objects=data.get("originalReviewDocuments")
    need(isinstance(objects,list) and len(objects)==2,"Two original separate review reports required")
    refs=set()
    summaries=[]
    for i,record in enumerate(objects):
        need(isinstance(record,dict),"Malformed original review record")
        need(record.get("reviewId")==IDS[i] and record.get("reviewClass")==CLASSES[i],
             "Original review identity or disposition changed")
        need(record.get("underlyingTechnicalObject")=="PyJWT 2.13.0",
             "Unrelated external review misattributed")
        need(record.get("reviewDateLabel")=="2026-07-20",
             "Report's stated review date changed")
        need(record.get("independentNativeVAReproduction") is False,
             "Reviewed external library promoted to V.A.")
        need(record.get("releaseCleared") is False,
             "No public source release authorizations established")
        need(record.get("reviewerCompetenceQualifiedForNativeVA") is False,
             "Bounded Python reviewer competence promoted to V.A. competence")
        ref=record.get("source")
        need(isinstance(ref,dict),"Missing private source ref")
        path=ref.get("path")
        need(path not in refs,"Duplicate original PDF")
        refs.add(path)
        size=safe_source(root,path,ref.get("sha256"))
        need(record.get("expectedBytes")==size,"Original PDF source size mismatch")
        summaries.append({"reviewId":record["reviewId"],"reviewClass":record["reviewClass"],
                          "sourceHashMatched":True,"sourceBytes":size,
                          "originalOutcomeCarrierVerified":True,
                          "substantiveTechnicalConclusionIndependentlyReproduced":False,
                          "originalReviewedOtherPeopleWorkNotNativeVA":True})
    return summaries

def run(root,manifest):
    root=Path(root).absolute()
    need(root.is_dir() and not root.is_symlink(),"Original PDF folder missing")
    root=root.resolve()
    source=Path(manifest).absolute()
    need(source.is_file() and not source.is_symlink()
         and not source.resolve().is_relative_to(root),
         "Private manifest must remain outside original source folder")
    data=json.loads(source.read_text(encoding="utf-8"))
    rows=verify_manifest(data,root)
    return {
        "schema":"va-private-external-review-original-byte-audit/1.0",
        "result":"ORIGINAL_REVIEW_PDF_BYTES_MATCH_PRIVATE_MANIFEST_ONLY",
        "checkedOriginalReports":len(rows),
        "originalReportResults":rows,
        "supportedHistoricalCredit":"REVIEW_DOCUMENTS_LOCATED_AND_BYTE_IDENTITIES_VERIFIED",
        "fullIndependentPyJWTDifferentialReproducedHere":False,
        "nativeVAOriginalRunReproducedHere":False,
        "thirdPartyWitnessOfNativeVAAuthenticated":False,
        "publicDisclosureAuthorized":False,
        "sourceClaimChronologyAuthenticated":False,
        "note":"PDF hashes support source byte identity only. These dated reports describe different review objects: one original qualification-carrier HOLD, another separately described same-object differential review with narrower PARTIAL reviewer qualification. Full source test harness, reviewer identity and publication rights require independent checks."
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",required=True)
    p.add_argument("--manifest",required=True)
    p.add_argument("--out",help="Private output JSON outside originals; no overwrite")
    a=p.parse_args()
    try:
        result=run(a.root,a.manifest)
        if a.out:
            output=Path(a.out).absolute()
            root=Path(a.root).resolve()
            need(not output.exists() and not output.is_symlink() and
                 not output.resolve().is_relative_to(root),"Unsafe private report destination")
            fd=os.open(str(output),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
            with os.fdopen(fd,"w",encoding="utf-8") as f:
                json.dump(result,f,indent=2)
                f.write("\n")
        print(json.dumps(result,indent=2))
    except (ValueError,TypeError,KeyError,OSError,UnicodeError,json.JSONDecodeError) as e:
        p.exit(2,"REFUSED: "+str(e)+"\n")

if __name__=="__main__":
    main()
