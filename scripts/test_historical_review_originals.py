#!/usr/bin/env python3
"""Synthetic fail-closed historical reviewer/original release standing tests."""
import copy
import json
from validate_historical_review_originals import ROOT,check

def reject(x,why):
    try:check(x)
    except (ValueError,KeyError,TypeError):return
    raise AssertionError("False historical review standing accepted: "+why)

def main():
    data=json.loads((ROOT/"proofs/HISTORICAL-REVIEW-ORIGINAL-REGISTER.json").read_text(encoding="utf-8"))
    assert check(data)==2
    muts=[
        ("native V.A. object",lambda v:v.update(externalReviewSubjectIsNativeVA=True)),
        ("native independent witness",lambda v:v.update(independentThirdPartyWitnessOfNativeVAAuthenticated=True)),
        ("private reviewer report falsely public",lambda v:v.update(authorizationToPublishOriginalPDFs=True)),
        ("old original PDF falsely attached",lambda v:v["entries"][0].update(publicOriginalPDFAttached=True)),
        ("both original reports called public release",lambda v:v.update(publicByteCarrierCount=2)),
        ("historical native pilot false publication",lambda v:v.update(historicalNativeVAPilotOriginalPubliclyAdmitted=True)),
        ("underlying differential code falsely rerun",lambda v:v.update(underlyingOriginalHarnessesOrDifferentialResultsSeparatelyExamined=True)),
        ("independent technical result fabricated",lambda v:v["entries"][1].update(independentlyReperformedClaimTestsByThisMilestone=True)),
        ("source 1 HOLD silently erased",lambda v:v["entries"][0].update(originallyRecordedDisposition="FULL_QUALIFIED")),
        ("source 2 partial promoted",lambda v:v["entries"][1].update(originallyRecordedDisposition="INDEPENDENT_NATIVE_VA_PASS")),
        ("source document chronology inferred",lambda v:v.update(sameDayDocumentsCannotEstablishChronology=False)),
        ("both review objects collapsed",lambda v:v.update(holdAndPartialConclusionsAddressDifferentEvidenceObjects=False)),
        ("source sizes changed",lambda v:v["entries"][0].update(sourcePDFPages=1)),
        ("source order reversed",lambda v:v["entries"].reverse()),
        ("fake human reviewer",lambda v:v["entries"][1].update(externallyAuthenticatedWitnessOfNativeVA=True)),
        ("source date invented",lambda v:v["entries"][0].update(reviewDateAsPrinted="2026-01-01")),
        ("release rights invented",lambda v:v["entries"][1].update(releaseRightsVerified=True)),
        ("earlier real original erased",lambda v:v["entries"][0].update(sourcePDFOriginalBytesRetrieved=False)),
        ("reproduction status manufactured",lambda v:v.update(publicIndependentReproductionClaim="PASSED")),
    ]
    for why,fn in muts:
        x=copy.deepcopy(data);fn(x);reject(x,why)
    print(f"PASS: {len(muts)} attempts to collapse original review objects, inflate standing or leak protected originals refused")

if __name__=="__main__":
    main()
