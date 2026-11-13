"""Tests ONLY newly constructed instances. Historical 329/441 stays closed."""
import copy, json, pathlib, random, time
from itertools import product
from width_kernel_v3 import solve,digest
from independent_verify_v3 import audit_receipt

ROOT=pathlib.Path(__file__).resolve().parent
rng=random.Random(20261112)
receipts=[]
summary={'new_small_truth_table_cases':0,'new_bounded_width_large_cases':0,
         'new_dense_cases':0,'SAT':0,'UNSAT':0,'negative_controls_rejected':0,
         'historical_native_examinations_reexecuted':0,'prior_v2_cases_reexecuted':0,
         'max_induced_width':0,'max_variables':0,'max_certified_resolution_pairs':0,
         'independent_trace_replays':0}

def certify_case(f,brute=False,order=None):
    q=solve(f,order=order)
    assert audit_receipt(q),f'cross-verifier rejection n={f["n"]}, m={len(f["clauses"])}'
    assert solve(f,order=order)==q,'non-deterministic receipt'
    if brute:
        actual=any(all(any(bits[abs(l)-1]==(l>0) for l in c) for c in f['clauses'])
                   for bits in product((False,True),repeat=f['n']))
        assert (q['decision']=='SAT')==actual,'wrong brute-force decision'
    summary['independent_trace_replays']+=1
    summary[q['decision']]+=1
    summary['max_induced_width']=max(summary['max_induced_width'],q['induced_width'])
    summary['max_variables']=max(summary['max_variables'],f['n'])
    summary['max_certified_resolution_pairs']=max(summary['max_certified_resolution_pairs'],q['resolution_pairs_checked'])
    receipts.append(q)
    return q

# Distinct from archived 329/441 tests: new seed and fresh corpus.
for n in range(0,9):
    for j in range(38):
        m=rng.randint(0, min(23, 3*n+7))
        clauses=[]
        for _ in range(m):
            arity=rng.randrange(0,4) if rng.random()<0.15 else rng.randrange(1,4)
            arity=0 if n==0 else arity
            c=[rng.choice((-1,1))*rng.randint(1,n) for _ in range(arity)]
            clauses.append(c)
        f={'n':n,'clauses':clauses}
        ord_=list(range(1,n+1));rng.shuffle(ord_)
        certify_case(f,brute=True,order=ord_)
        summary['new_small_truth_table_cases']+=1

# Real scalability: same low-width structural family but n as large as 512.
for n in [16,32,64,128,256,512]:
    sat={'n':n,'clauses':[[i,i+1] for i in range(1,n)]}
    q=certify_case(sat);assert q['decision']=='SAT' and q['induced_width']==1
    summary['new_bounded_width_large_cases']+=1
    unsat={'n':n,'clauses':[[1],[-n]]+[[-i,i+1] for i in range(1,n)]}
    q=certify_case(unsat);assert q['decision']=='UNSAT' and q['induced_width']==1
    summary['new_bounded_width_large_cases']+=1
    triple={'n':n,'clauses':[[i,i+1,i+2] for i in range(1,n-1)]}
    q=certify_case(triple);assert q['decision']=='SAT' and q['induced_width']==2
    summary['new_bounded_width_large_cases']+=1

for n in [5,6,7,8]:
    clauses=[]
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            for k in range(j+1,n+1):
                clauses.append([i,j,k])
    q=certify_case({'n':n,'clauses':clauses},brute=True)
    assert q['induced_width']==n-1
    summary['new_dense_cases']+=1

# Manipulations: checksum is recomputed. Independent replay must still refuse.
sat=next(q for q in receipts if q['decision']=='SAT' and q['formula']['n']>=2)
unsat=next(q for q in receipts if q['decision']=='UNSAT' and q['formula']['n']>=16 and q['proof'] and q['proof']['steps'])

mutations=[
 ('fake width',sat,lambda r:r.__setitem__('induced_width',0)),
 ('fake pair count',unsat,lambda r:r.__setitem__('resolution_pairs_checked',0)),
 ('fake trace pair count',unsat,lambda r:r['trace'][0].__setitem__('pairs_checked',999999)),
 ('fake trace derived count',unsat,lambda r:r['trace'][0].__setitem__('new_resolution_steps',999999)),
 ('fake fill neighbor',sat,lambda r:r['fill_witness'][0].__setitem__('neighbors',[12345])),
 ('fake SAT assignment',sat,lambda r:r.__setitem__('assignment',[3]*r['formula']['n'])),
 ('fake UNSAT step',unsat,lambda r:r['proof']['steps'][0].__setitem__('pivot',999999)),
 ('false input clause',sat,lambda r:r['formula']['clauses'].append([])),
 ('false native status',sat,lambda r:r.__setitem__('native_NEW_K_executed',True)),
 ('wrong execution order',unsat,lambda r:r['order'].reverse()),
]
for name,r,modify in mutations:
    q=copy.deepcopy(r);modify(q)
    q['receipt_sha256']=digest({k:v for k,v in q.items() if k!='receipt_sha256'})
    assert not audit_receipt(q),f'countermeasure failed {name}'
    summary['negative_controls_rejected']+=1

path=ROOT/'evidence'
path.mkdir(exist_ok=True)
(path/'new_receipts.json').write_text(json.dumps(receipts,indent=2,ensure_ascii=False),encoding='utf8')
(path/'new_test_report.json').write_text(json.dumps(summary,indent=2,sort_keys=True),encoding='utf8')
print('PASS',json.dumps(summary,sort_keys=True))
