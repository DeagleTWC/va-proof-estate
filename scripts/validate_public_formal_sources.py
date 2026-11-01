#!/usr/bin/env python3
"""Validate all public V.A. claim source links against original-PDF digest inventory.

Only source attribution, public metadata, and evidence ceilings are checked.
Does not execute, replace, or certify corrected NEW-K / native True Zero mathematics.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROW = re.compile(r"^\{id:'(VA-(?:F|N|P|H)\d{2})'[^ \n]*(?:[^\n]*)", re.M)
PDF_ROW = re.compile(
    r"^\|\s*\x60([^\x60]+\.pdf)\x60\s*\|[^|]*\|\s*\d+\s*\|\s*\x60([0-9a-f]{64})\x60\s*\|$",
    re.M,
)
FIELD = r"\b{key}:'([^']*)'"
UI_CLASS = {
    "formal-record": "formal",
    "native-claim": "software",
    "physical-proof-requirement": "physical",
    "historical-proof-requirement": "historical",
}


def validate(root=ROOT):
    root = Path(root).resolve()
    errors = []

    def read(path):
        try:
            target = (root / path).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                raise ValueError("missing or outside public repository")
            return target.read_text(encoding="utf-8")
        except (OSError, ValueError) as exc:
            errors.append(f"Cannot read {path}: {exc}")
            return ""

    try:
        registry = json.loads(read("proofs/CLAIM-TO-CARRIER.json"))
        manifest = json.loads(read("proof-estate-manifest.json"))
    except ValueError as exc:
        return errors + [f"Invalid JSON input: {exc}"]

    html = read("index.html")
    inventory = read("proofs/SOURCE-ESTATE.md")
    expected_pdf = dict(PDF_ROW.findall(inventory))
    if len(expected_pdf) != 4:
        errors.append(f"Original public PDF inventory must list four distinct historical source IDs, found {len(expected_pdf)}")
    actual_pdf = manifest.get("sourceOriginalPdfSHA256", {})
    if actual_pdf != expected_pdf:
        errors.append("Manifest original PDF hash register differs from the source estate's four recorded identities")
    provenance = manifest.get("sourceOriginalPdfSHA256Provenance", {})
    if provenance.get("publishedDigestCount") != len(expected_pdf):
        errors.append("Published original PDF digest count disagrees with source register")
    if provenance.get("originalPDFCopiesPubliclyAttached") != 0 or manifest.get("originalSourcePdfCopiesInRepository") != 0:
        errors.append("This audit has no basis for claiming attached original PDF bytes")
    if provenance.get("register") != "proofs/SOURCE-ESTATE.md":
        errors.append("PDF hash provenance no longer names the source estate")

    registered = [
        entry for entry in registry.get("entries", [])
        if entry.get("id", "").startswith("VA-") and entry.get("sourceTextCarrier")
    ]
    expected = {entry["id"]: entry for entry in registered}
    if len(expected) != 9 or len(registered) != len(expected):
        errors.append("Expected nine uniquely identified source-linked V.A. claims")
    frontend = {}
    for m in ROW.finditer(html):
        ident = m.group(1)
        if ident in frontend:
            errors.append(f"Duplicate public V.A. row: {ident}")
        frontend[ident] = m.group(0)

    if set(frontend) != set(expected):
        errors.append(f"Claim register/public site ID mismatch: {sorted(set(frontend) ^ set(expected))}")
    text_inventory = manifest.get("sourceTextInventory", [])
    if not isinstance(text_inventory, list) or len(set(text_inventory)) != 4:
        errors.append("Public transcript inventory must retain four distinct text sources")
        text_inventory = []

    for ident, reg in expected.items():
        row = frontend.get(ident, "")
        source = reg.get("sourceTextCarrier")
        digest = reg.get("sourcePdfSHA256")
        if reg.get("standing") != "DECLARED" or reg.get("nativeVAEvidence") is not False:
            errors.append(f"{ident} incorrectly promoted to operational evidence")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"{ident} has invalid original PDF hash")
            continue
        if digest not in expected_pdf.values():
            errors.append(f"{ident} PDF hash absent from original public source inventory")
        if not isinstance(source, str) or source not in text_inventory or not source.startswith("proofs/sources/"):
            errors.append(f"{ident} lacks a listed public transcript")
            continue
        transcript = read(source)
        if digest not in transcript:
            errors.append(f"{ident} transcript does not identify the source PDF SHA-256")
        if reg.get("source") and "://" in str(reg["source"]):
            errors.append(f"{ident} source must remain a first-party review route")
        for key, expected_value in (("sourceTextCarrier", source), ("sourcePdfSHA256", digest)):
            match = re.search(FIELD.format(key=key), row)
            if not match or match.group(1) != expected_value:
                errors.append(f"{ident} front-end {key} differs from registered source identity")
        if f"class:'{UI_CLASS.get(reg.get('class'), '__INVALID__')}'" not in row:
            errors.append(f"{ident} UI claim category differs from source register")
        if "standing:'DECLARED'" not in row:
            errors.append(f"{ident} front-end evidence standing is not DECLARED")
        if ",,sourceTextCarrier:" in row:
            errors.append(f"{ident} has a malformed JavaScript separator")

    if "individual source hash not bundled" in html:
        errors.append("False source-hash absence remains on page")
    for term in (
        "sourceTextCarrier:r.sourceTextCarrier||null",
        "originalPdfSHA256:r.sourcePdfSHA256||null",
        "link.href=record.sourceTextCarrier",
        "link.textContent=' View source transcript'",
    ):
        if term not in html:
            errors.append(f"Public claim links/exports do not retain source metadata: {term}")
    return errors


if __name__ == "__main__":
    failures = validate()
    for item in failures:
        print("SOURCE-IDENTITY ERROR:", item)
    if failures:
        raise SystemExit(1)
    print("PASS: nine True Zero / corrected NEW-K V.A. claims, four historical public PDF identities, transcript links and evidence ceilings")
