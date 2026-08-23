'use strict';
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.join(__dirname,'..');
const read=name=>fs.readFileSync(path.join(root,name),'utf8');

const services=read('servizi.html');
const intake=read('analisi-preventiva.html');
const project=read('progetto-cucina-sistema90g.html');
const verify=read('seconda-opinione-cucina.html');

for(const token of ['Consulenza 90G · 97 €','Verifica 90G · 127 €','Progetto Cucina 90G · 145 €','Add-on progettuali · 117 € ciascuno','Render fotorealistici · 57 € / vista']){
  assert.ok(services.includes(token),`offerta canonica assente: ${token}`);
}
assert.ok(project.includes('Progetto Cucina 90G · 145 €'),'prezzo progetto');
assert.ok(verify.includes('Verifica 90G · 127 €'),'prezzo verifica');

assert.ok(intake.includes('id="richiedi"'),'sezione Free Entry #richiedi');
assert.ok(intake.includes('service=valutazione-iniziale'),'servizio valutazione iniziale');
assert.ok(intake.includes("L'invio non avvia alcun servizio a pagamento"),'nessun acquisto automatico');
const portalLinks=[...intake.matchAll(/https:\/\/portale\.sistema90g\.it\/portal\.html\?[^\"']+/g)].map(m=>m[0]);
assert.ok(portalLinks.length>=7,'CTA gratuite per i ruoli');
for(const href of portalLinks){
  assert.ok(href.includes('service=valutazione-iniziale'),`link portale non Free Entry: ${href}`);
  assert.equal(href.includes('service_price='),false,`la valutazione gratuita non deve avere prezzo: ${href}`);
}

for(const obsolete of ['Restyling cucina esistente · 79 €','Seconda Opinione · controllo completo','Acquisto Assistito · 290 €','Analisi progetto cucina · 150 €']){
  assert.equal(services.includes(obsolete),false,`servizi contiene residuo: ${obsolete}`);
  assert.equal(intake.includes(obsolete),false,`analisi-preventiva contiene residuo: ${obsolete}`);
}

console.log('FREE ENTRY OFFER CONTRACT TEST: PASS');
