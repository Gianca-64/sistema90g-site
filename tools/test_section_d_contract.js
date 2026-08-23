'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.join(__dirname,'..');
const read=name=>fs.readFileSync(path.join(root,name),'utf8');

const nav=read('navigation-conversion.js');
for(const token of ['Rivenditori','Metodo 90G','Innovazioni','Contatti','aria-expanded','aria-controls','utm_source','role_hint','service_hint','source_page','content_type','cta_position']) assert.ok(nav.includes(token),token);
assert.ok(nav.includes('/analisi-preventiva.html#richiedi'),'navigazione deve usare #richiedi');
assert.ok(nav.includes('Chiedi la valutazione gratuita'),'normalizzazione CTA Free Entry');
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
  if(raw.includes('privacy-consent.js')){privacy++;assert.ok(raw.includes('privacy-consent.js?v=20260730a'),file);}
}
assert.ok(visual>=50);
assert.ok(privacy>=50);

const intake=read('analisi-preventiva.html');
assert.ok(intake.includes('id="richiedi"'),'Free Entry #richiedi');
assert.ok(intake.includes('service=valutazione-iniziale'),'valutazione iniziale');
assert.ok(intake.includes('Consulenza 90G · 97 €'),'Consulenza 90G');
assert.ok(intake.includes('Verifica 90G · 127 €'),'Verifica 90G');
assert.ok(intake.includes('Progetto Cucina 90G · 145 €'),'Progetto Cucina 90G');
assert.equal(intake.includes('role-case-path.js'),false,'la pagina Free Entry non deve dipendere dal catalogo legacy');
assert.equal(intake.includes('role-case-path.css'),false,'la pagina Free Entry non deve dipendere dallo stile legacy');

const consent=read('privacy-consent.js');
assert.ok(consent.includes('/navigation-conversion.js?v=20260815a'));
assert.equal(consent.includes('progetti casa'),false,'dati strutturati non devono descrivere il vecchio perimetro casa');
assert.equal(consent.includes('scelta-finiture-casa'),false,'privacy-consent non deve contenere il vecchio servizio finiture casa');
console.log('SECTION D FREE ENTRY CONTRACT TEST: PASS');
