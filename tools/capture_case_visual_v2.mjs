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
  console.error('Uso: node tools/capture_case_visual_v2.mjs <chrome> <output-dir> [base-url]');
  process.exit(2);
}

const pages = [
  ['lavastoviglie','caso-lavastoviglie-passaggio-cucina.html','90G Use'],
  ['isola','caso-isola-passaggi-cucina.html','90G Conflict'],
  ['preventivo','caso-preventivo-cucina-sconto-valore.html','90G Compare'],
];
const viewports = [['desktop',1440,1100,false],['mobile',390,844,true]];
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function waitForDevToolsPort(profile, timeoutMs = 10000) {
  const file = join(profile, 'DevToolsActivePort');
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    try {
      const lines = readFileSync(file, 'utf8').trim().split(/\r?\n/);
      const port = Number(lines[0]);
      if (Number.isInteger(port) && port > 0) return port;
    } catch {}
    await sleep(100);
  }
  throw new Error('Chrome non ha esposto DevToolsActivePort entro 10 secondi');
}

async function connectCdp(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let nextId = 1;
  const pending = new Map();
  const listeners = new Map();
  await new Promise((resolve,reject)=>{
    const timer=setTimeout(()=>reject(new Error('Timeout apertura WebSocket DevTools')),5000);
    ws.addEventListener('open',()=>{clearTimeout(timer);resolve();},{once:true});
    ws.addEventListener('error',()=>{clearTimeout(timer);reject(new Error('Errore WebSocket DevTools'));},{once:true});
  });
  ws.addEventListener('message',event=>{
    const message=JSON.parse(event.data.toString());
    if(message.id&&pending.has(message.id)){
      const {resolve,reject}=pending.get(message.id); pending.delete(message.id);
      if(message.error) reject(new Error(`${message.error.message||'Errore CDP'} (${message.error.code??'?'})`));
      else resolve(message.result||{});
      return;
    }
    if(message.method&&listeners.has(message.method)) for(const listener of [...listeners.get(message.method)]) listener(message.params||{});
  });
  const send=(method,params={})=>new Promise((resolve,reject)=>{
    const id=nextId++; pending.set(id,{resolve,reject}); ws.send(JSON.stringify({id,method,params}));
    setTimeout(()=>{if(pending.has(id)){pending.delete(id);reject(new Error(`Timeout CDP: ${method}`));}},10000);
  });
  const once=(method,timeoutMs=15000)=>new Promise((resolve,reject)=>{
    const set=listeners.get(method)||new Set(); listeners.set(method,set);
    const timer=setTimeout(()=>{set.delete(handler);reject(new Error(`Timeout evento CDP: ${method}`));},timeoutMs);
    const handler=params=>{clearTimeout(timer);set.delete(handler);resolve(params);}; set.add(handler);
  });
  return {ws,send,once};
}

async function auditPage(pageKey, rel, expectedMode, suffix, width, height, mobile) {
  const url = `${baseUrl}/${rel}`;
  const profile = mkdtempSync(join(tmpdir(), `s90g-case-v2-${pageKey}-${suffix}-`));
  let chromeProc;
  try {
    chromeProc=spawn(chrome,['--headless=new','--disable-gpu','--hide-scrollbars','--disable-extensions','--disable-background-networking','--disable-component-update','--disable-sync','--metrics-recording-only','--no-first-run','--no-default-browser-check',`--user-data-dir=${profile}`,'--remote-debugging-port=0','about:blank'],{detached:true,stdio:['ignore','pipe','pipe']});
    const port=await waitForDevToolsPort(profile);
    const targets=await fetch(`http://127.0.0.1:${port}/json/list`).then(r=>r.json());
    const pageTarget=targets.find(target=>target.type==='page');
    if(!pageTarget?.webSocketDebuggerUrl) throw new Error('Target pagina DevTools non trovato');
    const cdp=await connectCdp(pageTarget.webSocketDebuggerUrl);
    await cdp.send('Page.enable'); await cdp.send('Runtime.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile,screenWidth:width,screenHeight:height,positionX:0,positionY:0,dontSetVisibleSize:false});
    if(mobile) await cdp.send('Emulation.setTouchEmulationEnabled',{enabled:true,maxTouchPoints:5});
    const loaded=cdp.once('Page.loadEventFired'); await cdp.send('Page.navigate',{url}); await loaded; await sleep(1400);

    const stateResult=await cdp.send('Runtime.evaluate',{expression:`(() => {
      const root=document.documentElement;
      const hero=document.querySelector('.s90g-inner-hero');
      const mode=[...document.querySelectorAll('.s90g-dark-band .s90g-kicker')].map(e=>e.textContent.trim()).join(' | ');
      const consequence=[...document.querySelectorAll('.s90g-section .s90g-kicker')].find(e=>e.textContent.includes('La conseguenza'))?.closest('.s90g-section');
      const imgs=[...document.images].map(img=>({src:img.currentSrc||img.src,complete:img.complete,naturalWidth:img.naturalWidth}));
      return JSON.stringify({
        innerWidth:window.innerWidth, innerHeight:window.innerHeight,
        clientWidth:root.clientWidth, scrollWidth:root.scrollWidth, scrollHeight:root.scrollHeight,
        bodyClass:document.body.className, hero:!!hero, mode,
        consequence:!!consequence,
        consequenceText:consequence?.innerText||'',
        brokenImages:imgs.filter(img=>!img.complete||img.naturalWidth===0)
      });
    })()`,returnByValue:true});
    const state=JSON.parse(stateResult.result?.value||'{}');
    if(state.innerWidth!==width||state.innerHeight!==height) throw new Error(`${pageKey}/${suffix}: viewport reale ${state.innerWidth}x${state.innerHeight}, atteso ${width}x${height}`);
    if(!state.bodyClass.includes('s90g-case-visual-v2')) throw new Error(`${pageKey}/${suffix}: classe s90g-case-visual-v2 mancante`);
    if(!state.hero) throw new Error(`${pageKey}/${suffix}: hero mancante`);
    if(!state.consequence) throw new Error(`${pageKey}/${suffix}: blocco conseguenza mancante`);
    if(!state.mode.includes(expectedMode)) throw new Error(`${pageKey}/${suffix}: modalita attesa "${expectedMode}" non trovata in "${state.mode}"`);
    if(state.brokenImages?.length) throw new Error(`${pageKey}/${suffix}: immagini non caricate: ${state.brokenImages.map(i=>i.src).join(', ')}`);
    const overflow=Number(state.scrollWidth)>Number(state.clientWidth)+1;
    if(overflow) throw new Error(`${pageKey}/${suffix}: overflow orizzontale ${state.scrollWidth}px > ${state.clientWidth}px`);

    const full=await cdp.send('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:true,clip:{x:0,y:0,width:state.clientWidth,height:Math.min(state.scrollHeight,9000),scale:1}});
    writeFileSync(join(outDir,`${pageKey}-full-${suffix}.png`),Buffer.from(full.data,'base64'));

    const consequenceShot=await cdp.send('Runtime.evaluate',{expression:`(() => { const e=[...document.querySelectorAll('.s90g-section .s90g-kicker')].find(x=>x.textContent.includes('La conseguenza'))?.closest('.s90g-section'); if(!e)return null; const r=e.getBoundingClientRect(); return JSON.stringify({x:r.left+scrollX,y:r.top+scrollY,width:r.width,height:r.height}); })()`,returnByValue:true});
    const rect=consequenceShot.result?.value?JSON.parse(consequenceShot.result.value):null;
    if(rect){
      const shot=await cdp.send('Page.captureScreenshot',{format:'png',fromSurface:true,captureBeyondViewport:true,clip:{x:Math.max(0,rect.x),y:Math.max(0,rect.y),width:Math.min(state.clientWidth,rect.width),height:rect.height,scale:1}});
      writeFileSync(join(outDir,`${pageKey}-consequence-${suffix}.png`),Buffer.from(shot.data,'base64'));
    }
    cdp.ws.close();
    console.log(`OK ${pageKey} ${suffix}: ${expectedMode}, no overflow, immagini OK`);
    return {pageKey,rel,expectedMode,suffix,width,height,mobile,url,...state,horizontalOverflow:false};
  } finally {
    if(chromeProc?.pid){try{process.kill(-chromeProc.pid,'SIGKILL');}catch{}}
    rmSync(profile,{recursive:true,force:true});
  }
}

const results=[];
for(const page of pages) for(const viewport of viewports) results.push(await auditPage(...page,...viewport));
writeFileSync(join(outDir,'metrics.json'),JSON.stringify(results,null,2)+'\n');
console.log('OK Case Visual V2: campione Use/Conflict/Compare valido desktop/mobile.');
