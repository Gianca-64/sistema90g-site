#!/usr/bin/env node
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import process from 'node:process';

const chrome = process.argv[2];
const outDir = process.argv[3];
const baseUrl = (process.argv[4] || 'http://127.0.0.1:4174').replace(/\/$/, '');
if (!chrome || !outDir) {
  console.error('Uso: node tools/capture_case_visual_v2.mjs <chrome> <out-dir> [base-url]');
  process.exit(2);
}

const pages = [
  ['lavastoviglie','caso-lavastoviglie-passaggio-cucina.html','s90g-case-mode-use','90G Use'],
  ['isola','caso-isola-passaggi-cucina.html','s90g-case-mode-conflict','90G Conflict'],
  ['preventivo','caso-preventivo-cucina-sconto-valore.html','s90g-case-mode-compare','90G Compare'],
];
const viewports = [['desktop',1440,1100,false],['mobile',390,844,true]];
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function waitForPort(profile, timeout=10000){
  const file=join(profile,'DevToolsActivePort'); const started=Date.now();
  while(Date.now()-started<timeout){
    try{const port=Number(readFileSync(file,'utf8').trim().split(/\r?\n/)[0]); if(Number.isInteger(port)&&port>0)return port;}catch{}
    await sleep(100);
  }
  throw new Error('Chrome non ha esposto DevToolsActivePort entro 10 secondi');
}

async function connect(wsUrl){
  const ws=new WebSocket(wsUrl); let nextId=1; const pending=new Map(); const listeners=new Map();
  await new Promise((resolve,reject)=>{const t=setTimeout(()=>reject(new Error('Timeout WebSocket DevTools')),5000);ws.addEventListener('open',()=>{clearTimeout(t);resolve();},{once:true});ws.addEventListener('error',()=>{clearTimeout(t);reject(new Error('Errore WebSocket DevTools'));},{once:true});});
  ws.addEventListener('message',e=>{const m=JSON.parse(e.data.toString());if(m.id&&pending.has(m.id)){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(new Error(m.error.message||'Errore CDP')):p.resolve(m.result||{});return;}if(m.method&&listeners.has(m.method))for(const fn of [...listeners.get(m.method)])fn(m.params||{});});
  const send=(method,params={})=>new Promise((resolve,reject)=>{const id=nextId++;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}));setTimeout(()=>{if(pending.has(id)){pending.delete(id);reject(new Error(`Timeout CDP: ${method}`));}},10000);});
  const once=(method,timeout=15000)=>new Promise((resolve,reject)=>{const set=listeners.get(method)||new Set();listeners.set(method,set);const timer=setTimeout(()=>{set.delete(handler);reject(new Error(`Timeout evento CDP: ${method}`));},timeout);const handler=params=>{clearTimeout(timer);set.delete(handler);resolve(params);};set.add(handler);});
  return {ws,send,once};
}

async function auditPage(pageKey, rel, expectedClass, expectedLabel, suffix, width, height, mobile){
  const url=`${baseUrl}/${rel}`; const profile=mkdtempSync(join(tmpdir(),`s90g-case-v2-${pageKey}-${suffix}-`)); let proc;
  try{
    proc=spawn(chrome,['--headless=new','--disable-gpu','--hide-scrollbars','--disable-extensions','--disable-background-networking','--disable-component-update','--disable-sync','--metrics-recording-only','--no-first-run','--no-default-browser-check',`--user-data-dir=${profile}`,'--remote-debugging-port=0','about:blank'],{detached:true,stdio:['ignore','pipe','pipe']});
    const port=await waitForPort(profile); const targets=await fetch(`http://127.0.0.1:${port}/json/list`).then(r=>r.json()); const target=targets.find(t=>t.type==='page');
    if(!target?.webSocketDebuggerUrl)throw new Error('Target pagina DevTools non trovato');
    const cdp=await connect(target.webSocketDebuggerUrl); await cdp.send('Page.enable'); await cdp.send('Runtime.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile,screenWidth:width,screenHeight:height,positionX:0,positionY:0,dontSetVisibleSize:false});
    if(mobile)await cdp.send('Emulation.setTouchEmulationEnabled',{enabled:true,maxTouchPoints:5});
    const loaded=cdp.once('Page.loadEventFired'); await cdp.send('Page.navigate',{url}); await loaded; await sleep(1400);

    const stateResult=await cdp.send('Runtime.evaluate',{expression:`(() => {
      const root=document.documentElement;
      const modeEl=document.querySelector('.s90g-dark-band .s90g-kicker');
      const pseudo=modeEl ? getComputedStyle(modeEl,'::before').content.replace(/^['\"]|['\"]$/g,'') : '';
      const consequence=[...document.querySelectorAll('.s90g-section .s90g-kicker')].find(e=>e.textContent.includes('La conseguenza'))?.closest('.s90g-section');
      const imgs=[...document.images].map(img=>({src:img.currentSrc||img.src,complete:img.complete,naturalWidth:img.naturalWidth}));
      return JSON.stringify({innerWidth:innerWidth,innerHeight:innerHeight,clientWidth:root.clientWidth,scrollWidth:root.scrollWidth,scrollHeight:root.scrollHeight,bodyClass:document.body.className,hero:!!document.querySelector('.s90g-inner-hero'),modeText:modeEl?.textContent.trim()||'',modePseudo:pseudo,consequence:!!consequence,brokenImages:imgs.filter(i=>!i.complete||i.naturalWidth===0)});
    })()`,returnByValue:true});
    const state=JSON.parse(stateResult.result?.value||'{}');
    if(state.innerWidth!==width||state.innerHeight!==height)throw new Error(`${pageKey}/${suffix}: viewport reale ${state.innerWidth}x${state.innerHeight}, atteso ${width}x${height}`);
    if(!state.bodyClass.includes('s90g-case-visual-v2'))throw new Error(`${pageKey}/${suffix}: classe s90g-case-visual-v2 mancante`);
    if(!state.bodyClass.includes(expectedClass))throw new Error(`${pageKey}/${suffix}: classe modalita attesa ${expectedClass} mancante in ${state.bodyClass}`);
    if(!state.hero)throw new Error(`${pageKey}/${suffix}: hero mancante`);
    if(!state.consequence)throw new Error(`${pageKey}/${suffix}: blocco conseguenza mancante`);
    if(!state.modePseudo.includes(expectedLabel))throw new Error(`${pageKey}/${suffix}: etichetta visuale attesa "${expectedLabel}" non trovata nel ::before "${state.modePseudo}"`);
    if(state.brokenImages?.length)throw new Error(`${pageKey}/${suffix}: immagini non caricate: ${state.brokenImages.map(i=>i.src).join(', ')}`);
    if(Number(state.scrollWidth)>Number(state.clientWidth)+1)throw new Error(`${pageKey}/${suffix}: overflow orizzontale ${state.scrollWidth}px > ${state.clientWidth}px`);

    const full=await cdp.send('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:true,clip:{x:0,y:0,width:state.clientWidth,height:Math.min(state.scrollHeight,9000),scale:1}});
    writeFileSync(join(outDir,`${pageKey}-full-${suffix}.png`),Buffer.from(full.data,'base64'));
    const rectResult=await cdp.send('Runtime.evaluate',{expression:`(() => { const e=[...document.querySelectorAll('.s90g-section .s90g-kicker')].find(x=>x.textContent.includes('La conseguenza'))?.closest('.s90g-section'); if(!e)return null; const r=e.getBoundingClientRect(); return JSON.stringify({x:r.left+scrollX,y:r.top+scrollY,width:r.width,height:r.height}); })()`,returnByValue:true});
    const rect=rectResult.result?.value?JSON.parse(rectResult.result.value):null;
    if(rect){const shot=await cdp.send('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:true,clip:{x:Math.max(0,rect.x),y:Math.max(0,rect.y),width:Math.min(state.clientWidth,rect.width),height:rect.height,scale:1}});writeFileSync(join(outDir,`${pageKey}-consequence-${suffix}.png`),Buffer.from(shot.data,'base64'));}
    cdp.ws.close();
    console.log(`OK ${pageKey} ${suffix}: ${expectedLabel}, no overflow, immagini OK`);
    return {pageKey,rel,expectedClass,expectedLabel,suffix,width,height,mobile,url,...state,horizontalOverflow:false};
  } finally {if(proc?.pid){try{process.kill(-proc.pid,'SIGKILL');}catch{}}rmSync(profile,{recursive:true,force:true});}
}

const results=[];
for(const page of pages)for(const viewport of viewports)results.push(await auditPage(...page,...viewport));
writeFileSync(join(outDir,'metrics.json'),JSON.stringify(results,null,2)+'\n');
console.log('OK Case Visual V2: campione Use/Conflict/Compare valido desktop/mobile.');
