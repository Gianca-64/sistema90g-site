'use strict';

const assert =
  require('node:assert/strict');

const fs =
  require('node:fs');

const path =
  require('node:path');

const root =
  path.join(
    __dirname,
    '..',
  );

const read =
  name =>
    fs.readFileSync(
      path.join(
        root,
        name,
      ),
      'utf8',
    );

const normalize =
  value =>
    value
      .replace(
        /<[^>]+>/g,
        ' ',
      )
      .replace(
        /&amp;/g,
        '&',
      )
      .replace(
        /&nbsp;/g,
        ' ',
      )
      .replace(
        /&quot;/g,
        '"',
      )
      .replace(
        /&#39;|&apos;/g,
        "'",
      )
      .replace(
        /\s+/g,
        ' ',
      )
      .trim();

const extractClass =
  (
    block,
    tag,
    className,
  ) => {
    const pattern =
      new RegExp(
        `<${tag}\\b[^>]*`
        + `class="[^"]*\\b${className}\\b[^"]*"[^>]*>`
        + `([\\s\\S]*?)`
        + `<\\/${tag}>`,
        'i',
      );

    const match =
      block.match(pattern);

    assert.ok(
      match,
      `elemento ${className} assente`,
    );

    return normalize(
      match[1],
    );
  };

const services =
  read(
    'servizi.html',
  );

const intake =
  read(
    'analisi-preventiva.html',
  );

const expectedServices = [
  {
    id: 'scelta',
    name: 'Consulenza 90G',
    price: '79 €',
    href: '/consulenza-90g.html',
    detail: 'consulenza-90g.html',
  },
  {
    id: 'preventivo',
    name:
      'Analisi Preventivo & Ordine 90G',
    price: '129 €',
    href:
      '/analisi-preventivo-cucina.html',
    detail:
      'analisi-preventivo-cucina.html',
  },
  {
    id: 'verifica',
    name: 'Verifica Cucina 90G',
    price: '149 €',
    href: '/verifica-90g.html',
    detail: 'verifica-90g.html',
  },
  {
    id: 'progetto',
    name: 'Progetto Cucina 90G',
    price: '299 €',
    href:
      '/progetto-cucina-sistema90g.html',
    detail:
      'progetto-cucina-sistema90g.html',
  },
  {
    id: 'premontaggio',
    name:
      'Controllo Pre-Montaggio 90G',
    price: '179 €',
    href:
      '/controllo-pre-montaggio-cucina.html',
    detail:
      'controllo-pre-montaggio-cucina.html',
  },
  {
    id: 'problema',
    name: 'Analisi Problema 90G',
    price: '149 €',
    href:
      '/analisi-problema-cucina.html',
    detail:
      'analisi-problema-cucina.html',
  },
];

const articleBlocks =
  [
    ...services.matchAll(
      /<article\b[\s\S]*?<\/article>/gi,
    ),
  ]
    .map(
      match =>
        match[0],
    )
    .filter(
      block =>
        block.includes(
          's90g-svc-route',
        ),
    );

assert.equal(
  articleBlocks.length,
  expectedServices.length,
  'la pagina servizi deve esporre esattamente sei percorsi canonici',
);

for (
  const expected
  of expectedServices
) {
  const block =
    articleBlocks.find(
      candidate =>
        candidate.includes(
          `id="${expected.id}"`,
        ),
    );

  assert.ok(
    block,
    `percorso canonico assente: ${expected.id}`,
  );

  const name =
    extractClass(
      block,
      'p',
      's90g-svc-name',
    );

  const price =
    extractClass(
      block,
      'strong',
      's90g-svc-price',
    );

  assert.equal(
    name,
    expected.name,
    `nome servizio errato: ${expected.id}`,
  );

  assert.equal(
    price,
    expected.price,
    `prezzo servizio errato: ${expected.id}`,
  );

  assert.ok(
    block.includes(
      `href="${expected.href}"`,
    ),
    `link servizio errato: ${expected.id}`,
  );

  const detail =
    normalize(
      read(
        expected.detail,
      ),
    );

  assert.ok(
    detail.includes(
      expected.name,
    ),
    `nome assente nella pagina dettaglio: ${expected.name}`,
  );

  assert.ok(
    detail.includes(
      expected.price,
    ),
    `prezzo assente nella pagina dettaglio: ${expected.name}`,
  );
}

assert.ok(
  intake.includes(
    'id="richiedi"',
  ),
  'sezione Free Entry #richiedi assente',
);

assert.ok(
  normalize(
    intake,
  ).includes(
    'Non stai acquistando un servizio',
  ),
  'messaggio nessun acquisto assente',
);

assert.ok(
  normalize(
    intake,
  ).includes(
    'non sei obbligato a proseguire',
  ),
  'messaggio nessun obbligo assente',
);

assert.equal(
  intake.includes(
    'service_price=',
  ),
  false,
  'la pagina Free Entry non deve trasmettere prezzi',
);

const portalLinks =
  [
    ...intake.matchAll(
      /https:\/\/portale\.sistema90g\.it\/portal\.html\?[^"']+/g,
    ),
  ].map(
    match =>
      match[0]
        .replace(
          /&amp;/g,
          '&',
        ),
  );

assert.equal(
  portalLinks.length,
  2,
  'il Free Entry pubblico deve avere due ingressi controllati al Portale: hero e finale',
);

const positions =
  new Set();

for (
  const href
  of portalLinks
) {
  const url =
    new URL(href);

  assert.equal(
    url.origin,
    'https://portale.sistema90g.it',
    `origine Portale errata: ${href}`,
  );

  assert.equal(
    url.pathname,
    '/portal.html',
    `route Portale errata: ${href}`,
  );

  assert.equal(
    url.searchParams.get(
      'requester_role',
    ),
    'private',
    `Free Entry non B2C: ${href}`,
  );

  assert.equal(
    url.searchParams.get(
      'service',
    ),
    'valutazione-iniziale',
    `link Portale non Free Entry: ${href}`,
  );

  assert.equal(
    url.searchParams.has(
      'service_price',
    ),
    false,
    `Free Entry non deve avere prezzo: ${href}`,
  );

  assert.equal(
    url.searchParams.getAll(
      'requester_role',
    ).length,
    1,
    `requester_role duplicato: ${href}`,
  );

  assert.equal(
    url.searchParams.getAll(
      'service',
    ).length,
    1,
    `service duplicato: ${href}`,
  );

  positions.add(
    url.searchParams.get(
      'cta_position',
    ),
  );
}

assert.deepEqual(
  positions,
  new Set(
    [
      'hero',
      'final',
    ],
  ),
  'attribuzione CTA Free Entry non canonica',
);

for (
  const obsolete
  of [
    'Restyling cucina esistente · 79 €',
    'Seconda Opinione · controllo completo',
    'Acquisto Assistito · 290 €',
    'Analisi progetto cucina · 150 €',
  ]
) {
  assert.equal(
    services.includes(
      obsolete,
    ),
    false,
    `servizi contiene residuo: ${obsolete}`,
  );

  assert.equal(
    intake.includes(
      obsolete,
    ),
    false,
    `analisi-preventiva contiene residuo: ${obsolete}`,
  );
}

console.log(
  'GUIDED PRICING + FREE ENTRY CONTRACT TEST: PASS',
);
