#!/usr/bin/env python3
"""Synthetic public qualification promotion-mutation tests."""
import copy
import json
from validate_independent_witness_status import ROOT,check

def reject(obj,label):
    try:check(obj)
    except (ValueError,KeyError,TypeError):return
    raise AssertionError("Incorrectly accepted false standing: "+label)

def main():
    d=json.loads((ROOT/"proofs/INDEPENDENT-WITNESS-STATUS.json").read_text(encoding="utf-8"))
    assert check(d)
    edits=[
        ("native independent witness fabricated",lambda x:x.update(currentPublishedNativeV12IndependentWitnessCount=2)),
        ("historical independent reviewer fabricated",lambda x:x.update(currentPublishedHistoricalOriginalRunIndependentWitnessCount=2)),
        ("actual M14 effect invented",lambda x:x.update(outsideEffectMeasuredInM14Originals=True)),
        ("M14 signatures retroactively authenticated",lambda x:x.update(cryptographicOriginalReceiptSignatureVerifiedInM14=True)),
        ("human identity fabricated",lambda x:x.update(independentHumanIdentityAuthenticatedInM14=True)),
        ("privately held source published",lambda x:x.update(rawPrivateOriginalsPublished=True)),
        ("public original release falsely granted",lambda x:x.update(publicDisclosureAuthorityForOriginalCustomerRecords=True)),
        ("historic verification erased",lambda x:x.update(historicalEngineeringSourceReproducedInPrivateCustody=False)),
        ("historical version counted twice",lambda x:x.update(archivedConnectedV1V2ShareSameRun=False)),
        ("new applicant preflight declared independent",lambda x:x.update(localSignedRecordCheckResultCeiling="INDEPENDENTLY_REPRODUCED")),
        ("human review status fabricated",lambda x:x.update(disposition="APPROVED_FOR_PRODUCTION")),
        ("public carrier falsely admitted",lambda x:x.update(independentWitnessPacketAdmittedToPublicCarrierRegister=True)),
        ("history miscounted",lambda x:x.update(explicitHistoricalPilotCount=0)),
        ("standings automatic",lambda x:x.update(noAutomaticStandingPromotion=False)),
    ]
    for label,mut in edits:
        v=copy.deepcopy(d);mut(v);reject(v,label)
    print("PASS:",len(edits),"unsupported independent witness, source and effect promotions rejected")

if __name__=="__main__":
    main()
