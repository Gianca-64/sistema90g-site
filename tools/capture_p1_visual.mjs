#!/usr/bin/env node
import { spawn } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import process from 'node:process';

const chrome = process.argv[2];
const outDir = process.argv[3];
if (!chrome || !outDir) {
  console.error('Uso: node tools/capture_p1_visual.mjs <chrome> <output-dir>');
  process.exit(2);
}

const pages = [
  ['home', 'https://sistema90g.it/'],
  ['free-entry', 'https://sistema90g.it/analisi-preventiva.html'],
  ['servizi', 'https://sistema90g.it/servizi.html'],
  ['approfondimento', 'https://sistema90g.it/approfondimenti/colonna-lavanderia-a-piena-capacita-con-comandi-ad-altezza-accessibile-1ff0f9c.html'],
];

const viewports = [
  ['desktop', 1440, 1100, false],
  ['mobile', 390, 844, true],
];

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
    }, 10000);
  });

  const once = (method, timeoutMs = 15000) => new Promise((resolve, reject) => {
    const set = listeners.get(method) || new Set();
    listeners.set(method, set);
    const timer = setTimeout(() => {
      set.delete(handler);
      reject(new Error(`Timeout evento CDP: ${method}`));
    }, timeoutMs);
    const handler = params => {
      clearTimeout(timer);
      set.delete(handler);
      resolve(params);
    };
    set.add(handler);
  });

  return { ws, send, once };
}

async function capture(name, url, suffix, width, height, mobile) {
  const profile = mkdtempSync(join(tmpdir(), `s90g-p1-${suffix}-${name}-`));
  const screenshotPath = join(outDir, `${name}-${suffix}.png`);
  let chromeProc;
  try {
    console.log(`Cattura ${name}-${suffix} (${width}x${height}${mobile ? ', emulazione mobile' : ''})...`);
    chromeProc = spawn(chrome, [
      '--headless=new',
      '--disable-gpu',
      '--hide-scrollbars',
      '--disable-extensions',
      '--disable-background-networking',
      '--disable-component-update',
      '--disable-sync',
      '--metrics-recording-only',
      '--no-first-run',
      '--no-default-browser-check',
      `--user-data-dir=${profile}`,
      '--remote-debugging-port=0',
      'about:blank',
    ], { detached: true, stdio: ['ignore', 'pipe', 'pipe'] });

    const port = await waitForDevToolsPort(profile);
    const targets = await fetch(`http://127.0.0.1:${port}/json/list`).then(r => r.json());
    const pageTarget = targets.find(target => target.type === 'page');
    if (!pageTarget?.webSocketDebuggerUrl) throw new Error('Target pagina DevTools non trovato');

    const cdp = await connectCdp(pageTarget.webSocketDebuggerUrl);
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width,
      height,
      deviceScaleFactor: 1,
      mobile,
      screenWidth: width,
      screenHeight: height,
      positionX: 0,
      positionY: 0,
      dontSetVisibleSize: false,
    });
    if (mobile) {
      await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
    }

    const loaded = cdp.once('Page.loadEventFired');
    await cdp.send('Page.navigate', { url });
    await loaded;
    await sleep(1800);

    const metricsResult = await cdp.send('Runtime.evaluate', {
      expression: `JSON.stringify({innerWidth:window.innerWidth,innerHeight:window.innerHeight,devicePixelRatio:window.devicePixelRatio,clientWidth:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,bodyScrollWidth:document.body ? document.body.scrollWidth : 0})`,
      returnByValue: true,
    });
    const metrics = JSON.parse(metricsResult.result?.value || '{}');
    if (metrics.innerWidth !== width || metrics.innerHeight !== height) {
      throw new Error(`Viewport reale inatteso: ${metrics.innerWidth}x${metrics.innerHeight}, atteso ${width}x${height}`);
    }

    const shot = await cdp.send('Page.captureScreenshot', {
      format: 'png',
      fromSurface: true,
      captureBeyondViewport: false,
    });
    writeFileSync(screenshotPath, Buffer.from(shot.data, 'base64'));
    cdp.ws.close();

    console.log(`OK ${name}-${suffix}.png | viewport ${metrics.innerWidth}x${metrics.innerHeight} | scrollWidth ${metrics.scrollWidth}`);
    return { name, suffix, url, width, height, mobile, ...metrics, horizontalOverflow: Number(metrics.scrollWidth) > Number(metrics.clientWidth) + 1 };
  } finally {
    if (chromeProc?.pid) {
      try { process.kill(-chromeProc.pid, 'SIGKILL'); } catch {}
    }
    rmSync(profile, { recursive: true, force: true });
  }
}

const metrics = [];
for (const [name, url] of pages) {
  for (const [suffix, width, height, mobile] of viewports) {
    metrics.push(await capture(name, url, suffix, width, height, mobile));
  }
}
writeFileSync(join(outDir, 'metrics.json'), JSON.stringify(metrics, null, 2) + '\n');

const mobileOverflow = metrics.filter(item => item.mobile && item.horizontalOverflow);
if (mobileOverflow.length) {
  console.log('ATTENZIONE: overflow orizzontale reale rilevato in: ' + mobileOverflow.map(item => item.name).join(', '));
} else {
  console.log('OK viewport mobile reale: nessun overflow orizzontale rilevato nelle 4 pagine.');
}
