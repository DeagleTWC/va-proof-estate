#!/usr/bin/env python3
"""Check accessible, source-bound evidence reading navigation (not native proof)."""
from __future__ import annotations
import re
from html.parser import HTMLParser
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE_LINK = re.compile(r'href="(?:https://github.com/DeagleTWC/va-proof-estate/blob/main/)?([^"]+\.(?:md|json|html))"')

def validate(root=ROOT):
    root=Path(root).resolve()
    faults=[]
    try:
        reader=(root/"source-reading.html").read_text(encoding="utf-8")
        foundation=(root/"foundation.html").read_text(encoding="utf-8")
        reviewer=(root/"reviewer-route.html").read_text(encoding="utf-8")
    except OSError as exc:
        return [f"missing reader page: {exc}"]
    for html,tag in ((reader,"source-reading"),(foundation,"foundation"),(reviewer,"reviewer-route")):
        if 'href="#main">Skip to main content' not in html:
            faults.append(f"{tag} lacks keyboard skip link")
        if '<main id="main">' not in html:
            faults.append(f"{tag} lacks main landmark destination")
        if 'lang="en"' not in html:
            faults.append(f"{tag} lacks document language")
    for name,page in (("foundation","foundation.html"),("reviewer","reviewer-route.html")):
        if 'href="source-reading.html"' not in (foundation if name=="foundation" else reviewer):
            faults.append(f"{name} page has no source reader navigation")
    sources=set()
    for rel in SOURCE_LINK.findall(reader):
        if rel in ("source-reading.html","reviewer-route.html","index.html","foundation.html","end-to-end.html"):
            continue
        sources.add(rel)
        p=(root/rel).resolve()
        if not p.is_relative_to(root) or not p.is_file():
            faults.append("missing or unsafe public source: "+rel)
    if len(sources)<9:
        faults.append("source-reading inventory too short")
    if "synthetic observation cannot be relabeled" not in reader:
        faults.append("synthetic evidence boundary missing")
    if "Protected True Zero / corrected NEW-K" not in reader:
        faults.append("private foundation boundary missing")
    return faults

if __name__=="__main__":
    errors=validate()
    for error in errors:print("SOURCE READER ERROR:",error)
    if errors:raise SystemExit(1)
    print("PASS: source-reading navigation, keyboard access and original public source paths")
