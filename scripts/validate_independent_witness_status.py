#!/usr/bin/env python3
"""Fail closed on unsupported public independent witness/native V12 promotion."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCHEMA="va-witness-qualification-status/1.0"

def need(ok, why):
    if not ok: raise ValueError(why)

def check(data):
    need(data.get("schema")==SCHEMA and data.get("milestone")==15,"Unknown witness qualification register")
    for key in ("currentPublishedNativeV12IndependentWitnessCount",
                "currentPublishedHistoricalOriginalRunIndependentWitnessCount"):
        need(type(data.get(key)) is int and data[key]==0,
             "Independent qualified public count promoted without original evidence")
    for flag in ("independentWitnessPacketAdmittedToPublicCarrierRegister",
                 "outsideEffectMeasuredInM14Originals",
                 "cryptographicOriginalReceiptSignatureVerifiedInM14",
                 "independentHumanIdentityAuthenticatedInM14",
                 "publicDisclosureAuthorityForOriginalCustomerRecords",
                 "rawPrivateOriginalsPublished"):
        need(data.get(flag) is False,"Unsupported private/public witness promotion: "+flag)
    for flag in ("recordedEarlierEngineeringProofExists",
                 "recordedEarlierCompletedSourceCapturesExist",
                 "historicalEngineeringSourceReproducedInPrivateCustody",
                 "archivedConnectedV1V2ShareSameRun",
                 "newQualificationToolingDeployed",
                 "historicalReviewOfThirdPartyEngineeringSeparate",
                 "noAutomaticStandingPromotion"):
        need(data.get(flag) is True,"Recorded historic engineering lineage erased: "+flag)
    need(data.get("localSignedRecordCheckResultCeiling")==
         "SIGNED_RECORDS_INTERNALLY_BOUND_HUMAN_QUALIFICATION_PENDING",
         "Cryptographic preflight status inflated")
    need(data.get("disposition")=="HOLD_PUBLIC_INDEPENDENT_QUALIFICATION_PENDING_ACTUAL_ORIGINAL_WITNESS_CARRIER",
         "Human witness evidence barrier lowered")
    need(data.get("explicitHistoricalPilotCount")=="NOT DETERMINED BY THIS PUBLICATION",
         "Previous historical pilots falsely counted from website")
    carriers=json.loads((ROOT/"proofs/historical/PUBLIC-CARRIER-REGISTER.json").read_text(encoding="utf-8"))
    need(carriers["entries"]==[],"Human original source release gate bypassed")
    m14=json.loads((ROOT/"proofs/HISTORICAL-RUN-RECONCILIATION.json").read_text(encoding="utf-8"))
    need(m14["externalProtectedEffectsIndependentlyMeasured"] is False
         and m14["qualifiedThirdPartyExaminerIdentityEstablishedBySource"] is False,
         "Earlier original M14 evidence falsely reclassified")
    return True

def main():
    data=json.loads((ROOT/"proofs/INDEPENDENT-WITNESS-STATUS.json").read_text(encoding="utf-8"))
    check(data)
    print("PASS: original recorded history retained; no unsupported third-party native V.A. or physical effect evidence admitted")

if __name__=="__main__":
    main()
