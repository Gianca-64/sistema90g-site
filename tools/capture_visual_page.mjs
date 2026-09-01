#!/usr/bin/env node
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import process from 'node:process';

const chrome = process.argv[2];
const outDir = process.argv[3];
const baseUrl = (process.argv[4] || 'http://127.0.0.1:4178').replace(/\/$/, '');
const rel = process.argv[5] || 'chi-e-sistema90g.html';
const key = process.argv[6] || 'page';

if (!chrome || !outDir) {
  console.error('Uso: node tools/capture_visual_page.mjs <chrome> <out-dir> [base-url] [pagina] [chiave]');
  process.exit(2);
}

mkdirSync(outDir, { recursive: true });
const viewports = [['desktop', 1440, 1100, false], ['mobile', 390, 844, true]];
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function waitForPort(profile, timeout = 10000) {
  const file = join(profile, 'DevToolsActivePort');
  const started = Date.now();
  while (Date.now() - started < timeout) {
    try {
      const port = Number(readFileSync(file, 'utf8').trim().split(/\r?\n/)[0]);
      if (Number.isInteger(port) && port > 0) return port;
    } catch {}
    await sleep(100);
  }
  throw new Error('Chrome non ha esposto DevToolsActivePort entro 10 secondi');
}

async function connect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let nextId = 1;
  const pending = new Map();
  const listeners = new Map();

  await new Promise((resolve, reject) => {
    const t = setTimeout(() => reject(new Error('Timeout WebSocket DevTools')), 5000);
    ws.addEventListener('open', () => { clearTimeout(t); resolve(); }, { once: true });
    ws.addEventListener('error', () => { clearTimeout(t); reject(new Error('Errore WebSocket DevTools')); }, { once: true });
  });

  ws.addEventListener('message', e => {
    const m = JSON.parse(e.data.toString());
    if (m.id && pending.has(m.id)) {
      const p = pending.get(m.id);
      pending.delete(m.id);
      m.error ? p.reject(new Error(m.error.message || 'Errore CDP')) : p.resolve(m.result || {});
      return;
    }
    if (m.method && listeners.has(m.method)) {
      for (const fn of [...listeners.get(m.method)]) fn(m.params || {});
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
    }, 10000);
  });

  const once = (method, timeout = 15000) => new Promise((resolve, reject) => {
    const set = listeners.get(method) || new Set();
    listeners.set(method, set);
    const timer = setTimeout(() => {
      set.delete(handler);
      reject(new Error(`Timeout evento CDP: ${method}`));
    }, timeout);
    const handler = params => {
      clearTimeout(timer);
      set.delete(handler);
      resolve(params);
    };
    set.add(handler);
  });

  return { ws, send, once };
}

async function capture(suffix, width, height, mobile) {
  const url = `${baseUrl}/${rel}`;
  const profile = mkdtempSync(join(tmpdir(), `s90g-visual-${key}-${suffix}-`));
  let proc;

  try {
    proc = spawn(chrome, [
      '--headless=new', '--disable-gpu', '--hide-scrollbars', '--disable-extensions',
      '--disable-background-networking', '--disable-component-update', '--disable-sync',
      '--metrics-recording-only', '--no-first-run', '--no-default-browser-check',
      `--user-data-dir=${profile}`, '--remote-debugging-port=0', 'about:blank'
    ], { detached: true, stdio: ['ignore', 'pipe', 'pipe'] });

    const port = await waitForPort(profile);
    const targets = await fetch(`http://127.0.0.1:${port}/json/list`).then(r => r.json());
    const target = targets.find(t => t.type === 'page');
    if (!target?.webSocketDebuggerUrl) throw new Error('Target pagina DevTools non trovato');

    const cdp = await connect(target.webSocketDebuggerUrl);
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width, height, deviceScaleFactor: 1, mobile,
      screenWidth: width, screenHeight: height,
      positionX: 0, positionY: 0, dontSetVisibleSize: false
    });
    if (mobile) await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });

    const loaded = cdp.once('Page.loadEventFired');
    await cdp.send('Page.navigate', { url });
    await loaded;
    await sleep(1400);

    const stateResult = await cdp.send('Runtime.evaluate', {
      expression: `(() => {
        const root = document.documentElement;
        const imgs = [...document.images].map(img => ({src: img.currentSrc || img.src, complete: img.complete, naturalWidth: img.naturalWidth}));
        return JSON.stringify({
          title: document.title,
          innerWidth, innerHeight,
          clientWidth: root.clientWidth,
          scrollWidth: root.scrollWidth,
          scrollHeight: root.scrollHeight,
          bodyClass: document.body.className,
          h1: document.querySelector('h1')?.textContent.trim() || '',
          brokenImages: imgs.filter(i => !i.complete || i.naturalWidth === 0)
        });
      })()`,
      returnByValue: true
    });

    const state = JSON.parse(stateResult.result?.value || '{}');
    if (state.innerWidth !== width || state.innerHeight !== height) throw new Error(`${key}/${suffix}: viewport reale ${state.innerWidth}x${state.innerHeight}, atteso ${width}x${height}`);
    if (!state.h1) throw new Error(`${key}/${suffix}: H1 mancante`);
    if (state.brokenImages?.length) throw new Error(`${key}/${suffix}: immagini non caricate: ${state.brokenImages.map(i => i.src).join(', ')}`);
    if (Number(state.scrollWidth) > Number(state.clientWidth) + 1) throw new Error(`${key}/${suffix}: overflow orizzontale ${state.scrollWidth}px > ${state.clientWidth}px`);

    const full = await cdp.send('Page.captureScreenshot', {
      format: 'png', fromSurface: true, captureBeyondViewport: true,
      clip: { x: 0, y: 0, width: state.clientWidth, height: Math.min(state.scrollHeight, 12000), scale: 1 }
    });
    writeFileSync(join(outDir, `${key}-full-${suffix}.png`), Buffer.from(full.data, 'base64'));

    cdp.ws.close();
    console.log(`OK ${key} ${suffix}: ${width}x${height}, no overflow, immagini OK`);
    return { key, rel, suffix, width, height, mobile, url, ...state, horizontalOverflow: false };
  } finally {
    if (proc?.pid) { try { process.kill(-proc.pid, 'SIGKILL'); } catch {} }
    rmSync(profile, { recursive: true, force: true });
  }
}

const results = [];
for (const viewport of viewports) results.push(await capture(...viewport));
writeFileSync(join(outDir, 'metrics.json'), JSON.stringify(results, null, 2) + '\n');
console.log(`OK cattura visuale: ${rel} desktop/mobile.`);
