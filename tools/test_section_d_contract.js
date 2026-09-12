'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.join(__dirname,'..');
const read=name=>fs.readFileSync(path.join(root,name),'utf8');

const nav=read('navigation-conversion.js');
for(const token of ['Problemi da evitare','Casi reali','Guide','Come funziona','Servizi e prezzi','Chi sono','aria-expanded','aria-controls','utm_source','role_hint','service_hint','source_page','content_type','cta_position']) assert.ok(nav.includes(token),token);

assert.ok(
  nav.includes("nav.dataset.s90gNavManaged==='page'"),
  'navigation runtime must preserve page-managed navigation'
);

for(const obsoleteNav of ['Professionisti','Rivenditori','/professionisti.html','/rivenditori-cucine.html']){
  assert.equal(nav.includes(obsoleteNav),false,`navigation contiene target B2B pubblico ${obsoleteNav}`);
}
assert.ok(nav.includes('/analisi-preventiva.html#richiedi'),'navigazione deve usare #richiedi');
assert.ok(nav.includes('Mostra il tuo caso'),'normalizzazione CTA customer-first');
for(const obsolete of ['controllo-mirato','analisi-completa','acquisto-assistito-cucina-90g','verifica-progetto-cucina',"'restyling-cucina-esistente':'79'",'SERVICE_PRICES']){
  assert.equal(nav.includes(obsolete),false,`navigation contiene residuo ${obsolete}`);
}
for(const obsolete of ['scelta-finiture-casa','studio-preliminare-spazi','analisi-unita-varianti','verifica-planimetria-distribuzione-casa']) assert.equal(nav.includes(obsolete),false,`navigation contiene residuo ${obsolete}`);

const htmlFiles=[];
const walk=dir=>{for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
  if(entry.name==='.git'||entry.name.startsWith('._')||entry.name==='dist')continue;
  const full=path.join(dir,entry.name);
  if(entry.isDirectory())walk(full);else if(entry.name.endsWith('.html'))htmlFiles.push(full);
}};
walk(root);
let visual=0,privacy=0;
for(const file of htmlFiles){
  const raw=fs.readFileSync(file,'utf8');
  if(raw.includes('sistema90g-visual-2026.css')){visual++;assert.ok(raw.includes('sistema90g-visual-2026.css?v=20260730a')||raw.includes('sistema90g-visual-2026.css?v=20260817b'),file);}
  if(raw.includes('privacy-consent.js')){
  privacy++;
  assert.ok(
    raw.includes('privacy-consent.js?v=20260730a') ||
    raw.includes('privacy-consent.js?v=20260912a'),
    file
  );
}
}
assert.ok(visual>=50);
assert.ok(privacy>=50);

const intake=read('analisi-preventiva.html');
const services=read('servizi.html');
assert.ok(intake.includes('id="richiedi"'),'Free Entry #richiedi');
assert.ok(intake.includes('service=valutazione-iniziale'),'valutazione iniziale');
assert.ok(intake.includes('requester_role=private'),'Free Entry pubblico per privati');
for(const forbiddenRole of [
  'requester_role=interior',
  'requester_role=technician',
  'requester_role=company',
  'requester_role=agency',
  'requester_role=other',
  'requester_role=retailer'
]){
  assert.equal(intake.includes(forbiddenRole),false,`Free Entry pubblico contiene ruolo B2B ${forbiddenRole}`);
}
for(const forbiddenLabel of [
  'Interior designer',
  'Architetto o geometra',
  'Agenzia immobiliare',
  'Altro professionista',
  'Rivenditore cucine',
  'Per professionisti e rivenditori'
]){
  assert.equal(intake.includes(forbiddenLabel),false,`Free Entry pubblico contiene target B2B ${forbiddenLabel}`);
}
assert.equal(intake.includes('service_price='),false,'Free Entry senza prezzi nel portale');
assert.equal(intake.includes('#percorso'),false,'Free Entry non deve usare anchor legacy');
for(const principle of [
  'Mostraci cosa non ti convince.',
  'Non devi scegliere un servizio',
  'Prima capiamo cosa sta succedendo.',
  'Se non serve altro, te lo diciamo.',
  'Cosa non ti convince della tua cucina?'
]) assert.ok(intake.includes(principle),`principio Free Entry assente: ${principle}`);
const canonicalServiceRoutes = [
  {
    id: "scelta",
    name: "Consulenza 90G",
    price: "79 €",
  },
  {
    id: "preventivo",
    name: "Analisi Preventivo &amp; Ordine 90G",
    price: "129 €",
  },
  {
    id: "verifica",
    name: "Verifica Cucina 90G",
    price: "149 €",
  },
  {
    id: "progetto",
    name: "Progetto Cucina 90G",
    price: "299 €",
  },
  {
    id: "premontaggio",
    name: "Controllo Pre-Montaggio 90G",
    price: "179 €",
  },
  {
    id: "problema",
    name: "Analisi Problema 90G",
    price: "149 €",
  },
];

for (const { id, name, price } of canonicalServiceRoutes) {
  const articlePattern = new RegExp(
    `<article[\\s\\S]*?id="${id}"[\\s\\S]*?` +
      name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") +
      `[\\s\\S]*?` +
      price.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") +
      `[\\s\\S]*?</article>`
  );

  assert.ok(
    articlePattern.test(services),
    `serviceso/prezzo canonico assente dalla situazione ${id}: ${name} / ${price}`
  );
}

/*
 * Project & Preventivo is intentionally an extension,
 * not a seventh primary situation.
 */
assert.ok(
  /Progetto &amp; Preventivo 90G[\s\S]{0,1800}349 €/.test(services),
  "estensione Progetto & Preventivo 90G / 349 € assente"
);

assert.ok(
  /Render fotorealistico aggiuntivo[\s\S]{0,1000}39 €/.test(services),
  "render aggiuntivo / 39 € assente"
);

assert.equal(intake.includes('role-case-path.js'),false,'la pagina Free Entry non deve dipendere dal catalogo legacy');
assert.equal(intake.includes('role-case-path.css'),false,'la pagina Free Entry non deve dipendere dallo stile legacy');

const home=read('index.html');

assert.ok(
  home.includes('data-s90g-nav-managed="page"'),
  'homepage must own its acquisition navigation'
);

const homeNavMatch=home.match(
  /<nav\b[^>]*class=["'][^"']*\bs90g-nav\b[^"']*["'][^>]*>([\s\S]*?)<\/nav>/i
);

assert.ok(
  homeNavMatch,
  'homepage acquisition navigation must be parseable'
);

const homeNav=homeNavMatch[1];

for(const legacyHomeNav of [
  '>Metodo e AI<',
  '>Innovazioni<',
  '>Contatti<'
]){
  assert.equal(
    homeNav.includes(legacyHomeNav),
    false,
    `homepage acquisition nav contains ${legacyHomeNav}`
  );
}

const consent=read('privacy-consent.js');
assert.ok(consent.includes('/navigation-conversion.js?v=20260912a'));

assert.ok(
  consent.includes('function s90gIntegrateMethodFooterLink()'),
  'shared runtime must expose Method footer integration'
);

assert.equal(
  consent.includes('s90gIntegrateAiTransparencyPage'),
  false,
  'retired AI transparency integration must stay removed'
);

assert.equal(
  consent.includes("link.textContent='Metodo e AI';"),
  false,
  'retired Metodo e AI runtime label must stay removed'
);

assert.ok(
  consent.includes("link.textContent='Metodo';"),
  'shared Method footer label must remain canonical'
);
assert.ok(consent.includes('analisi-preventiva.html#richiedi'),'privacy-consent deve usare il Free Entry #richiedi');
assert.equal(consent.includes('#percorso'),false,'privacy-consent non deve usare anchor legacy #percorso');
for(const obsolete of ['controllo-mirato','analisi-completa','acquisto-assistito-cucina-90g','verifica-progetto-cucina']){
  assert.equal(consent.includes(obsolete),false,`privacy-consent contiene residuo servizio legacy ${obsolete}`);
}
assert.equal(consent.includes('progetti casa'),false,'dati strutturati non devono descrivere il vecchio perimetro casa');
assert.equal(consent.includes('scelta-finiture-casa'),false,'privacy-consent non deve contenere il vecchio servizio finiture casa');
console.log('SECTION D FREE ENTRY CONTRACT TEST: PASS');
