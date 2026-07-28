'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
global.window={addEventListener(){}};
global.document={addEventListener(){}};
require('../role-case-path.js');
const {catalog,calculatePrice}=window.S90G_PATH;
const expected=[
 ['private','scelta-finiture-cucina',47],
 ['private','restyling-cucina-esistente',79],
 ['private','controllo-mirato',127],
 ['private','analisi-completa',253],
 ['private','acquisto-assistito-cucina',290],
 ['private','studio-preliminare-spazi',560],
 ['professional','verifica-preliminare-immobile',149],
 ['retailer','verifica-progetto-cucina',150]
];
for(const [group,id,price] of expected){
 const item=catalog[group].find(x=>x.id===id);
 assert.ok(item,id);
 assert.equal(calculatePrice(item).price,price,id);
 assert.ok(item.checks.length>=2,`${id}: checks`);
 assert.ok(item.deliverables.length>=2,`${id}: deliverables`);
 assert.ok(item.limits.length>=2,`${id}: limits`);
}
const multi=catalog.professional.find(x=>x.id==='analisi-unita-varianti');
assert.equal(calculatePrice(multi,4).price,440);
assert.equal(calculatePrice(multi,1).unitCount,3);
const guided=fs.readFileSync(path.join(__dirname,'..','role-case-path.js'),'utf8');
for(const token of ['requester_role','case_context','service','service_title','service_price','service_currency','service_time','source_page','content_type','cta_position','units','utm_source','pushState','popstate','initialPathIntent','restore({scroll:initialPathIntent})','else if(step===3)step=2','else if(step>1)step=1']) assert.ok(guided.includes(token),token);
const nav=fs.readFileSync(path.join(__dirname,'..','navigation-conversion.js'),'utf8');
for(const token of ['Rivenditori','Metodo 90G','Contatti','aria-expanded','aria-controls','utm_source','role_hint','service_hint']) assert.ok(nav.includes(token),token);
const htmlFiles=[];const walk=dir=>{for(const entry of fs.readdirSync(dir,{withFileTypes:true})){if(entry.name==='.git'||entry.name.startsWith('._'))continue;const full=path.join(dir,entry.name);if(entry.isDirectory())walk(full);else if(entry.name.endsWith('.html'))htmlFiles.push(full)}};walk(path.join(__dirname,'..'));let visual=0,privacy=0;for(const file of htmlFiles){const raw=fs.readFileSync(file,'utf8');if(raw.includes('sistema90g-visual-2026.css')){visual++;assert.ok(raw.includes('sistema90g-visual-2026.css?v=20260728e'),file)}if(raw.includes('privacy-consent.js')){privacy++;assert.ok(raw.includes('privacy-consent.js?v=20260728e'),file)}}assert.ok(visual>=50);assert.ok(privacy>=50);const pathPage=fs.readFileSync(path.join(__dirname,'..','analisi-preventiva.html'),'utf8');assert.ok(pathPage.includes('role-case-path.css?v=20260728e'));assert.ok(pathPage.includes('role-case-path.js?v=20260728e'));const consent=fs.readFileSync(path.join(__dirname,'..','privacy-consent.js'),'utf8');assert.ok(consent.includes('/navigation-conversion.js?v=20260728e'));console.log('SECTION D CONTRACT TEST: PASS');
