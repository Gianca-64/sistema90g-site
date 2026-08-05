import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs/promises';
import path from 'node:path';

const baseURL = process.env.S90G_TEST_BASE_URL || 'http://127.0.0.1:4173';
const outputDir = process.env.S90G_TEST_OUTPUT || 'artifacts/kitchen-focus';

const pages = [
  '/',
  '/servizi.html',
  '/controllo-mirato.html',
  '/analisi-completa.html',
  '/acquisto-assistito-cucina.html',
  '/analisi-preventivo-cucina.html',
  '/problemi-errori-cucina.html',
  '/casi-cucina.html',
  '/analisi-preventiva.html'
];

const viewports = {
  desktop: { width: 1440, height: 1000 },
  mobile: { width: 390, height: 844 }
};

const services = [
  { slug: 'controllo-mirato', code: 'S90G-K01', price: '127' },
  { slug: 'analisi-completa', code: 'S90G-K02', price: '253' },
  { slug: 'acquisto-assistito-cucina', code: 'S90G-K03', price: '290' }
];

const failures = [];
const observations = [];

function fail(scope, message) {
  failures.push(`${scope}: ${message}`);
}

function note(scope, message) {
  observations.push(`${scope}: ${message}`);
}

await fs.mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });

try {
  for (const [viewportName, viewport] of Object.entries(viewports)) {
    const context = await browser.newContext({ viewport, locale: 'it-IT' });

    for (const pagePath of pages) {
      const page = await context.newPage();
      const scope = `${viewportName} ${pagePath}`;
      const consoleErrors = [];
      const pageErrors = [];

      page.on('console', message => {
        if (message.type() === 'error') consoleErrors.push(message.text());
      });
      page.on('pageerror', error => pageErrors.push(error.message));

      const response = await page.goto(`${baseURL}${pagePath}`, {
        waitUntil: 'networkidle',
        timeout: 30_000
      });

      if (!response || !response.ok()) {
        fail(scope, `risposta HTTP non valida: ${response?.status() ?? 'nessuna risposta'}`);
        await page.close();
        continue;
      }

      const title = await page.title();
      if (!title.trim()) fail(scope, 'title assente');

      const h1Count = await page.locator('h1').count();
      if (h1Count !== 1) fail(scope, `H1 attesi 1, trovati ${h1Count}`);
      if (h1Count === 1 && !(await page.locator('h1').isVisible())) fail(scope, 'H1 non visibile');

      const canonical = await page.locator('link[rel="canonical"]').getAttribute('href');
      if (!canonical?.startsWith('https://sistema90g.it/')) fail(scope, 'canonical assente o non valido');

      const overflow = await page.evaluate(() => ({
        documentWidth: document.documentElement.scrollWidth,
        viewportWidth: document.documentElement.clientWidth
      }));
      if (overflow.documentWidth > overflow.viewportWidth + 2) {
        fail(scope, `overflow orizzontale ${overflow.documentWidth - overflow.viewportWidth}px`);
      }

      const brokenImages = await page.locator('img').evaluateAll(images => images
        .filter(image => !image.complete || image.naturalWidth === 0)
        .map(image => image.getAttribute('src') || '(src assente)'));
      if (brokenImages.length) fail(scope, `immagini non caricate: ${brokenImages.join(', ')}`);

      const emptyLinks = await page.locator('a').evaluateAll(links => links
        .filter(link => {
          const href = (link.getAttribute('href') || '').trim();
          return !href || href === '#';
        })
        .filter(link => !link.hasAttribute('data-cookie-settings'))
        .map(link => (link.textContent || '').trim() || '(link senza testo)'));
      if (emptyLinks.length) fail(scope, `link vuoti o segnaposto: ${emptyLinks.join(', ')}`);

      if (consoleErrors.length) fail(scope, `errori console: ${consoleErrors.join(' | ')}`);
      if (pageErrors.length) fail(scope, `errori pagina: ${pageErrors.join(' | ')}`);

      const accessibility = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze();
      const severe = accessibility.violations.filter(item => ['serious', 'critical'].includes(item.impact));
      if (severe.length) {
        fail(scope, `violazioni accessibilità gravi: ${severe.map(item => `${item.id} (${item.nodes.length})`).join(', ')}`);
      }
      if (accessibility.violations.length) {
        note(scope, `violazioni axe complessive: ${accessibility.violations.map(item => `${item.id}:${item.impact || 'n/a'}:${item.nodes.length}`).join(', ')}`);
      }

      const safeName = pagePath === '/' ? 'home' : pagePath.replace(/^\//, '').replace(/\.html$/, '');
      await page.screenshot({
        path: path.join(outputDir, `${viewportName}-${safeName}.png`),
        fullPage: true
      });

      await page.close();
    }

    await context.close();
  }

  const context = await browser.newContext({ viewport: viewports.desktop, locale: 'it-IT' });
  const page = await context.newPage();

  for (const service of services) {
    const scope = `percorso ${service.slug}`;
    await page.goto(`${baseURL}/analisi-preventiva.html?service_hint=${service.slug}#percorso`, {
      waitUntil: 'networkidle',
      timeout: 30_000
    });

    const input = page.locator(`input[name="kitchen_situation"][value="${service.slug}"]`);
    if (!(await input.isChecked())) fail(scope, 'selezione iniziale non ripristinata');

    const result = page.locator('#s90g-path-result');
    if (await result.isHidden()) fail(scope, 'risultato nascosto');

    const code = (await page.locator('#s90g-result-code').textContent())?.trim();
    if (code !== service.code) fail(scope, `codice ricevuto ${code}, atteso ${service.code}`);

    const priceText = (await page.locator('#s90g-result-price').textContent()) || '';
    if (!priceText.includes(service.price)) fail(scope, `prezzo ricevuto ${priceText}, atteso ${service.price}`);

    const href = await page.locator('#s90g-result-cta').getAttribute('href');
    if (!href) {
      fail(scope, 'CTA senza href');
      continue;
    }

    const target = new URL(href, baseURL);
    if (target.hostname !== 'portale.sistema90g.it') fail(scope, `host portale inatteso: ${target.hostname}`);
    if (target.searchParams.get('service') !== service.code) fail(scope, 'parametro service non coerente');
    if (target.searchParams.get('service_slug') !== service.slug) fail(scope, 'parametro service_slug non coerente');
    if (target.searchParams.get('service_price') !== service.price) fail(scope, 'parametro service_price non coerente');
    if (target.searchParams.get('service_currency') !== 'EUR') fail(scope, 'valuta non coerente');
    if (target.searchParams.get('source_page') !== 'analisi-preventiva') fail(scope, 'source_page non coerente');
  }

  await context.close();
} finally {
  await browser.close();
}

const report = {
  generatedAt: new Date().toISOString(),
  baseURL,
  pages,
  viewports,
  failures,
  observations
};

await fs.writeFile(path.join(outputDir, 'report.json'), JSON.stringify(report, null, 2));

if (observations.length) {
  console.log('\nOsservazioni:');
  observations.forEach(item => console.log(`- ${item}`));
}

if (failures.length) {
  console.error('\nAudit browser NON superato:');
  failures.forEach(item => console.error(`- ${item}`));
  process.exit(1);
}

console.log(`Audit browser superato: ${pages.length} pagine, ${Object.keys(viewports).length} viewport, ${services.length} percorsi servizio.`);
