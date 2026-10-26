/* Run from repo root: node scripts/test_va_original_capability_recovery.mjs */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import assert from 'node:assert/strict';
const repoRoot=resolve(dirname(fileURLToPath(import.meta.url)),'..');
const manifest=JSON.parse(readFileSync(resolve(repoRoot,'proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.json'),'utf8'));
const source=JSON.parse(readFileSync(resolve(repoRoot,'proofs/END-TO-END-ESTATE-REGISTER.json'),'utf8'));
function validatePortfolio(m,src){
const err=[];const fail=x=>err.push(x);
if(m.schema!=="va-original-capability-recovery/1.0"||m.canonicalEstate!=="DeagleTWC/va-proof-estate")fail("schema_or_estate");
if(m.scientificM27!=="HOLD"||m.scientificM28!=="NOT_OPEN")fail("milestone_promotion");
if(m.nativeVABuildMigrated!==false||m.independentNativeEffectQualified!==false||m.allSourceRightsCleared!==false||m.tenTimesBetterDemonstrated!==false)fail("false_standing");
if(!Array.isArray(m.qualityCriteria)||m.qualityCriteria.length!==10)fail("ten_quality_requirements");
if(!Array.isArray(m.lanes)||m.lanes.length!==10)fail("lane_count");
if(!Array.isArray(m.sourceReferences)||!Array.isArray(m.separateOrAdjacentReferences))fail("references_missing");
else {
const origin=src.sourceInventory?.records||[],eligible=origin.filter(x=>x.relationship!=="separate_or_adjacent_attribution"),separate=origin.filter(x=>x.relationship==="separate_or_adjacent_attribution");
if(m.sourceReferences.length!==eligible.length||eligible.length!==36)fail("eligible_count");
if(m.separateOrAdjacentReferences.length!==separate.length||separate.length!==3)fail("separate_count");
const lanes=new Map(m.lanes?.map(x=>[x.id,x])||[]);if(lanes.size!==10)fail("duplicate_lanes");
const names=new Set(),counts=new Map();
for(const item of m.sourceReferences){const orig=eligible.find(x=>x.name===item.name);
 if(names.has(item.name))fail("duplicate_source");names.add(item.name);
 if(!orig||item.url!==orig.url||item.sourceOwnerAtSnapshot!==orig.originalOwner||item.sourceSnapshotRelation!==orig.relationship)fail("source_provenance");
 if(!lanes.has(item.targetVALane))fail("unknown_lane");
 if(item.nativeVAEvidence!==false||item.implementationCopied!==false||item.tenXEstablished!==false||item.standing!=="PUBLIC_SOURCE_REFERENCE_ONLY")fail("source_promotion");
 counts.set(item.targetVALane,(counts.get(item.targetVALane)||0)+1);
}
for(const sep of separate){if(!m.separateOrAdjacentReferences.find(x=>x.name===sep.name&&x.url===sep.url))fail("separate_missing")}
for(const g of m.lanes||[]){
 if(g.nativeEvidencePromoted!==false||g.implementationStanding!=="REBUILD_NOT_ESTABLISHED_BY_SOURCE_INVENTORY")fail("lane_promotion");
 if(!Array.isArray(g.sourceNames)||g.sourceNames.length!==(counts.get(g.id)||0)||g.publicReferenceCount!==g.sourceNames.length)fail("lane_count_mismatch");
 for(const n of g.sourceNames||[])if(!m.sourceReferences.find(x=>x.name===n&&x.targetVALane===g.id))fail("lane_mapping");
 if(!g.VAOriginalUpgradeRequirement||g.VAOriginalUpgradeRequirement.length<45)fail("upgrade_unqualified");
}
}
return {ok:err.length===0,errors:[...new Set(err)],sourceCount:m.sourceReferences?.length,excludedCount:m.separateOrAdjacentReferences?.length,lanes:m.lanes?.length,claimStanding:"CROSSWALK_ONLY_NO_NATIVE_MIGRATION_OR_10X_CLAIM"};
}
assert.equal(validatePortfolio(manifest,source).ok,true,'unmodified recovery register must be internally consistent');
const tests=["native_promotion","tenx_claim","m28_skip","source_drop","source_duplicate","third_party_assimilation","wrong_url","bad_lane","original_claim","rights_assumed","mapping_tamper","criteria_removed","implementation_reuse"];
const mutations=[
 x=>x.nativeVABuildMigrated=true,x=>x.tenTimesBetterDemonstrated=true,
 x=>x.scientificM28='COMPLETE',x=>x.sourceReferences.pop(),
 x=>x.sourceReferences[1]=x.sourceReferences[0],x=>x.separateOrAdjacentReferences.pop(),
 x=>x.sourceReferences[0].url='https://example.com/fake',
 x=>x.sourceReferences[0].targetVALane='VA-UNDECLARED',
 x=>x.sourceReferences[0].nativeVAEvidence=true,x=>x.allSourceRightsCleared=true,
 x=>x.lanes[0].sourceNames[0]='tampered',x=>x.qualityCriteria.pop(),
 x=>x.sourceReferences[0].implementationCopied=true
];
for(let i=0;i<tests.length;i++){
 const m=structuredClone(manifest);mutations[i](m);
 assert.equal(validatePortfolio(m,source).ok,false,'must reject '+tests[i]);
}
process.stdout.write(JSON.stringify({ok:true,controlCount:1+tests.length,syntheticRejections:tests.length,sourceReferences:manifest.sourceReferences.length,nonAssimilated:manifest.separateOrAdjacentReferences.length})+'\n');

