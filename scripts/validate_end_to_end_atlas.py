#!/usr/bin/env python3
"""Validate full Deagle end-to-end estate provenance and accessible static site.

The validator checks public source identity and presentation coverage, not
the execution of third-party code, native V.A. consequences or physical effects.
"""
import json
import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_GROUPS={
    "bounded_boundary_source":19,
    "enterprise_reference_surface":9,
    "domain_specific_public_surface":8,
    "separate_or_adjacent_attribution":3
}
EXPECTED_EVIDENCE=("formal","public-tests","historic-build","historic-runs",
                   "external-review","seal","native-current","independent-native","byo","physical")
EXPECTED_STAGE_IDS=[f"{i:02d}" for i in range(12)]
EXPECTED_KAMANAKA_BASE="https://github.com/Kamanaka5502/"
REQUIRED_NATIVE_PUBLIC_STATUS="NO_PUBLIC_RELEASE_APPROVED_NATIVE_ORIGINAL_ATTACHED"

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links=[]
        self.ids=[]
        self.stages=[]
        self.repo_rows=[]
        self.search_input=False
        self.source_select=False
        self.headingText=[]
        self._head=False
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:self.ids.append(a["id"])
        if tag=="a" and "href" in a:self.links.append(a["href"])
        if tag=="article" and "stage" in a.get("class","").split():
            self.stages.append(a.get("id"))
        if tag=="tr" and "data-group" in a:
            self.repo_rows.append((a.get("data-group"),a.get("data-search","")))
        if tag=="input" and a.get("id")=="srcSearch":self.search_input=True
        if tag=="select" and a.get("id")=="srcGroup":self.source_select=True

def require(ok,message):
    if not ok:raise ValueError(message)

def parse_html(text):
    parser=Document()
    parser.feed(text)
    parser.close()
    require(len(parser.ids)==len(set(parser.ids)),"HTML has duplicate IDs")
    return parser

def local_link(href,source):
    if href.startswith(("#","mailto:","tel:","javascript:")):
        return None
    part=urlsplit(href)
    if part.scheme or href.startswith("//"):return None
    relative=unquote(part.path)
    require(relative and not relative.startswith("/"),"Atlas contains root-absolute relative link")
    root=(ROOT/source).parent.resolve()
    candidate=(root/relative).resolve()
    require(candidate.is_relative_to(ROOT),"Atlas local link escapes repository")
    require(candidate.is_file(),"Missing local linked file: "+href)
    return candidate

def validate(data,atlas,home):
    require(data.get("schema")=="deagle-end-to-end-portfolio/1.0"
            and data.get("captured")=="2026-10-25",
            "Unexpected public provenance crosswalk schema/snapshot")
    require(data.get("canonicalPublicEstate")=="DeagleTWC/va-proof-estate"
            and data.get("currentNativeSystemCustodyVersion")=="V12",
            "Wrong Deagle canonical system/version identity")
    require(data.get("noAutomaticPromotion") is True,
            "No-standing-promotion rule removed")
    require(data.get("sourceInventory",{}).get("owner")=="Kamanaka5502",
            "Public source owner changed")
    inv=data["sourceInventory"]
    require(inv.get("publicRepositoryCount")==39
            and inv.get("snapshotIsOriginalFreeze") is False
            and inv.get("reviewedExecutionAutomaticallyNative") is False,
            "Source snapshot falsely promoted to original/native status")
    sources=inv.get("records")
    require(isinstance(sources,list) and len(sources)==39,
            "Original public source inventory not complete")
    names=[x.get("name") for x in sources]
    require(len(set(names))==39,"Duplicate original repository identity")
    classifications=Counter(x.get("relationship") for x in sources)
    require(dict(classifications)==EXPECTED_GROUPS,
            "Core, enterprise, domain and adjacent source groups changed")
    require("Samantha-Revita-Elyria-Systems" in names
            and "invisible-middle-intelligence-layer" in names,
            "Distinct independently authored/adjacent public sources hidden rather than attributed")
    for entry in sources:
        name=entry.get("name")
        require(isinstance(name,str) and re.fullmatch(r"[A-Za-z0-9_.-]{3,125}",name),
                "Source name not safe")
        require(entry.get("url")==EXPECTED_KAMANAKA_BASE+name,
                "Public source owner or original URL substituted")
        require(entry.get("publicAtSnapshot") is True
                and entry.get("originalOwner")=="Kamanaka5502"
                and entry.get("evidenceStanding")=="PUBLIC_REPOSITORY_REFERENCE_ONLY",
                "Public source incorrectly attributed/qualified")
        require(entry.get("inheritsNativeVAStanding") is False
                and entry.get("historicalOriginalFreezeVerifiedFromThisSnapshot") is False,
                "Kamanaka HEAD description became native proof or original historical freeze")
        require(isinstance(entry.get("description"),str) and len(entry["description"])>5,
                "Original source description absent")
    for independent in ("Samantha-Revita-Elyria-Systems",
                        "invisible-middle-intelligence-layer",
                        "creative-ops-ai-specialist-evaluation"):
        row=next((v for v in sources if v["name"]==independent),None)
        require(row is not None and
                row["relationship"]=="separate_or_adjacent_attribution",
                "Outside project silently assimilated to native V.A.: "+independent)
    stages=data.get("endToEndStages")
    require(isinstance(stages,list) and [x.get("id") for x in stages]==EXPECTED_STAGE_IDS,
            "Twelve end-to-end examination stages incomplete/out of order")
    original_names=set(names)
    for x in stages:
        require(x.get("notAnImplementationSequence") is True and
                x.get("evidenceStatus")=="MIXED_EXAMINE_EACH_ORIGINAL",
                "Examination stages falsely presented as executed architecture")
        require(isinstance(x.get("scope"),str) and len(x["scope"])>32,
                "Stage description incomplete")
        path=x.get("proofEstateRecord")
        require(isinstance(path,str) and not Path(path).is_absolute()
                and ".." not in Path(path).parts
                and (ROOT/path).is_file(),"Stage exact local Deagle source missing: "+str(path))
        for public in x.get("publicPatterns",[]):
            require(public in original_names,"Stage cites unverified public source")
    evidence=data.get("evidenceFamilies")
    require(isinstance(evidence,list) and
            tuple(x.get("id") for x in evidence)==EXPECTED_EVIDENCE,
            "Missing original/historical/physical/BYO/independent evidence lane")
    expected_status={
        "native-current":REQUIRED_NATIVE_PUBLIC_STATUS,
        "independent-native":"NOT_PUBLICLY_ADMITTED",
        "seal":"ORIGINAL_HOLD_DERIVATIVE_PRIVATE_57_OF_57_MATCH",
        "historic-build":"PRIVATE_ORIGINAL_EIGHT_CASE_VERIFIER_REPRODUCED"
    }
    for x in evidence:
        local=x.get("path")
        require(isinstance(local,str) and (ROOT/local).is_file(),
                "Evidence lane has no exact local proof record: "+str(local))
        if x.get("id") in expected_status:
            require(x.get("status")==expected_status[x["id"]],
                    "Historical or native proof stage inappropriately promoted")
    require("not literal computational geometry" not in data.get("architectureSequenceRule","").lower()
            or True,"architectural source rule") # actual check below
    require("not literal computational geometry" in data["architectureSequenceRule"].lower(),
            "Architecture review route may not be treated as constructed topology")
    doc=parse_html(atlas)
    require(doc.stages==["stage-"+x for x in EXPECTED_STAGE_IDS],
            "The website does not show every one of twelve examination stages")
    require(doc.search_input and doc.source_select and "srcCount" in doc.ids,
            "39-source catalog interactive search/filter is missing")
    require(len(doc.repo_rows)==39,
            "Rendered source table omits public repositories")
    for expected, actual in zip(sources,doc.repo_rows):
        cat, searchable=actual
        require(cat==expected["relationship"] and
                expected["name"].lower() in searchable,
                "Displayed source category or search metadata does not match original record")
        require(expected["url"] in doc.links,
                "Public source cannot be opened from end-to-end page: "+expected["name"])
    for special in ("architecture","realization","evidence","applications","sources","examine"):
        require(special in doc.ids,"End-to-end section not accessible: "+special)
    require("proofs/END-TO-END-ESTATE-REGISTER.json" in doc.links,
            "Human/structured provenance crosswalk disconnected")
    for href in doc.links:
        local_link(href,"end-to-end.html")
    home_doc=parse_html(home)
    require("full-estate-atlas" in home_doc.ids and
            "end-to-end.html" in home_doc.links and
            "proofs/FULL-END-TO-END-REPRESENTATION.md" in home_doc.links,
            "Original homepage doesn't introduce full end-to-end architecture")
    require("from" in atlas.lower() and "independent" in atlas.lower()
            and "historical" in atlas.lower() and "consequence" in atlas.lower(),
            "Complete end-to-end narrative absent")
    return {"stages":len(stages),"repositories":len(sources),"evidence":len(evidence),
            "sourceGroups":dict(classifications)}

def main():
    data=json.loads((ROOT/"proofs/END-TO-END-ESTATE-REGISTER.json").read_text(encoding="utf-8"))
    atlas=(ROOT/"end-to-end.html").read_text(encoding="utf-8")
    homepage=(ROOT/"index.html").read_text(encoding="utf-8")
    result=validate(data,atlas,homepage)
    print("PASS: Deagle end-to-end atlas rooted in correct source and current native identity")
    print("PASS: 12 stages, 10 evidence families and 39 original public source identities",result)
    print("PASS: all repo links/source classifications and local evidence carriers connected")
    print("PASS: protected construction, outside authorship and native standing non-promotion retained")

if __name__=="__main__":
    main()
