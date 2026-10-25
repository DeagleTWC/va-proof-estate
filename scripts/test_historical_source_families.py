#!/usr/bin/env python3
"""Synthetic negative controls for historical source-family publication classification."""
import copy
import json
from pathlib import Path
from validate_historical_source_families import validate

ROOT=Path(__file__).resolve().parents[1]

def reject(obj,label):
    try: validate(obj)
    except (ValueError,KeyError,TypeError): return
    raise AssertionError("Accepted false source promotion: "+label)

def main():
    src=json.loads((ROOT/"proofs/HISTORICAL-SOURCE-FAMILIES.json").read_text(encoding="utf-8"))
    assert validate(src)==5
    tests=[
        ("invented pilot count",lambda d:d.update(totalHistoricalPilotCount=5)),
        ("original freeze count invented",lambda d:d.update(originalFreezeCount=5)),
        ("unreleased original marked attached",lambda d:d["historicalFamilies"][0].update(originalBytesPubliclyAttached=True)),
        ("sourced engineering build relabeled native",lambda d:d["historicalFamilies"][0].update(nativeV12StandingInherited=True)),
        ("unexecuted run form relabeled observed",lambda d:d["historicalFamilies"][3].update(actualLiveEffectEstablishedHere=True)),
        ("third party engineering source elevated",lambda d:d["historicalFamilies"][4].update(status="INDEPENDENTLY_REPRODUCED")),
        ("unapproved private source release",lambda d:d.update(privateSourceLocatorPublication="PUBLIC")),
        ("false native reproduction count",lambda d:d.update(publicIndependentNativeVAReproductionsThisMilestone=1)),
        ("missing stage",lambda d:d["historicalFamilies"][1].update(stage="LIVE_RUN_PROVEN")),
        ("six public surfaces conflated",lambda d:d.update(knownAdditionalPublicSurfaces="")),
        ("missing original carrier gate",lambda d:d.update(admittedPublicOriginalCarriers="")),
        ("duplicate source family",lambda d:d["historicalFamilies"].append(copy.deepcopy(d["historicalFamilies"][0])))
    ]
    for label,mutate in tests:
        modified=copy.deepcopy(src);mutate(modified);reject(modified,label)
    print(f"PASS: {len(tests)} false-promotion and private-source negative controls rejected")
    print("PASS: prior historic pilots and freezes not downgraded by missing public attachments")

if __name__=="__main__":
    main()
