#!/usr/bin/env python3
"""Synthetic original-PDF custody and false standing mutations; no actual historical PDF content."""
import copy
import hashlib
import json
import tempfile
from pathlib import Path

from verify_historical_external_review_originals import run, verify_manifest

def sha(b): return hashlib.sha256(b).hexdigest()

def fail(data,folder,why):
    try:verify_manifest(data,folder)
    except (ValueError,TypeError,KeyError,OSError):return
    raise AssertionError("Original-custody preflight accepted: "+why)

def main():
    with tempfile.TemporaryDirectory(prefix="va-synthetic-review-custody-") as tmp:
        tmp=Path(tmp);src=tmp/"actual-originals";src.mkdir()
        reviews=[]
        originals=[
            ("IQR-ITR-001-v1.0","CARRIER_QUALIFICATION_HOLD"),
            ("ITR-PYJWT-2130-INDEPENDENT-v1.0","SAME_OBJECT_DIFFERENTIAL_REVIEW_PARTIAL")]
        for id,cl in originals:
            filename=id+".pdf"
            data=(b"%PDF-1.4\n% SYNTHETIC, NOT A TRUE HISTORICAL REVIEW\n"+
                  (id+" X"*30).encode()+b"\n%%EOF\n")
            (src/filename).write_bytes(data)
            reviews.append({"reviewId":id,"reviewClass":cl,"underlyingTechnicalObject":"PyJWT 2.13.0",
                            "reviewDateLabel":"2026-07-20",
                            "independentNativeVAReproduction":False,"releaseCleared":False,
                            "reviewerCompetenceQualifiedForNativeVA":False,
                            "expectedBytes":len(data),"source":{"path":filename,"sha256":sha(data)}})
        manifest={"schema":"va-private-original-review-document-check/1.0",
                  "classification":"PRIVATE_DO_NOT_PUBLISH",
                  "releaseAuthorization":False,
                  "independentNativeVAWitnessAuthenticated":False,
                  "independentDifferentialHarnessReproducedInThisAudit":False,
                  "originalReviewDocuments":reviews}
        intake=tmp/"private-intake.json";intake.write_text(json.dumps(manifest))
        report=run(src,intake)
        assert report["checkedOriginalReports"]==2
        assert report["publicDisclosureAuthorized"] is False
        assert report["thirdPartyWitnessOfNativeVAAuthenticated"] is False
        assert report["fullIndependentPyJWTDifferentialReproducedHere"] is False
        mutations=[
            ("original PDF source hash altered",lambda d:d["originalReviewDocuments"][0]["source"].update(sha256="0"*64)),
            ("original report length inflated",lambda d:d["originalReviewDocuments"][0].update(expectedBytes=999)),
            ("reviewer reclassified native V.A.",lambda d:d["originalReviewDocuments"][1].update(independentNativeVAReproduction=True)),
            ("reviewer competence scope promoted",lambda d:d["originalReviewDocuments"][1].update(reviewerCompetenceQualifiedForNativeVA=True)),
            ("unauthorized source release",lambda d:d.update(releaseAuthorization=True)),
            ("direct public status altered",lambda d:d["originalReviewDocuments"][0].update(releaseCleared=True)),
            ("unrun harness called reproduced",lambda d:d.update(independentDifferentialHarnessReproducedInThisAudit=True)),
            ("human witness self-declared",lambda d:d.update(independentNativeVAWitnessAuthenticated=True)),
            ("earlier HOLD erased",lambda d:d["originalReviewDocuments"][0].update(reviewClass="FULL_PASS")),
            ("later partial inflated",lambda d:d["originalReviewDocuments"][1].update(reviewClass="INDEPENDENT_VA_PASS")),
            ("wrong reported object",lambda d:d["originalReviewDocuments"][1].update(underlyingTechnicalObject="native VA")),
            ("distinct source made same file",lambda d:d["originalReviewDocuments"][1].update(source=d["originalReviewDocuments"][0]["source"])),
            ("path traversal",lambda d:d["originalReviewDocuments"][0]["source"].update(path="../private-intake.json")),
        ]
        for why,mutation in mutations:
            bad=copy.deepcopy(manifest);mutation(bad);fail(bad,src,why)
        # Original PDF actually altered but expected manifest digest unchanged.
        p=src/(originals[0][0]+".pdf");original=p.read_bytes()
        p.write_bytes(original+b"TAMPER");fail(manifest,src,"actual PDF bytes changed")
        p.write_bytes(original)
        # Symlink attack (Linux CI).
        bad=copy.deepcopy(manifest)
        symlink=src/"linked.pdf";symlink.symlink_to(p)
        bad["originalReviewDocuments"][0]["source"]["path"]="linked.pdf"
        fail(bad,src,"symlink original PDF")
        # Public-looking file that is not PDF: matching hash alone cannot substitute original PDF.
        bad=copy.deepcopy(manifest)
        fake=src/"impostor.pdf";fake.write_bytes(b"NOT A PDF BUT LONG ENOUGH "*10)
        bad["originalReviewDocuments"][0]["source"]={"path":"impostor.pdf","sha256":sha(fake.read_bytes())}
        bad["originalReviewDocuments"][0]["expectedBytes"]=fake.stat().st_size
        fail(bad,src,"non-PDF substituted")
        assert run(src,intake)["checkedOriginalReports"]==2
        print(f"PASS: two synthetic PDF source objects checked with {len(mutations)+3} negative controls")
        print("PASS: HOLD and PARTIAL remain distinct; neither grants native V.A. independent witness standing")
        print("PASS: original source content not uploaded or executed")

if __name__=="__main__":
    main()
