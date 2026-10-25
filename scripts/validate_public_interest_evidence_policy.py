#!/usr/bin/env python3
"""Assert the controlling public-interest evidence policy is truthful and privacy-safe."""
import copy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ID=["scientific","engineering","historical_pilots","independent_safety","TMU"]
def need(cond,msg):
    if not cond:raise ValueError(msg)

def validate(policy,tmu):
    need(policy.get("schema")=="va-public-interest-evidence-pipeline/1.0","Wrong charter schema")
    need(policy.get("charterVersion")=="2026-10-25","Charter revision not recorded")
    need(policy.get("sourcePolicy")=="proofs/PUBLIC-INTEREST-PUBLICATION-CHARTER.md"
         and (ROOT/policy["sourcePolicy"]).is_file(),"Controlling charter source missing")
    priorities=policy.get("priorityOrder")
    need(isinstance(priorities,list) and len(priorities)>=4 and
         priorities[0]=="PREVENT_HARM_AND_OBEY_LAWFUL_DISCLOSURE_AUTHORITY" and
         "MAXIMIZE_INDEPENDENTLY_VERIFIABLE_FUNCTIONAL_EVIDENCE" in priorities,
         "Proof/harms priority changed")
    need(policy.get("commercialExclusivityAloneBlocksSafeEvidence") is False,
         "Commercial exclusivity must not suppress safe demonstrable evidence")
    for k in ("publicationMustBindExactProposedBytes",
              "humanCustodySafetyRightsReviewRequired",
              "redactedExtractHasDistinctSHA256FromOriginal",
              "independentReviewMustBeAuthenticatedWhenClaimed",
              "documentedNegativeOutcomesRetained"):
        need(policy.get(k) is True,"Human/independent/safe evidence publication duty removed: "+k)
    for k in ("protectedKernelConstructionIsPublic",
              "dangerousReplicationInformationIsPublic",
              "unreviewedOriginalPilotDataIsPublic"):
        need(policy.get(k) is False,"Unapproved sensitive material classified public: "+k)
    need(policy.get("allowedDispositions")==["RELEASE","NARROW","CONTROLLED_REVIEW",
                                              "HOLD","REFUSE_PUBLICATION"],
         "Cannot erase conditional safe disclosure or genuine HOLD")
    need(policy.get("newReleaseCarriersApprovedByThisCharter")==0,
         "Charter alone cannot approve particular original evidence")
    need(policy.get("reviewTemplate")=="proofs/RELEASE-REVIEW-PRIVATE-TEMPLATE.json"
         and policy.get("reviewTool")=="scripts/preflight_public_interest_release.py",
         "Human exact-byte release review procedure missing")
    families=policy.get("candidateFamilies")
    need(isinstance(families,list) and [x.get("id") for x in families]==ID,
         "Missing complete scientific/engineering/pilot/independent/TMU evidence scope")
    for x in families:
        need(x.get("newOriginalApprovedByThisCharter") is False
             and (ROOT/x.get("source","")).is_file(),
             "Candidate implicitly approved or its source absent")
    need(tmu.get("schema")=="va-tmu-public-evidence-candidate/1.0"
         and tmu.get("classification")=="PUBLIC_SAFE_REVIEW_STATUS_ONLY"
         and tmu.get("publicationEligibility")==
            "CAN_BE_CONSIDERED_FOR_PUBLIC_RELEASE_AFTER_EXACT_EVIDENCE_RIGHTS_CUSTODY_SAFETY_REVIEW",
         "TMU eligibility wrong")
    for flag in ("actualTMUExecutionPacketEstablishedByLocatedPlanningTexts",
                 "originalTMURunReceiptsAdmittedHere","changedConditionOutcomeOriginalsAdmittedHere",
                 "independentTMUWitnessOriginalsAdmittedHere","TMUDisclosureRightsEstablishedHere",
                 "specificProposedExtractApprovedHere","sensitiveParticipantOrKernelDataPublished"):
        need(tmu.get(flag) is False,"TMU source drafting falsely promoted to completed public proof: "+flag)
    need(tmu.get("standing")=="REVIEW_CANDIDATE_ONLY_NO_COMPLETED_TMU_CARRIER_ADMITTED_FROM_PLANNING_TEXT",
         "TMU draft improperly promoted")
    require_original=json.loads((ROOT/"proofs/historical/PUBLIC-CARRIER-REGISTER.json").read_text())
    need(require_original.get("entries")==[],"Separate exact original public carrier admission must occur")
    return len(families)

def main():
    p=json.loads((ROOT/"proofs/PUBLIC-INTEREST-EVIDENCE-PIPELINE.json").read_text(encoding="utf-8"))
    t=json.loads((ROOT/"proofs/TMU-PUBLIC-EVIDENCE-STATUS.json").read_text(encoding="utf-8"))
    assert validate(p,t)==5
    mutations=[
      ("release rights inferred",lambda a,b:a.update(newReleaseCarriersApprovedByThisCharter=1)),
      ("commercial secrecy takes priority",lambda a,b:a.update(commercialExclusivityAloneBlocksSafeEvidence=True)),
      ("human signoff removed",lambda a,b:a.update(humanCustodySafetyRightsReviewRequired=False)),
      ("negative findings erased",lambda a,b:a.update(documentedNegativeOutcomesRetained=False)),
      ("unaltered original promised public",lambda a,b:a.update(unreviewedOriginalPilotDataIsPublic=True)),
      ("harmful reproduction details exposed",lambda a,b:a.update(dangerousReplicationInformationIsPublic=True)),
      ("TMU draft called real run",lambda a,b:b.update(actualTMUExecutionPacketEstablishedByLocatedPlanningTexts=True)),
      ("TMU independent witness fabricated",lambda a,b:b.update(independentTMUWitnessOriginalsAdmittedHere=True)),
      ("TMU rights fabricated",lambda a,b:b.update(TMUDisclosureRightsEstablishedHere=True)),
      ("TMU originals leaked",lambda a,b:b.update(sensitiveParticipantOrKernelDataPublished=True)),
      ("conditional narrow removed",lambda a,b:a.update(allowedDispositions=["RELEASE","HOLD"])),
      ("original scientific lane dropped",lambda a,b:a["candidateFamilies"].pop(0))
    ]
    for msg,fn in mutations:
        a,b=copy.deepcopy(p),copy.deepcopy(t)
        fn(a,b)
        try:validate(a,b)
        except (ValueError,KeyError,TypeError):continue
        raise AssertionError("Unsafe charter mutation accepted: "+msg)
    print("PASS: five priority evidence lanes protected, including TMU review eligibility")
    print("PASS:",len(mutations),"synthetic false authorization, harmful disclosure and outcome suppression regressions")

if __name__=="__main__":main()
