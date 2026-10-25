#!/usr/bin/env python3
"""Enforce third-party credit is not converted into unsupported native V.A. evidence."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def require(ok,reason):
    if not ok: raise ValueError(reason)

def validate(data):
    require(data.get("schema")=="deagle-third-party-evidence-publication-register/1.0","wrong schema")
    require(data.get("noAutomaticPromotion") is True,"automatic promotion enabled")
    pending=data.get("publicReviewCandidates")
    require(isinstance(pending,list),"history index missing")
    seen=set()
    for obj in pending:
        require(obj["id"] not in seen,"duplicate review candidate")
        seen.add(obj["id"])
        require(obj["publicationState"]=="EXTERNAL_SUBMISSION_UNRELEASED",
                "unreleased historic review promoted without new public source review")
        require(obj["originalFrozenPackagePubliclyAttached"] is False,"private original mislabeled public")
        require(obj["externalSourceRightsCleared"] is False,"invented release rights")
        require(obj["qualifiedThirdPartyWitnessOfNativeVA"] is False,"historic external-object review promoted to V.A.")
        require(obj["reviewOutcomePublished"] is False and obj["publicObservationClaims"]==[],
                "private disposition leaked into publication")
    require(data["admittedPublicThirdPartyReviewCarriers"]==[],"no released external review carrier yet")
    require(data["publicNativeVAThirdPartyReproductions"]==[],"no independent native carrier attached")
    require("not independent reproduction" in data["prohibitedInference"].lower() or
            "are not independent reproduction" in data["prohibitedInference"].lower(),
            "source-to-native noninheritance lost")
    return len(pending)

def main():
    data=json.loads((ROOT/"proofs/THIRD-PARTY-REVIEW-REGISTER.json").read_text(encoding="utf-8"))
    count=validate(data)
    print(f"PASS: {count} private-custody third-party review index entries; zero invented native independent examinations")
    print("No historical external source or review disposition has been publicly admitted by this registry.")

if __name__=="__main__":
    main()
