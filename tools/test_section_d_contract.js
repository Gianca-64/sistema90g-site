'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
global.window={addEventListener(){}};
global.document={readyState:'loading',addEventListener(){},getElementById(){return null;},querySelectorAll(){return [];}};
require('../role-case-path.js');
const {catalog,calculatePrice}=window.S90G_PATH;
const expected=[
 ['private','scelta-finiture-cucina',47],
 ['private','restyling-cucina-esistente',79],
 ['private','controllo-mirato',127],
 ['private','analisi-completa',253],
 ['private','acquisto-assistito-cucina',290],
 ['professional','controllo-mirato',127],
 ['professional','analisi-completa',253],
 ['retailer','verifica-progetto-cucina',150]
];
for(const [group,id,price] of expected){
 const item=catalog[group].find(x=>x.id===id);
 assert.ok(item,`${group}/${id}`);
 assert.equal(calculatePrice(item).price,price,id);
 assert.ok(item.checks.length>=2,`${id}: checks`);
 assert.ok(item.deliverables.length>=2,`${id}: deliverables`);
 assert.ok(item.limits.length>=2,`${id}: limits`);
}
for(const obsolete of ['studio-preliminare-spazi','verifica-preliminare-immobile','analisi-unita-varianti']){
 assert.equal(Object.values(catalog).flat().some(item=>item.id===obsolete),false,`${obsolete} non deve essere nel catalogo cucina corrente`);
}
const guided=fs.readFileSync(path.join(__dirname,'..','role-case-path.js'),'utf8');
for(const token of ['requester_role','case_context','service','service_title','service_price','service_currency','service_time']) assert.ok(guided.includes(token),token);
const nav=fs.readFileSync(path.join(__dirname,'..','navigation-conversion.js'),'utf8');
for(const token of ['Rivenditori','Metodo 90G','Innovazioni','Contatti','aria-expanded','aria-controls','utm_source','role_hint','service_hint','source_page','content_type','cta_position']) assert.ok(nav.includes(token),token);
for(const obsolete of ['scelta-finiture-casa','studio-preliminare-spazi','analisi-unita-varianti','verifica-planimetria-distribuzione-casa']) assert.equal(nav.includes(obsolete),false,`navigation contiene residuo ${obsolete}`);
const htmlFiles=[];const walk=dir=>{for(const entry of fs.readdirSync(dir,{withFileTypes:true})){if(entry.name==='.git'||entry.name.startsWith('._')||entry.name==='dist')continue;const full=path.join(dir,entry.name);if(entry.isDirectory())walk(full);else if(entry.name.endsWith('.html'))htmlFiles.push(full)}};walk(path.join(__dirname,'..'));let visual=0,privacy=0;for(const file of htmlFiles){const raw=fs.readFileSync(file,'utf8');if(raw.includes('sistema90g-visual-2026.css')){visual++;assert.ok(raw.includes('sistema90g-visual-2026.css?v=20260730a'),file)}if(raw.includes('privacy-consent.js')){privacy++;assert.ok(raw.includes('privacy-consent.js?v=20260730a'),file)}}assert.ok(visual>=50);assert.ok(privacy>=50);const pathPage=fs.readFileSync(path.join(__dirname,'..','analisi-preventiva.html'),'utf8');assert.ok(pathPage.includes('role-case-path.css?v=20260728e'));assert.ok(pathPage.includes('role-case-path.js?v=20260815a'));const consent=fs.readFileSync(path.join(__dirname,'..','privacy-consent.js'),'utf8');assert.ok(consent.includes('/navigation-conversion.js?v=20260815a'));assert.equal(consent.includes('progetti casa'),false,'dati strutturati non devono descrivere il vecchio perimetro casa');assert.equal(consent.includes('scelta-finiture-casa'),false,'privacy-consent non deve contenere il vecchio servizio finiture casa');console.log('SECTION D CONTRACT TEST: PASS');
