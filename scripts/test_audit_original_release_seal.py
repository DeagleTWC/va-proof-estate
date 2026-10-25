#!/usr/bin/env python3
"""Synthetic regressions for the original-release candidate hash closure auditor."""
import hashlib
import json
import tempfile
import warnings
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from audit_original_release_seal import examine

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def write_archive(p, files, index, duplicate=False, unsafe=False):
    with ZipFile(p, "w", ZIP_DEFLATED) as z:
        for n, data in files.items():
            z.writestr(n, data)
        z.writestr("RELEASE_HASHES.json", (json.dumps(index, indent=2)+"\n").encode())
        if duplicate:
            z.writestr("runtime/source.js", files["runtime/source.js"])
        if unsafe:
            z.writestr("../escape.js", b"attack")

def expect_fail(p, reason, fixed=None):
    try:
        obj = examine(p, fixed_archive_sha=fixed)
        if obj["result"] != "INTERNAL_SOURCE_HASH_CLOSURE_PASS":
            return obj
    except (ValueError, TypeError):
        return None
    raise AssertionError("False ZIP seal admitted: " + reason)

def main():
    files={
        "runtime/source.js": b"// SYNTHETIC non-operational original\n",
        "docs/CHANGELOG.md": b"synthetic written revision history\n",
        "proof/receipt.json": b'{"synthetic": true}\n'
    }
    index={n:digest(d) for n,d in files.items()}
    with tempfile.TemporaryDirectory(prefix="M18_SYNTHETIC_ZIP_SEAL_") as temp:
        root=Path(temp)
        good=root/"synthetic-valid.zip"
        write_archive(good,files,index)
        sha=digest(good.read_bytes())
        passed=examine(good,fixed_archive_sha=sha)
        assert passed["result"]=="INTERNAL_SOURCE_HASH_CLOSURE_PASS"
        assert passed["verifiedMemberHashes"]==3 and passed["archiveMembers"]==4
        assert passed["qualifiedNativeVAWitnessAuthenticated"] is False
        assert passed["observedExternalConsequenceVerified"] is False
        assert passed["sourceRedistributionAuthorized"] is False
        expect_fail(good,"incorrect independently pinned archived digest",fixed="0"*64)
        altered=dict(files);altered["docs/CHANGELOG.md"]=b"altered after release\n"
        a=root/"altered.zip";write_archive(a,altered,index)
        assert expect_fail(a,"mismatch")["registeredButDigestMismatch"] == ["docs/CHANGELOG.md"]
        uncovered=dict(files);uncovered["runtime/independent_verifier.js"]=b"// unindexed code\n"
        u=root/"unindexed-source.zip";write_archive(u,uncovered,index)
        status=expect_fail(u,"unindexed executable")
        assert status["unindexedExecutableMembers"]==["runtime/independent_verifier.js"]
        untouched=dict(files);untouched["docs/UNLISTED.md"]=b"not registered"
        x=root/"unlisted-doc.zip";write_archive(x,untouched,index)
        assert expect_fail(x,"unindexed non-code")["unindexedOriginalMembers"]==["docs/UNLISTED.md"]
        missing=dict(files);missing.pop("proof/receipt.json")
        m=root/"missing-receipt.zip";write_archive(m,missing,index)
        assert expect_fail(m,"indexed but missing")["declaredButMissing"]==["proof/receipt.json"]
        selfref=dict(index);selfref["RELEASE_HASHES.json"]="0"*64
        s=root/"manifest-recursion.zip";write_archive(s,files,selfref)
        expect_fail(s,"self-referential digest")
        forged={n:digest(d) for n,d in altered.items()}
        new_archive=root/"recomputed-new-archive.zip"
        write_archive(new_archive,altered,forged)
        # An internally consistent re-seal does not authenticate history:
        # separately pinned original ZIP digest must reject replacement.
        assert examine(new_archive)["result"]=="INTERNAL_SOURCE_HASH_CLOSURE_PASS"
        expect_fail(new_archive,"re-sealed historic substitution",fixed=sha)
        wrong_hash=dict(index);wrong_hash["runtime/source.js"]="invalid-sha"
        h=root/"bad-hash.zip";write_archive(h,files,wrong_hash)
        expect_fail(h,"invalid declared digest")
        duplicate=root/"duplicate-member.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",UserWarning)
            write_archive(duplicate,files,index,duplicate=True)
        expect_fail(duplicate,"duplicate member path")
        traversal=root/"traversal.zip";write_archive(traversal,files,index,unsafe=True)
        expect_fail(traversal,"path traversal")
        print("PASS: 3-member synthetic release closure with optional pinned archive SHA-256")
        print("PASS: 10 false-seal, stale-index, unregistered-code, tamper and historic-substitution regressions")
        print("PASS: no native V.A. witness, real-world consequence or source redistribution granted")

if __name__ == "__main__":
    main()
