#!/usr/bin/env python3
"""Single authoritative exact arithmetic run. No network/actuation capabilities."""
import hashlib,json,pathlib,datetime
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[1]
def canonical(o):return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def h(o):return hashlib.sha256(canonical(o)).hexdigest()
def f(x):return Fraction(str(x))
def evaluate(contract,scenario):
 cap=dict(contract['edge_capacities_normal']); cap['S>A']=scenario['effective_A_capacity']
 if not scenario['backup_activated']:cap.update(contract['edge_capacities_standby_off'])
 flow={e:f(v) for e,v in scenario['flow'].items()}; req={v:f(x) for v,x in scenario['demand'].items()}
 inflow={n:Fraction(0) for n in contract['nodes']};outflow=dict(inflow)
 for e,v in flow.items():
  left,right=e.split('>');outflow[left]+=v;inflow[right]+=v
 failures=[]
 for e,v in flow.items():
  if v<0: failures.append('negative_flow:'+e)
  if e not in cap:failures.append('unknown_edge:'+e)
  elif v>f(cap[e]):failures.append('capacity:'+e)
 for n in contract['nodes']:
  if n==contract['source']:continue
  net=inflow[n]-outflow[n]
  target=req.get(n,Fraction(0))
  if net!=target: failures.append('balance:'+n)
 source_out=outflow[contract['source']]-inflow[contract['source']]
 if source_out!=sum(req.values()):failures.append('source_total')
 if scenario['action']=='DEGRADE':
  for n,v in contract['critical_minimum_degraded'].items():
   if req[n]<f(v):failures.append('critical_minimum:'+n)
 elif scenario['action'] in ('CONTINUE','REROUTE'):
  if req!={k:f(v) for k,v in contract['baseline_demand'].items()}:failures.append('baseline_demand')
 if scenario['action'] not in scenario['permissions']:failures.append('permission')
 if not scenario['authority_valid']:failures.append('authority')
 if not scenario['fresh_evidence']:failures.append('evidence_freshness')
 next_debt=f(contract['cumulative_debt']['initial'])+f(scenario['debt_increment_SA'])
 budget=f(contract['cumulative_debt']['strict_budget'])
 if not next_debt<budget:failures.append('strict_debt_reserve')
 cut_capacity=sum(f(cap[e]) for e in ('S>A','S>B','S>C'))
 cut_demand=sum(req.values())
 cut_deficit=max(Fraction(0),cut_demand-cut_capacity)
 if cut_deficit>0:failures.append('source_cut_shortfall')
 def s(x):return str(x.numerator)+'/'+str(x.denominator)
 return {'scenario_id':scenario['id'],'action':scenario['action'],'admitted':not failures,
 'outcome':scenario['action'] if not failures else 'REFUSE',
 'failed_constraints':sorted(set(failures)),
 'source_cut_capacity':s(cut_capacity),'required_service':s(cut_demand),'source_cut_deficit':s(cut_deficit),
 'source_outflow':s(source_out),'next_debt_SA':s(next_debt),'strict_budget_SA':s(budget),
 'flow':{e:s(v) for e,v in flow.items()},'demand':{n:s(v) for n,v in req.items()},
 'scope':'exact synthetic scenario arithmetic; not a universal physical safety proof'}
def main():
 contract=json.loads((ROOT/'output'/'PREPARED_CONTRACT.json').read_text()); key=contract.pop('contract_sha256')
 if h(contract)!=key:raise SystemExit('PREPARED CONTRACT HASH MISMATCH')
 contract['contract_sha256']=key
 result={'schema':'deagle.grid_k1.exact_witnesses.v1','run_id':contract['run_id'],'contract_sha256':key,
 'method':'prepared, single pass, exact fractions','timestamp_source':'execution_host_utc_not_independently_attested','certificates':[],'receipts':[]}
 prev='0'*64
 for i,scenario in enumerate(contract['scenarios'],1):
  proof=evaluate(contract,scenario)
  cert={'ordinal':i,'scenario_input_sha256':h(scenario),'proposition':'The reported decision follows from all explicitly modeled guard checks for the specified finite synthetic scenario.', 'witness':proof}
  cert['certificate_sha256']=h(cert)
  receipt={'ordinal':i,'case_id':scenario['id'],'run_id':contract['run_id'],
   'decision_id':contract['run_id']+':'+scenario['id'],
   'corridor_id':'SYNTHETIC-POWER-WATER-TELECOM-001',
   'participating_domains':['power','water','telecommunications'],
   'proposed_transition':scenario['action'],
   'authority_basis':{'authority_valid_input':scenario['authority_valid'],'action_permitted_input':scenario['action'] in scenario['permissions'],'fresh_evidence_input':scenario['fresh_evidence']},
   'state_snapshot_ref':h(scenario),
   'decision_outcome':proof['outcome'],'failed_constraint_if_any':proof['failed_constraints'],
   'reroute_or_degrade_mode_if_any':scenario['action'] if scenario['action'] in ('REROUTE','DEGRADE') else None,
   'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
   'timestamp_source':'execution_host_clock_not_attested',
   'prev_receipt_sha256':prev,'certificate_sha256':cert['certificate_sha256'],
   'decision':proof['outcome'],'failed_constraints':proof['failed_constraints']}
  receipt['receipt_sha256']=h(receipt)
  result['certificates'].append(cert);result['receipts'].append(receipt);prev=receipt['receipt_sha256']
 result['final_receipt_sha256']=prev
 out=ROOT/'output'/'EXACT_WITNESSES_CERTIFICATES_RECEIPTS.json';out.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+'\n');print('One run complete:',len(result['certificates']),'certificates',len(result['receipts']),'receipts')
 for r in result['certificates']:
  w=r['witness'];print(w['scenario_id'],w['outcome'],w['failed_constraints'],'cut',w['source_cut_capacity'],'/',w['required_service'])
if __name__=='__main__':main()
