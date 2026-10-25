#!/usr/bin/env python3
"""Synthetic tamper regression: public third-party history must not confer native standing."""
import copy
import json
from pathlib import Path
from validate_third_party_review import validate

def expect_refusal(obj,label):
    try: validate(obj)
    except (ValueError,KeyError,TypeError): return
    raise AssertionError("Accepted bad third-party standing: "+label)

def main():
    root=Path(__file__).resolve().parents[1]
    data=json.loads((root/"proofs/THIRD-PARTY-REVIEW-REGISTER.json").read_text(encoding="utf-8"))
    validate(data)
    changes=[
        ("false native V.A. reproduction",lambda x:x["publicNativeVAThirdPartyReproductions"].append({"claim":"PASS"})),
        ("unreleased review marked published",lambda x:x["publicReviewCandidates"][0].update(reviewOutcomePublished=True)),
        ("private source marked released",lambda x:x["publicReviewCandidates"][0].update(externalSourceRightsCleared=True)),
        ("external carrier invents V.A. witness",lambda x:x["publicReviewCandidates"][0].update(qualifiedThirdPartyWitnessOfNativeVA=True)),
        ("third-party results leaked",lambda x:x["publicReviewCandidates"][0].update(publicObservationClaims=["PASS"])),
        ("released list without carrier",lambda x:x["admittedPublicThirdPartyReviewCarriers"].append({"test":"fake"})),
        ("review duplicate",lambda x:x["publicReviewCandidates"].append(copy.deepcopy(x["publicReviewCandidates"][0]))),
    ]
    for label,change in changes:
        v=copy.deepcopy(data);change(v);expect_refusal(v,label)
    print(f"PASS: third-party custody and seven synthetic unsupported evidence promotions rejected")

if __name__=="__main__":
    main()
