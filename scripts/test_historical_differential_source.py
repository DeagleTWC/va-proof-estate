#!/usr/bin/env python3
"""Negative publication mutations for independently authored non-native review source."""
import copy
import json
from validate_historical_differential_source import ROOT,validate

def refuse(d,label):
    try:validate(d)
    except (ValueError,KeyError,TypeError):return
    raise AssertionError("False differential source standing admitted: "+label)

def main():
    original=json.loads((ROOT/"proofs/HISTORICAL-DIFFERENTIAL-SOURCE-REGISTER.json").read_text(encoding="utf-8"))
    assert validate(original)==3
    mutations=[
     ("archive never recovered",lambda d:d.update(historicalOriginalArchivePresentInLibrary=False)),
     ("source PDF different",lambda d:d.update(priorM16OriginalPDFExactBytesMatched=False)),
     ("wrong harness SHA",lambda d:d["reportedSha256MembersChecked"][0].update(sha256="0"*64)),
     ("false result count",lambda d:d["sourceResults"].update(fixedSavedPassCount=7)),
     ("baseline controls falsified",lambda d:d["sourceResults"].update(baselineSavedFailCount=0)),
     ("unmatched test IDs hidden",lambda d:d["sourceResults"].update(sameSixCaseIdsOnBothVersions=False)),
     ("new reenactment fabricated",lambda d:d.update(originalHarnessExecutedInMilestone17=True)),
     ("original environment fabricated",lambda d:d.update(originalRunEnvironmentOrTimestampAuthenticatedInMilestone17=True)),
     ("new native V.A. witness invented",lambda d:d.update(nativeVAIndependentEffectReproduced=True)),
     ("human reviewer invented",lambda d:d.update(independentHumanWitnessIdentityAuthenticatedInMilestone17=True)),
     ("third party work relabeled native",lambda d:d.update(historicalExternalReviewClass="NATIVE_VA")),
     ("private original released",lambda d:d.update(publicArchiveOrOriginalTestBytesAttached=True)),
     ("release approval invented",lambda d:d.update(publicPermissionToRepublishOriginalArchiveOrPDF=True)),
     ("original archive hash leaked",lambda d:d.update(originalArchiveExactHashKeptPrivate=False)),
     ("HOLD rewritten",lambda d:d.update(earlierM16SubmittedCarrierDispositionPreserved="PASS")),
     ("PARTIAL rewritten",lambda d:d.update(historicalReviewerDispositionPreserved="FULL_QUALIFIED")),
     ("same object provenance erased",lambda d:d.update(differentReviewObjectsKeptSeparate=False)),
     ("substituted underlying PyJWT source",lambda d:d["reportedSha256MembersChecked"][1].update(name="other-results.json")),
    ]
    for label,edit in mutations:
        x=copy.deepcopy(original);edit(x);refuse(x,label)
    print("PASS:",len(mutations),"source promotion, hash substitution and unsupported disclosure tests rejected")

if __name__=="__main__":
    main()
