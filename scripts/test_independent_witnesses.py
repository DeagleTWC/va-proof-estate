#!/usr/bin/env python3
"""Ephemeral real RSA detached-signature regression. Data and keys are synthetic and private."""
import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from verify_independent_witnesses import validate

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def encode(data):
    return (json.dumps(data, sort_keys=True, indent=2) + "\n").encode("utf-8")

def create(root, rel, data):
    path=root/rel
    path.parent.mkdir(parents=True, exist_ok=True)
    content=encode(data) if isinstance(data, dict) else data
    path.write_bytes(content)
    return {"path":rel,"sha256":sha(content)}

def run(*args):
    p=subprocess.run(["openssl", *map(str,args)],check=False,capture_output=True,text=True)
    if p.returncode:
        raise AssertionError("OpenSSL test setup: "+p.stderr[:350])

def genkeys(root):
    for i in (1,2):
        priv=root/f"test-key-{i}.pem"
        pub=root/f"pub-{i}.pem"
        run("genpkey","-algorithm","RSA","-pkeyopt","rsa_keygen_bits:2048","-out",priv)
        run("pkey","-in",priv,"-pubout","-out",pub)

def sign(root, path, observer):
    signature=root/(path+".sig")
    run("dgst","-sha256","-sign",root/f"test-key-{observer}.pem","-out",signature,root/path)
    return {"path":path+".sig","sha256":sha(signature.read_bytes())}

def refused(root, description):
    try:validate(root,root/"original-synthetic.bin")
    except (ValueError,KeyError,TypeError,OSError):
        return
    raise AssertionError("Fail-open independent witness preflight: "+description)

def packet(root):
    root.mkdir()
    (root/"original-synthetic.bin").write_bytes(b"SYNTHETIC NONOPERATIONAL TEST ARTIFACT\n")
    orig=sha((root/"original-synthetic.bin").read_bytes())
    genkeys(root)
    challenge={
        "schema":"va-witness-challenge/1.0","challengeId":"TEST-SYNTHETIC-001",
        "originalFrozenSHA256":orig,"declaredRoutes":["route-A","route-B"]}
    challenge_ref=create(root,"challenge.json",challenge)
    bundle={
        "schema":"va-independent-observation-bundle/1.0",
        "classification":"PRIVATE_CUSTODIAL_REVIEW","releaseAuthorized":False,
        "independentHumanWitnessStatus":"NOT_AUTHENTICATED",
        "originalFrozenSHA256":orig,
        "challenge":challenge_ref,
        "unexaminedNegativeRoutes":["route-B"],
        "cases":[]}
    for cid,kind,cond,route,original in [
        ("allowed-01","ALLOW","condition-valid","route-A",None),
        ("refused-01","REFUSE","condition-invalid","route-A",None),
        ("changed-01","CHANGED","condition-revoked","route-A","allowed-01")]:
        d=sha(cond.encode());candidate="same-candidate"
        decision="EXECUTE" if kind=="ALLOW" else "REFUSE"
        receipt=create(root,f"receipts/{cid}.json",{
            "caseId":cid,"candidateId":candidate,"decision":decision,
            "governingConditionSHA256":d})
        case={"caseId":cid,"kind":kind,"candidateId":candidate,
              "governingConditionSHA256":d,"route":route,
              "decision":decision,"receipt":receipt,"witnesses":[]}
        if original:
            case["changedFrom"]=original
        for i in (1,2):
            observer=f"SYNTHETIC-OBSERVER-{i}"
            method="SEPARATE_SYSTEM_AUDIT"
            measurement=create(root,f"measurements/{cid}-observer-{i}.json",{
                "schema":"va-external-effect-measurement/1.0",
                "caseId":cid,"observerId":observer,"observedRoute":route,
                "effectObserved":kind=="ALLOW",
                "instrumentId":f"TEST-INSTRUMENT-{i}",
                "sourceDescription":"Artificial offline counter record for unit tests, not an actual effect."})
            statement={
                "schema":"va-independent-effect-statement/1.0",
                "caseId":cid,"candidateId":candidate,"challengeId":challenge["challengeId"],
                "challengeSHA256":challenge_ref["sha256"],"originalFrozenSHA256":orig,
                "originalReceiptSHA256":receipt["sha256"],
                "governingConditionSHA256":d,"declaredRoute":route,
                "effectObserved":kind=="ALLOW",
                "measurementExternalToDecisionLabel":True,
                "measurementMethod":method,
                "methodology":"Synthetic offline third-party-style observation of a dummy counter only.",
                "instrumentId":f"TEST-INSTRUMENT-{i}",
                "observerId":observer,
                "independenceDeclaration":"I conducted this observation separately; affiliations and conflicts are disclosed.",
                "affiliationAndConflicts":"Synthetic test; no real person or conflict assertion.",
                "measurement":measurement}
            ref=create(root,f"statements/{cid}-observer-{i}.json",statement)
            sig=sign(root,ref["path"],i)
            pub=root/f"pub-{i}.pem"
            case["witnesses"].append({
                "statement":ref,"signature":sig,
                "publicKey":{"path":f"pub-{i}.pem","sha256":sha(pub.read_bytes())}})
        bundle["cases"].append(case)
    (root/"manifest.json").write_bytes(encode(bundle))
    return bundle

def rebuild_statement(root,d,ci=0,wi=0):
    ref=d["cases"][ci]["witnesses"][wi]["statement"]
    sig=d["cases"][ci]["witnesses"][wi]["signature"]
    path=root/ref["path"]
    ref["sha256"]=sha(path.read_bytes())
    new_sig=sign(root,ref["path"],wi+1)
    sig.update(new_sig)
    (root/"manifest.json").write_bytes(encode(d))

def main():
    with tempfile.TemporaryDirectory(prefix="synthetic-signed-witness-") as temp:
        root=Path(temp)/"packet"
        good=packet(root)
        verified=validate(root,root/"original-synthetic.bin")
        assert verified["result"]=="SIGNED_RECORDS_INTERNALLY_BOUND_HUMAN_QUALIFICATION_PENDING"
        assert verified["casesChecked"]==3
        assert verified["detachedWitnessSignaturesVerified"]==6
        assert verified["frozenOriginalBytesRechecked"] is True
        assert verified["knownUnexaminedNegativeRoutes"]==["route-B"]
        assert verified["humanWitnessIndependenceAuthenticated"] is False
        assert verified["externalConsequencesIndependentlyValidatedByThisTool"] is False
        original_files={p.relative_to(root).as_posix():p.read_bytes()
                        for p in root.rglob("*") if p.is_file()}
        def restore():
            for rel,data in original_files.items():
                (root/rel).write_bytes(data)
        def mutate_manifest(fn,reason):
            restore()
            d=copy.deepcopy(good)
            fn(d)
            (root/"manifest.json").write_bytes(encode(d))
            refused(root,reason)
        def mutate_signed(fn,reason):
            restore()
            d=copy.deepcopy(good)
            ref=d["cases"][0]["witnesses"][0]["statement"]
            path=root/ref["path"];obj=json.loads(path.read_text())
            fn(obj)
            path.write_bytes(encode(obj))
            rebuild_statement(root,d,0,0)
            refused(root,reason)
        def corrupt_raw(rel,reason):
            restore()
            path=root/rel;path.write_bytes(b"SYNTHETIC TAMPER")
            refused(root,reason)
        mutate_manifest(lambda d:d.update(releaseAuthorized=True),"unapproved release")
        mutate_manifest(lambda d:d.update(independentHumanWitnessStatus="CERTIFIED"),"fake identity standing")
        mutate_manifest(lambda d:d["cases"][1].update(decision="EXECUTE"),"refusal flips execution")
        mutate_manifest(lambda d:d["cases"][2].update(changedFrom="refused-01"),"invalid changed control")
        mutate_manifest(lambda d:d.update(unexaminedNegativeRoutes=[]),"undeclared effect route gap")
        mutate_manifest(lambda d:d["cases"][0]["witnesses"][1].update(publicKey=d["cases"][0]["witnesses"][0]["publicKey"]),"two observers same key")
        corrupt_raw("statements/allowed-01-observer-1.json","unsigned witness mutation")
        corrupt_raw("challenge.json","frozen challenge mutation")
        corrupt_raw("measurements/refused-01-observer-2.json","external measurement mutation")
        mutate_signed(lambda x:x.update(originalFrozenSHA256="0"*64),"signed but crossbound wrong original")
        mutate_signed(lambda x:x.update(originalReceiptSHA256="0"*64),"signed but wrong original receipt")
        mutate_signed(lambda x:x.update(effectObserved=False),"signed false positive")
        mutate_signed(lambda x:x.update(declaredRoute="route-B"),"signed untested route")
        mutate_signed(lambda x:x.update(measurementExternalToDecisionLabel=False),"signer self-report not effect")
        mutate_signed(lambda x:x.update(affiliationAndConflicts=""),"unsigned conflict disclosures")
        restore()
        assert validate(root,root/"original-synthetic.bin")["detachedWitnessSignaturesVerified"]==6
        print("PASS: six synthetic RSA detached signatures verified over three bounded cases")
        print("PASS: 15 tamper/false-role/cross-binding/non-effect/route-gap mutations refused")
        print("PASS: no actual third-party identity, native V.A. effect or disclosure standing conferred")

if __name__=="__main__":
    main()
