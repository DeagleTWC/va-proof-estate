#!/usr/bin/env python3
"""Synthetic-only exact-byte publication preflight mutation tests."""
import copy
import hashlib
import json
import tempfile
from pathlib import Path
from preflight_public_interest_release import check

def h(x):return hashlib.sha256(x).hexdigest()

def blocked(d,root,original,why):
    try:check(d,root,original)
    except (ValueError,TypeError,KeyError,OSError):return
    raise AssertionError("False public clearance accepted: "+why)

def main():
    with tempfile.TemporaryDirectory(prefix="SYNTHETIC_EVIDENCE_DISCLOSURE_") as tmp:
        base=Path(tmp)
        staging=base/"staging";staging.mkdir()
        original=base/"original.txt";original.write_bytes(b"PRIVATE SYNTHETIC TEST OBJECT; NO REAL OPERATIONS\n")
        candidate=staging/"public-extract.json"
        candidate.write_bytes(b'{"synthetic":true,"result":"refusal observed only in example"}\n')
        oh=h(original.read_bytes());ch=h(candidate.read_bytes())
        roles=["custody","rights","safety"]
        d={
         "schema":"va-private-disclosure-review/1.0",
         "status":"NARROW","candidateId":"SYNTHETIC-001",
         "originalSHA256":oh,"extractRelativePath":"public-extract.json","extractSHA256":ch,
         "claim":"Non-operational synthetic unit example only",
         "rightsApproved":True,"safetyApproved":True,"privacyApproved":True,"custodyApproved":True,
         "reviewerIndependenceVerified":True,"originalRetained":True,"releaseAuthorized":True,
         "dangerousConstructionExcluded":True,"linkageAndReconstructionRiskReviewed":True,
         "negativeFindingsRetained":True,
         "scopeOfPermission":"SYNTHETIC TEST DATA ONLY; no real legal permission represented",
         "releaseLimitations":"No real pilot or technical result represented",
         "reviews":{role:{"approved":True,"reviewerId":"SYNTHETIC-REVIEWER-"+str(i+1),
                         "candidateSHA256":ch,"authorizationRef":"SYNTHETIC-ONLY-"+role+"-REVIEW"}
                     for i,role in enumerate(roles)}
        }
        result=check(d,staging,original)
        assert result["candidateMatched"] and result["originalMatched"]
        assert result["filePublishedByThisTool"] is False
        assert result["actualHumanIdentityCryptographicallyAuthenticated"] is False
        assert result["actualPermissionsLegallyAuthenticatedByThisTool"] is False
        edits=[
            ("unapproved disposition",lambda v:v.update(status="HOLD")),
            ("publication approval false",lambda v:v.update(releaseAuthorized=False)),
            ("old original wrong digest",lambda v:v.update(originalSHA256="0"*64)),
            ("extract digest wrong",lambda v:v.update(extractSHA256="0"*64)),
            ("rights unapproved",lambda v:v.update(rightsApproved=False)),
            ("safety unapproved",lambda v:v.update(safetyApproved=False)),
            ("privacy unapproved",lambda v:v.update(privacyApproved=False)),
            ("custody unapproved",lambda v:v.update(custodyApproved=False)),
            ("danger assessment absent",lambda v:v.update(dangerousConstructionExcluded=False)),
            ("linkage assessment absent",lambda v:v.update(linkageAndReconstructionRiskReviewed=False)),
            ("negative outcomes removed",lambda v:v.update(negativeFindingsRetained=False)),
            ("independent review not qualified",lambda v:v.update(reviewerIndependenceVerified=False)),
            ("exact-byte safety approval mismatch",lambda v:v["reviews"]["safety"].update(candidateSHA256="0"*64)),
            ("consent scope missing",lambda v:v.update(scopeOfPermission="NO")),
            ("claim limits missing",lambda v:v.update(releaseLimitations="")),
            ("rights reviewer absent",lambda v:v["reviews"]["rights"].update(approved=False)),
            ("reviewer roles conflated",lambda v:v["reviews"]["safety"].update(reviewerId="SYNTHETIC-REVIEWER-1")),
            ("historical original discarded",lambda v:v.update(originalRetained=False)),
            ("source swap via traversal",lambda v:v.update(extractRelativePath="../original.txt"))
        ]
        for why,fn in edits:
            v=copy.deepcopy(d);fn(v);blocked(v,staging,original,why)
        before=candidate.read_bytes()
        candidate.write_bytes(before+b"EXTRACT CHANGED AFTER APPROVAL")
        blocked(d,staging,original,"one-byte post-approval extract change")
        candidate.write_bytes(before)
        original.write_bytes(original.read_bytes()+b"ORIGINAL CHANGED")
        blocked(d,staging,original,"original source tamper")
        print("PASS:",len(edits)+2,"synthetic exact-byte, clearance, original and unsafe promotion controls")
        print("PASS: all marked reviewer/permission assertions remain separate HUMAN obligations, not facts")
        print("PASS: code never publishes data or declares an actual safe release")

if __name__=="__main__":main()
