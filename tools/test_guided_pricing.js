'use strict';
const assert = require('node:assert/strict');
global.window = {};
global.document = { readyState:'loading', addEventListener() {}, getElementById(){ return null; }, querySelectorAll(){ return []; } };
require('../role-case-path.js');
const { catalog, calculatePrice } = window.S90G_PATH;
const get = (group, id) => catalog[group].find(item => item.id === id);
const expected = [
  ['private','scelta-finiture-cucina',47],
  ['private','restyling-cucina-esistente',79],
  ['private','controllo-mirato',127],
  ['private','analisi-completa',253],
  ['private','acquisto-assistito-cucina',290],
  ['professional','controllo-mirato',127],
  ['professional','analisi-completa',253],
  ['retailer','verifica-progetto-cucina',150]
];
for (const [group,id,price] of expected) {
  const item=get(group,id);
  assert.ok(item, `${group}/${id} deve esistere`);
  assert.equal(calculatePrice(item).price, price, id);
}
for (const obsolete of ['studio-preliminare-spazi','verifica-preliminare-immobile','analisi-unita-varianti']) {
  assert.equal(Object.values(catalog).flat().some(item => item.id === obsolete), false, `${obsolete} non deve essere nel catalogo cucina corrente`);
}
console.log('GUIDED PRICING TEST: PASS');

const source=require('node:fs').readFileSync(require('node:path').join(__dirname,'..','role-case-path.js'),'utf8');
for (const token of ['requester_role','case_context','service_price','service_time','service_currency']) assert.ok(source.includes(token), token);
console.log('GUIDED PORTAL CONTRACT TEST: PASS');
