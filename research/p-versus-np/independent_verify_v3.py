"""Independent child: parse formula, verify proof and replay exact work counts.

Different implementations of clause evolution and parent-proof checking from
width_kernel_v3; does NOT trust self-reported resolution counts or checksum alone.
"""
from __future__ import annotations
from itertools import combinations
import hashlib, json

def key(x):
    return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)

def hash_obj(x):
    return hashlib.sha256(key(x).encode('utf8')).hexdigest()

def input_check(f,order):
    if type(f)!=dict or set(f)!={'n','clauses'} or type(f['n'])!=int or f['n']<0 or type(f['clauses'])!=list:return False
    n=f['n']
    if type(order)!=list or len(order)!=n or any(type(v)!=int for v in order) or set(order)!=set(range(1,n+1)):return False
    for c in f['clauses']:
        if type(c)!=list or len(c)>3 or any(type(x)!=int or abs(x)>n or x==0 for x in c):return False
    return True

def independent_axioms(f):
    result=set()
    for c in f['clauses']:
        q=set(c)
        if any(-x in q for x in q):continue
        result.add(tuple(sorted(q)))
    return sorted(result)

def proof_check(f, proof):
    if type(proof)!=dict or set(proof)!={'axioms','steps','empty_clause_index'}:return False
    expected=[list(c) for c in independent_axioms(f)]
    if proof['axioms']!=expected or type(proof['steps'])!=list:return False
    derived=[tuple(c) for c in expected]
    for step in proof['steps']:
        if type(step)!=dict or set(step)!={'left','right','pivot','clause'}:return False
        i=step['left'];j=step['right'];v=step['pivot'];c=step['clause']
        if any(type(z)!=int for z in (i,j,v)) or i<0 or j<0 or i>=len(derived) or j>=len(derived) or v<=0 or v>f['n'] or type(c)!=list:return False
        l=set(derived[i]);r=set(derived[j])
        if v not in l or -v not in r:return False
        q=(l-{v})|(r-{-v})
        if any(-x in q for x in q) or tuple(c)!=tuple(sorted(q)):return False
        derived.append(tuple(sorted(q)))
    ix=proof['empty_clause_index']
    return type(ix)==int and 0<=ix<len(derived) and derived[ix]==()

def audit_fill(f,order):
    # Separate representation: edge-set and fill by restriction to uneliminated nodes.
    E=set()
    for c in independent_axioms(f):
        vs=sorted(set(abs(v) for v in c))
        E.update(tuple(sorted(x)) for x in combinations(vs,2))
    remain=set(range(1,f['n']+1));out=[]
    for x in order:
        N=sorted(y for y in remain if y!=x and tuple(sorted((x,y))) in E)
        out.append({'v':x,'neighbors':N,'width':len(N)})
        E.update(tuple(sorted(e)) for e in combinations(N,2))
        remain.remove(x)
    return max((t['width'] for t in out),default=0),out

def audit_eliminate(f,order):
    """Independent clause-set evolution (no proof DB or shared generator methods)."""
    current=set(independent_axioms(f))
    if () in current:return 'UNSAT',[],0,0
    counts=[];total=0;step_count=0
    for v in order:
        pp=sorted(c for c in current if v in c)
        nn=sorted(c for c in current if -v in c)
        after=set(c for c in current if abs(v) not in {abs(y) for y in c})
        seen_all=set(current)
        pairs=0;new_steps=0;terminal=False
        for l in pp:
            for r in nn:
                pairs+=1;total+=1
                q=set(l);q.discard(v)
                t=set(r);t.discard(-v)
                q.update(t)
                if any(-z in q for z in q):continue
                cl=tuple(sorted(q))
                # Generator keeps global knowledge of prior derived clauses;
                # all clauses possible at this point have unique non-eliminated variables.
                if cl not in seen_all:
                    new_steps+=1
                    seen_all.add(cl)
                after.add(cl)
                if not cl:
                    terminal=True;break
            if terminal:break
        # Count step-canonical unique resolvents within this step.
        counts.append({'v':v,'positive':len(pp),'negative':len(nn),
                       'pairs_checked':pairs,'new_resolution_steps':new_steps,
                       'active_before':len(current),'active_after':len(after),
                       'terminated_on_empty':terminal})
        step_count+=new_steps
        if terminal:return 'UNSAT',counts,total,step_count
        current=after
    return 'SAT',counts,total,step_count

def audit_receipt(r):
    if type(r)!=dict or set(r)!={'kernel','formula','formula_sha256','order','induced_width','fill_witness','decision','assignment','proof','trace','resolution_pairs_checked','resolution_steps','native_NEW_K_executed','receipt_sha256'}:return False
    payload={k:v for k,v in r.items() if k!='receipt_sha256'}
    if r['receipt_sha256']!=hash_obj(payload) or r['formula_sha256']!=hash_obj(r['formula']):return False
    if r['kernel']!='VA-PVNP-INDUCED-WIDTH-CERTIFICATE-v3' or r['native_NEW_K_executed'] is not False:return False
    f=r['formula'];order=r['order']
    if not input_check(f,order):return False
    w,fw=audit_fill(f,order)
    if r['induced_width']!=w or r['fill_witness']!=fw:return False
    d,trace,pairs,steps=audit_eliminate(f,order)
    if r['decision']!=d or r['trace']!=trace or r['resolution_pairs_checked']!=pairs or r['resolution_steps']!=steps:return False
    for row,fill in zip(trace,fw):
        if row['pairs_checked']>9**fill['width'] or row['positive']>3**fill['width'] or row['negative']>3**fill['width']:return False
    if d=='UNSAT':
        return r['assignment'] is None and proof_check(f,r['proof']) and len(r['proof']['steps'])==steps
    if r['proof'] is not None:return False
    bits=r['assignment'];n=f['n']
    if type(bits)!=list or len(bits)!=n or any(type(z)!=int or z not in (0,1) for z in bits):return False
    for c in f['clauses']:
        if not any((bits[abs(x)-1]==1)==(x>0) for x in c):return False
    return True

if __name__=='__main__':
    import sys,pathlib
    data=json.loads(pathlib.Path(sys.argv[1]).read_text())
    print('PASS' if all(audit_receipt(r) for r in data) else 'FAIL',len(data))
