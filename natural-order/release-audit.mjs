import {readdir,readFile,lstat,access} from 'node:fs/promises';
import {join,relative,resolve,dirname,sep,extname} from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {DEFINITIONS} from './definition-kernel.mjs';
import {TEACHING_KERNELS,auditTeachingKernelBank} from './teaching-kernels.mjs';

// Every file in a public GitHub Pages repository is downloadable, including
// developer tests. A fixed manifest is therefore the release boundary.
export const PUBLIC_FILES=Object.freeze([
  'README.md','VA_Universal_Bounded_Review_MNDA.pdf','access.html','about-terry.html','about-frankie.html','shared-purpose.html','ethical-reasoning.html','app.mjs','engine.mjs','index.html','repair-evidence.html',
  'knowledge.mjs','definition-kernel.mjs','teaching-kernels.mjs','human-interaction-kernel.mjs','open-conversation-kernel.mjs','frankie-client.mjs','release-audit.mjs','styles.css',
  'tests/app-interaction.test.mjs','tests/definition-kernel.test.mjs','tests/teaching-kernels.test.mjs',
  'tests/engine.test.mjs','tests/human-interaction-kernel.test.mjs','tests/open-conversation-kernel.test.mjs','tests/frankie-client.test.mjs','tests/pages.test.mjs','tests/release.test.mjs',
]);
const manifest=new Set(PUBLIC_FILES);
const allowedExtensions=new Set(['.html','.css','.mjs','.md']);
const publicNda='VA_Universal_Bounded_Review_MNDA.pdf';
const publicNdaSha256='8a4993180ad411920c15d79ad3ffea7f06dab469ae6bf4b5f1810df0c23bb056';
// Unlike the original offline lesson finder, the optional companion has a
// network-capable code path. Pin its exact public-safe bytes AND its disabled
// endpoint configuration until a new reviewed release explicitly changes both.
const frankieClientSha256='7517d7e2c7875e051358e690c182cd3262d461b2881137e2940e5cc1984dfa93';
const offlineCsp='Content-Security-Policy" content="default-src \'self\'; script-src \'self\'; style-src \'self\'; img-src \'self\'; connect-src \'none\'; object-src \'none\'; base-uri \'none\'; form-action \'none\'';
const secretPattern=/-----BEGIN\s+(?:RSA |EC |OPENSSH )?PRIVATE KEY-----|(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}/;
const networkCalls=/\b(?:fetch|XMLHttpRequest|sendBeacon|WebSocket|EventSource)\s*\(/;
const urls=/https?:\/\/[^\s"'<>`]+/g;
const attributes=/\b(?:href|src)="([^"]+)"/g;
const catalogSources=/\bsource\('[^']*','([^']+)'\)/g;

async function present(path) {try{await access(path);return true;}catch{return false;}}

export async function auditRelease(root,{allowPartial=false,siteRoot}={}) {
  const base=resolve(typeof root==='string'?root:fileURLToPath(root));
  const siteBase=resolve(siteRoot ? (typeof siteRoot==='string'?siteRoot:fileURLToPath(siteRoot)) : dirname(base));
  const errors=[];
  const files=[];

  async function checkLink(href,from) {
    if(href.startsWith('#')) {
      const fragment=href.slice(1);
      if(fragment && !from.data.includes(`id="${fragment}"`)) errors.push(`${from.rel}: broken in-page link ${href}`);
      return;
    }
    if(/^https?:\/\//i.test(href)) {
      let url;
      try{url=new URL(href);}catch{errors.push(`${from.rel}: invalid external endpoint ${href}`);return;}
      if(['README.md','release-audit.mjs'].includes(from.rel) && url.origin==='http://localhost:8765')return;
      const permitted=(url.origin==='https://deagletwc.github.io' && url.pathname.startsWith('/va-proof-estate/')) ||
        (url.origin==='https://github.com' && url.pathname.startsWith('/DeagleTWC/va-proof-estate/')) ||
        (from.rel==='release-audit.mjs' && ['https://deagletwc.github.io','https://github.com'].includes(url.origin) && url.pathname==='/');
      if(!permitted) errors.push(`${from.rel}: unapproved external endpoint ${href}`);
      return;
    }
    if(from.rel==='access.html' && href==='mailto:canarybird0618@gmail.com?subject=V.A.%20Bounded%20Review%20NDA')return;
    if(from.rel==='index.html' && href==='mailto:canarybird0618@gmail.com?subject=Natural%20Order%20Teaching%20Example')return;
    if(/^[a-z]+:/i.test(href) || href.startsWith('//')) {errors.push(`${from.rel}: unapproved link scheme ${href}`);return;}
    const path=href.split(/[?#]/,1)[0];
    const local=path.startsWith('../') ? resolve(siteBase,path.slice(3)) : resolve(dirname(join(base,from.rel)),path);
    if(!(local===siteBase || local.startsWith(`${siteBase}${sep}`) || local===base || local.startsWith(`${base}${sep}`))) {errors.push(`${from.rel}: link escapes public site ${href}`);return;}
    if(!(await present(local))) errors.push(`${from.rel}: broken local link ${href}`);
  }

  async function inspect(directory) {
    for(const item of await readdir(directory,{withFileTypes:true})) {
      const absolute=join(directory,item.name);
      const rel=relative(base,absolute).split(sep).join('/');
      if(item.isSymbolicLink()){errors.push(`${rel}: symlinks prohibited`);continue;}
      if(item.isDirectory()){await inspect(absolute);continue;}
      if(!item.isFile()){errors.push(`${rel}: unexpected file type`);continue;}
      files.push(rel);
      if(rel===publicNda) {
        const bytes=await readFile(absolute);
        if(bytes.length>1500000 || bytes.subarray(0,5).toString()!=='%PDF-' ||
          createHash('sha256').update(bytes).digest('hex')!==publicNdaSha256) {
          errors.push(`${rel}: public NDA PDF SHA-256 or format mismatch`);
        }
        continue;
      }
      if(!manifest.has(rel) || item.name.startsWith('.') || !allowedExtensions.has(extname(rel))) {
        errors.push(`${rel}: file not on public release manifest`);continue;
      }
      const stat=await lstat(absolute);
      if(stat.size>500000){errors.push(`${rel}: oversized release asset`);continue;}
      const data=await readFile(absolute,'utf8');
      if(secretPattern.test(data))errors.push(`${rel}: possible secret key in release`);
      // Published tests contain malicious examples, but their type, size,
      // path and real secret-key bytes remain checked.
      if(rel.startsWith('tests/'))continue;
      if(rel==='frankie-client.mjs'){
        const hash=createHash('sha256').update(data).digest('hex');
        if(hash!==frankieClientSha256||!data.includes("export const FRANKIE_GATEWAY_URL='';")){
          errors.push(`${rel}: pinned inactive client boundary changed without release review`);
        }
      }
      if(rel==='index.html'&&!data.includes(offlineCsp)){
        errors.push(`${rel}: disabled Frankie release lacks a no-connect CSP`);
      }
      if(networkCalls.test(data))errors.push(`${rel}: unapproved runtime network endpoint`);
      for(const url of data.match(urls)||[])await checkLink(url.replace(/[),.;]+$/,''),{rel,data});
      if(rel.endsWith('.html'))for(const match of data.matchAll(attributes))await checkLink(match[1],{rel,data});
      if(rel==='knowledge.mjs')for(const match of data.matchAll(catalogSources))await checkLink(match[1],{rel,data});
    }
  }
  await inspect(base);
  for(const issue of auditTeachingKernelBank(TEACHING_KERNELS))errors.push(`teaching bank: ${issue}`);
  for(const definition of DEFINITIONS){
    await checkLink(definition.source.href,{rel:'definition-kernel.mjs',data:''});
  }
  if(!allowPartial)for(const name of manifest)if(!files.includes(name))errors.push(`${name}: missing from public release`);
  return {files:files.sort(),errors};
}

if(process.argv[1]&&import.meta.url===new URL(`file://${process.argv[1]}`).href){
  const result=await auditRelease(new URL('.',import.meta.url),{siteRoot:process.env.VA_SITE_ROOT});
  for(const file of result.files)process.stdout.write(`PUBLIC ${file}\n`);
  if(result.errors.length){for(const error of result.errors)process.stderr.write(`FAIL ${error}\n`);process.exitCode=1;}
  else process.stdout.write('RELEASE AUDIT PASSED\n');
}
