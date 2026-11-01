#!/usr/bin/env python3
"""Bind public formal True Zero / corrected NEW-K claim references to their registered source.

Validates public-safe source references and claims only; not the protected math or a
native runtime result.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMAL_IDS = ("VA-F01", "VA-F02")
ID_PATTERN = re.compile(r"^\{id:'(VA-F0[12])'[^\n]*", re.M)


def validate(root=ROOT):
    root = Path(root).resolve()
    errors = []
    try:
        register = json.loads((root / "proofs/CLAIM-TO-CARRIER.json").read_text(encoding="utf-8"))
        html = (root / "index.html").read_text(encoding="utf-8")
        inventory = (root / "proofs/SOURCE-ESTATE.md").read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        return [f"Formal source inspection failed: {exc}"]

    records = {r.get("id"): r for r in register.get("entries", [])}
    frontend = {}
    for match in ID_PATTERN.finditer(html):
        row = match.group(0)
        ident = match.group(1)
        if ident in frontend:
            errors.append(f"Duplicate front-end claim row: {ident}")
        frontend[ident] = row

    for ident in FORMAL_IDS:
        reg = records.get(ident)
        row = frontend.get(ident)
        if not reg or not row:
            errors.append(f"Formal claim {ident} missing from register or front-end")
            continue
        source = reg.get("sourceTextCarrier")
        digest = reg.get("sourcePdfSHA256")
        if reg.get("standing") != "DECLARED" or reg.get("nativeVAEvidence") is not False:
            errors.append(f"{ident} wrongly promoted to operational evidence")
        if not isinstance(digest, str) or not re.fullmatch(r"[a-f0-9]{64}", digest):
            errors.append(f"{ident} has invalid original PDF digest")
            continue
        if not isinstance(source, str) or not source.startswith("proofs/sources/"):
            errors.append(f"{ident} lacks scoped public source transcript")
            continue
        if not (root / source).is_file():
            errors.append(f"{ident} transcript path is not present: {source}")
        if digest not in inventory:
            errors.append(f"{ident} original PDF digest is absent from source inventory")
        for key, expected in (("sourceTextCarrier", source), ("sourcePdfSHA256", digest)):
            pattern = rf"\b{key}:'([^']*)'"
            match = re.search(pattern, row)
            if not match or match.group(1) != expected:
                errors.append(f"{ident} page source {key} differs from registered public carrier")
        if "standing:'DECLARED'" not in row:
            errors.append(f"{ident} page status is not DECLARED")

    if "individual source hash not bundled" in html:
        errors.append("False source-hash absence remains on the public page")
    for required in ("sourceTextCarrier:r.sourceTextCarrier||null",
                     "originalPdfSHA256:r.sourcePdfSHA256||null"):
        if required not in html:
            errors.append(f"Claim export omits registered public formal source metadata: {required}")
    return errors


if __name__ == "__main__":
    faults = validate()
    for fault in faults:
        print("FORMAL SOURCE ERROR:", fault)
    print("PASS: source-bound True Zero/NEW-K claim traceability" if not faults
          else f"FAIL: {len(faults)} source traceability errors")
    if faults:
        raise SystemExit(1)
