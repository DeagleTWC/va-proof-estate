#!/usr/bin/env python3
"""Transfer an original public PDF into a previously verified Zenodo draft.
The user's authenticated Zenodo browser already verified both IDs/creators.
Only the exact release-manifest SHA256 and size are permitted. Never publish
without a separate remote verification pass.
"""
import hashlib, os, pathlib, sys, requests

ROOT=pathlib.Path(__file__).resolve().parents[1]
URL="https://zenodo.org/api/records"
TARGETS={
 "grid-k1":(24194644,"research/grid-k1/Snyder_GRID_K1_Infrastructure_Continuity_Formal_Proofs_2026-11-11.pdf","57ae364ba9ddc398ac8b8b02c19ad04ed0ec2c1b3478d28d642e677412308ddc",320368,"GRID-K1"),
 "adg":(24194875,"research/admissibility-debt-geometry/Snyder_Admissibility_Debt_Geometry_Formal_Proofs_2026-11-11.pdf","d5efe3dd89c8a7cca5e097292a8276df7884383d7ec0154a81f7d9b5ebe81e57",302294,"Admissibility")
}

def check(res,step,codes=(200,201,202)):
 print(step,"HTTP",res.status_code)
 if res.status_code not in codes:
  print("Zenodo response",res.text[:350].replace("\n"," "))
  raise SystemExit("Stopped without publication.")
 return res.json()

def main():
 if len(sys.argv)!=2 or sys.argv[1] not in TARGETS:
  raise SystemExit("Choose grid-k1 or adg")
 token=os.environ.get("ZENODO_TOKEN")
 if not token:raise SystemExit("No Zenodo token")
 print("ZENODO_TOKEN_SHAPE", "length",len(token), "alphanumeric",token.isalnum(),"64_chars",len(token)==64)
 rid,rel,expected,size,word=TARGETS[sys.argv[1]]
 path=ROOT/rel
 data=path.read_bytes()
 sha=hashlib.sha256(data).hexdigest()
 if len(data)!=size or sha!=expected:raise SystemExit("Source does not match release manifest; STOP")
 sess=requests.Session()
 sess.headers.update({"Authorization":"Bearer "+token,"User-Agent":"VA-Public-Research-Transfer/1.0 (+https://github.com/DeagleTWC/va-proof-estate)"})
 base=f"{URL}/{rid}/draft"
 d=sess.get(base,timeout=40)
 print("Zenodo draft read HTTP",d.status_code)
 if d.ok:
  obj=d.json()
  if str(obj.get("id"))!=str(rid) or word.lower() not in obj.get("metadata",{}).get("title","").lower():
   raise SystemExit("Wrong target title/ID, STOP")
 elif d.status_code not in (403,404):
  check(d,"Get existing draft")
 else:
  # Two exact targets verified in signed-in account via Zenodo browser UI.
  # Permission to write is enforced independently by server on every request.
  print("Read access denied; attempt permitted write to confirmed draft ID",rid)
 files=f"{base}/files"
 existing=sess.get(files,timeout=35)
 print("File-list read HTTP",existing.status_code)
 if existing.ok:
  entries=existing.json()
  if isinstance(entries,dict):entries=entries.get("entries",[])
  if any(f.get("key",f.get("filename"))==path.name and f.get("status")=="completed" for f in entries):
   print("Original PDF already committed, no duplicate action")
   return
 check(sess.post(files,json=[{"key":path.name}],timeout=45),"Initialize original PDF")
 check(sess.put(f"{files}/{path.name}/content",data=data,headers={"Content-Type":"application/octet-stream"},timeout=120),"Upload exact PDF bytes")
 commit=check(sess.post(f"{files}/{path.name}/commit",timeout=90),"Commit original PDF")
 if commit.get("status")!="completed" or commit.get("size")!=size:
  raise SystemExit("File commit or byte count not verified; draft left unpublished")
 print("PDF ATTACHED",rid,path.name,size,sha)
 print("This workflow deliberately does not publish.")

if __name__=="__main__": main()
