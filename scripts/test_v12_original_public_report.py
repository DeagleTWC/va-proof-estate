#!/usr/bin/env python3
"""No unauthorized public promotion from custodian-local V1.2 historical ZIP checks."""
import copy
import json
from validate_v12_original_public_report import ROOT, check


def reject(data, name):
    try:
        check(data)
    except (ValueError, KeyError, TypeError):
        return
    raise AssertionError("Unsupported V1.2 evidence elevation accepted: " + name)


def main():
    original = json.loads((ROOT / "proofs/V1.2-ORIGINAL-SOURCE-VERIFICATION.json").read_text(encoding="utf-8"))
    assert check(original) == 8
    mutations = [
        ("native result falsely inherited", lambda d:d["proofBoundary"].update(nativeV12Result="PASS")),
        ("external effect falsely witnessed", lambda d:d["proofBoundary"].update(realWorldPilotEffect="PASS")),
        ("independent reviewer falsely attributed", lambda d:d["proofBoundary"].update(authenticIndependentHumanReview="PASS")),
        ("private ZIP falsely published", lambda d:d.update(originalZipBytesReleasedInThisPublicRecord=True)),
        ("unverified original freeze date supplied", lambda d:d.update(originalFreezeDateAuthenticatedFromOriginal=True)),
        ("local verification falsely independent", lambda d:d.update(verificationClass="INDEPENDENT_NATIVE_REPRODUCTION")),
        ("fixture count increased without proof", lambda d:d.update(originalFixtureCases=88)),
        ("original copy mismatch erased", lambda d:d.update(twoOriginalLibraryCopiesIdentical=False)),
        ("physical KCD promoted", lambda d:d["proofBoundary"].update(physicalKCD="VERIFIED")),
        ("original public admission falsely attached", lambda d:d["proofBoundary"].update(originalPublicCarrierAdmission="ATTACHED")),
        ("supplied tamper test silently removed", lambda d:d.update(originalSuppliedTamperTestExecutedOnControlledExtract=False)),
    ]
    for name, action in mutations:
        obj = copy.deepcopy(original)
        action(obj)
        reject(obj, name)
    print(f"PASS: {len(mutations)} synthetic source-to-native/physical/independent promotion errors refused")


if __name__ == "__main__":
    main()
