#!/usr/bin/env python3
"""Ensure source-recorded historical pilots cannot be promoted without real original effect evidence."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
KINDS=["EXECUTE","REFUSE","ESCALATE"]
STAGES=[
    "ARCHIVED_INTEGRATION_SIMULATION_CAPTURE",
    "COMPLETED_CAPTURE_RECORD_RETAINED",
    "REVISED_COMPLETED_CAPTURE_RECORD_RETAINED",
    "CONSTRAINED_READINESS_DECISION_RECORD",
]

def need(ok,msg):
    if not ok:
        raise ValueError(msg)

def check(data):
    need(data.get("schema")=="va-historical-connected-run-source-crosscheck/1.0",
         "Changed public source register schema")
    need(data.get("findingClass")=="ORIGINAL_ARCHIVED_RECORD_CONSISTENCY_WITH_VERSIONED_RUN_ID",
         "Archive review misclassified as execution standing")
    src=data.get("sourceFamilies")
    need(isinstance(src,list) and len(src)==4,"Original source-family count changed")
    for i,row in enumerate(src):
        need(row.get("stage")==STAGES[i],"Original source-stage identity changed")
        need(row.get("originalZipRetainedPrivate") is True,"Protected source falsely promoted as public")
        need(row.get("recordedOutcomeClasses")== (KINDS if i<3 else []),
             "Original observed class labels altered")
        need(row.get("originalRecordEntriesCrossChecked")==(3 if i<3 else 0),
             "Original record counts altered")
        need(row.get("recordedDisposition")=="GO_WITH_CONSTRAINTS",
             "Archived qualification limits removed")
        need(row.get("actualExternalEffectEstablished") is False,
             "Uninstrumented source result falsely marked as external effect")
    need(data.get("recordedCaseEntriesAcrossThreeSourceArchives")==9,
         "Record entries silently reclassified/count changed")
    for flag in (
        "archiveCopiesOrVersionsDoNotEqualPilots","connectedV1V2ShareSameRunId",
        "connectedV1V2RecordedLatenciesRevised","readinessV2ReportedLatencyMatchesConnectedV2",
        "threeDecisionClassesRemainConsistentWithinEachOriginal",
        "sourceReplayFieldsAssertedAsHeld"
    ):
        need(data.get(flag) is True,"Required historic revision/provenance constraint missing: "+flag)
    for flag in (
        "differentConnectedRunsEstablishedBetweenV1V2",
        "replayFreshlyExecutedAgainstNativeRuntime",
        "receiptSignaturesIndependentlyCryptographicallyValidated",
        "externalProtectedEffectsIndependentlyMeasured",
        "qualifiedThirdPartyExaminerIdentityEstablishedBySource",
        "originalPilotRunPubliclyReleased",
        "publicOriginalPilotCarrierRegisterChanged"
    ):
        need(data.get(flag) is False,"Unsupported source-to-effect promotion: "+flag)
    for flag in ("originalZipBytesUploaded","privateZipHashesPublished",
                 "customerOrClinicalRecordsPublished","originalRunIdsPublished",
                 "thirdPartyPrivateIdentitiesPublished"):
        need(data.get("privacy",{}).get(flag) is False,"Release clearance error: "+flag)
    original=json.loads((ROOT/"proofs/historical/PUBLIC-CARRIER-REGISTER.json").read_text(encoding="utf-8"))
    need(original["entries"]==[], "New admitted original requires independent authorization, not implicit promotion")
    return 9

def main():
    record=json.loads((ROOT/"proofs/HISTORICAL-RUN-RECONCILIATION.json").read_text(encoding="utf-8"))
    n=check(record)
    print("PASS: original privately retained connected-run record reconciliation; entries:",n)
    print("PASS: same-run v1/v2 provenance preserved; no witness, native effect or unauthorized source release")

if __name__=="__main__":
    main()
