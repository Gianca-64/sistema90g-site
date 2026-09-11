'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.join(__dirname,'..');
const read=name=>fs.readFileSync(path.join(root,name),'utf8');

const services=read('servizi.html');
const intake=read('analisi-preventiva.html');
const project=read('progetto-cucina-sistema90g.html');
const verify=read('verifica-90g.html');

for(const token of [
  'Consulenza 90G · 79 €',
  'Analisi Preventivo &amp; Ordine 90G · 129 €',
  'Verifica Cucina 90G · 149 €',
  'Progetto Cucina 90G · 299 €',
  'Controllo Pre-Montaggio 90G · 179 €',
  'Analisi Problema 90G · 149 €',
  'Progetto &amp; Preventivo 90G · 349 €',
  'Render fotorealistico aggiuntivo · 39 € / vista'
]){
  assert.ok(services.includes(token),`offerta canonica assente: ${token}`);
}
assert.ok(project.includes('Progetto Cucina 90G · 299 €'),'prezzo progetto');
assert.ok(verify.includes('Verifica Cucina 90G · 149 €'),'prezzo verifica');

assert.ok(intake.includes('id="richiedi"'),'sezione Free Entry #richiedi');
assert.ok(intake.includes('service=valutazione-iniziale'),'servizio valutazione iniziale');
assert.ok(intake.includes('Non avvia alcun acquisto'),'nessun acquisto automatico');
assert.equal(intake.includes('service_price='),false,'la pagina Free Entry non deve trasmettere prezzi');
const portalLinks=[...intake.matchAll(/https:\/\/portale\.sistema90g\.it\/portal\.html\?[^\"']+/g)].map(m=>m[0]);
assert.equal(portalLinks.length,1,'il Free Entry pubblico deve avere un solo ingresso al Portale');
for(const href of portalLinks){
  assert.ok(href.includes('requester_role=private'),`il Free Entry pubblico deve essere solo per privati: ${href}`);
  assert.ok(href.includes('service=valutazione-iniziale'),`link portale non Free Entry: ${href}`);
  assert.equal(href.includes('service_price='),false,`la valutazione gratuita non deve avere prezzo: ${href}`);
}

for(const obsolete of ['Restyling cucina esistente · 79 €','Seconda Opinione · controllo completo','Acquisto Assistito · 290 €','Analisi progetto cucina · 150 €']){
  assert.equal(services.includes(obsolete),false,`servizi contiene residuo: ${obsolete}`);
  assert.equal(intake.includes(obsolete),false,`analisi-preventiva contiene residuo: ${obsolete}`);
}

console.log('FREE ENTRY OFFER CONTRACT TEST: PASS');
