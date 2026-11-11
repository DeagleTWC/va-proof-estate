#!/usr/bin/env python3
"""Read-only verifier for ADG rational-example certificates/receipts and source custody."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def verify(obj):
    source=(ROOT/'source/MATH_SOLUTIONS_original_unchanged.txt').read_bytes()
    contract=json.loads((ROOT/'output/PREPARED_CONTRACT.json').read_text())
    chash=contract.pop('contract_sha256')
    assert chash==sha(canon(contract))
    assert contract['source_sha256']==sha(source)
    run=obj['run']; ws=obj['witnesses']; certs=obj['certificates']; receipts=obj['receipts']
    assert run['spec_sha256']==chash
    assert run['source_sha256']==contract['source_sha256']
    assert run['run_id']==sha(canon({'spec_sha256':chash,'witnesses':ws}))
    assert len(ws)==len(certs)==len(receipts)==5
    for w,c in zip(ws,certs):
        assert w['verified'] is True and c['scope']=='exact rational example only'
        assert c['run_id']==run['run_id'] and c['parent_contract_sha256']==chash
        assert c['witness_sha256']==sha(canon(w))
    last='0'*64
    for i,(w,r) in enumerate(zip(ws,receipts),1):
        assert r['receipt_no']==i and r['claim_id']==w['claim_id']
        assert r['run_id']==run['run_id'] and r['prev_receipt_sha256']==last
        assert r['witness_sha256']==sha(canon(w))
        assert r['receipt_sha256']==sha(canon({k:v for k,v in r.items() if k!='receipt_sha256'}))
        last=r['receipt_sha256']
    assert last==obj['final_receipt_sha256']
    # Independently recompute all published rational witnesses, not only their hashes.
    d0=Q(1,3); B=Q(10,3)
    def debt(t):return d0+Q(1,2)*min(t,Q(2))+Q(3,2)*max(t-Q(2),Q(0))
    hit=Q(2)+(B-debt(Q(2)))/Q(3,2)
    assert hit==Q(ws[0]['value']['t_first_hit'])
    assert [debt(Q(0)),debt(Q(2)),debt(hit),debt(Q(4))]==[Q(ws[0]['value'][k]) for k in ['d_0','d_2','d_at_hit','d_4']]
    assert Q(ws[1]['value']['lower'])<=hit<=Q(ws[1]['value']['upper'])
    assert Q(ws[2]['value']['t_first_hit'])==(B-d0)/Q(ws[2]['value']['kappa'])
    t_tensor=min((Q(5,3)-v)/k for v,k in ((Q(1,3),Q(1,2)),(Q(2,3),Q(1,4))))
    assert t_tensor==Q(ws[3]['value']['t_first_hit'])
    assert [debt(hit-Q(1,100)),debt(hit+Q(1,100)),debt(Q(4))]==[Q(ws[4]['value'][k]) for k in ['before_hit','after_hit','end_debt']]
    return True
obj=json.loads((ROOT/'output/EXACT_EXAMPLE_CERTIFICATES_AND_RECEIPTS.json').read_text())
assert verify(obj)
# Negative control: mutate a witnessed value without recalculating certificates.
tampered=json.loads(json.dumps(obj));tampered['witnesses'][0]['value']['d_2']='5/3'
try:
    verify(tampered)
except AssertionError:
    pass
else:
    raise AssertionError('Tampered example was not rejected')
print('PASS: source, contract, five exact rational examples, five certificates, five linked receipts, tamper rejection')
