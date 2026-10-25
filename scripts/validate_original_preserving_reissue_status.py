#!/usr/bin/env python3
"""Public original-vs-derived review status invariant, with no new witness standing."""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def need(ok,msg):
    if not ok:raise ValueError(msg)

def validate(d):
    need(d.get("schema")=="va-original-preserving-derived-seal/1.0"
         and d.get("milestone")==19, "Unexpected review derivative register")
    need(d.get("evidenceCategory")==
         "HISTORIC_RELEASE_ARCHIVE_INTEGRITY_DERIVATIVE_NOT_ORIGINAL_NATIVE_WITNESS",
         "Original review object category was changed")
    orig=d.get("original")
    der=d.get("derivative")
    wit=d.get("independentQualification")
    need(isinstance(orig,dict) and isinstance(der,dict) and isinstance(wit,dict),
         "Source / derivative / witness separation missing")
    for f in ("originalArchivePreserved","originalCopiesUnchanged"):
        need(orig.get(f) is True,"Historical original record mutated")
    vals={"originalSourceContentMembers":56,"originallyIndexedMembers":55,
          "originallyMatchingHashes":54,"originallyMismatchingHashes":1,
          "originallyUnindexedMembers":1}
    for f,n in vals.items():need(type(orig.get(f)) is int and orig[f]==n,"Original evidence historical count changed")
    need(orig.get("originalArchiveStatus")=="HOLD_UNCHANGED",
         "Original historic integrity HOLD wrongly cleared")
    for f in ("historicalFreezeAuthenticatedByNewDerivative","exactPrivateOriginalDigestPublished"):
        need(orig.get(f) is False,"Unsupported original claim/public disclosure")
    for f in ("createdUnderPrivateCustody","newIndependentArtifactIdentity","reviewPurposeOnly",
              "originalSourceMemberPayloadsByteIdentical","newCustodyProvenanceRecordAdded",
              "newHashIndexCoversAllMembersExceptItself","newArchiveExactDigestRetainedPrivate"):
        need(der.get(f) is True,"Derived private review custody lost: "+f)
    vals={"originalContentMembersRetained":56,"indexedMembers":57,"matchingSHA256Entries":57,
          "missingIndexEntries":0,"sourceMemberAlterations":0}
    for f,n in vals.items():need(type(der.get(f)) is int and der[f]==n,"Derived source member count changed")
    need(der.get("localDerivativeSealResult")=="PASS_PRIVATE_DERIVED_MEMBER_HASH_CLOSURE_ONLY",
         "Derived hash closure improperly promoted")
    for f in ("derivativePubliclyReleased","derivedRuntimeRerun"):
        need(der.get(f) is False,"Derived source or original code execution was falsely published")
    for f in ("externalEffectMeasuredByDerivative","cryptographicIndependentHumanIdentityEstablished",
              "nativeV12StandingInherited","originalHistoricReleaseHOLDOverturned",
              "independentNativeVAPublicCarrierAdmitted"):
        need(wit.get(f) is False,"Unsupported native V.A. standing: "+f)
    need(wit.get("actualHistoricPilotCount")=="NOT DETERMINED","Historical pilots falsely counted")
    need(d.get("disclosure")=="ORIGINAL_AND_DERIVATIVE_BYTES_PRIVATE_NOT_RELEASE_APPROVED"
         and d.get("noAutomaticPromotion") is True,
         "Source release or historic promotion permission fabricated")
    old=json.loads((ROOT/"proofs/NATIVE-WITNESS-ORIGINAL-CANDIDATE-STATUS.json").read_text(encoding="utf-8"))
    need(old.get("currentStage")=="SOURCE_ORIGINAL_INTEGRITY_HOLD"
         and old.get("internalCandidateSourceSealQualified") is False,
         "Milestone 18 original archive HOLD must remain unchanged")
    reg=json.loads((ROOT/"proofs/historical/PUBLIC-CARRIER-REGISTER.json").read_text(encoding="utf-8"))
    need(reg.get("entries")==[],"Original or derivative privately held release was admitted without authority")
    return 57

if __name__=="__main__":
    data=json.loads((ROOT/"proofs/ORIGINAL-PRESERVING-REISSUE-STATUS.json").read_text(encoding="utf-8"))
    print("PASS: independently derived member hash count:",validate(data))
    print("PASS: historical original HOLD and private custody unchanged; no witness standing promoted")
