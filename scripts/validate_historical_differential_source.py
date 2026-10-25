#!/usr/bin/env python3
"""Ensure historic recovered review sources never convert to independent V.A. or released originals."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FILENAMES=("independent_pyjwt_2_13_0_review_harness.py",
           "independent_results_pyjwt_2.13.0.json",
           "independent_results_pyjwt_2.12.1.json")
EXPECTED=("02c17c0590c0a848e1e79f8d04409c8687a7900a56b2aae483cbd3970c9ff824",
          "2892c50c3abdf2379fe861fc88a0dc53ec09762a754a14b9e1d39d681b91f9bd",
          "8c8effa686a40b8d8d4adbdbfcf918337370bc75558ba08f18e595227e07b070")

def require(ok,message):
    if not ok:raise ValueError(message)

def validate(d):
    require(d.get("schema")=="va-historical-differential-source-reconciliation/1.0"
            and d.get("milestone")==17,"Different source register")
    require(d.get("historicalExternalReviewClass")=="REVIEW_OF_THIRD_PARTY_SOFTWARE_NOT_NATIVE_VA",
            "PyJWT software review promoted to native V.A.")
    for flag in ("historicalOriginalArchivePresentInLibrary","originalArchiveBytesExamined",
                 "priorM16SameObjectOriginalPDFAgainInsideArchive",
                 "priorM16OriginalPDFExactBytesMatched",
                 "differentReviewObjectsKeptSeparate",
                 "originalArchiveExactHashKeptPrivate"):
        require(d.get(flag) is True,"Lost genuine source custody: "+flag)
    for flag in ("originalHarnessExecutedInMilestone17",
                 "underlyingPyJWTDependenciesReinstalledAndRerunInMilestone17",
                 "originalRunEnvironmentOrTimestampAuthenticatedInMilestone17",
                 "independentHumanWitnessIdentityAuthenticatedInMilestone17",
                 "nativeVAOriginalExaminedByThisSource",
                 "nativeVAIndependentEffectReproduced",
                 "publicPermissionToRepublishOriginalArchiveOrPDF",
                 "publicArchiveOrOriginalTestBytesAttached"):
        require(d.get(flag) is False,"Unsupported execution/witness/release promotion: "+flag)
    require(d.get("originalArchiveMemberCount")==5,"Original archive size wrong")
    source=d.get("reportedSha256MembersChecked")
    require(isinstance(source,list) and len(source)==3,"Three report-listed source members required")
    for row,name,sha in zip(source,FILENAMES,EXPECTED):
        require(isinstance(row,dict) and row.get("name")==name and
                row.get("sha256")==sha and row.get("actualBytesMatched") is True,
                "Recovered original member hash not established or changed")
    obj=d.get("sourceResults")
    require(isinstance(obj,dict) and
            obj.get("fixedVersion")=="2.13.0" and obj.get("baselineVersion")=="2.12.1"
            and obj.get("sameSixCaseIdsOnBothVersions") is True
            and obj.get("fixedSavedPassCount")==6 and obj.get("baselineSavedFailCount")==6
            and obj.get("caseVariantCount")==6
            and obj.get("fiveReleaseClaimFamilies")==["C001","C002","C003","C004","C005"],
            "Archived six-case outcome count/identity corrupted")
    require(d.get("evidenceCeiling")==
            "ORIGINAL_HARNESS_AND_SAVED_DIFFERENTIAL_RESULTS_SOURCE_HASHES_MATCH_HISTORIC_REPORT",
            "Historic source byte matching improperly promoted to actual execution")
    require(d.get("historicalReviewerDispositionPreserved")==
            "PARTIAL_QUALIFICATION_BOUNDED_PYTHON_RELEASE_CLAIM_REVIEW",
            "Historic bounded reviewer disposition changed")
    require(d.get("earlierM16SubmittedCarrierDispositionPreserved")==
            "HOLD_SUBMITTED_QUALIFICATION_CARRIER",
            "Earlier independent review HOLD incorrectly erased")
    old=json.loads((ROOT/"proofs/HISTORICAL-REVIEW-ORIGINAL-REGISTER.json").read_text(encoding="utf-8"))
    require(old["underlyingOriginalHarnessesOrDifferentialResultsSeparatelyExamined"] is False,
            "Historical M16 snapshot should not be retroactively overwritten")
    witness=json.loads((ROOT/"proofs/INDEPENDENT-WITNESS-STATUS.json").read_text(encoding="utf-8"))
    require(witness["currentPublishedNativeV12IndependentWitnessCount"]==0,
            "Native independent witnesses fabricated")
    admission=json.loads((ROOT/"proofs/historical/PUBLIC-CARRIER-REGISTER.json").read_text(encoding="utf-8"))
    require(admission.get("entries")==[],"Original protected pilot release requires independent authorization")
    return 3

def main():
    d=json.loads((ROOT/"proofs/HISTORICAL-DIFFERENTIAL-SOURCE-REGISTER.json").read_text(encoding="utf-8"))
    n=validate(d)
    print(f"PASS: {n} actual historical review original hashes documented and six paired saved differential results")
    print("PASS: source standing only; old HOLD/PARTIAL, native V.A. and release limits remain distinct")

if __name__=="__main__":
    main()
