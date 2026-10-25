#!/usr/bin/env python3
"""Reject false publication/operational promotion of recovered TMU staging originals."""
import copy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def need(ok,msg):
    if not ok:raise ValueError(msg)

def validate(d):
    need(d.get("schema")=="va-tmu-recorded-staging-evidence-candidate/1.0",
         "Wrong original saved staging evidence schema")
    need(d.get("sourceRecordClass")=="HISTORICAL_SAVED_STAGING_GATE_AND_RECEIPT_LOGS",
         "Staging source reclassified without actual native/external evidence")
    need(d.get("sourceRecordPack")=="TMU_One_Path_Proof_Pack"
         and d.get("sourceRecordPackVersion")=="v1.2_FULL_ENV",
         "Wrong source package identity")
    need(d.get("reportedEnvironment")=="staging_docker",
         "Staging result promoted to production")
    for field,n in (
        ("originalEmailAttachmentsLocated",7),("originalMetadataFilesLocated",1),
        ("originalGateLogFilesLocated",5),("originalReceiptBundleLocated",1),
        ("savedReceiptsFound",2),("savedReplayOutcomeClassComparisonsReported",2)
    ):
        need(type(d.get(field)) is int and d[field]==n,
             "Missing or inflated original source count: "+field)
    need(d.get("savedDecisionClasses")==["EXECUTE","REFUSE"],
         "Source decision-class and no-effect distinction changed")
    need(d.get("fiveGateOutputsReportedPass") is True
         and d.get("originalReceiptBundleMatchesRecordedCaseIdentifiers") is True,
         "Newly recovered original source/receipt binding erased")
    need(d.get("recordedTotalSpansMilliseconds")=={"execute":142,"refuse":67}
         and d.get("recordedCommitSubspansMilliseconds")=={"execute":38,"refuse":12},
         "Reported historical staging time samples falsified")
    for key in ("originalArtifactBytesRetainedPrivate",
                "originalArtifactHashesRetainedPrivate",
                "noNewPublicationPermissionGranted","noAutomaticProofPromotion"):
        need(d.get(key) is True,"Original private custodian/source integrity lost: "+key)
    for key in ("separatelyFixedContemporaneousSourceDigestLocated",
                "originalExecutedRuntimeReproducedInThisMilestone",
                "independentNativeVaWitnessAuthenticated",
                "externalEffectAndNonEffectInstrumented",
                "actualTMUCustomerDeploymentEstablished",
                "partnerReleaseRightsConfirmed",
                "exactOutcomeOrReceiptExtractSafetyApproved"):
        need(d.get(key) is False,"Unqualified staging evidence promoted: "+key)
    need(d.get("charterDisposition")=="CONTROLLED_REVIEW_UNTIL_RIGHTS_AND_SAFETY_APPROVAL"
         and d.get("publicCarrierStatus")=="NO_ORIGINAL_RECEIPT_OR_TEST_PAYLOAD_ADMITTED",
         "Unauthorized public original carrier")
    need(d.get("completedRunSourceStatus")=="ORIGINAL_RECORDED_STAGING_TEST_OUTPUTS_FOUND"
         and d.get("tmupilotStatus")=="LIVE_EXTERNAL_TMU_PILOT_NOT_ESTABLISHED_BY_THIS_SOURCE",
         "Recorded staging and actual live pilot conflated")
    need(isinstance(d.get("obligationsBeforeRelease"),list)
         and len(d["obligationsBeforeRelease"])>=6,
         "Exact-byte rights, independent custody and safety duties removed")
    for key in ("relatedMission","relatedExistingTMUStatus","separateHistoricVeritasPilot"):
        value=d.get(key)
        need(isinstance(value,str) and (ROOT/value).is_file(),
             "Source relationship broken: "+key)
    status=json.loads((ROOT/"proofs/TMU-PUBLIC-EVIDENCE-STATUS.json").read_text(encoding="utf-8"))
    need(status.get("historicalRecordedStagingSourceFilesRecovered")==7
         and status.get("historicalRecordedReceiptBundleRecovered") is True
         and status.get("historicalRecordedReceiptBundleReceiptCount")==2
         and status.get("historicalStagingEvidenceSource")=="proofs/TMU-RECORDED-STAGING-CANDIDATE.json",
         "Original seven-file source recovery missing from existing candidate status")
    for key in ("historicalSourceSHA256AuthenticatedAtOriginalFreeze",
                "originalPartnerTMULiveEffectWitnessEstablished",
                "historicalRawTMUReceiptSourceApprovedForPublicRelease"):
        need(status.get(key) is False,
             "Existing TMU review status falsely certified")
    admitted=json.loads((ROOT/"proofs/historical/PUBLIC-CARRIER-REGISTER.json").read_text(encoding="utf-8"))
    need(admitted.get("entries")==[],
         "Raw original pilot carrier admitted without exact rights and safety review")
    return 7

def main():
    obj=json.loads((ROOT/"proofs/TMU-RECORDED-STAGING-CANDIDATE.json").read_text(encoding="utf-8"))
    assert validate(obj)==7
    mutations=[
      ("real TMU production invented",lambda v:v.update(actualTMUCustomerDeploymentEstablished=True)),
      ("independent witness invented",lambda v:v.update(independentNativeVaWitnessAuthenticated=True)),
      ("measured external effect invented",lambda v:v.update(externalEffectAndNonEffectInstrumented=True)),
      ("source original rights falsely granted",lambda v:v.update(partnerReleaseRightsConfirmed=True)),
      ("original release safety falsely approved",lambda v:v.update(exactOutcomeOrReceiptExtractSafetyApproved=True)),
      ("raw records assumed public",lambda v:v.update(publicCarrierStatus="LIVE_NATIVE_PROOF_PUBLISHED")),
      ("retrieved receipt bundle erased",lambda v:v.update(originalReceiptBundleLocated=0)),
      ("different recorded case count",lambda v:v.update(savedReceiptsFound=4)),
      ("historical source type changed",lambda v:v.update(sourceRecordClass="NATIVE_V12_PRODUCTION_RUN")),
      ("staging relabeled production",lambda v:v.update(reportedEnvironment="production")),
      ("external review self-authenticated",lambda v:v.update(charterDisposition="RELEASE")),
      ("runtime allegedly rerun",lambda v:v.update(originalExecutedRuntimeReproducedInThisMilestone=True)),
      ("recorded refusal deleted",lambda v:v.update(savedDecisionClasses=["EXECUTE"])),
      ("historical timestamps altered",lambda v:v.update(recordedTotalSpansMilliseconds={"execute":4,"refuse":8})),
      ("original source byte custody made public",lambda v:v.update(originalArtifactBytesRetainedPrivate=False)),
      ("previous original freeze falsely authenticated",lambda v:v.update(separatelyFixedContemporaneousSourceDigestLocated=True))
    ]
    for reason,fn in mutations:
        v=copy.deepcopy(obj);fn(v)
        try:validate(v)
        except (ValueError,TypeError,KeyError):continue
        raise AssertionError("Unqualified original source claim accepted: "+reason)
    print("PASS: seven original private source items, five PASS reports and two saved receipt paths preserved")
    print("PASS:",len(mutations),"false safety authorization, native deployment, witness and source mutation controls refused")

if __name__=="__main__":main()
