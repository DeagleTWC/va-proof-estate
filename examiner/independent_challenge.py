#!/usr/bin/env python3
"""Frozen external BYO challenge and signed local reproduction. Synthetic only."""
import argparse, base64, hashlib, json, secrets, subprocess, sys, tempfile
from pathlib import Path
from adversarial_matrix import build_cases, run_matrix, sha, SCOPE as MATRIX_SCOPE
from session_challenge import generate, run as run_session, SCOPE as SESSION_SCOPE
from verify_matrix import integrity_check
from verify_session import verify as verify_session
from compare_reports import compare as compare_reports

CEILING = "SIGNED LOCAL SYNTHETIC INTERFACE CHECK; NOT NATIVE V.A., PHYSICAL PROOF OR INDEPENDENT WITNESS ATTESTATION"
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()
def load(p):
    x=json.loads(Path(p).read_text(encoding="utf8"))
    if type(x) is not dict: raise ValueError("Expected one JSON object")
    return x
def save(p,x): Path(p).write_text(json.dumps(x,sort_keys=True,indent=2)+"\n",encoding="utf8")
def file_sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1048576),b""): h.update(b)
    return h.hexdigest()
def sealed(x,field): return dict(x,**{field:sha(x)})
def unseal(x,schema,field):
    if x.get("schema")!=schema or x.get(field)!=sha({k:v for k,v in x.items() if k!=field}):
        raise ValueError("Altered or invalid "+schema)
def freeze(artifact,participant,revision):
    if not participant.strip() or not revision.strip(): raise ValueError("Name and revision required")
    return sealed({"schema":"DEAGLE-FREEZE-1","participant":participant,"revision":revision,
                   "artifact_sha256":file_sha(artifact),"artifact_size":Path(artifact).stat().st_size,
                   "commitment_nonce":secrets.token_hex(32),
                   "independent_chronology_proven":False},"freeze_sha256")
def check_freeze(f,artifact=None):
    unseal(f,"DEAGLE-FREEZE-1","freeze_sha256")
    if (not isinstance(f.get("commitment_nonce"),str) or len(f["commitment_nonce"])!=64
        or f.get("independent_chronology_proven") is not False
        or not isinstance(f.get("participant"),str) or not f["participant"].strip()
        or not isinstance(f.get("revision"),str) or not f["revision"].strip()):
        raise ValueError("Invalid freeze declaration")
    if artifact and (file_sha(artifact)!=f.get("artifact_sha256") or Path(artifact).stat().st_size!=f.get("artifact_size")):
        raise ValueError("Frozen artifact file differs")
def fixture(family,seed,rounds):
    if family=="matrix": return sha(build_cases(seed,rounds))
    if family=="session": return sha(generate(seed,rounds))
    raise ValueError("Unsupported challenge family")
def issue(f,family,rounds):
    check_freeze(f)
    if type(rounds) is not int or not 1<=rounds<=(40 if family=="matrix" else 20):
        raise ValueError("Invalid rounds")
    seed=secrets.randbits(64)
    return sealed({"schema":"DEAGLE-CHALLENGE-1","freeze_sha256":f["freeze_sha256"],
                   "family":family,"seed":seed,"rounds":rounds,
                   "fixture_sha256":fixture(family,seed,rounds),
                   "examiner_nonce":secrets.token_hex(32),"chronology_authenticated":False,
                   "standing":CEILING},"challenge_sha256")
def check_challenge(f,c):
    check_freeze(f); unseal(c,"DEAGLE-CHALLENGE-1","challenge_sha256")
    if (c.get("freeze_sha256")!=f["freeze_sha256"] or
        type(c.get("seed")) is not int or type(c.get("rounds")) is not int or
        not isinstance(c.get("examiner_nonce"),str) or len(c["examiner_nonce"])!=64 or
        c.get("chronology_authenticated") is not False or c.get("standing")!=CEILING or
        c.get("fixture_sha256")!=fixture(c.get("family"),c["seed"],c["rounds"])):
        raise ValueError("Challenge mismatch")
def check_report(c,r):
    if c["family"]=="matrix":
        if (r.get("protocol")!="DEAGLE-BYO-SEAM-1" or r.get("version")!="MATRIX-1.0"
                or r.get("examiner_scope")!=MATRIX_SCOPE): raise ValueError("Report standing/protocol mismatch")
        integrity_check(r); num=r["case_count"]; report_fixture=r["fixture_manifest_sha256"]; unit=9
    else:
        if r.get("protocol")!="DEAGLE-BYO-SESSION-1" or r.get("scope")!=SESSION_SCOPE:
            raise ValueError("Session standing/protocol mismatch")
        verify_session(r); num=r["event_count"]; report_fixture=r["fixture_sha256"]; unit=27
    if (r.get("seed")!=c["seed"] or r.get("rounds")!=c["rounds"] or
        report_fixture!=c["fixture_sha256"] or num!=unit*c["rounds"]):
        raise ValueError("Report not from issued challenge")
    return num
def examine(f,c,artifact,examiner,argv):
    check_challenge(f,c); check_freeze(f,artifact)
    if not examiner.strip() or not argv: raise ValueError("Examiner and command required")
    if not any(Path(a).resolve()==Path(artifact).resolve() for a in argv):
        raise ValueError("Frozen source file must appear explicitly in adapter command")
    r=(run_matrix(argv,c["seed"],c["rounds"]) if c["family"]=="matrix"
       else run_session(argv,c["seed"],c["rounds"]))
    if "error" in r and c["family"]=="session": raise ValueError("Incomplete stateful report")
    count=check_report(c,r)
    obj={"schema":"DEAGLE-WITNESS-RECORD-1","freeze_sha256":f["freeze_sha256"],
         "challenge_sha256":c["challenge_sha256"],"artifact_sha256":f["artifact_sha256"],
         "fixture_sha256":c["fixture_sha256"],"participant":f["participant"],
         "examiner":examiner,"report_sha256":r["report_sha256"],
         "pass_count":r["pass_count"],"case_count":count,"standing":CEILING,
         "real_effect_witnessed":False,"native_VA_execution":False,
         "identity_authenticated":False,"separate_host_execution_authenticated":False}
    return r,sealed(obj,"record_sha256")
def check_record(f,c,r,w,artifact=None):
    check_challenge(f,c); check_freeze(f,artifact)
    unseal(w,"DEAGLE-WITNESS-RECORD-1","record_sha256"); count=check_report(c,r)
    expected={"freeze_sha256":f["freeze_sha256"],"challenge_sha256":c["challenge_sha256"],
              "artifact_sha256":f["artifact_sha256"],"fixture_sha256":c["fixture_sha256"],
              "participant":f["participant"],"report_sha256":r["report_sha256"],
              "pass_count":r["pass_count"],"case_count":count,"standing":CEILING,
              "real_effect_witnessed":False,"native_VA_execution":False,
              "identity_authenticated":False,"separate_host_execution_authenticated":False}
    if not isinstance(w.get("examiner"),str) or not w["examiner"].strip():
        raise ValueError("Examiner declaration missing")
    if set(w)!=(set(expected)|{"examiner","schema","record_sha256"}) or any(w.get(k)!=v for k,v in expected.items()):
        raise ValueError("Witness record changed, contains unexpected fields, or promotes status")
def openssl(args,data=None):
    try: p=subprocess.run(["openssl",*map(str,args)],input=data,capture_output=True,check=False)
    except FileNotFoundError as e: raise ValueError("OpenSSL command-line required") from e
    if p.returncode: raise ValueError("OpenSSL refused operation or signature")
    return p.stdout
def pub_der(pub): return openssl(["pkey","-pubin","-in",pub,"-outform","DER"])
def sign(w,priv,pub):
    unseal(w,"DEAGLE-WITNESS-RECORD-1","record_sha256")
    if openssl(["pkey","-in",priv,"-pubout","-outform","DER"])!=pub_der(pub):
        raise ValueError("Public key does not match private key")
    signature=openssl(["dgst","-sha256","-sign",priv],canon(w))
    return {"schema":"DEAGLE-SIGNED-WITNESS-1","record_sha256":w["record_sha256"],
            "public_key_sha256":hashlib.sha256(pub_der(pub)).hexdigest(),
            "signature_b64":base64.b64encode(signature).decode("ascii"),
            "real_identity_authenticated":False}
def check_signature(w,s,pub):
    unseal(w,"DEAGLE-WITNESS-RECORD-1","record_sha256")
    fp=hashlib.sha256(pub_der(pub)).hexdigest()
    if (set(s)!={"schema","record_sha256","public_key_sha256","signature_b64","real_identity_authenticated"}
        or s.get("schema")!="DEAGLE-SIGNED-WITNESS-1" or
        s.get("record_sha256")!=w["record_sha256"] or
        s.get("public_key_sha256")!=fp or s.get("real_identity_authenticated") is not False):
        raise ValueError("Unsupported signature/identity metadata")
    try: sig=base64.b64decode(s["signature_b64"],validate=True)
    except (KeyError,TypeError,ValueError) as e: raise ValueError("Bad signature encoding") from e
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"sig";p.write_bytes(sig)
        openssl(["dgst","-sha256","-verify",pub,"-signature",str(p)],canon(w))
    return fp
def cross(f,c,l,r):
    for entry in (l,r):
        check_record(f,c,entry["report"],entry["record"])
        entry["key"]=check_signature(entry["record"],entry["signature"],entry["public_key"])
    if l["key"]==r["key"] or l["record"]["examiner"]==r["record"]["examiner"]:
        raise ValueError("Two distinct signing keys and declared examiners required")
    out=compare_reports(l["report"],r["report"],l["record"]["examiner"],r["record"]["examiner"])
    return sealed({"schema":"DEAGLE-CROSS-EXAM-1","freeze_sha256":f["freeze_sha256"],
                   "challenge_sha256":c["challenge_sha256"],"left_record_sha256":l["record"]["record_sha256"],
                   "right_record_sha256":r["record"]["record_sha256"],"left_key_sha256":l["key"],
                   "right_key_sha256":r["key"],"case_count":out["case_count"],
                   "matching_cases":out["matching_results"],"differing_cases":out["differing_results"],
                   "independent_identity_verified":False,"separate_execution_verified":False,
                   "native_VA_execution":False,"standing":CEILING},"comparison_sha256")
def main():
    p=argparse.ArgumentParser(description="Frozen public-safe challenge and two-key local witness records")
    s=p.add_subparsers(dest="action",required=True)
    z=s.add_parser("freeze")
    for n in ("artifact","participant","revision","out"):z.add_argument("--"+n,required=True)
    z=s.add_parser("issue")
    for n in ("freeze","family","out"):z.add_argument("--"+n,required=True)
    z.add_argument("--rounds",type=int,default=2)
    z=s.add_parser("run")
    for n in ("freeze","challenge","artifact","examiner","report","record"):z.add_argument("--"+n,required=True)
    z.add_argument("--adapter",nargs=argparse.REMAINDER,required=True)
    z=s.add_parser("sign")
    for n in ("freeze","challenge","report","record","private-key","public-key","out"):
        z.add_argument("--"+n,required=True)
    z=s.add_parser("verify")
    for n in ("freeze","challenge","report","record","signature","public-key"):
        z.add_argument("--"+n,required=True)
    z.add_argument("--artifact")
    z=s.add_parser("compare")
    for n in ("freeze","challenge","out"):z.add_argument("--"+n,required=True)
    for side in ("left","right"):
        for n in ("report","record","signature","public-key"):z.add_argument("--"+side+"-"+n,required=True)
    a=p.parse_args()
    try:
        if a.action=="freeze": result=freeze(a.artifact,a.participant,a.revision);save(a.out,result)
        elif a.action=="issue": result=issue(load(a.freeze),a.family,a.rounds);save(a.out,result)
        elif a.action=="run":
            result,record=examine(load(a.freeze),load(a.challenge),a.artifact,a.examiner,a.adapter)
            save(a.report,result);save(a.record,record)
        elif a.action=="sign":
            f,c,r,w=map(load,(a.freeze,a.challenge,a.report,a.record));check_record(f,c,r,w)
            result=sign(w,a.private_key,a.public_key);save(a.out,result)
        elif a.action=="verify":
            f,c,r,w=map(load,(a.freeze,a.challenge,a.report,a.record))
            check_record(f,c,r,w,a.artifact)
            result={"status":"SIGNED_SYNTHETIC_RECORD_VALID",
                    "public_key_sha256":check_signature(w,load(a.signature),a.public_key),
                    "identity_verified":False,"native_VA_execution":False,"standing":CEILING}
        else:
            f,c=load(a.freeze),load(a.challenge);left={};right={}
            for side,entry in (("left",left),("right",right)):
                for n in ("report","record","signature"):entry[n]=load(getattr(a,side+"_"+n))
                entry["public_key"]=getattr(a,side+"_public_key")
            result=cross(f,c,left,right);save(a.out,result)
        print(json.dumps(result,sort_keys=True,indent=2));return 0
    except (OSError,ValueError,KeyError,TypeError,AssertionError,json.JSONDecodeError) as e:
        print("EXAMINATION REFUSED: "+str(e),file=sys.stderr);return 1
if __name__=="__main__":sys.exit(main())
