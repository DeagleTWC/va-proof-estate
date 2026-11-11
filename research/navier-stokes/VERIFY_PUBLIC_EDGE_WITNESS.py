#!/usr/bin/env python3
"""Public-safe snapshot witness verifier; not original URK protected kernel.
Requires Python standard library only. No network requests or source changes.
"""
from pathlib import Path
import tempfile,subprocess,hashlib,json,sys
r=Path(__file__).resolve().parent
p=r/'04_PUBLIC_COMPANION'
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
checks={}
checks['source_sha256']=h(p/'urk_harmonic_edge_rates.py')=='baad535857070231eabcadcbb13b5b44f365fee2568fb2cbf75a4eaf1ad167e8'
checks['input_sha256']=h(p/'urk_harmonic_edge_input.json')=='9ed1612238f7685cdf250fe2e79191279d84974665c37120b52dccf8f1fa9692'
checks['archived_output_sha256']=h(p/'urk_harmonic_edge_rates_example.json')=='3be2cad99b8b66441b9ca62a3db7dfec53a59bc56201f8636556076282496258'
with tempfile.TemporaryDirectory() as t:
 out=Path(t)/'replay.json'
 subprocess.run([sys.executable,str(p/'urk_harmonic_edge_rates.py'),'--input',str(p/'urk_harmonic_edge_input.json'),'--output',str(out)],capture_output=True,text=True,check=True)
 fresh=json.loads(out.read_text())
 checks['byte_identical_replay']=out.read_bytes()==(p/'urk_harmonic_edge_rates_example.json').read_bytes()
 checks['six_modes']=fresh['input_mode_count']==6
 checks['thirty_ordered_edges']=fresh['generated_ordered_edge_count']==30
 c=fresh['numerical_consistency']
 checks['divergence_and_reality']=c['divergence_error']==0 and c['conjugacy_error']==0
 checks['nonlinear_balance']=c['nonlinear_energy_transfer_sum']==0 and c['nonlinear_energy_transfer_balance_pass']
 checks['kinetic_heat_residual']=c['kinetic_heat_balance_residual']==0
 checks['initial_smallness_test']=fresh['small_data_reference']['continuation_77_smallness_test_pass'] and fresh['small_data_reference']['epsilon'] < fresh['small_data_reference']['threshold_nu_over_8']
 checks['no_native_proof_claim']=fresh['candidate_classification']=='DREAM_OR_PAUSE_PENDING_ORIGINAL_URK_INVARIANT_CHECKS'
 print(json.dumps({'classification':'public finite Fourier snapshot only; no unrestricted NS proof','checks':checks,'passed':sum(checks.values()),'total':len(checks)},indent=2))
 assert all(checks.values()),'A public witness check failed'
