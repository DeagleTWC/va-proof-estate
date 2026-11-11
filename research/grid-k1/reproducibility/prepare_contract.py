#!/usr/bin/env python3
"""Author-review preparation: freeze a synthetic cross-domain corridor before one arithmetic run."""
import json,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
SRC=ROOT/'sources'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(o): return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
base_caps={'S>A':6,'S>B':5,'S>C':4,'A>W':4,'A>T':2,'B>W':4,'B>T':3,'C>T':4}
healthy={'S>A':6,'S>B':5,'A>W':4,'A>T':2,'B>W':2,'B>T':3}
degrade={'S>A':3,'S>B':5,'A>W':3,'B>W':3,'B>T':2}
reroute={'S>A':3,'S>B':5,'S>C':3,'A>W':3,'B>W':3,'B>T':2,'C>T':3}
def sc(id,action,flows,loads,branch_A,backup=False,authority=True,fresh=True,permissions=None,inc='1/8'):
    return {'id':id,'action':action,'flow':flows,'demand':loads,'effective_A_capacity':branch_A,'backup_activated':backup,'authority_valid':authority,'fresh_evidence':fresh,'permissions':permissions if permissions is not None else ['CONTINUE','DEGRADE','REROUTE'],'debt_increment_SA':inc}
contract={
 'contract_schema':'deagle.grid_k1.synthetic_continuity.v1',
 'run_id':'GRID-K1-EXAM-001-2026-11-11',
 'prepared_before_execution':True,
 'description':'Synthetic directed single-commodity service-capacity abstraction, NOT a physical AC power-flow solver or deployed control kernel.',
 'nodes':['S','A','B','C','W','T'],
 'source':'S','service_sinks':['W','T'],
 'source_notes':{'S':'upstream power/continuity resource','A':'primary corridor','B':'secondary corridor','C':'pre-existing standby corridor','W':'water pumping service','T':'telecom service'},
 'edge_capacities_normal':base_caps,
 'edge_capacities_standby_off':{'S>C':0,'C>T':0},
 'baseline_demand':{'W':6,'T':5},
 'critical_minimum_degraded':{'W':6,'T':2},
 'cumulative_debt':{'edge':'S>A','initial':'3/4','strict_budget':'1'},
 'guard_contract':{'flow_nonnegative':True,'flow_capacity':True,'node_conservation':True,'all_sink_demand_exact':True,'mode_minimums':True,'permission':True,'authority':True,'evidence_freshness':True,'strict_debt_reserve':True},
 'proof_obligations':['flow_conservation_and_capacity','cut_capacity_certificate','mode_service_minima','cumulative_debt_reserve','authority_freshness_and_permissions','receipt_and_replay_integrity'],
 'scenarios':[
  sc('C01_HEALTHY_CONTINUE','CONTINUE',healthy,{'W':6,'T':5},6),
  sc('C02_FAULT_FULL_DEMAND','CONTINUE',healthy,{'W':6,'T':5},3),
  sc('C03_FAULT_DEGRADE','DEGRADE',degrade,{'W':6,'T':2},3),
  sc('C04_FAULT_BACKUP_REROUTE','REROUTE',reroute,{'W':6,'T':5},3,True),
  sc('C05_STALE_BACKUP_REROUTE','REROUTE',reroute,{'W':6,'T':5},3,True,True,False),
  sc('C06_DEBT_EXHAUSTION','DEGRADE',degrade,{'W':6,'T':2},3,False,True,True,None,'3/8'),
  sc('C07_UNAUTHORIZED_BACKUP','REROUTE',reroute,{'W':6,'T':5},3,True,True,True,['CONTINUE','DEGRADE'])
 ],
 'source_custody':{'continuity_kernel_json_sha256':sha((SRC/'Critical_Infrastructure_Continuity_Kernel_v1.json').read_bytes()),'world_kernel_atlas_docx_sha256':sha((SRC/'1886f847-cbfc-4955-8884-8ca6235568b2.docx').read_bytes())},
 'source_boundary':'Full Library drafts included in author-only review archive; separate public-ready archive excludes them pending author release approval.',
 'frozen_date':'2026-11-11',
}
contract['contract_sha256']=sha(dump(contract))
out=ROOT/'output'/'PREPARED_CONTRACT.json';out.write_text(json.dumps(contract,sort_keys=True,indent=2,ensure_ascii=False)+'\n');print('Prepared contract:',out,'sha256:',contract['contract_sha256'])
