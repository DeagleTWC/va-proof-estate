#!/usr/bin/env python3
"""Reject promotion of authentic historic reviewer PDFs into unsupported V.A. witness standing."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REVIEW_IDS=("IQR-ITR-001-v1.0","ITR-PYJWT-2130-INDEPENDENT-v1.0")
CLASSES=("REVIEW_OF_EXTERNAL_REVIEWER_SUBMISSION_CARRIER",
         "SEPARATELY_DESCRIBED_SAME_OBJECT_DIFFERENTIAL_REVIEW")
OUTCOMES=("HOLD_QUALIFICATION_NOT_ESTABLISHED_BY_SUBMITTED_CARRIER",
          "FIVE_RELEASE_CLAIMS_REPORTED_PASS_REVIEWER_PARTIALLY_QUALIFIED")
PAGES=(8,5)

def need(ok,why):
    if not ok: raise ValueError(why)

def check(data):
    need(data.get("schema")=="va-historical-external-review-original-register/1.0"
         and data.get("milestone")==16,"Historical review source register changed")
    need(data.get("externalArtifact")=="PyJWT 2.13.0"
         and data.get("externalReviewSubjectIsNativeVA") is False,
         "External PyJWT review was mislabeled native V.A.")
    for flag in ("sameDayDocumentsCannotEstablishChronology",
                 "holdAndPartialConclusionsAddressDifferentEvidenceObjects",
                 "noReleaseRightsOrSourceTruthByMetadataAlone"):
        need(data.get(flag) is True,"Historic review boundary removed: "+flag)
    for flag in ("underlyingOriginalHarnessesOrDifferentialResultsSeparatelyExamined",
                 "independentThirdPartyWitnessOfNativeVAAuthenticated",
                 "historicalNativeVAPilotOriginalPubliclyAdmitted",
                 "authorizationToPublishOriginalPDFs"):
        need(data.get(flag) is False,"Review documentary source promoted beyond evidence: "+flag)
    need(data.get("publicByteCarrierCount")==0,"Original private PDF falsely admitted")
    need(data.get("publicVerificationResult")==
         "TWO_ORIGINAL_REVIEW_PDFS_IDENTIFIED_AND_FINGERPRINTED_IN_PRIVATE_CUSTODY",
         "Exact historical source byte check misrepresented")
    need(data.get("publicIndependentReproductionClaim")=="NOT_ESTABLISHED",
         "Historic review source converted to independent native witness")
    records=data.get("entries")
    need(isinstance(records,list) and len(records)==2,"Source review count mismatch")
    for i,item in enumerate(records):
        need(isinstance(item,dict) and item.get("reviewId")==REVIEW_IDS[i],
             "Original review identity absent/swapped")
        need(item.get("documentKind")==CLASSES[i],"Historic distinct review objects collapsed")
        need(item.get("originallyRecordedDisposition")==OUTCOMES[i],
             "Original HOLD/PARTIAL disposition overwritten")
        need(item.get("sourcePDFPages")==PAGES[i],"Source PDF page count modified")
        need(item.get("reviewDateAsPrinted")=="2026-07-20",
             "Stated date changed without source review")
        for flag in ("sourcePDFOriginalBytesRetrieved","privateOriginalSHA256MatchedSourceCustody"):
            need(item.get(flag) is True,"Original source byte custody de-established: "+flag)
        for flag in ("publicOriginalPDFAttached","independentlyReperformedClaimTestsByThisMilestone",
                     "externallyAuthenticatedWitnessOfNativeVA","releaseRightsVerified"):
            need(item.get(flag) is False,"Unverified source release/standing: "+flag)
    previous=json.loads((ROOT/"proofs/INDEPENDENT-WITNESS-STATUS.json").read_text(encoding="utf-8"))
    need(previous["currentPublishedNativeV12IndependentWitnessCount"]==0
         and previous["independentWitnessPacketAdmittedToPublicCarrierRegister"] is False,
         "Native V.A. witness source falsely promoted")
    public=json.loads((ROOT/"proofs/historical/PUBLIC-CARRIER-REGISTER.json").read_text(encoding="utf-8"))
    need(public.get("entries")==[],"Original customer run released without independent admission")
    return len(records)

def main():
    d=json.loads((ROOT/"proofs/HISTORICAL-REVIEW-ORIGINAL-REGISTER.json").read_text(encoding="utf-8"))
    n=check(d)
    print("PASS: two historical externally reviewed original PDFs retained under separate source scope:",n)
    print("PASS: HOLD and later differential review PARTIAL findings both preserved")
    print("PASS: no private original redistributed, native V.A. or independent human effect standing inherited")

if __name__=="__main__":
    main()
