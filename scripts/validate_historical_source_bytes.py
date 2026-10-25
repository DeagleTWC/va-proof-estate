#!/usr/bin/env python3
"""Check original historic public-source identities. No source execution and no standing promotion."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]
SHA1=re.compile(r"^[a-f0-9]{40}$")
SHA256=re.compile(r"^[a-f0-9]{64}$")
EXPECTED=[
    ("Kamanaka5502/elyria-one-proof","receipts/demo-valid-001_receipt.json",
     "7ef8c424ca95d0bf55b18b9d13aa79e4ac29a058",1),
    ("Kamanaka5502/authority-revocation-witness","authority_receipt.json",
     "620324048ff1b067af6602d50d3016adcaed3747",5),
    ("Kamanaka5502/scope-expiry-gate","scope_receipt.json",
     "d0acaa0b4dee8cc26b357ce0e26c57f2d989da34",5),
]
PDF_DIGEST="dd5a626e4ed5efafb49e70e987f61f151e220d793e35b96c55b05e59dc426ca6"


def require(ok,why):
    if not ok: raise ValueError(why)


def check_registry(data):
    require(data.get("schema")=="deagle-historical-source-bytes/1.0","registry schema mismatch")
    require(data.get("noStandingPromotion") is True,"standing promotion not barred")
    require(data["historicalOriginalV12ZIPPubliclyAttached"] is False,"private V1.2 ZIP falsely published")
    require(data["historicalEngineeringV12ZipSourceVerifiedHere"] is False,"unread engineering ZIP marked verified")
    require(data["nativeObservedEffectEstablishedByTheseSourceLinks"] is False,"native effect falsely promoted")
    require(data["independentNativeV12ReproductionsEstablished"] is False,"independent standing falsely promoted")
    pdf=data["sourcePDF"]
    require(pdf["originalPDFSHA256"]==PDF_DIGEST,"PDF original digest differs from original")
    require(pdf["originalPDFBytesExamined"] is True and
            pdf["originalPDFBytesMirroredOnGitHubEstate"] is False,"PDF original's custody misrepresented")
    require(pdf["sourceFileSizeBytes"]==71495,"PDF source byte count mismatch")
    require(pdf["sourceExtraction"]=="proofs/sources/shift-public-proof-path-v2-extracted.md",
            "Wrong PDF transcript link")
    source_text=(ROOT/pdf["sourceExtraction"]).read_text(encoding="utf-8")
    source_estate=(ROOT/"proofs/SOURCE-ESTATE.md").read_text(encoding="utf-8")
    require(PDF_DIGEST in source_estate,"Original PDF digest not in source estate")
    require("elyria-one-proof" in source_text and "authority-revocation-witness" in source_text,
            "PDF-original source-reference comparison failed")
    src=data.get("publicHistoricalSourceFiles")
    require(isinstance(src,list) and len(src)==len(EXPECTED),"Source count mismatch")
    total=0
    for row,(repo,path,commit,count) in zip(src,EXPECTED):
        require(row["repo"]==repo and row["path"]==path and row["commit"]==commit,
                "Historical original identity changed")
        require(row["url"]==f"https://github.com/{repo}/blob/{commit}/{path}",
                "Source reference no longer immutably pinned")
        require(SHA1.fullmatch(row["gitBlobSHA1"]) and
                SHA256.fullmatch(row["sourceTextSHA256"]),"Malformed source identity digest")
        require(row["publicationState"]=="PUBLIC_SOURCE_REVISION_PINNED","Illicit status promotion")
        require(row["actualRecordedCaseCount"]==count,"Source case count changed")
        require(row["originalHistoricalFreezeIdentityNotInferred"] is True,"Snapshot treated as original freeze")
        require(row["externalObservedEffectVerified"] is False and row["nativeV12"] is False,
                "Public source decisions promoted to native/external effect")
        require(row["sourceSizeUTF8Bytes"]>0,"Missing source byte count")
        total+=count
    require(data["caseCountAcrossPinnedReceiptRecords"]==total and total==11,
            "Stored source record count no longer matches verified archive")
    require(data["publicHistoricalPilotCarrierRegister"]=="proofs/historical/PUBLIC-CARRIER-REGISTER.json",
            "Original release register changed")
    public_carriers=json.loads((ROOT/data["publicHistoricalPilotCarrierRegister"]).read_text(encoding="utf-8"))
    require(public_carriers["entries"]==[], "Public original run admissions changed without reviewed register update")
    return src


def compare_source(row,content):
    require(len(content)==row["sourceSizeUTF8Bytes"],"Original source byte size mismatched")
    require(hashlib.sha256(content).hexdigest()==row["sourceTextSHA256"],
            "Original source SHA-256 mismatch")
    git_digest=hashlib.sha1((f"blob {len(content)}\0").encode()+content).hexdigest()
    require(git_digest==row["gitBlobSHA1"],"Original source Git blob SHA-1 mismatch")
    obj=json.loads(content)
    if row["actualRecordedCaseCount"]==1:
        require(obj["decision"]=="EXECUTE" and obj["transition_id"]=="demo-valid-001",
                "Archived decision-receipt subject mismatch")
    else:
        require(len(obj["results"])==row["actualRecordedCaseCount"],
                "Original bounded case count mismatch")
    return git_digest


def download_source(row):
    raw=f"https://raw.githubusercontent.com/{row['repo']}/{row['commit']}/{row['path']}"
    req=Request(raw,headers={"User-Agent":"DeagleTWC-public-source-integrity/1.0"})
    with urlopen(req,timeout=20) as rsp:
        require(rsp.status==200,"Pinned original retrieval unsuccessful")
        data=rsp.read(2_000_001)
    require(len(data)<=2_000_000,"Source unexpectedly exceeds safe byte limit")
    return data


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--fetch-originals",action="store_true",
                    help="Read only exact pinned historic sources over HTTPS; compare bytes and Git blob identities")
    args=ap.parse_args()
    d=json.loads((ROOT/"proofs/HISTORICAL-SOURCE-BYTE-VERIFICATION.json").read_text(encoding="utf-8"))
    src=check_registry(d)
    print(f"PASS: {len(src)} immutably pinned historic public sources; 11 source entries; PDF digest reconciled")
    print("PASS: no historic original native ZIP / external effect / independent-witness promotion")
    if args.fetch_originals:
        for row in src:
            compare_source(row,download_source(row))
            print("PASS: original remote bytes match SHA-256 and Git blob:",row["repo"])
    else:
        print("OFFLINE: remote original bytes not refetched; run --fetch-originals to authenticate public source links")


if __name__=="__main__":
    main()
