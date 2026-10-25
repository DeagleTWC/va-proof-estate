#!/usr/bin/env python3
"""Preflight exact bytes of a proposed PUBLIC-SAFE evidence extract.

This is a private, read-only STRUCTURAL CHECK. It cannot determine whether
permissions are genuine, human reviewers exist, metadata leaks information,
or the evidence is safe. Actual signed human source, rights and safety
approvals are mandatory separately before anyone publishes material.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

HEX=re.compile(r"^[0-9a-f]{64}$")
ROLES=("custody","rights","safety")
SAFE_DECISIONS=("RELEASE","NARROW")
MAX_BYTES=20_000_000

def require(ok,msg):
    if not ok:raise ValueError(msg)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def safe_file(root,relative):
    require(isinstance(relative,str) and relative and len(relative)<240
            and "\\" not in relative,"Unsafe staged file reference")
    p=Path(relative)
    require(not p.is_absolute() and ".." not in p.parts and p.as_posix()==relative,
            "Staged file reference escapes custody")
    path=root
    for component in p.parts:
        path=path/component
        require(not path.is_symlink(),"Staged source symlinks refused")
    require(path.resolve().is_relative_to(root) and path.is_file(),
            "Staged evidence file missing")
    require(0<path.stat().st_size<=MAX_BYTES,"Staged file size invalid")
    before=path.stat()
    data=path.read_bytes()
    require(path.stat().st_mtime_ns==before.st_mtime_ns
            and path.stat().st_size==before.st_size,"Source file changed while inspected")
    return data

def check(manifest,root,original):
    require(isinstance(manifest,dict) and manifest.get("schema")=="va-private-disclosure-review/1.0",
            "Invalid exact-byte candidate schema")
    require(manifest.get("status") in SAFE_DECISIONS
            and manifest.get("releaseAuthorized") is True,
            "Release must have completed explicit decision")
    original_hash=manifest.get("originalSHA256")
    extract_hash=manifest.get("extractSHA256")
    require(isinstance(original_hash,str) and HEX.fullmatch(original_hash)
            and isinstance(extract_hash,str) and HEX.fullmatch(extract_hash),
            "Actual original and extract SHA-256 identities are required")
    original=Path(original).absolute()
    require(original.is_file() and not original.is_symlink()
            and original.stat().st_size<=MAX_BYTES,"Original carrier unavailable")
    require(digest(original.read_bytes())==original_hash,
            "Actual historical original bytes do not match original custody identity")
    relative=manifest.get("extractRelativePath")
    released= safe_file(root,relative)
    require(digest(released)==extract_hash,"Exact proposed public bytes do not match approval candidate")
    require(original.resolve()!=(root/relative).resolve()
            and original_hash!=extract_hash,"Original and extract must be separate objects")
    require(manifest.get("originalRetained") is True,
            "The original historical carrier cannot be overwritten")
    require(isinstance(manifest.get("candidateId"),str)
            and 4<=len(manifest["candidateId"])<=128
            and manifest.get("claim") not in ("UNFILLED",None,""),
            "Precise bounded claim and candidate identity required")
    for gate in ("rightsApproved","safetyApproved","privacyApproved","custodyApproved"):
        require(manifest.get(gate) is True,"Missing human clearance gate: "+gate)
    require(manifest.get("reviewerIndependenceVerified") is True,
            "Actual separate reviewer qualification required for this public release type")
    require(manifest.get("dangerousConstructionExcluded") is True
            and manifest.get("linkageAndReconstructionRiskReviewed") is True
            and manifest.get("negativeFindingsRetained") is True,
            "Protection, cross-document linkage or inconvenient outcome transparency gate missing")
    require(isinstance(manifest.get("scopeOfPermission"),str)
            and len(manifest["scopeOfPermission"].strip())>=15,
            "Specific written release authorization scope required")
    require(isinstance(manifest.get("releaseLimitations"),str)
            and len(manifest["releaseLimitations"].strip())>=12,
            "Exact claim limits and negative routes must be disclosed")
    reviews=manifest.get("reviews")
    require(isinstance(reviews,dict) and set(reviews)==set(ROLES),
            "Three explicit original, rights and safety review records required")
    identities=[]
    for role in ROLES:
        record=reviews[role]
        require(isinstance(record,dict) and record.get("approved") is True
                and record.get("candidateSHA256")==extract_hash,
                "Review is not explicitly approved for exact proposed release bytes: "+role)
        require(isinstance(record.get("reviewerId"),str) and
                4<=len(record["reviewerId"])<=120,"Reviewer role identity absent")
        require(isinstance(record.get("authorizationRef"),str)
                and 6<=len(record["authorizationRef"])<=200,
                "Documented review authority/custody reference absent")
        identities.append(record["reviewerId"])
    require(len(set(identities))==3,
            "Source custody, permission and safety reviews require distinct reviewers")
    return {
        "result":"EXACT_BYTES_AND_DECLARED_REVIEW_GATES_CONSISTENT_HUMAN_VALIDATION_STILL_REQUIRED",
        "candidateMatched":True,
        "originalMatched":True,
        "threeDistinctDeclaredReviewers":True,
        "actualHumanIdentityCryptographicallyAuthenticated":False,
        "actualPermissionsLegallyAuthenticatedByThisTool":False,
        "dangerOfPublicationDeterminedByThisTool":False,
        "independentEffectMeasuredByThisTool":False,
        "filePublishedByThisTool":False
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest",required=True,help="PRIVATE reviewed candidate manifest, never commit completed manifest")
    p.add_argument("--staging-root",required=True,help="Private folder containing the exact proposed public extract")
    p.add_argument("--original",required=True,help="Unmodified privately held original whose SHA-256 predates candidate")
    args=p.parse_args()
    try:
        root=Path(args.staging_root).resolve()
        require(root.is_dir(),"Staging source directory unavailable")
        manifest_file=Path(args.manifest).absolute()
        require(manifest_file.is_file() and not manifest_file.is_symlink()
                and not manifest_file.resolve().is_relative_to(root),
                "Private approval manifest must not be staged as a public extract")
        doc=json.loads(manifest_file.read_text(encoding="utf-8"))
        print(json.dumps(check(doc,root,args.original),indent=2))
    except (OSError,ValueError,TypeError,KeyError,UnicodeError) as e:
        p.exit(2,"REFUSED: "+str(e)+"\n")

if __name__=="__main__":
    main()
