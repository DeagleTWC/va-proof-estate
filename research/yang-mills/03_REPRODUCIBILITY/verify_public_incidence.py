#!/usr/bin/env python3
"""Independent public replay of Stage 79 combinatorics using published Stage 72 ledger.

No native/protected URK kernel is invoked. This recomputes the finite incidence
results, not Yang-Mills continuum existence or mass gap. Python standard library only.
"""
import collections,hashlib,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent

def key(x):return (int(x[0]),)+tuple(int(v) for v in x[1])
def components(adj):
 seen=set();out=[]
 for s in adj:
  if s in seen:continue
  q=[s];seen.add(s);comp=[]
  while q:
   v=q.pop();comp.append(v)
   for w in adj[v]:
    if w not in seen:seen.add(w);q.append(w)
  out.append(comp)
 return out

def distances(adj,source):
 d={source:0};q=collections.deque([source])
 while q:
  v=q.popleft()
  for w in adj[v]:
   if w not in d:d[w]=d[v]+1;q.append(w)
 return d

def tarjan(adj):
 timer=0;tin={};low={};parent={};arts=set();bridges=[]
 def dfs(v):
  nonlocal timer
  timer+=1;tin[v]=low[v]=timer;children=0
  for w in adj[v]:
   if w==parent.get(v):continue
   if w in tin:low[v]=min(low[v],tin[w])
   else:
    parent[w]=v;children+=1;dfs(w);low[v]=min(low[v],low[w])
    if v in parent and low[w]>=tin[v]:arts.add(v)
    if low[w]>tin[v]:bridges.append(tuple(sorted((v,w),key=repr)))
  if v not in parent and children>1:arts.add(v)
 for v in adj:
  if v not in tin:dfs(v)
 return arts,bridges

data=json.loads((ROOT/'STAGE72_MEDIATOR_LEDGER.json').read_text())
summary=json.loads((ROOT/'STAGE72_RESULTS.json').read_text())
expected=json.loads((ROOT/'STAGE79_ARCHIVED_RESULTS.json').read_text())
chords={key(c) for c in data['chords']}
internal=[m for m in data['residual_mediators'] if m['is_internal']]
adj=collections.defaultdict(set);md={}
for m in internal:
 mk=('M',)+key(m['link']);cs=[key(c) for c in m['chords']];md[mk]=len(cs);adj[mk]
 for c in cs:
  ck=('C',)+c;adj[mk].add(ck);adj[ck].add(mk)
comps=components(adj);diameter=max(max(distances(adj,v).values()) for v in adj)
arts,bridges=tarjan(adj);art=next(iter(arts)) if len(arts)==1 else None
adj2={v:set(ws) for v,ws in adj.items() if v!=art}
for v in adj2:adj2[v].discard(art)
removed=sorted((len(c) for c in components(adj2)),reverse=True)
proj={('C',)+c:set() for c in chords}
for m in internal:
 cs=[('C',)+key(c) for c in m['chords']]
 for i,u in enumerate(cs):proj[u].update(cs[:i]+cs[i+1:])
edges=sum(map(len,proj.values()))//2
pcomps=components(proj);pdiam=max(max(distances(proj,v).values()) for v in proj)
checks={
 'stage72_source':summary['stage']==72,
 'chords_125':len(chords)==125,
 'internal_mediators_96':len(internal)==96,
 'internal_incidences_491':sum(md.values())==491,
 'bipartite_connected':len(comps)==1,
 'bipartite_diameter_11':diameter==11,
 'one_articulation_vertex':len(arts)==1,
 'one_bridge':len(bridges)==1,
 'articulation_removal_sizes_219_1':removed==[219,1],
 'chord_projection_connected':len(pcomps)==1,
 'chord_projection_edges_951':edges==951,
 'chord_projection_diameter_5':pdiam==5,
 'source_ledger_exact_bytes':hashlib.sha256((ROOT/'STAGE72_MEDIATOR_LEDGER.json').read_bytes()).hexdigest()=='a6209231f4e5f7a14ea713c33910301c4fbfa194e89bb34355392d127cc24bc3',
 'archived_result_exact_bytes':hashlib.sha256((ROOT/'STAGE79_ARCHIVED_RESULTS.json').read_bytes()).hexdigest()=='d2c99c3ac2026a1ffe2408c8c19d11c30dd60b45a9a3e6b19c4a51ffcde264e9',
}
assert all(checks.values()),checks
assert expected['checks']['source_zip_integrity'] and expected['checks']['parent_zip_integrity']
assert expected['articulation']['chord']==list(art[1:])
assert expected['chord_projection']['edges']==edges
out={'public_replay':True,'scope':'Exact finite chord-mediator incidence topology only; no continuum or Yang-Mills mass-gap proof.', 'checks':checks,'passed':sum(checks.values()),'total':len(checks),'bipartite_vertices':len(adj),'bipartite_incidences':sum(md.values()),'diameter':diameter,'articulation_chord':list(art[1:]),'bridge_count':len(bridges),'chord_projection_edges':edges,'chord_projection_diameter':pdiam}
(ROOT/'PUBLIC_REPLAY_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(f"{out['passed']}/{out['total']} bounded public verification checks passed")
