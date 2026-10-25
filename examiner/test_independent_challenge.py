#!/usr/bin/env python3
"""External examiner local positive/negative, signature, and falsification checks."""
import copy, subprocess, sys, tempfile, unittest
from pathlib import Path
from independent_challenge import freeze, issue, examine, check_record, check_challenge, sign, check_signature, cross
ROOT=Path(__file__).resolve().parents[1]/"examiner"
def keypair(root,name):
    priv=root/(name+"-private.pem");pub=root/(name+"-public.pem")
    subprocess.run(["openssl","genpkey","-algorithm","RSA","-pkeyopt","rsa_keygen_bits:2048",
                    "-out",str(priv)],check=True,capture_output=True)
    subprocess.run(["openssl","pkey","-in",str(priv),"-pubout","-out",str(pub)],check=True,capture_output=True)
    return priv,pub
class TestExternal(unittest.TestCase):
    def test_frozen_matrix_and_signatures(self):
        artifact=ROOT/"example_layer.py"
        f=freeze(artifact,"Participant A","rev1");c=issue(f,"matrix",1)
        cmd=[sys.executable,str(artifact)]
        a,ra=examine(f,c,artifact,"Examiner Alpha",cmd)
        b,rb=examine(f,c,artifact,"Examiner Beta",cmd)
        self.assertEqual(a["pass_count"],9)
        with tempfile.TemporaryDirectory() as td:
            d=Path(td);pk1,pub1=keypair(d,"one");pk2,pub2=keypair(d,"two")
            s1=sign(ra,pk1,pub1);s2=sign(rb,pk2,pub2)
            self.assertNotEqual(check_signature(ra,s1,pub1),check_signature(rb,s2,pub2))
            result=cross(f,c,{"report":a,"record":ra,"signature":s1,"public_key":pub1},
                           {"report":b,"record":rb,"signature":s2,"public_key":pub2})
            self.assertEqual(result["matching_cases"],9)
            self.assertFalse(result["independent_identity_verified"])
            self.assertFalse(result["separate_execution_verified"])
            with self.assertRaises(ValueError):check_signature(ra,s1,pub2)
            changed=copy.deepcopy(ra);changed["pass_count"]=-1
            with self.assertRaises(ValueError):check_signature(changed,s1,pub1)
            altered=copy.deepcopy(a);altered["cases"][0]["passed"]=False
            with self.assertRaises(ValueError):check_record(f,c,altered,ra,artifact)
            wrong=copy.deepcopy(c);wrong["seed"]+=1
            with self.assertRaises(ValueError):check_challenge(f,wrong)
            changed_file=d/"changed.py";changed_file.write_bytes(artifact.read_bytes()+b"# modified")
            with self.assertRaises(ValueError):check_record(f,c,a,ra,changed_file)
            with self.assertRaises(ValueError):
                cross(f,c,{"report":a,"record":ra,"signature":s1,"public_key":pub1},
                      {"report":a,"record":ra,"signature":s1,"public_key":pub1})
            with self.assertRaises(ValueError):
                examine(f,c,artifact,"Fake",[sys.executable,"-c","print('x')"])
    def test_session_and_unsafe_negative(self):
        good=ROOT/"session_reference.py";f=freeze(good,"P","1");c=issue(f,"session",1)
        report,record=examine(f,c,good,"E",[sys.executable,str(good)])
        self.assertEqual(report["pass_count"],27)
        check_record(f,c,report,record,good)
        bad=ROOT/"session_broken.py";f2=freeze(bad,"Q","1");c2=issue(f2,"session",1)
        negative,rec=examine(f2,c2,bad,"Negative",[sys.executable,str(bad)])
        self.assertLess(negative["pass_count"],27)
        self.assertFalse(rec["native_VA_execution"])
        with self.assertRaises(ValueError):check_record(f,c,negative,rec)
if __name__=="__main__":unittest.main()
