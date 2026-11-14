#!/usr/bin/env python3
"""Attach only original public PDFs to two existing Zenodo RDM draft records.
Official current InvenioRDM file upload protocol; does NOT publish records.
"""
import hashlib, os, pathlib, sys, requests

ROOT = pathlib.Path(__file__).resolve().parents[1]
API = "https://zenodo.org/api/records"
TARGETS = {
    "grid-k1": (24194644,
        "research/grid-k1/Snyder_GRID_K1_Infrastructure_Continuity_Formal_Proofs_2026-11-11.pdf",
        "57ae364ba9ddc398ac8b8b02c19ad04ed0ec2c1b3478d28d642e677412308ddc",
        320368, "GRID-K1"),
    "adg": (24194875,
        "research/admissibility-debt-geometry/Snyder_Admissibility_Debt_Geometry_Formal_Proofs_2026-11-11.pdf",
        "d5efe3dd89c8a7cca5e097292a8276df7884383d7ec0154a81f7d9b5ebe81e57",
        302294, "Admissibility"),
}

def expect(response, action, ok=(200, 201, 202)):
    print(action, "HTTP", response.status_code)
    if response.status_code not in ok:
        print("Zenodo error:", response.text[:900])
        raise SystemExit("Zenodo operation failed: " + action)
    return response.json()

def files_list(result):
    entries = result.get("entries", result) if isinstance(result,dict) else result
    if isinstance(entries, dict):
        return [dict(x, key=k) if isinstance(x,dict) and not x.get("key") else x for k,x in entries.items()]
    return entries if isinstance(entries,list) else []

def main():
    if len(sys.argv)!=2 or sys.argv[1] not in TARGETS:
        raise SystemExit("Choose grid-k1 or adg")
    token=os.environ.get("ZENODO_TOKEN")
    if not token: raise SystemExit("Missing authenticated GitHub Zenodo secret; no upload")
    rid, rel_path, sha, size, title_prefix=TARGETS[sys.argv[1]]
    p=ROOT/rel_path
    data=p.read_bytes()
    if len(data)!=size or hashlib.sha256(data).hexdigest()!=sha:
        raise SystemExit("Original public PDF hash or size mismatch; NO UPLOAD.")
    sess=requests.Session()
    sess.headers.update({
        "Authorization":"Bearer "+token,
        "User-Agent":"VA-Public-Research-Zenodo-PDF-Transfer/1.0 (+https://github.com/DeagleTWC/va-proof-estate)"
    })
    # Read-only authentication preflight using Zenodo's documented legacy endpoint.
    # Print status codes only; never log bearer token or personal account fields.
    public=requests.get("https://zenodo.org/api/records",params={"size":1},headers={"User-Agent":"VA-Public-Research-Zenodo-Diagnostic/1.0"},timeout=35)
    print("ZENODO_PUBLIC_API_NO_AUTH_STATUS",public.status_code)
    if not public.ok: print("ZENODO_PUBLIC_ERROR",public.text[:350].replace("\\n"," "))
    legacy=sess.get("https://zenodo.org/api/deposit/depositions",timeout=35)
    print("ZENODO_LEGACY_API_AUTH_STATUS",legacy.status_code)
    if not legacy.ok: print("ZENODO_LEGACY_ERROR",legacy.text[:350].replace("\\n"," "))
    if legacy.ok:
        deposits=legacy.json()
        print("ZENODO_LEGACY_DEPOSIT_COUNT",len(deposits) if isinstance(deposits,list) else "nonlist")
    current=sess.get("https://zenodo.org/api/user/records",timeout=35)
    print("ZENODO_CURRENT_USER_RECORDS_STATUS",current.status_code)
    if current.ok:
        hits=current.json().get("hits",{}).get("hits",[])
        print("ZENODO_CURRENT_USER_RECORDS_COUNT",len(hits))
        for d in hits:
            if str(d.get("id"))==str(rid):
                print("ZENODO_TARGET_ID_IN_USER_RECORDS","yes")
    base=f"{API}/{rid}/draft"
    response=sess.get(base,timeout=35)
    if response.status_code != 200:
        print("Draft lookup status", response.status_code, "message", response.text[:260])
        me=sess.get("https://zenodo.org/api/me",timeout=25)
        print("Zenodo token account test", me.status_code)
        # Summarize only public research record IDs and titles; no account email/token in logs.
        listing=sess.get("https://zenodo.org/api/user/records?is_published=false&size=100",timeout=35)
        print("Zenodo user draft listing status",listing.status_code)
        if listing.ok:
            body=listing.json()
            hits=body.get("hits",{}).get("hits",[]) if isinstance(body,dict) else []
            print("Available draft count",len(hits))
            for obj in hits:
                title=str(obj.get("metadata",{}).get("title",""))
                if any(word.lower() in title.lower() for word in ("GRID-K1","Admissibility")):
                    print("Matching user draft",obj.get("id"),title[:100])
        raise SystemExit("Target draft not visible through Zenodo API; no file upload attempted")
    draft=response.json()
    title=draft.get("metadata",{}).get("title","")
    if title_prefix.lower() not in title.lower() or str(draft.get("id"))!=str(rid):
        raise SystemExit(f"Wrong Zenodo draft identity or title: id={rid} title={title!r}")
    print("Verified draft title:",title)
    files_base=base+"/files"
    entries=files_list(expect(sess.get(files_base,timeout=35),"GET current draft file list"))
    name=p.name
    existing=[f for f in entries if f.get("key",f.get("filename",f.get("name")))==name]
    if existing:
        if existing[0].get("status")!="completed":
            raise SystemExit("Same-name file is in unfinished state; do not overwrite.")
        print("Existing completed file; verifying.")
    else:
        expect(sess.post(files_base,json=[{"key":name}],timeout=35),"POST initialize PDF")
        expect(sess.put(files_base+"/"+name+"/content",data=data,
                 headers={"Content-Type":"application/octet-stream"},
                 timeout=90),"PUT original PDF bytes",ok=(200,201))
        committed=expect(sess.post(files_base+"/"+name+"/commit",timeout=90),"POST commit PDF")
        print("Commit status",committed.get("status"),"size",committed.get("size"))
    state=files_list(expect(sess.get(files_base,timeout=35),"GET verify committed PDF"))
    matches=[f for f in state if f.get("key",f.get("filename",f.get("name")))==name]
    if not matches: raise SystemExit("PDF missing from Zenodo draft.")
    remote=matches[0]
    if remote.get("status")!="completed":
        raise SystemExit("Zenodo has not committed PDF (status "+str(remote.get("status"))+")")
    if int(remote.get("size",-1))!=size:
        raise SystemExit("Remote committed file size mismatch")
    md5=str(remote.get("checksum","")).split(":")[-1]
    if md5 and md5 != hashlib.md5(data).hexdigest():
        raise SystemExit("Remote MD5 checksum mismatch")
    print("PDF VERIFIED AND ATTACHED to draft",rid, name, size,"bytes.")
    print("SHA256",sha)
    print("DRAFT_URL",f"https://zenodo.org/uploads/{rid}")
    print("NOTICE: NOT YET PUBLISHED. Publication requires final copyright review.")

if __name__=="__main__":main()
