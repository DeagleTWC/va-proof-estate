#!/usr/bin/env python3
"""Fully synthetic original/derivative chain regressions. Never includes protected CASE bytes."""
import hashlib
import json
import tempfile
import warnings
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from reissue_original_seal_for_review import reissue, unpack_original, INDEX, PROVENANCE

def sha(data):
    return hashlib.sha256(data).hexdigest()

def write(p, files, hashes, duplicate=False, traversal=False):
    with ZipFile(p,"w",ZIP_DEFLATED) as z:
        for name,raw in files.items():
            z.writestr(name,raw)
        z.writestr(INDEX,json.dumps(hashes).encode("utf-8"))
        if duplicate:
            z.writestr("src/old.js",files["src/old.js"])
        if traversal:
            z.writestr("../escape.js",b"unsafe")

def refused(fn,label):
    try:fn()
    except (ValueError,TypeError,KeyError,OSError):return
    raise AssertionError("Failure was not rejected: "+label)

def main():
    with tempfile.TemporaryDirectory(prefix="SYNTHETIC_PRIVATE_M19_") as temp:
        base=Path(temp)
        orig=base/"historical"/"original.zip"
        orig.parent.mkdir()
        dest=base/"derived"
        dest.mkdir()
        files={"src/old.js":b"// SYNTHETIC CODE; NOT HISTORICAL\n",
               "docs/log.md":b"ORIGINAL DUMMY LOG\n"}
        hashes={name:sha(raw) for name,raw in files.items()}
        hashes["docs/log.md"]="0"*64
        write(orig,{**files,"src/new_verifier.js":b"// SYNTHETIC UNINDEXED\n"},hashes)
        original_bytes=orig.read_bytes()
        expected=sha(original_bytes)
        outfile=dest/"derived-review.zip"
        report=reissue(orig,expected,outfile,"2026-10-25")
        assert report["result"]=="PRIVATE_DERIVED_MEMBER_HASH_CLOSURE_PASS"
        assert report["originalSourceMembersPreserved"]==3
        assert report["derivedHashEntries"]==4
        assert report["originalHashMismatches"]==1
        assert report["originalUnindexedFiles"]==1
        assert original_bytes==orig.read_bytes()
        with ZipFile(outfile) as z:
            assert set(z.namelist())==set(files)|{"src/new_verifier.js",INDEX,PROVENANCE}
            index=json.loads(z.read(INDEX))
            assert set(index)==set(files)|{"src/new_verifier.js",PROVENANCE}
            assert all(sha(z.read(n))==v for n,v in index.items())
            assert json.loads(z.read(PROVENANCE))["originalZipSHA256"]==expected
            assert z.read("docs/log.md")==files["docs/log.md"]
        refused(lambda:reissue(orig,expected,outfile,"2026-10-25"),"cannot overwrite old derived ZIP")
        refused(lambda:reissue(orig,"0"*64,dest/"bad-digest.zip","2026-10-25"),
                "substituted source despite new internally valid index")
        refused(lambda:reissue(orig,expected,orig,"2026-10-25"),"cannot overwrite original")
        refused(lambda:reissue(orig,expected,orig.parent/"beside.zip","2026-10-25"),
                "co-located original source")
        refused(lambda:reissue(orig,expected,dest/"fake.zip","date unknown"),"unspecified derivative edition")
        o=base/"fully-sealed.zip"
        write(o,files,{n:sha(raw) for n,raw in files.items()})
        refused(lambda:reissue(o,sha(o.read_bytes()),dest/"unnecessary.zip","2026-10-25"),
                "unnecessary reissue of an already fully sealed original")
        special=base/"traversal.zip"
        write(special,files,hashes,traversal=True)
        refused(lambda:reissue(special,sha(special.read_bytes()),dest/"escape.zip","2026-10-25"),
                "ZIP traversal source")
        duplicate=base/"duplicate.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",UserWarning)
            write(duplicate,files,hashes,duplicate=True)
        refused(lambda:reissue(duplicate,sha(duplicate.read_bytes()),dest/"duplicate.zip","2026-10-25"),
                "duplicate source member")
        # Changing original bytes requires a separately fixed archived digest.
        orig.write_bytes(original_bytes+b"tampered")
        refused(lambda:reissue(orig,expected,dest/"tampered.zip","2026-10-25"),
                "changed historical source after original frozen fingerprint")
        print("PASS: original-payload preservation with independently pinned source SHA-256")
        print("PASS: complete new index of every original file and new provenance; original HOLD retained")
        print("PASS: nine synthetic overwrite, source substitution, duplicate and traversal failures")
        print("PASS: no archived execution or independent native effect witness granted")

if __name__=="__main__":
    main()
