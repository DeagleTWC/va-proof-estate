#!/usr/bin/env python3
"""Synthetic-only archive mutations for historic PyJWT differential source verifier."""
import copy
import hashlib
import json
import tempfile
import warnings
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

from verify_historical_pyjwt_differential_original import (
    inspect_original, validate_outcomes, REPORT, DOCX, HARNESS, FIXED, BASELINE
)

def encode(obj):
    return (json.dumps(obj,indent=2)+"\n").encode()

def sha(raw):return hashlib.sha256(raw).hexdigest()

def fixture():
    names=["C001 raw JWK JSON rejected","C002 algorithm binding","C003 URI schemes",
           "C004 cache preserved","C005a detached segment","C005b crit required"]
    rows=lambda state:[{"test":name,"expected_fixed":True,"outcome":state,
                        "detail":"Synthetic outcome; not an actual PyJWT execution"}
                       for name in names]
    code=("import sys\nimport jwt\nROOT=sys.argv[1]\nsys.path.insert(0, ROOT)\n"+
          "\n".join("record('"+n+"', True, lambda: None)" for n in names)+"\n").encode()
    contents={
      REPORT:b"%PDF-1.4\nSYNTHETIC PDF; no historic standing\n%%EOF\n",
      DOCX:b"PK\x03\x04synthetic stub bytes",
      HARNESS:code,
      FIXED:encode({"version":"2.13.0","module":"/tmp/pyjwt213/jwt/__init__.py","results":rows("PASS")}),
      BASELINE:encode({"version":"2.12.1","module":"/tmp/pyjwt2121/jwt/__init__.py","results":rows("FAIL")})
    }
    return contents

def write(p,data,duplicate=False):
    with ZipFile(p,"w",ZIP_DEFLATED) as z:
        for name,content in data.items():z.writestr(name,content)
        if duplicate:z.writestr(FIXED,data[FIXED])

def refuse(p,hashes,desc):
    try:inspect_original(p,expected_hashes=hashes)
    except (ValueError,TypeError,KeyError):return
    raise AssertionError("Verifier falsely admitted synthetic mutation: "+desc)

def main():
    with tempfile.TemporaryDirectory(prefix="M17_SYNTHETIC_") as d:
        folder=Path(d)
        src=fixture()
        def digests(o):
            return {k:sha(o[k]) for k in (HARNESS,FIXED,BASELINE)}
        orig=folder/"original-synthetic.zip"
        write(orig,src)
        good=inspect_original(orig,expected_hashes=digests(src))
        assert good["reportedFixedVersionPASS"]==6
        assert good["reportedBaselineVersionFAIL"]==6
        assert good["testHarnessExecutedByThisTool"] is False
        changes=[
         ("altered original code",HARNESS,b"# fake"),
         ("tampered source fixed result",FIXED,b'{}'),
         ("tampered baseline result",BASELINE,b'{}'),
         ("substituted report original",REPORT,b"not a PDF"),
         ("substituted DOCX original",DOCX,b"not zip"),
        ]
        for i,(name,path,changed) in enumerate(changes):
            other=dict(src);other[path]=changed
            candidate=folder/f"mutation-{i}.zip";write(candidate,other)
            refuse(candidate,digests(src),name)
        row_errors=[
          ("fixed FAIL instead of PASS",FIXED,lambda v:v["results"][0].update(outcome="FAIL")),
          ("vulnerable PASS instead of FAIL",BASELINE,lambda v:v["results"][0].update(outcome="PASS")),
          ("baseline version substituted",BASELINE,lambda v:v.update(version="2.13.0")),
          ("fixed version substituted",FIXED,lambda v:v.update(version="2.12.1")),
          ("baseline case reordered",BASELINE,lambda v:v["results"].reverse()),
          ("duplicate first test",BASELINE,lambda v:v["results"][1].update(test=v["results"][0]["test"])),
          ("claim dropped",BASELINE,lambda v:v["results"].pop()),
          ("claim expected_fixed reversed",BASELINE,lambda v:v["results"][1].update(expected_fixed=False)),
          ("reported observation missing",FIXED,lambda v:v["results"][0].update(detail=""))
        ]
        for j,(name,p,fn) in enumerate(row_errors):
            other=dict(src);item=json.loads(other[p]);fn(item);other[p]=encode(item)
            cand=folder/f"source-mutation-{j}.zip";write(cand,other)
            refuse(cand,digests(other),name+" even when injected synthetic source hashes match")
        missing=dict(src);missing.pop(FIXED)
        bad=folder/"missing.zip";write(bad,missing);refuse(bad,digests(src),"source missing")
        dup=folder/"duplicate.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore",UserWarning)
            write(dup,src,duplicate=True)
        refuse(dup,digests(src),"duplicated source entry")
        wrong=folder/"wrong-prior.pdf";wrong.write_bytes(b"%PDF-1.4\nOther report\n%%EOF")
        try:inspect_original(orig,prior_review_pdf=wrong,expected_hashes=digests(src))
        except ValueError:pass
        else:raise AssertionError("Wrong prior report admitted")
        valid_prior=folder/"matching-prior.pdf";valid_prior.write_bytes(src[REPORT])
        assert inspect_original(orig,prior_review_pdf=valid_prior,expected_hashes=digests(src))["earlierOriginalReportIdentical"]
        print(f"PASS: synthetic archived two-version result source; {len(changes)+len(row_errors)+3} negative source/manipulation tests")
        print("PASS: no original historic PyJWT execution, authentic human identity or native V.A. witness inferred")

if __name__=="__main__":
    main()
