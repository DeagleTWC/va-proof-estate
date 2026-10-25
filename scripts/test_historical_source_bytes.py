#!/usr/bin/env python3
"""Synthetic negative controls for historical original-source bytes and standing claims."""
import copy
import hashlib
import json
from pathlib import Path
from validate_historical_source_bytes import ROOT,check_registry,compare_source

def reject(data,label):
    try:check_registry(data)
    except (ValueError,KeyError,TypeError): return
    raise AssertionError("Bad source promotion was accepted: "+label)

def main():
    d=json.loads((ROOT/"proofs/HISTORICAL-SOURCE-BYTE-VERIFICATION.json").read_text(encoding="utf-8"))
    check_registry(d)
    mutations=[
        ("source commit substituted",lambda x:x["publicHistoricalSourceFiles"][0].update(commit="0"*40)),
        ("source byte digest substituted",lambda x:x["publicHistoricalSourceFiles"][0].update(sourceTextSHA256="z"*64)),
        ("other repository substituted",lambda x:x["publicHistoricalSourceFiles"][0].update(repo="evil/unknown")),
        ("wrong recorded case count",lambda x:x.update(caseCountAcrossPinnedReceiptRecords=999)),
        ("native V12 inherited",lambda x:x.update(nativeObservedEffectEstablishedByTheseSourceLinks=True)),
        ("independent third-party witnessed",lambda x:x.update(independentNativeV12ReproductionsEstablished=True)),
        ("historic source promoted to original freeze",lambda x:x["publicHistoricalSourceFiles"][0].update(originalHistoricalFreezeIdentityNotInferred=False)),
        ("unread private original ZIP falsely verified",lambda x:x.update(historicalEngineeringV12ZipSourceVerifiedHere=True)),
        ("private original Zip falsely publicly attached",lambda x:x.update(originalHistoricalV12ZIPPubliclyAttached=True)),
        ("PDF digest changed",lambda x:x["sourcePDF"].update(originalPDFSHA256="0"*64)),
        ("public source case count changed",lambda x:x["publicHistoricalSourceFiles"][1].update(actualRecordedCaseCount=99)),
        ("source linked as external physical effect",lambda x:x["publicHistoricalSourceFiles"][1].update(externalObservedEffectVerified=True)),
    ]
    for label,edit in mutations:
        v=copy.deepcopy(d);edit(v);reject(v,label)
    fake=b'{"case_id":"fake"}'
    row=copy.deepcopy(d["publicHistoricalSourceFiles"][0])
    row["sourceSizeUTF8Bytes"]=len(fake)
    row["sourceTextSHA256"]=hashlib.sha256(fake).hexdigest()
    row["gitBlobSHA1"]="0"*40
    try:compare_source(row,fake)
    except ValueError:pass
    else:raise AssertionError("Data-only fake source falsely passed original Git identity")
    print(f"PASS: {len(mutations)+1} negative controls reject unsupported source, test, effect and freeze standing")


if __name__=="__main__":
    main()
