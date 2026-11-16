'use strict';
(async function displayExactOfficialMark() {
  const element = document.getElementById('vaOfficialLogo');
  if (!element) return;
  try {
    const filenames = Array.from({length:12},(_,i)=>'assets/logo-parts/logo.part.'+String(i).padStart(2,'0')+'.b64');
    const parts = await Promise.all(filenames.map(async name=>{
      const response=await fetch(name,{cache:'force-cache'});
      if(!response.ok) throw Error('Missing original-logo part: '+name);
      return (await response.text()).replace(/\s+/g,'');
    }));
    const binary=atob(parts.join(''));
    const bytes=new Uint8Array(binary.length);
    for(let i=0;i<binary.length;i++)bytes[i]=binary.charCodeAt(i);
    const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),x=>x.toString(16).padStart(2,'0')).join('');
    if(hash!=='c18391f95a487ea8b11141bc4ebe7781aaa33e767ed8003f854e52a49e68eace')throw Error('Official V.A. logo integrity check failed');
    const url=URL.createObjectURL(new Blob([bytes],{type:'image/png'}));
    element.addEventListener('load',()=>URL.revokeObjectURL(url),{once:true});
    element.src=url;
    element.hidden=false;
  }catch(error){console.error('Official V.A. logo unavailable; no substitute displayed',error);}
})();