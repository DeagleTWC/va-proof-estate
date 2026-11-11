#!/usr/bin/env python3
"""Read-only independent verifier for the public exact-grid illustrative record.
Does not import the producer. Checks source hashes, prepared contract, each
model constraint, the result/certificate hash chain, and a tamper negative control.
"""
import pathlib,hashlib,json,copy,sys
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[1]

def wire(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def H(x):return hashlib.sha256(wire(x)).hexdigest()
def F(x):return Fraction(str(x))
def exact(x):return f'{x.numerator}/{x.denominator}'
def fail(msg):raise AssertionError(msg)

def independently_calculate(c,s):
 caps={k:F(v) for k,v in c['edge_capacities_normal'].items()};caps['S>A']=F(s['effective_A_capacity'])
 if not s['backup_activated']:
  for key,val in c['edge_capacities_standby_off'].items():caps[key]=F(val)
 flows={k:F(v) for k,v in s['flow'].items()};demands={k:F(v) for k,v in s['demand'].items()}
 incoming={v:F(0) for v in c['nodes']};outgoing={v:F(0) for v in c['nodes']};violations=[]
 for edge,amount in flows.items():
  if edge not in caps:violations.append('unknown_edge:'+edge);continue
  if amount<0:violations.append('negative_flow:'+edge)
  if amount>caps[edge]:violations.append('capacity:'+edge)
  origin,destination=edge.split('>');outgoing[origin]+=amount;incoming[destination]+=amount
 for vertex in c['nodes']:
  if vertex!=c['source'] and incoming[vertex]-outgoing[vertex]!=demands.get(vertex,F(0)):violations.append('balance:'+vertex)
 sent=outgoing[c['source']]-incoming[c['source']]
 required=sum(demands.values(),F(0))
 if sent!=required:violations.append('source_total')
 action=s['action']
 if action=='DEGRADE':
  for key,minimum in c['critical_minimum_degraded'].items():
   if demands[key]<F(minimum):violations.append('critical_minimum:'+key)
 elif action in ('REROUTE','CONTINUE'):
  if demands!={k:F(v) for k,v in c['baseline_demand'].items()}:violations.append('baseline_demand')
 if action not in s['permissions']:violations.append('permission')
 if not s['authority_valid']:violations.append('authority')
 if not s['fresh_evidence']:violations.append('evidence_freshness')
 debt=F(c['cumulative_debt']['initial'])+F(s['debt_increment_SA']);budget=F(c['cumulative_debt']['strict_budget'])
 if not debt<budget:violations.append('strict_debt_reserve')
 cut=caps['S>A']+caps['S>B']+caps['S>C']
 deficit=max(F(0),required-cut)
 if deficit>0:violations.append('source_cut_shortfall')
 return {'scenario_id':s['id'],'action':action,'admitted':not violations,'outcome':action if not violations else 'REFUSE',
 'failed_constraints':sorted(set(violations)), 'source_cut_capacity':exact(cut),'required_service':exact(required),'source_cut_deficit':exact(deficit),
 'source_outflow':exact(sent),'next_debt_SA':exact(debt),'strict_budget_SA':exact(budget),
 'flow':{e:exact(v) for e,v in flows.items()},'demand':{k:exact(v) for k,v in demands.items()},
 'scope':'exact synthetic scenario arithmetic; not a universal physical safety proof'}

def verify(c,output,source_dir=None):
 original=copy.deepcopy(c)
 source_sha=original['source_custody']; key=original.pop('contract_sha256')
 assert H(original)==key,'prepared contract hash invalid'
 if source_dir is not None:
  for filename,ref in [('Critical_Infrastructure_Continuity_Kernel_v1.json','continuity_kernel_json_sha256'),('1886f847-cbfc-4955-8884-8ca6235568b2.docx','world_kernel_atlas_docx_sha256')]:
   assert hashlib.sha256((source_dir/filename).read_bytes()).hexdigest()==source_sha[ref],'custody source changed: '+filename
 assert output['run_id']==c['run_id'] and output['contract_sha256']==key
 assert len(c['scenarios'])==len(output['certificates'])==len(output['receipts'])==7
 prior='0'*64
 for i,(s,cert,receipt) in enumerate(zip(c['scenarios'],output['certificates'],output['receipts']),1):
  assert cert['ordinal']==receipt['ordinal']==i
  assert cert['scenario_input_sha256']==H(s),'scenario hash failure'
  assert cert['witness']==independently_calculate(c,s),'exact rational or model evaluation mismatch'
  cert_bare={k:v for k,v in cert.items() if k!='certificate_sha256'}
  assert H(cert_bare)==cert['certificate_sha256'],'certificate digest mismatch'
  assert receipt['prev_receipt_sha256']==prior and receipt['certificate_sha256']==cert['certificate_sha256']
  assert receipt['run_id']==c['run_id'] and receipt['decision']==cert['witness']['outcome']
  assert receipt['failed_constraints']==cert['witness']['failed_constraints']
  assert receipt['decision_id']==c['run_id']+':'+s['id']
  assert receipt['corridor_id']=='SYNTHETIC-POWER-WATER-TELECOM-001'
  assert receipt['participating_domains']==['power','water','telecommunications']
  assert receipt['proposed_transition']==s['action']
  assert receipt['state_snapshot_ref']==H(s)
  assert receipt['decision_outcome']==cert['witness']['outcome']
  assert receipt['failed_constraint_if_any']==cert['witness']['failed_constraints']
  assert receipt['reroute_or_degrade_mode_if_any']==(s['action'] if s['action'] in ('REROUTE','DEGRADE') else None)
  assert receipt['authority_basis']=={'authority_valid_input':s['authority_valid'],'action_permitted_input':s['action'] in s['permissions'],'fresh_evidence_input':s['fresh_evidence']}
  assert receipt['timestamp_utc'].endswith('+00:00') and receipt['timestamp_source']=='execution_host_clock_not_attested'
  bare={k:v for k,v in receipt.items() if k!='receipt_sha256'}
  assert H(bare)==receipt['receipt_sha256'],'receipt digest mismatch'
  prior=receipt['receipt_sha256']
 assert output['final_receipt_sha256']==prior
 return True

def main():
 c=json.loads((ROOT/'output/PREPARED_CONTRACT.json').read_text())
 p=json.loads((ROOT/'output/EXACT_WITNESSES_CERTIFICATES_RECEIPTS.json').read_text())
 sources=ROOT/'sources';sources=sources if sources.exists() else None
 verify(c,p,sources)
 tampered=copy.deepcopy(p);tampered['certificates'][2]['witness']['outcome']='CONTINUE'
 try:verify(c,tampered,sources)
 except AssertionError:pass
 else:fail('tamper negative control not rejected')
 print('PASS: prepared contract, seven separately recomputed exact witnesses, seven scoped certificates, seven linked receipts, and tamper rejection; original-source byte check: '+('VERIFIED' if sources else 'NOT AVAILABLE (hashes retained)'))
if __name__=='__main__':main()
