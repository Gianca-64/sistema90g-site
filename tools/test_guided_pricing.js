'use strict';
const assert = require('node:assert/strict');
global.window = {};
global.document = { addEventListener() {} };
require('../role-case-path.js');
const { catalog, calculatePrice } = window.S90G_PATH;
const get = (group, id) => catalog[group].find(item => item.id === id);
const expected = [
  ['private','scelta-finiture-cucina',47],
  ['private','restyling-cucina-esistente',79],
  ['private','controllo-mirato',127],
  ['private','analisi-completa',253],
  ['private','acquisto-assistito-cucina',290],
  ['private','studio-preliminare-spazi',560],
  ['professional','verifica-preliminare-immobile',149],
  ['retailer','verifica-progetto-cucina',150]
];
for (const [group,id,price] of expected) assert.equal(calculatePrice(get(group,id)).price, price, id);
const multi=get('professional','analisi-unita-varianti');
assert.deepEqual({price:calculatePrice(multi,4).price,units:calculatePrice(multi,4).unitCount},{price:440,units:4});
assert.deepEqual({price:calculatePrice(multi,1).price,units:calculatePrice(multi,1).unitCount},{price:330,units:3});
console.log('GUIDED PRICING TEST: PASS');

const source=require('node:fs').readFileSync(require('node:path').join(__dirname,'..','role-case-path.js'),'utf8');
for (const token of ['requester_role','case_context','service_price','service_time','service_currency']) assert.ok(source.includes(token), token);
console.log('GUIDED PORTAL CONTRACT TEST: PASS');
