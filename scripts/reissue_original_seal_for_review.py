#!/usr/bin/env python3
"""Make a NEW private data-only archive whose SHA-256 index covers every source.

Never replaces an original, executes its contents, authenticates historic freeze
chronology, observes external effects or grants publication/production standing.
"""
import argparse
import hashlib
import json
import os
import re
import stat
from datetime import date
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZIP_DEFLATED, BadZipFile

MAX_MEMBERS=300
MAX_MEMBER=10_000_000
MAX_TOTAL=80_000_000
HEX=re.compile(r"^[a-f0-9]{64}$")
INDEX="RELEASE_HASHES.json"
PROVENANCE="CUSTODY_REISSUE_PROVENANCE.json"


def require(ok, msg):
    if not ok: raise ValueError(msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(data):
    return (json.dumps(data,sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode("utf-8")


def unpack_original(original, expected_sha):
    original=Path(original).absolute()
    require(original.is_file() and not original.is_symlink(),"Original source missing or symlinked")
    require(isinstance(expected_sha,str) and HEX.fullmatch(expected_sha),
            "A separately fixed original SHA-256 is required")
    before=original.stat()
    require(0<before.st_size<=MAX_TOTAL,"Original ZIP exceeds file limit")
    raw_zip=original.read_bytes()
    require(sha(raw_zip)==expected_sha,"Original bytes differ from separately fixed source SHA-256")
    require(original.stat().st_mtime_ns==before.st_mtime_ns,"Original changed during source read")
    members={}
    with ZipFile(original) as z:
        info=z.infolist()
        require(2<=len(info)<=MAX_MEMBERS,"Original archive member count invalid")
        require(len(set(i.filename for i in info))==len(info),"Duplicate original archive names")
        size=0
        for entry in info:
            name=entry.filename
            pp=PurePosixPath(name)
            require(name and len(name)<300 and not pp.is_absolute() and
                    ".." not in pp.parts and "\\" not in name and not entry.is_dir(),
                    "Unsafe original member path")
            require(entry.flag_bits&1==0,"Encrypted original member refused")
            require(stat.S_IFMT(entry.external_attr>>16)!=stat.S_IFLNK,
                    "Original symlink refused")
            require(0<=entry.file_size<=MAX_MEMBER,"Oversized source member")
            size+=entry.file_size
            require(size<=MAX_TOTAL,"Source expansion over limit")
            members[name]=(entry,z.read(entry))
    require(INDEX in members,"Original source release manifest absent")
    require(PROVENANCE not in members,"Origin already contains reserved reissue identity")
    try:
        original_index=json.loads(members[INDEX][1].decode("utf-8"))
    except (ValueError, UnicodeError) as e:
        raise ValueError("Unreadable original release index") from e
    require(isinstance(original_index,dict),"Original index must be object")
    require(all(isinstance(n,str) and isinstance(v,str) and HEX.fullmatch(v)
                for n,v in original_index.items()),
            "Invalid declared original SHA-256 index")
    content={n:raw for n,(_,raw) in members.items() if n!=INDEX}
    declared=set(original_index)
    require(INDEX not in declared,"Circular hash entry disallowed")
    mismatched=sorted(n for n in declared & set(content)
                      if original_index[n]!=sha(content[n]))
    missing=sorted(declared-set(content))
    unindexed=sorted(set(content)-declared)
    # This creates a specifically described correction candidate, not another
    # original. We refuse to reissue already fully sealed archives needlessly.
    require(mismatched or missing or unindexed,"Original already has complete hash closure")
    return original, members, original_index, content, mismatched, missing, unindexed


def reissue(original, expected_sha, output, edition):
    require(isinstance(edition,str) and re.fullmatch(r"20[0-9]{2}-[01][0-9]-[0-3][0-9]",edition),
            "Edition must be an explicit calendar date YYYY-MM-DD")
    date.fromisoformat(edition)
    origin, members, original_index, content, mismatched, missing, unindexed=unpack_original(original,expected_sha)
    dest=Path(output).absolute()
    require(not dest.exists() and not dest.is_symlink(),"Derivative destination exists or is symlink")
    require(dest!=origin and dest.parent!=origin.parent,
            "Use separate private custody directory; do not overwrite or co-locate original")
    require(dest.suffix.lower()==".zip","Derivative should retain ZIP extension")
    provenance={
        "schema":"va-private-derived-review-seal/1.0",
        "classification":"PRIVATE_REVIEW_DERIVATIVE_NOT_ORIGINAL_RELEASE",
        "edition":edition,
        "originalArchiveSHA256":expected_sha,
        "originalArchiveBytes":origin.stat().st_size,
        "originalFileCount":len(members),
        "originalHashIndexSHA256":sha(members[INDEX][1]),
        "originalSourceMemberBytesUnchanged":True,
        "originalSealDisposition":"HOLD_ORIGINAL_UNCHANGED",
        "originalHashMismatchPaths":mismatched,
        "originalDeclaredButMissing":missing,
        "originalUnindexedPaths":unindexed,
        "modifiedMemberNames":[INDEX,PROVENANCE],
        "nativeVAIndependentWitnessAuthenticated":False,
        "outsideEffectInstrumented":False,
        "historicalFreezeChronologyEstablished":False,
        "publicReleaseAuthorized":False,
        "productionReleaseQualified":False
    }
    provenance_raw=json_bytes(provenance)
    source={**content,PROVENANCE:provenance_raw}
    new_index=json_bytes({n:sha(v) for n,v in sorted(source.items())})
    try:
        with ZipFile(dest,"x",ZIP_DEFLATED,compresslevel=9) as z:
            for name,(meta,raw) in members.items():
                z.writestr(meta,new_index if name==INDEX else raw)
            z.writestr(PROVENANCE,provenance_raw,compress_type=ZIP_DEFLATED)
        os.chmod(dest,0o600)
        # Verify each original source member's payload against the ORIGINAL
        # archive and full new seal against new archive BEFORE saying success.
        with ZipFile(dest) as z:
            newnames=z.namelist()
            require(len(newnames)==len(source)+1 and len(set(newnames))==len(newnames),
                    "Derived package member count changed")
            newfiles={n:z.read(n) for n in newnames if n!=INDEX}
            newhashes=json.loads(z.read(INDEX))
            require(set(newfiles)==set(newhashes) and
                    all(sha(raw)==newhashes[name] for name,raw in newfiles.items()),
                    "Derived archive hash closure failed")
            require(all(newfiles[n]==raw for n,raw in content.items()),
                    "Historic source member data changed in review derivative")
            require(json.loads(newfiles[PROVENANCE])==provenance,
                    "Derivative provenance mismatch")
        require(sha(origin.read_bytes())==expected_sha,"Historical original changed after reissue")
    except BaseException:
        if dest.exists(): dest.unlink()
        raise
    return {
        "result":"PRIVATE_DERIVED_MEMBER_HASH_CLOSURE_PASS",
        "originalHashIntegrityStatus":"HOLD_UNCHANGED",
        "originalZipSHA256":expected_sha,
        "newDerivedZipSHA256":sha(dest.read_bytes()),
        "originalSourceMembersPreserved":len(content),
        "derivedHashEntries":len(source),
        "derivedMemberHashMatches":len(source),
        "originalHashMismatches":len(mismatched),
        "originalUnindexedFiles":len(unindexed),
        "originalDeclaredButMissing":len(missing),
        "originalBytesMutated":False,
        "archivedCodeExecuted":False,
        "nativeIndependentWitnessQualified":False,
        "historicalFreezeDateAuthenticated":False,
        "externalEffectObserved":False,
        "redistributionAuthorized":False
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--original",required=True)
    p.add_argument("--expected-original-sha256",required=True,
                   help="Pinned digest from earlier separate custody; never derived afresh from applicant input")
    p.add_argument("--out",required=True,help="New PRIVATE ZIP in separate directory; never overwritten")
    p.add_argument("--edition",required=True,help="Explicit date labeling the new derivative, not original freeze")
    args=p.parse_args()
    try:
        report=reissue(args.original,args.expected_original_sha256,args.out,args.edition)
        print(json.dumps(report,indent=2))
    except (ValueError,KeyError,TypeError,UnicodeError,OSError,BadZipFile) as exc:
        p.exit(2,"REFUSED: "+str(exc)+"\n")


if __name__=="__main__": main()
