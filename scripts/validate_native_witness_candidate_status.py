#!/usr/bin/env python3
"""Fail closed on unqualified native witness admission and private-source disclosure."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STAGES=("ORIGINAL_CARRIER_REVIEWED_RELEASE_SEAL_HOLD",
        "SEPARATE_INTERFACE_TEST_SURFACE",
        "THIRD_PARTY_ENGINEERING_SUBJECT_NOT_NATIVE_VA")
CATEGORIES=("LOCAL_INDEPENDENT_VERIFIER_RELEASE_CANDIDATE",
            "BOUNDARY_INTERFACE_SAMPLE_PILOT",
            "EXTERNAL_SEAM_FORMAL_REASONING_DEMONSTRATOR")

def need(test,msg):
    if not test:raise ValueError(msg)

def check(x):
    need(x.get("schema")=="va-native-witness-candidate-gate/1.0" and x.get("milestone")==18,
         "Unexpected M18 native witness source status schema")
    need(x.get("currentStage")=="SOURCE_ORIGINAL_INTEGRITY_HOLD"
         and x.get("disposition")=="HOLD_NATIVE_INDEPENDENT_ADMISSION_PENDING_QUALIFIED_ORIGINAL",
         "Native witness candidate prematurely qualified")
    for key in ("independentNativeVAWitnessPubliclyAdmitted",
                "originalNativeVAExternalEffectCarrierAdmitted",
                "exactPrivateOriginalBytesRepublished",
                "originalPrivateSourceIdentifiersPublished",
                "duplicateCopiesTreatedAsDistinctWitnesses",
                "internalCandidateSourceSealQualified"):
        need(x.get(key) is False, "Private/unfinished source falsely promoted: "+key)
    for key in ("privateCandidateSourcesReconciled","archiveCandidateCopiesCompared",
                "privateCandidateDefectDetailsRetainedOffPublicSite",
                "noAutomaticStandingPromotion"):
        need(x.get(key) is True, "M18 original source custody safeguard lost: "+key)
    need(type(x.get("nativeIndependentWitnessPublicCount")) is int and
         x["nativeIndependentWitnessPublicCount"]==0, "No new authenticated native witness public carriers exist")
    need(x.get("actualHistoricalPilotCountEstablishedByThisMilestone")=="NOT DETERMINED",
         "Historic pilot census misrepresented")
    sources=x.get("reviewedPublicSafeCategories")
    need(isinstance(sources,list) and len(sources)==3, "Three original candidate classes expected")
    for i,source in enumerate(sources):
        need(isinstance(source,dict) and source.get("category")==CATEGORIES[i]
             and source.get("stage")==STAGES[i], "Origin category promoted or altered")
        for key in ("nativeIndependentHumanWitness","actualExternallyInstrumentedEffectProven",
                    "originalReleaseRightsEstablished"):
            need(source.get(key) is False, "Unproven result promoted: "+key)
    need(x.get("releaseSealLocalTool")=="scripts/audit_original_release_seal.py",
         "Original integrity examiner reference altered")
    need(x.get("originalSourceDisclosureGate")=="EXPLICIT_AUTHORIZED_EXTRACT_REQUIRED"
         and x.get("humanWitnessQualificationGate")==
         "ACTUAL_SEPARATE_QUALIFIED_HUMAN_AND_EFFECT_MEASUREMENT_REQUIRED",
         "Authority or real effect witness gate removed")
    prior=json.loads((ROOT/"proofs/INDEPENDENT-WITNESS-STATUS.json").read_text(encoding="utf-8"))
    need(prior["currentPublishedNativeV12IndependentWitnessCount"]==0,
         "Earlier native witness register independently changed")
    admitted=json.loads((ROOT/"proofs/historical/PUBLIC-CARRIER-REGISTER.json").read_text(encoding="utf-8"))
    need(admitted.get("entries")==[], "Historical original release authorization must be separately reviewed")
    return len(sources)

def main():
    d=json.loads((ROOT/"proofs/NATIVE-WITNESS-ORIGINAL-CANDIDATE-STATUS.json").read_text(encoding="utf-8"))
    c=check(d)
    print(f"PASS: {c} original witness-candidate source categories classified; source-seal HOLD retained")
    print("PASS: no unqualified human, native V.A. effect, archived pilot census or private source release")

if __name__=="__main__":
    main()
