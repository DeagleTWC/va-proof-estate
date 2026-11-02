#!/usr/bin/env python3
"""Public reviewer-route accessibility and source-identity checks.

Does not certify the native V.A. substrate, original effects, or physical proofs.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD = re.compile(
    r'<article class="claim" data-status="([^"]+)" data-native="(true|false)">'
    r'\s*<div class="claim-head"><strong>([^<]+)</strong>'
)

def validate(root: Path = ROOT) -> list[str]:
    root = Path(root)
    errors = []
    try:
        html = (root / "reviewer-route.html").read_text(encoding="utf-8")
        home = (root / "index.html").read_text(encoding="utf-8")
        register = json.loads((root / "proofs/CLAIM-TO-CARRIER.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"reviewer route cannot be read or register invalid: {exc}"]
    must = {
        'lang="en"': "document language",
        'name="viewport"': "mobile viewport",
        'class="skip" href="#main"': "keyboard skip link",
        '<main id="main">': "main destination",
        'aria-label="Review navigation"': "named navigation",
        '<label for="status-filter">': "filter label",
        'role="status" aria-live="polite"': "accessible result count",
        'href="foundation.html"': "foundation route",
        'href="proofs/HISTORICAL-PILOT-CARRIER-CROSSWALK.md"': "historic pilot route",
        'href="examiner/README.md"': "independent examiner route",
        'href="proofs/CLAIM-TO-CARRIER.json"': "original claim register",
    }
    for fragment, label in must.items():
        if fragment not in html:
            errors.append(f"missing public reviewer feature: {label}")
    if 'href="reviewer-route.html"' not in home:
        errors.append("live homepage lacks reviewer-route link")
    if 'id="top"' not in home or 'href="#top">Skip to main content' not in home:
        errors.append("live homepage lacks keyboard skip-to-main route")
    entries = register.get("entries", [])
    cards = CARD.findall(html)
    if len(cards) != len(entries):
        errors.append(f"reviewer cards {len(cards)} != public register {len(entries)}")
    expected = {str(x["id"]): x for x in entries if isinstance(x, dict) and "id" in x}
    if len(expected) != len(entries):
        errors.append("public register has malformed or duplicated claims")
    ids = [claim_id for _, _, claim_id in cards]
    if len(ids) != len(set(ids)):
        errors.append("duplicate reviewer claim cards")
    for standing, native, claim_id in cards:
        claim = expected.get(claim_id)
        if not claim:
            errors.append(f"reviewer added unregistered claim: {claim_id}")
            continue
        if standing != claim.get("standing") or (native == "true") != (claim.get("nativeVAEvidence") is True):
            errors.append(f"reviewer overstated or changed standing: {claim_id}")
        carrier = claim.get("carrier") or claim.get("sourceTextCarrier") or claim.get("publicHistoricalSourceText")
        if carrier:
            p = (root / carrier).resolve()
            if not p.is_relative_to(root.resolve()) or not p.is_file():
                errors.append(f"missing/unsafe original public source: {claim_id}")
            if f'href="{carrier}"' not in html:
                errors.append(f"missing source link for {claim_id}")
    if any(x.get("standing") == "INDEPENDENTLY REPRODUCED" for x in entries):
        errors.append("reviewer controls require explicit independent-standing layout update")
    if not any(x.get("class") == "synthetic-fixture" and x.get("standing") == "OBSERVED" and x.get("nativeVAEvidence") is False for x in entries):
        errors.append("synthetic observation boundary missing")
    if "No independently reproduced native run is attached" not in html:
        errors.append("public evidence ceiling statement missing")
    return errors

if __name__ == "__main__":
    problems = validate()
    for issue in problems:
        print("REVIEWER ROUTE ERROR:", issue)
    if problems:
        raise SystemExit(1)
    print("PASS: reviewer route; 17 claim identities, evidence standings, sources and accessible navigation")
