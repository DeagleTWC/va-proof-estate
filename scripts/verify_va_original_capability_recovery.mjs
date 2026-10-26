/* V.A. original-source capability recovery gate: inventory consistency only.
   Does not execute native V.A., validate rights, or prove measured consequences.
   Usage: node scripts/verify_va_original_capability_recovery.mjs */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
const repoRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const manifest = JSON.parse(readFileSync(resolve(repoRoot, 'proofs/VA-ORIGINAL-CAPABILITY-RECOVERY.json'), 'utf8'));
const source = JSON.parse(readFileSync(resolve(repoRoot, 'proofs/END-TO-END-ESTATE-REGISTER.json'), 'utf8'));
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
const result = validatePortfolio(manifest, source);
process.stdout.write(JSON.stringify(result,null,2)+'\n');
if(!result.ok) process.exitCode=1;

