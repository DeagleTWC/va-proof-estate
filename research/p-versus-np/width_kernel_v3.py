"""V.A. / P-vs-NP public mathematical extension, November 12, 2026.

Exact Davis–Putnam variable elimination with SAT reconstruction and UNSAT
resolution certificates. Induced-width cost theorem is about THIS ALGORITHM,
not a claim about the original proprietary NEW K, P=NP, or P!=NP.

Source v2 is preserved verbatim under reference/ and never changed.
"""
from __future__ import annotations
import hashlib
import json
from itertools import combinations

KERNEL = 'VA-PVNP-INDUCED-WIDTH-CERTIFICATE-v3'

def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def digest(x):
    return hashlib.sha256(canonical(x).encode('utf8')).hexdigest()

def normalize(formula):
    if type(formula) is not dict or set(formula) != {'n', 'clauses'}:
        raise ValueError('expected n, clauses')
    n = formula['n']
    if type(n) is not int or n < 0 or type(formula['clauses']) is not list:
        raise ValueError('malformed formula')
    clauses=[]
    for c in formula['clauses']:
        if type(c) is not list or len(c)>3 or any(type(x) is not int or x==0 or abs(x)>n for x in c):
            raise ValueError('expected 0..3 signed literals from [1,n]')
        clauses.append(list(c))
    return {'n':n, 'clauses':clauses}

def taut(c):
    s=set(c)
    return any(-x in s for x in s)

def canonical_clauses(formula):
    return sorted({tuple(sorted(set(c))) for c in formula['clauses'] if not taut(c)})

def valid_order(n, order):
    if type(order) is not list or len(order)!=n or any(type(x) is not int for x in order) or set(order)!=set(range(1,n+1)):
        raise ValueError('order must be a permutation of 1..n')
    return order[:]

def induced_width(formula, order):
    """Exact fill-graph construction, where width is max later-neighbor count."""
    n=formula['n']
    neighbors={v:set() for v in range(1,n+1)}
    for c in canonical_clauses(formula):
        vars_={abs(x) for x in c}
        for a,b in combinations(sorted(vars_), 2):
            neighbors[a].add(b);neighbors[b].add(a)
    widths=[]
    for v in order:
        rest=sorted(neighbors[v])
        widths.append({'v':v,'neighbors':rest,'width':len(rest)})
        for a,b in combinations(rest,2):
            neighbors[a].add(b);neighbors[b].add(a)
        for x in rest:
            neighbors[x].remove(v)
        neighbors[v].clear()
    return max((x['width'] for x in widths),default=0), widths

def satisfies(formula, bits):
    if type(bits) is not list or len(bits)!=formula['n'] or any(type(x) is not int or x not in (0,1) for x in bits):
        return False
    return all(any(bits[abs(l)-1]==int(l>0) for l in c) for c in formula['clauses'])

def solve(formula, order=None):
    f=normalize(formula)
    n=f['n']
    order=valid_order(n, list(range(1,n+1)) if order is None else order)
    w, fill=induced_width(f,order)
    axioms=canonical_clauses(f)
    db=list(axioms)
    known={c:i for i,c in enumerate(db)}
    active=set(known.values())
    steps=[];trace=[];snapshots=[]
    pair_checks=0
    empty_ix=known.get(())
    if empty_ix is None:
        for v in order:
            pos=sorted((i for i in active if v in db[i]),key=lambda i: db[i])
            neg=sorted((i for i in active if -v in db[i]),key=lambda i: db[i])
            kept={i for i in active if v not in db[i] and -v not in db[i]}
            positive_residuals=[list(x for x in db[i] if x!=v) for i in pos]
            negative_residuals=[list(x for x in db[i] if x!=-v) for i in neg]
            snapshots.append({'v':v,'positive_residuals':positive_residuals,'negative_residuals':negative_residuals})
            this_pairs=0;new_steps=0
            stop=False
            for i in pos:
                for j in neg:
                    this_pairs+=1;pair_checks+=1
                    out=tuple(sorted((set(db[i])-{v}) | (set(db[j])-{-v})))
                    if taut(out): continue
                    if out not in known:
                        known[out]=len(db)
                        db.append(out)
                        steps.append({'left':i,'right':j,'pivot':v,'clause':list(out)})
                        new_steps+=1
                    kept.add(known[out])
                    if out==():
                        empty_ix=known[out];stop=True;break
                if stop:break
            trace.append({'v':v,'positive':len(pos),'negative':len(neg),
                          'pairs_checked':this_pairs,'new_resolution_steps':new_steps,
                          'active_before':len(active), 'active_after':len(kept),
                          'terminated_on_empty':stop})
            if stop:break
            active=kept
    if empty_ix is not None:
        decision='UNSAT'; assignment=None
        proof={'axioms':[list(c) for c in axioms], 'steps':steps, 'empty_clause_index':empty_ix}
    else:
        # Correct backward model reconstruction from original elimination buckets.
        a={}
        for snap in reversed(snapshots):
            v=snap['v']
            def lit_value(l):
                bit=a[abs(l)]
                return bit==int(l>0)
            positive_fails=any(not any(lit_value(l) for l in c) for c in snap['positive_residuals'])
            a[v]=int(positive_fails)
            # Local invariant: all eliminated clauses are satisfied once v is chosen.
            for c in snap['positive_residuals']:
                if not (a[v]==1 or any(lit_value(l) for l in c)):
                    raise AssertionError('invalid positive back-substitution')
            for c in snap['negative_residuals']:
                if not (a[v]==0 or any(lit_value(l) for l in c)):
                    raise AssertionError('invalid negative back-substitution')
        assignment=[a[i] for i in range(1,n+1)]
        if not satisfies(f,assignment):
            raise AssertionError('original formula failed model reconstruction')
        decision='SAT';proof=None
    # Hard checks: actual work cannot exceed the combinatorial predicted ceiling.
    assert all(row['pairs_checked']<=9**fill[i]['width'] for i,row in enumerate(trace))
    assert all(row['positive']<=3**fill[i]['width'] and row['negative']<=3**fill[i]['width'] for i,row in enumerate(trace))
    payload={'kernel':KERNEL,'formula':f,'formula_sha256':digest(f),'order':order,
             'induced_width':w,'fill_witness':fill,'decision':decision,
             'assignment':assignment,'proof':proof,'trace':trace,
             'resolution_pairs_checked':pair_checks,'resolution_steps':len(steps),
             'native_NEW_K_executed':False}
    return {**payload,'receipt_sha256':digest(payload)}
