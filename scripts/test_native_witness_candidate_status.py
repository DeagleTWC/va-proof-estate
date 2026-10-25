#!/usr/bin/env python3
"""Synthetic false-promotion controls for historic original witness candidate review."""
import copy
import json
from validate_native_witness_candidate_status import ROOT,check

def refuse(d,label):
    try:check(d)
    except (ValueError,KeyError,TypeError):return
    raise AssertionError("False native admission accepted: "+label)

def main():
    orig=json.loads((ROOT/"proofs/NATIVE-WITNESS-ORIGINAL-CANDIDATE-STATUS.json").read_text(encoding="utf-8"))
    assert check(orig)==3
    edits=[
      ("manufactured native reviewer",lambda d:d.update(independentNativeVAWitnessPubliclyAdmitted=True)),
      ("invented independently measured effect",lambda d:d.update(originalNativeVAExternalEffectCarrierAdmitted=True)),
      ("private original falsely released",lambda d:d.update(exactPrivateOriginalBytesRepublished=True)),
      ("unqualified seal promoted",lambda d:d.update(internalCandidateSourceSealQualified=True)),
      ("same source copy counted as witness",lambda d:d.update(duplicateCopiesTreatedAsDistinctWitnesses=True)),
      ("private source identity leaked",lambda d:d.update(originalPrivateSourceIdentifiersPublished=True)),
      ("unqualified witness count",lambda d:d.update(nativeIndependentWitnessPublicCount=1)),
      ("historic pilot count fabricated",lambda d:d.update(actualHistoricalPilotCountEstablishedByThisMilestone=3)),
      ("quarantine erased",lambda d:d.update(currentStage="INDEPENDENT_NATIVE_PASS")),
      ("human qualification barrier removed",lambda d:d.update(humanWitnessQualificationGate="NOT_REQUIRED")),
      ("release authority fabricated",lambda d:d["reviewedPublicSafeCategories"][0].update(originalReleaseRightsEstablished=True)),
      ("external observation fabricated",lambda d:d["reviewedPublicSafeCategories"][0].update(actualExternallyInstrumentedEffectProven=True)),
      ("sample interface promoted to native",lambda d:d["reviewedPublicSafeCategories"][1].update(nativeIndependentHumanWitness=True)),
      ("external formal solver called native",lambda d:d["reviewedPublicSafeCategories"][2].update(stage="VERIFIED_NATIVE_VA")),
      ("sensitive defect details stated public",lambda d:d.update(privateCandidateDefectDetailsRetainedOffPublicSite=False)),
      ("bounded stance reclassified",lambda d:d.update(disposition="CERTIFIED_NATIVE_WITNESS"))
    ]
    for label,edit in edits:
        v=copy.deepcopy(orig);edit(v);refuse(v,label)
    print("PASS:",len(edits),"synthetic source-integrity, native-standing and private release inflations refused")

if __name__=="__main__":
    main()
