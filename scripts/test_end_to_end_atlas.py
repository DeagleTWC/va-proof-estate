#!/usr/bin/env python3
"""Synthetic negative controls for whole-of-estate completeness and original attribution."""
import copy
import json
from validate_end_to_end_atlas import ROOT,validate

def reject(data,atlas,home,reason):
    try:validate(data,atlas,home)
    except (ValueError,KeyError,TypeError,FileNotFoundError):
        return
    raise AssertionError("Atlas accepted source gap or false standing: "+reason)

def main():
    data=json.loads((ROOT/"proofs/END-TO-END-ESTATE-REGISTER.json").read_text(encoding="utf-8"))
    html=(ROOT/"end-to-end.html").read_text(encoding="utf-8")
    home=(ROOT/"index.html").read_text(encoding="utf-8")
    original=validate(data,html,home)
    assert original["stages"]==12 and original["repositories"]==39
    defects=[
      ("public repo dropped",lambda x:x["sourceInventory"]["records"].pop()),
      ("source owner secretly substituted",lambda x:x["sourceInventory"].update(owner="OtherOrg")),
      ("duplicate public original",lambda x:x["sourceInventory"]["records"][1].update(name=x["sourceInventory"]["records"][0]["name"])),
      ("public URL of source rewritten",lambda x:x["sourceInventory"]["records"][0].update(url="https://example.invalid")),
      ("snapshot called historic freeze",lambda x:x["sourceInventory"].update(snapshotIsOriginalFreeze=True)),
      ("outside GitHub source called native V.A.",lambda x:x["sourceInventory"]["records"][0].update(inheritsNativeVAStanding=True)),
      ("separate author source assimilated",lambda x:next(p for p in x["sourceInventory"]["records"] if p["name"]=="invisible-middle-intelligence-layer").update(relationship="bounded_boundary_source")),
      ("historical repo HEAD promoted to original",lambda x:x["sourceInventory"]["records"][1].update(historicalOriginalFreezeVerifiedFromThisSnapshot=True)),
      ("native V12 observation fabricated",lambda x:next(p for p in x["evidenceFamilies"] if p["id"]=="native-current").update(status="COMPLETE_NATIVE_V12_PASS")),
      ("independent witness invented",lambda x:next(p for p in x["evidenceFamilies"] if p["id"]=="independent-native").update(status="TWO_INDEPENDENT_NATIVE_PASSES")),
      ("old HOLD silently cleared",lambda x:next(p for p in x["evidenceFamilies"] if p["id"]=="seal").update(status="ORIGINAL_FULL_PASS")),
      ("private historic build erased",lambda x:next(p for p in x["evidenceFamilies"] if p["id"]=="historic-build").update(status="ONLY_A_SYNTHETIC_PLAN")),
      ("removed consequence stage",lambda x:x["endToEndStages"].pop(8)),
      ("stage source path nonexistent",lambda x:x["endToEndStages"][1].update(proofEstateRecord="proofs/FAKE-UNSEEN-SOURCE.md")),
      ("stage incorrectly called executable implementation order",lambda x:x["endToEndStages"][0].update(notAnImplementationSequence=False)),
      ("physical KCD lane hidden",lambda x:x["evidenceFamilies"].pop()),
      ("original category description erased",lambda x:x["sourceInventory"]["records"][2].update(description="")),
      ("no-standing rule removed",lambda x:x.update(noAutomaticPromotion=False)),
    ]
    for label,mutate in defects:
        x=copy.deepcopy(data)
        mutate(x)
        reject(x,html,home,label)
    htmlDefects=[
      ("one public source row missing",html.replace('data-group="bounded_boundary_source"','data-group="absent_category"',1)),
      ("missing first end-to-end stage",html.replace('id="stage-00"','id="stage-missing"',1)),
      ("source filter removed",html.replace('id="srcSearch"','id="removedSearch"')),
      ("evidence section removed",html.replace('id="evidence"','id="missing-evidence-section"')),
      ("unsafe local link added",html.replace('</main>','<a href="../not-public.txt">unsafe</a></main>',1)),
      ("public owner link redirected",html.replace('https://github.com/Kamanaka5502/3lockbox-ip-admission-gate','https://example.invalid/bad-link',1)),
    ]
    for label,text in htmlDefects:
        reject(data,text,home,label)
    reject(data,html,home.replace('id="full-estate-atlas"','id="lost-full-atlas"'),
           "Homepage strips full route")
    print(f"PASS: {len(defects)+len(htmlDefects)+1} synthetic source loss, false standing, unsafe link and incomplete site controls refused")
    print("PASS: all 39 public source groups, 12 stages and ten evidence lanes preserved")
    print("PASS: independent authorship, historical pilots, native V12 and private source boundaries remain separated")

if __name__=="__main__":
    main()
