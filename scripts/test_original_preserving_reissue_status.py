#!/usr/bin/env python3
"""Synthetic regressions for protecting the historic original from false reissue standing."""
import copy
import json
from validate_original_preserving_reissue_status import ROOT,validate

def reject(d,label):
    try:validate(d)
    except (ValueError,TypeError,KeyError):return
    raise AssertionError("Incorrect standing admitted: "+label)

def main():
    base=json.loads((ROOT/"proofs/ORIGINAL-PRESERVING-REISSUE-STATUS.json").read_text(encoding="utf-8"))
    assert validate(base)==57
    edits=[
      ("old historic HOLD rewritten",lambda d:d["original"].update(originalArchiveStatus="PASS")),
      ("original count falsely changed",lambda d:d["original"].update(originallyMatchingHashes=55)),
      ("historical freeze authenticated by new archive",lambda d:d["original"].update(historicalFreezeAuthenticatedByNewDerivative=True)),
      ("old original changed",lambda d:d["original"].update(originalCopiesUnchanged=False)),
      ("derived no longer distinct",lambda d:d["derivative"].update(newIndependentArtifactIdentity=False)),
      ("not all original files retained",lambda d:d["derivative"].update(originalContentMembersRetained=55)),
      ("member source mutated",lambda d:d["derivative"].update(sourceMemberAlterations=1)),
      ("derivative hash count forged",lambda d:d["derivative"].update(matchingSHA256Entries=58)),
      ("private derivative disclosed without consent",lambda d:d["derivative"].update(derivativePubliclyReleased=True)),
      ("archived runtime falsely rerun",lambda d:d["derivative"].update(derivedRuntimeRerun=True)),
      ("human observer invented",lambda d:d["independentQualification"].update(cryptographicIndependentHumanIdentityEstablished=True)),
      ("native V.A. attributed",lambda d:d["independentQualification"].update(nativeV12StandingInherited=True)),
      ("real effect fabricated",lambda d:d["independentQualification"].update(externalEffectMeasuredByDerivative=True)),
      ("original HOLD falsely overturned",lambda d:d["independentQualification"].update(originalHistoricReleaseHOLDOverturned=True)),
      ("private original hash leaked",lambda d:d["original"].update(exactPrivateOriginalDigestPublished=True)),
      ("historic pilot count fabricated",lambda d:d["independentQualification"].update(actualHistoricPilotCount=0)),
      ("public original release fabricated",lambda d:d.update(disclosure="APPROVED_FOR_PUBLIC_RELEASE"))
    ]
    for label,fn in edits:
        d=copy.deepcopy(base);fn(d);reject(d,label)
    print("PASS:",len(edits),"public historical original/derived/native witness false promotions rejected")

if __name__=="__main__": main()
