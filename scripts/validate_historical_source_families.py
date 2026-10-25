#!/usr/bin/env python3
"""Guard the public-safe historical source-family index. Does not verify private originals."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EXPECTED=[
    ("M11-ENG-BUILD","ORIGINAL_ENGINEERING_FREEZE","BUILD_PACKAGE_AND_VERIFICATION_HISTORY"),
    ("M11-PILOT-SCOPE","LIVE_WORKFLOW_PILOT_PLAN","PLANNED_EXECUTION_AND_ACCEPTANCE_CRITERIA"),
    ("M11-LAUNCH","PILOT_LAUNCH_PACKAGE","RECORDED_LAUNCH_PACKAGE"),
    ("M11-RUN-FORM","PILOT_RESULT_FORM","PENDING_IN_EXAMINED_FORM"),
    ("M11-EXT-REVIEW","EXTERNAL_ENGINEERING_REVIEW","HISTORICALLY_DOCUMENTED_BOUNDED_REVIEW")
]

def require(test,message):
    if not test:
        raise ValueError(message)

def validate(doc):
    require(isinstance(doc,dict) and doc.get("schema")=="deagle-m11-public-historical-source-family-index/1.0","Unknown index schema")
    require(doc.get("publication")=="DeagleTWC/va-proof-estate","Changed publication identity")
    require(doc.get("noProductionOrNativePromotion") is True,"Unauthorized evidence promotion")
    require(doc.get("privateSourceLocatorPublication")=="NOT_AUTHORIZED","Private custody leak declaration")
    require(doc.get("originalFreezeCount")=="NOT_ESTABLISHED_FROM_THIS_PUBLIC_INDEX","Original freeze count invented")
    require(doc.get("totalHistoricalPilotCount")=="NOT_ESTABLISHED_FROM_THIS_PUBLIC_INDEX","Historical pilot count invented")
    require(doc.get("publicNativeObservedResultCountThisMilestone")==0,"Unsupported native V.A. standing")
    require(doc.get("publicIndependentNativeVAReproductionsThisMilestone")==0,"Unsupported native reproduction")
    statuses=doc.get("statusVocabulary")
    require(statuses==["PRIVATE_SOURCE_LOCATED","PUBLIC_SOURCE_LINKED","PUBLIC_ORIGINAL_ADMITTED","INDEPENDENTLY_REPRODUCED"],"Status types changed")
    families=doc.get("historicalFamilies")
    require(isinstance(families,list) and len(families)==len(EXPECTED),"Unexpected source-family count or ordering")
    for f,(eid,etype,stage) in zip(families,EXPECTED):
        require(f["id"]==eid and f["sourceType"]==etype and f["stage"]==stage,"Historical source family identity or scope changed")
        require(f["status"]=="PRIVATE_SOURCE_LOCATED","Unreviewed private original promoted")
        require(f["originalBytesPubliclyAttached"] is False,"Unattached original marked public")
        require(f["actualLiveEffectEstablishedHere"] is False,"Source metadata converted to live effect")
        require(f["nativeV12StandingInherited"] is False,"Older source inherited native V12 standing")
        require(isinstance(f.get("note"),str) and len(f["note"])>25,"Missing scope statement")
        link=f.get("link")
        require(isinstance(link,str) and link.startswith("proofs/") and
                (ROOT/link).is_file(),"Original public reading-route link missing")
    require(doc.get("knownAdditionalPublicSurfaces")=="proofs/HISTORICAL-PUBLIC-SURFACES.json","Separate six public surfaces omitted")
    require(doc.get("admittedPublicOriginalCarriers")=="proofs/historical/PUBLIC-CARRIER-REGISTER.json","Historical original admission register omitted")
    require(isinstance(doc.get("sourceReviewRule"),str) and "original" in doc["sourceReviewRule"].lower(),"Public provenance ceiling absent")
    return len(families)

def main():
    path=ROOT/"proofs/HISTORICAL-SOURCE-FAMILIES.json"
    n=validate(json.loads(path.read_text(encoding="utf-8")))
    text=(ROOT/"proofs/MILESTONE-11-SOURCE-RECONCILIATION.md").read_text(encoding="utf-8")
    require("five" in text.lower() and "not five total pilots" in text.lower(),
            "Documentary distinction between source families and historical pilot counts missing")
    require("HISTORICAL-SOURCE-FAMILIES.json" in text,"Guide lacks machine-readable reference")
    print(f"PASS: {n} historical source categories recorded separately from pilot and native counts")
    print("PASS: public source locators exclude protected originals and false evidence promotion")

if __name__=="__main__":
    main()
