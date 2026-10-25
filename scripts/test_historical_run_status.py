#!/usr/bin/env python3
"""Synthetic attacks against original historical run claims, identity, rights and independence."""
import copy
import json
from validate_historical_run_status import ROOT,check

def refuse(obj, why):
    try:
        check(obj)
    except (ValueError,KeyError,TypeError):
        return
    raise AssertionError("Unsupported historical source promotion accepted: "+why)

def main():
    d=json.loads((ROOT/"proofs/HISTORICAL-RUN-RECONCILIATION.json").read_text(encoding="utf-8"))
    assert check(d)==9
    cases=[
        ("recorded runs become distinct pilots",lambda x:x.update(differentConnectedRunsEstablishedBetweenV1V2=True)),
        ("connected IDs falsely unlinked",lambda x:x.update(connectedV1V2ShareSameRunId=False)),
        ("independent verifier assigned",lambda x:x.update(qualifiedThirdPartyExaminerIdentityEstablishedBySource=True)),
        ("signed chain fabricated",lambda x:x.update(receiptSignaturesIndependentlyCryptographicallyValidated=True)),
        ("native replay fabricated",lambda x:x.update(replayFreshlyExecutedAgainstNativeRuntime=True)),
        ("real external effect invented",lambda x:x.update(externalProtectedEffectsIndependentlyMeasured=True)),
        ("version difference erased",lambda x:x.update(connectedV1V2RecordedLatenciesRevised=False)),
        ("readiness mismatch suppressed",lambda x:x.update(readinessV2ReportedLatencyMatchesConnectedV2=False)),
        ("run receipts called production pilot",lambda x:x["sourceFamilies"][0].update(stage="PRODUCTION_PILOT_PASS")),
        ("source falsely released",lambda x:x.update(originalPilotRunPubliclyReleased=True)),
        ("private customer data posted",lambda x:x["privacy"].update(customerOrClinicalRecordsPublished=True)),
        ("GO WITH CONSTRAINTS erased",lambda x:x["sourceFamilies"][2].update(recordedDisposition="PASS_UNCONDITIONAL")),
        ("nine records called nine pilots",lambda x:x.update(archiveCopiesOrVersionsDoNotEqualPilots=False)),
        ("simulation silently promoted",lambda x:x["sourceFamilies"][0].update(actualExternalEffectEstablished=True)),
    ]
    for name,mutate in cases:
        bad=copy.deepcopy(d);mutate(bad);refuse(bad,name)
    print("PASS:",len(cases),"synthetic publication standing/release/provenance false promotions refused")

if __name__=="__main__":
    main()
