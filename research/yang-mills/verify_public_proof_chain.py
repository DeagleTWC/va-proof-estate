#!/usr/bin/env python3
"""Public URK-proof-chain scope and data check for Yang-Mills v1.1.
This is NOT a native URK kernel or mass-gap certificate.
"""
import json,pathlib,subprocess,sys,hashlib
p=pathlib.Path(__file__).resolve().parent
ledger=p/'03_REPRODUCIBILITY'/'STAGE72_MEDIATOR_LEDGER.json'
assert hashlib.sha256(ledger.read_bytes()).hexdigest()=='a6209231f4e5f7a14ea713c33910301c4fbfa194e89bb34355392d127cc24bc3'
contract=json.loads((p/'URK_PROOF_CHAIN_STATUS.json').read_text())
assert contract['schema']=='va-urk-generated-formula-proof-chain/v1.1'
assert [c['yang_mills_proof_binding'] for c in contract['carriers']][-1].startswith('author-proposed')
s=subprocess.run([sys.executable,str(p/'03_REPRODUCIBILITY'/'verify_public_incidence.py')],capture_output=True,text=True,check=True)
assert '14/14' in s.stdout
print('PASS: generator-to-formula provenance labels are explicit; Stage 72 bytes match; 14/14 public finite-lattice replay; no unsupported native continuum proof standing asserted.')
