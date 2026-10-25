#!/usr/bin/env python3
"""No real candidate is created: validate issuance only with a synthetic Github comment."""
import copy
import json
import unittest
from datetime import datetime, timezone
from pathlib import Path
from independent_challenge import freeze
from issue_cycle_challenge import issue_from_comment, verify, REPO

ARTIFACT = Path(__file__).resolve().parent / "example_layer.py"
NOW = datetime(2026, 10, 25, 15, tzinfo=timezone.utc)

def comment():
    return {"id":123456789,
            "issue_url":"https://api.github.com/repos/"+REPO+"/issues/1",
            "html_url":"https://github.com/"+REPO+"/issues/1#issuecomment-123456789",
            "user":{"login":"outside-engineer"},
            "created_at":"2026-10-25T14:00:00Z",
            "updated_at":"2026-10-25T14:00:00Z",
            "body":json.dumps(freeze(ARTIFACT,"Example external actor","r1"),sort_keys=True)}

class IssuanceTests(unittest.TestCase):
    def make(self,c=None,actor="deagle-custodian"):
        return issue_from_comment(c if c is not None else comment(),actor,887765,1,"a"*40,"session",1,NOW)

    def test_issued_packet_and_tamper(self):
        frozen,challenge,receipt,snapshot=self.make()
        self.assertEqual(verify(frozen,challenge,receipt,snapshot)["status"],"LOCAL_ISSUANCE_PACKET_VALID")
        self.assertFalse(receipt["native_VA_execution"])
        changed=copy.deepcopy(challenge)
        changed["seed"]+=1
        with self.assertRaises(ValueError):verify(frozen,changed,receipt,snapshot)
        changed=copy.deepcopy(receipt)
        changed["native_VA_execution"]=True
        with self.assertRaises(ValueError):verify(frozen,challenge,changed,snapshot)
        changed=copy.deepcopy(snapshot)
        changed["body"]+="\n"
        with self.assertRaises(ValueError):verify(frozen,challenge,receipt,changed)

    def test_edited_wrong_issue_or_self_issued_refused(self):
        c=comment();c["updated_at"]="2026-10-25T14:01:00Z"
        with self.assertRaises(ValueError):self.make(c)
        c=comment();c["issue_url"]=c["issue_url"].replace("/issues/1","/issues/2")
        with self.assertRaises(ValueError):self.make(c)
        c=comment();c["body"]="not a freeze"
        with self.assertRaises(ValueError):self.make(c)
        c=comment();c["created_at"]="2026-10-25T16:00:00Z";c["updated_at"]=c["created_at"]
        with self.assertRaises(ValueError):self.make(c)
        with self.assertRaises(ValueError):self.make(comment(),"outside-engineer")

if __name__=="__main__":unittest.main()
