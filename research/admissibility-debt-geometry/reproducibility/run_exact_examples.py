#!/usr/bin/env python3
"""Public-safe exact-rational worked-example witness, NOT proprietary URK code.
Preserves distinctions between theorem derivation and finite example verification.
Usage: python reproducibility/run_exact_examples.py
"""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'; OUT.mkdir(parents=True, exist_ok=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(obj):return json.dumps(obj,sort_keys=True,separators=(',',':')).encode('utf-8')
def f(q):return str(q)
SOURCE=ROOT/'source'/'MATH_SOLUTIONS_original_unchanged.txt'
source_sha=sha(SOURCE.read_bytes())
spec={"title":"Admissibility-Debt Geometry: exact one-run example", "source_sha256":source_sha,"d0":"1/3","dmax":"10/3","stress_segments":[{"start":"0","end":"2","kappa":"1/2"},{"start":"2","end":None,"kappa":"3/2"}],"tensor_initial_diagonal":["1/3","2/3"],"tensor_rate_diagonal":["1/2","1/4"],"tensor_max":"5/3","claim_scope":"finite exact rational demonstration of the published algebraic identities; analytic theorems are proved in the manuscript"}
contract_id=sha(canon(spec))
(OUT/'PREPARED_CONTRACT.json').write_text(json.dumps(spec|{'contract_sha256':contract_id},indent=2,sort_keys=True)+'\n')
d0=Q(1,3); dmax=Q(10,3)
segments=[(Q(0),Q(2),Q(1,2)),(Q(2),None,Q(3,2))]
def debt(t):
 y=d0
 for a,b,k in segments:
  y+=k*max(Q(0),(min(t,b) if b is not None else t)-a)
 return y
assert debt(Q(0))==d0
assert debt(Q(2))==Q(4,3)
assert debt(Q(10,3))==dmax
assert debt(Q(4))==Q(13,3)
# Exact threshold solving second segment: first segment fails, second crosses.
tc=Q(2)+(dmax-debt(Q(2)))/Q(3,2)
assert tc==Q(10,3)
assert debt(tc-Q(1,100))<dmax<debt(tc+Q(1,100))
assert Q(2)<=tc<=Q(6) # bounds for k in [1/2,3/2]
constant_tc=(dmax-d0)/Q(3,4)
assert constant_tc==Q(4)
# Symmetric 2x2 commuting diagonal matrix, positive-semidefinite growth.
D0=(Q(1,3),Q(2,3)); K=(Q(1,2),Q(1,4)); cap=Q(5,3)
tensor_tc=min((cap-D0[i])/K[i] for i in range(2))
assert tensor_tc==Q(8,3)
assert max(D0[i]+K[i]*(tensor_tc-Q(1,100)) for i in range(2))<cap
assert max(D0[i]+K[i]*(tensor_tc+Q(1,100)) for i in range(2))>cap
witnesses=[
 {"claim_id":"EX-01","claim":"piecewise debt and exact first hitting time", "value":{"d_0":f(debt(Q(0))),"d_2":f(debt(Q(2))),"t_first_hit":f(tc),"d_at_hit":f(debt(tc)),"d_4":f(debt(Q(4)))},"verified":True},
 {"claim_id":"EX-02","claim":"comparison time bounds", "value":{"lower":'2',"observed":f(tc),"upper":'6'},"verified":True},
 {"claim_id":"EX-03","claim":"constant-stress time formula", "value":{"kappa":'3/4',"t_first_hit":f(constant_tc)},"verified":True},
 {"claim_id":"EX-04","claim":"tensor eigenvalue first crossing: exact diagonal example", "value":{"t_first_hit":f(tensor_tc),"threshold":f(cap)},"verified":True},
 {"claim_id":"EX-05","claim":"strict pre/post crossing and no-return on the computed horizon", "value":{"before_hit":f(debt(tc-Q(1,100))),"after_hit":f(debt(tc+Q(1,100))),"end_debt":f(debt(Q(4)))},"verified":True},
]
run_info={'spec_sha256':contract_id,'source_sha256':source_sha,'run_time_utc':datetime.now(timezone.utc).isoformat(),'engine':'CPython fractions.Fraction exact arithmetic','claim_count':len(witnesses)}
run_id=sha(canon({'spec_sha256':contract_id,'witnesses':witnesses}))
run_info['run_id']=run_id
receipts=[];prev='0'*64
for i, w in enumerate(witnesses,1):
 payload={'receipt_no':i,'run_id':run_id,'claim_id':w['claim_id'],'witness_sha256':sha(canon(w)),'prev_receipt_sha256':prev}
 payload['receipt_sha256']=sha(canon(payload));prev=payload['receipt_sha256'];receipts.append(payload)
certs=[{'certificate_id':'ADG-'+w['claim_id'],'scope':'exact rational example only','claim':w['claim'],'witness_sha256':sha(canon(w)),'run_id':run_id,'parent_contract_sha256':contract_id} for w in witnesses]
result={'run':run_info,'witnesses':witnesses,'certificates':certs,'receipts':receipts,'final_receipt_sha256':prev}
(OUT/'EXACT_EXAMPLE_CERTIFICATES_AND_RECEIPTS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
# Independent checker of internal chain; source remains part of the contract.
assert sha(SOURCE.read_bytes())==source_sha
assert all(c['witness_sha256']==sha(canon(w)) for c,w in zip(certs,witnesses))
last='0'*64
for rec in receipts:
 assert rec['prev_receipt_sha256']==last
 last=rec['receipt_sha256']
 assert sha(canon({k:v for k,v in rec.items() if k!='receipt_sha256'}))==last
assert last==result['final_receipt_sha256']
print('PASS',len(witnesses),'exact example witnesses;',len(certs),'scope-limited certificates;',len(receipts),'chained receipts')
print('run_id',run_id)
print('source_sha256',source_sha)
