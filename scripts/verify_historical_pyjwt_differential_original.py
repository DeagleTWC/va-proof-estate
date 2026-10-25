#!/usr/bin/env python3
"""Read-only verification of a historic independent PyJWT *review archive*.

This checks actual ZIP member bytes and saved differential claims. It NEVER
executes archived code or the installed PyJWT releases, and it does NOT confer
independent reviewer identity, native V.A. standing or redistribution rights.
"""
import argparse
import hashlib
import json
import os
import re
import stat
from pathlib import Path
from zipfile import ZipFile, BadZipFile, LargeZipFile

REPORT = "Independent_Technical_Review_PyJWT_2.13.0_and_Reviewer_Comparison_v1.0.pdf"
DOCX = "Independent_Technical_Review_PyJWT_2.13.0_and_Reviewer_Comparison_v1.0.docx"
HARNESS = "independent_pyjwt_2_13_0_review_harness.py"
FIXED = "independent_results_pyjwt_2.13.0.json"
BASELINE = "independent_results_pyjwt_2.12.1.json"
MEMBERS = {REPORT, DOCX, HARNESS, FIXED, BASELINE}
# These three hashes are the exact three objects cited in the original July 20 review.
# No original ZIP digest, source PDF digest, private key or customer carrier is released.
EXPECTED = {
  HARNESS: "02c17c0590c0a848e1e79f8d04409c8687a7900a56b2aae483cbd3970c9ff824",
  FIXED: "2892c50c3abdf2379fe861fc88a0dc53ec09762a754a14b9e1d39d681b91f9bd",
  BASELINE: "8c8effa686a40b8d8d4adbdbfcf918337370bc75558ba08f18e595227e07b070"
}
TEST_ORDER = ("C001 ", "C002 ", "C003 ", "C004 ", "C005a ", "C005b ")
MAX_MEMBER = 2_000_000
MAX_TOTAL = 5_000_000


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def validate_outcomes(fixed, baseline):
    require(isinstance(fixed, dict) and isinstance(baseline, dict),
            "Saved results must be separate JSON objects")
    require(fixed.get("version") == "2.13.0" and baseline.get("version") == "2.12.1",
            "Historical package versions do not match the original review scope")
    rows_f, rows_b = fixed.get("results"), baseline.get("results")
    require(isinstance(rows_f, list) and isinstance(rows_b, list)
            and len(rows_f) == 6 and len(rows_b) == 6,
            "There must be exactly six saved result rows on each archived version")
    for i, (a, b) in enumerate(zip(rows_f, rows_b)):
        require(isinstance(a, dict) and isinstance(b, dict),
                "Malformed saved test outcome")
        name = a.get("test")
        require(isinstance(name, str) and name.startswith(TEST_ORDER[i])
                and b.get("test") == name,
                "Baseline and fixed test identities or ordering diverge")
        require(a.get("expected_fixed") is True and b.get("expected_fixed") is True,
                "Unexpected fixed-claim semantics in saved results")
        require(a.get("outcome") == "PASS" and b.get("outcome") == "FAIL",
                "Missing reported fail-before/pass-after discrimination")
        for row in (a, b):
            require(isinstance(row.get("detail"), str) and row["detail"].strip(),
                    "Saved observation detail missing")
    for obj in (fixed, baseline):
        require(isinstance(obj.get("module"), str) and
                obj["module"].endswith("/jwt/__init__.py"),
                "Saved package module identity missing")
        # Historical module path is a recorded string, not an independently
        # attested runtime provenance or trusted execution transcript.
    return [x["test"] for x in rows_f]


def inspect_original(path, prior_review_pdf=None, expected_hashes=None):
    path = Path(path).absolute()
    require(path.is_file() and not path.is_symlink(), "Original archive missing")
    hashes = EXPECTED if expected_hashes is None else expected_hashes
    require(set(hashes) == {HARNESS, FIXED, BASELINE},
            "Must verify the three original claim carrier roles")
    with ZipFile(path) as archive:
        rows = archive.infolist()
        require(len(rows) == 5 and {x.filename for x in rows} == MEMBERS
                and len(set(x.filename for x in rows)) == len(rows),
                "Missing, duplicated or unexpected ZIP original")
        raw = {}
        total = 0
        for entry in rows:
            require(not entry.is_dir() and not entry.filename.startswith("/")
                    and ".." not in entry.filename and "\\" not in entry.filename,
                    "Unsafe ZIP path")
            require(entry.flag_bits & 1 == 0, "Encrypted ZIP cannot be examined")
            require(stat.S_IFMT(entry.external_attr >> 16) != stat.S_IFLNK,
                    "ZIP symlink refused")
            require(0 < entry.file_size <= MAX_MEMBER and entry.compress_size <= MAX_MEMBER,
                    "Unsafe ZIP member byte size")
            total += entry.file_size
            require(total <= MAX_TOTAL, "Excessive expanded ZIP size")
            raw[entry.filename] = archive.read(entry.filename)
    for name, original in hashes.items():
        require(re.fullmatch(r"[0-9a-f]{64}", original) is not None,
                "Missing source SHA-256 reference")
        require(sha(raw[name]) == original, "Original review source hash mismatch: " + name)
    require(raw[REPORT].startswith(b"%PDF-") and b"%%EOF" in raw[REPORT][-2048:],
            "Original report must be an intact PDF")
    require(raw[DOCX].startswith(b"PK\\x03\\x04".replace(b"\\x03", b"\x03").replace(b"\\x04", b"\x04")),
            "Original DOCX must be a ZIP-backed document")
    script = raw[HARNESS].decode("utf-8")
    require("import jwt" in script and "sys.path.insert(0, ROOT)" in script,
            "Original harness no longer targets version-scoped supplied location")
    for token in ("record('C001 ", "record('C002 ", "record('C003 ",
                  "record('C004 ", "record('C005a ", "record('C005b "):
        require(token in script, "Original harness no longer records every selected release claim")
    try:
        original_fixed = json.loads(raw[FIXED].decode("utf-8"))
        original_base = json.loads(raw[BASELINE].decode("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError("Original archived result JSON not parseable") from exc
    cases = validate_outcomes(original_fixed, original_base)
    prior_equal = False
    if prior_review_pdf is not None:
        prior = Path(prior_review_pdf).absolute()
        require(prior.is_file() and not prior.is_symlink()
                and prior.stat().st_size <= MAX_MEMBER,
                "Separate prior July report source unavailable")
        prior_equal = prior.read_bytes() == raw[REPORT]
        require(prior_equal, "Archived PDF differs from earlier original July report")
    return {
        "schema":"va-public-m17-review-archive-local-preflight/1.0",
        "result":"ORIGINAL_REVIEW_PACKAGE_MEMBERS_MATCH_REPORTED_HASHES",
        "sourceMembersFound":len(raw),
        "originalHarnessAndSavedResultDigestsMatched":3,
        "archivedVersionPair":["2.12.1","2.13.0"],
        "reportedFixedVersionPASS":len(cases),
        "reportedBaselineVersionFAIL":len(cases),
        "matchedIndependentReviewClaimIDs":["C001","C002","C003","C004","C005a","C005b"],
        "earlierOriginalReportBytesCompared":prior_review_pdf is not None,
        "earlierOriginalReportIdentical":prior_equal if prior_review_pdf is not None else None,
        "testHarnessExecutedByThisTool":False,
        "historicalExecutionChronologyVerified":False,
        "originalPyJWTPackageVersionsRerun":False,
        "nativeVAExternallyWitnessed":False,
        "reviewerHumanIndependenceAuthenticated":False,
        "publicReleaseRightsGranted":False,
        "note":"Three original claimed review objects matched SHA-256 values cited by a historic document; archived version-result rows reflect differential outcomes. No code execution or independent effect witness is inferred."
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--zip",required=True,help="Original privately held historic review archive")
    p.add_argument("--prior-review-pdf",help="Optional separately held July source PDF for exact byte comparison")
    p.add_argument("--out",help="Private report path outside original source tree; never overwrites")
    a=p.parse_args()
    try:
        result=inspect_original(a.zip,a.prior_review_pdf)
        if a.out:
            dest=Path(a.out).absolute()
            base=Path(a.zip).absolute().parent.resolve()
            require(not dest.exists() and not dest.is_symlink() and
                    not dest.resolve().is_relative_to(base),
                    "Result destination must be outside source folder and not previously used")
            fd=os.open(str(dest),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,"w",encoding="utf-8") as f:
                json.dump(result,f,indent=2)
                f.write("\n")
        print(json.dumps(result,indent=2))
    except (ValueError,KeyError,TypeError,UnicodeError,OSError,BadZipFile,LargeZipFile) as exc:
        p.exit(2,"REFUSED: "+str(exc)+"\n")

if __name__=="__main__":
    main()
