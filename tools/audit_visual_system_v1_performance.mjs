#!/usr/bin/env node
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const chrome = process.argv[2];
const url = process.argv[3] || 'http://127.0.0.1:4174/';
if (!chrome) {
  console.error('Uso: node tools/audit_visual_system_v1_performance.mjs <chrome> [url]');
  process.exit(2);
}

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
  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('Timeout apertura WebSocket DevTools')), 5000);
    ws.addEventListener('open', () => { clearTimeout(timer); resolve(); }, { once: true });
    ws.addEventListener('error', () => { clearTimeout(timer); reject(new Error('Errore WebSocket DevTools')); }, { once: true });
  });
  ws.addEventListener('message', event => {
    const message = JSON.parse(event.data.toString());
    if (message.id && pending.has(message.id)) {
      const { resolve, reject } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) reject(new Error(`${message.error.message || 'Errore CDP'} (${message.error.code ?? '?'})`));
      else resolve(message.result || {});
      return;
    }
    if (message.method && listeners.has(message.method)) {
      for (const listener of [...listeners.get(message.method)]) listener(message.params || {});
    }
  });
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const id = nextId++;
    pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params }));
    setTimeout(() => {
      if (pending.has(id)) {
        pending.delete(id);
        reject(new Error(`Timeout CDP: ${method}`));
      }
    }, 15000);
  });
  const once = (method, timeoutMs = 15000) => new Promise((resolve, reject) => {
    const set = listeners.get(method) || new Set();
    listeners.set(method, set);
    const handler = params => {
      clearTimeout(timer);
      set.delete(handler);
      resolve(params);
    };
    const timer = setTimeout(() => {
      set.delete(handler);
      reject(new Error(`Timeout evento CDP: ${method}`));
    }, timeoutMs);
    set.add(handler);
  });
  return { ws, send, once };
}

async function runAudit(label, width, height, mobile) {
  const profile = mkdtempSync(join(tmpdir(), `s90g-perf-${label}-`));
  let chromeProc;
  try {
    chromeProc = spawn(chrome, [
      '--headless=new', '--disable-gpu', '--hide-scrollbars', '--disable-extensions',
      '--disable-background-networking', '--disable-component-update', '--disable-sync',
      '--metrics-recording-only', '--no-first-run', '--no-default-browser-check',
      `--user-data-dir=${profile}`, '--remote-debugging-port=0', 'about:blank'
    ], { detached: true, stdio: ['ignore', 'pipe', 'pipe'] });

    const port = await waitForDevToolsPort(profile);
    const targets = await fetch(`http://127.0.0.1:${port}/json/list`).then(r => r.json());
    const pageTarget = targets.find(target => target.type === 'page');
    if (!pageTarget?.webSocketDebuggerUrl) throw new Error('Target pagina DevTools non trovato');

    const cdp = await connectCdp(pageTarget.webSocketDebuggerUrl);
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Network.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width, height, deviceScaleFactor: mobile ? 2 : 1, mobile,
      screenWidth: width, screenHeight: height, positionX: 0, positionY: 0,
      dontSetVisibleSize: false
    });
    if (mobile) {
      await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
      await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
      await cdp.send('Network.emulateNetworkConditions', {
        offline: false,
        latency: 150,
        downloadThroughput: 200000,
        uploadThroughput: 90000,
        connectionType: 'cellular4g'
      });
    }

    await cdp.send('Page.addScriptToEvaluateOnNewDocument', { source: `
      window.__s90gVitals = { cls: 0, lcp: 0, longTasks: [] };
      try {
        new PerformanceObserver(list => {
          for (const e of list.getEntries()) if (!e.hadRecentInput) window.__s90gVitals.cls += e.value;
        }).observe({ type: 'layout-shift', buffered: true });
      } catch {}
      try {
        new PerformanceObserver(list => {
          const entries = list.getEntries();
          const last = entries[entries.length - 1];
          if (last) window.__s90gVitals.lcp = last.startTime;
        }).observe({ type: 'largest-contentful-paint', buffered: true });
      } catch {}
      try {
        new PerformanceObserver(list => {
          for (const e of list.getEntries()) window.__s90gVitals.longTasks.push(e.duration);
        }).observe({ type: 'longtask', buffered: true });
      } catch {}
    ` });

    const loaded = cdp.once('Page.loadEventFired');
    await cdp.send('Page.navigate', { url });
    await loaded;
    await sleep(mobile ? 4500 : 2500);

    const evalResult = await cdp.send('Runtime.evaluate', {
      expression: `JSON.stringify((() => {
        const paints = performance.getEntriesByType('paint');
        const fcp = paints.find(e => e.name === 'first-contentful-paint')?.startTime || 0;
        const nav = performance.getEntriesByType('navigation')[0];
        const longTasks = window.__s90gVitals?.longTasks || [];
        const tbt = longTasks.reduce((sum, d) => sum + Math.max(0, d - 50), 0);
        const doc = document.documentElement;
        const hero = document.querySelector('.s90g-hero');
        const visualProof = document.querySelector('[data-s90g-wow-visual-proof="true"]');
        return {
          fcp,
          lcp: window.__s90gVitals?.lcp || 0,
          cls: window.__s90gVitals?.cls || 0,
          tbt,
          domContentLoaded: nav?.domContentLoadedEventEnd || 0,
          loadEventEnd: nav?.loadEventEnd || 0,
          transferSize: nav?.transferSize || 0,
          encodedBodySize: nav?.encodedBodySize || 0,
          scrollWidth: doc.scrollWidth,
          clientWidth: doc.clientWidth,
          horizontalOverflow: doc.scrollWidth > doc.clientWidth + 1,
          heroPresent: !!hero,
          visualProofPresent: !!visualProof
        };
      })())`,
      returnByValue: true
    });
    const metrics = JSON.parse(evalResult.result?.value || '{}');
    cdp.ws.close();
    return { label, width, height, mobile, ...metrics };
  } finally {
    if (chromeProc?.pid) { try { process.kill(-chromeProc.pid, 'SIGKILL'); } catch {} }
    rmSync(profile, { recursive: true, force: true });
  }
}

const results = [];
results.push(await runAudit('desktop', 1440, 1100, false));
results.push(await runAudit('mobile', 390, 844, true));

for (const r of results) {
  console.log(`\n=== ${r.label.toUpperCase()} ${r.width}x${r.height} ===`);
  console.log(`FCP: ${Math.round(r.fcp)} ms`);
  console.log(`LCP: ${Math.round(r.lcp)} ms`);
  console.log(`TBT stimato: ${Math.round(r.tbt)} ms`);
  console.log(`CLS: ${Number(r.cls).toFixed(3)}`);
  console.log(`Overflow orizzontale: ${r.horizontalOverflow ? 'SI' : 'NO'}`);
  console.log(`Hero presente: ${r.heroPresent ? 'SI' : 'NO'}`);
  console.log(`Visual proof presente: ${r.visualProofPresent ? 'SI' : 'NO'}`);
}

const failures = [];
for (const r of results) {
  if (r.horizontalOverflow) failures.push(`${r.label}: overflow orizzontale`);
  if (!r.heroPresent) failures.push(`${r.label}: hero mancante`);
  if (!r.visualProofPresent) failures.push(`${r.label}: visual proof mancante`);
  if (r.cls > 0.10) failures.push(`${r.label}: CLS ${r.cls.toFixed(3)} > 0.10`);
}
if (failures.length) {
  console.error('\nSTOP performance gate:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}
console.log('\nOK performance gate strutturale: nessun overflow, hero/prova presenti, CLS <= 0.10.');
console.log('Nota: FCP/LCP/TBT sono misure locali diagnostiche; non sostituiscono PageSpeed Insights sul sito live.');
