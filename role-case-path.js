(() => {
'use strict';

const portalConfig = window.S90G_PORTAL_CONFIG || {
  enabled: false,
  url: '',
  message: 'Il collegamento alla richiesta non è configurato.'
};

const services = {
  'controllo-mirato': {
    serviceId: 'S90G-K01',
    requesterRole: 'private',
    title: 'Controllo mirato cucina',
    price: 127,
    time: 'Entro 2 giorni lavorativi',
    description: 'Per una sola domanda determinante su un progetto, una misura, un’apertura, un’interferenza, un elettrodomestico o una voce del preventivo.',
    checks: [
      'il dubbio principale dichiarato',
      'le misure e i documenti pertinenti',
      'le conseguenze visibili nell’uso quotidiano',
      'i dati mancanti e le verifiche da richiedere'
    ],
    deliverables: [
      'risposta strutturata sul problema concordato',
      'criticità, conseguenze e condizioni da verificare',
      'domande da rivolgere al soggetto competente',
      'un chiarimento sul documento consegnato'
    ],
    limits: [
      'una domanda principale',
      'nessuna verifica completa dell’intero progetto',
      'nessuna nuova composizione, Configuratore o render'
    ]
  },
  'analisi-completa': {
    serviceId: 'S90G-K02',
    requesterRole: 'private',
    title: 'Verifica completa progetto e preventivo cucina',
    price: 253,
    time: 'Entro 2 giorni lavorativi',
    description: 'Per controllare nel loro insieme una cucina già progettata, le misure, le immagini, gli elettrodomestici e il preventivo prima dell’ordine.',
    checks: [
      'coerenza tra ambiente, misure e progetto',
      'passaggi, aperture e interferenze leggibili',
      'uso quotidiano e coordinamento tra mobili ed elettrodomestici',
      'voci, esclusioni e dati da chiarire nel preventivo'
    ],
    deliverables: [
      'report strutturato con criticità ordinate per priorità',
      'conseguenze possibili e dati mancanti',
      'verifiche da svolgere prima dell’ordine',
      'un chiarimento scritto sul report'
    ],
    limits: [
      'una cucina, una soluzione principale e un preventivo',
      'nessuna nuova progettazione o ricostruzione nel Configuratore',
      'nessun render, progetto esecutivo o seconda soluzione completa'
    ]
  },
  'acquisto-assistito-cucina': {
    serviceId: 'S90G-K03',
    requesterRole: 'private',
    title: 'Acquisto Assistito Cucina 90G',
    price: 290,
    time: 'Prima fase entro 3 giorni lavorativi',
    description: 'Per sviluppare una direzione indipendente e una proposta preliminare prima del progetto commerciale definitivo del rivenditore.',
    checks: [
      'esigenze, funzioni e vincoli documentati',
      'rapporti tra composizione, passaggi e aperture',
      'coerenza della proposta principale',
      'punti da affidare al rivenditore per l’adattamento definitivo'
    ],
    deliverables: [
      'una proposta funzionale principale',
      'sviluppo nel Configuratore con viste preliminari',
      'cinque render della soluzione principale e una vista della variante di finitura',
      'fascicolo conclusivo e una revisione circoscritta'
    ],
    limits: [
      'nessun rilievo o progetto esecutivo',
      'nessun preventivo, ordine, montaggio o collaudo',
      'nessuna seconda composizione completa o revisione illimitata'
    ]
  },
  'scelta-finiture-cucina': {
    serviceId: 'S90G-K11',
    requesterRole: 'private',
    title: 'Scelta finiture cucina',
    price: 47,
    time: 'Entro 1 giorno lavorativo',
    description: 'Per confrontare un massimo di due alternative già individuate, quando la composizione della cucina è definita.',
    checks: [
      'rapporto tra ante, top, schienale, pavimento e pareti',
      'coerenza delle due alternative con luce e ambiente',
      'uso quotidiano, manutenzione e punti da verificare dal vivo',
      'differenze rilevanti tra le combinazioni proposte'
    ],
    deliverables: [
      'confronto motivato tra le due alternative',
      'punti di forza e possibili incoerenze',
      'indicazione della direzione più equilibrata',
      'verifiche da effettuare su campioni e materiali reali'
    ],
    limits: [
      'massimo due alternative già selezionate',
      'nessuna ricerca illimitata di materiali o prodotti',
      'nessun render, campione fisico o garanzia cromatica dello schermo'
    ]
  },
  'restyling-cucina-esistente': {
    serviceId: 'S90G-K12',
    requesterRole: 'private',
    title: 'Restyling cucina esistente',
    price: 79,
    time: 'Entro 1 giorno lavorativo',
    description: 'Per ordinare che cosa conservare, che cosa modificare e quali verifiche chiedere al fornitore prima di intervenire su una cucina esistente.',
    checks: [
      'stato documentabile degli elementi esistenti',
      'coordinamento tra parti conservate e parti nuove',
      'criticità visibili di ante, top, schienale e ferramenta',
      'dati e compatibilità da verificare con rivenditore o artigiano'
    ],
    deliverables: [
      'direzione principale del restyling',
      'elenco ordinato degli elementi da conservare o modificare',
      'criticità e richieste da sottoporre al fornitore',
      'limiti e controlli necessari prima dell’ordine'
    ],
    limits: [
      'nessun rilievo o certificazione di compatibilità',
      'nessun progetto esecutivo, render, preventivo o ordine',
      'i casi che richiedono una nuova composizione vengono riclassificati'
    ]
  }
};

const choiceDefinitions = [
  {
    slug: 'controllo-mirato',
    title: 'Ho un solo dubbio preciso',
    description: 'Una misura, un passaggio, un’apertura, un elettrodomestico, un’interferenza o una voce del preventivo.'
  },
  {
    slug: 'analisi-completa',
    title: 'Ho un progetto o un preventivo da controllare nel suo insieme',
    description: 'Voglio verificare la cucina prima di firmare o confermare l’ordine.'
  },
  {
    slug: 'acquisto-assistito-cucina',
    title: 'Non ho ancora una soluzione soddisfacente',
    description: 'Voglio sviluppare una direzione indipendente prima del progetto commerciale definitivo.'
  },
  {
    slug: 'scelta-finiture-cucina',
    title: 'Devo scegliere tra due finiture cucina',
    description: 'La composizione è definita e voglio confrontare due alternative già individuate.'
  },
  {
    slug: 'restyling-cucina-esistente',
    title: 'Voglio aggiornare una cucina esistente',
    description: 'Devo capire che cosa conservare, che cosa modificare e quali compatibilità verificare.'
  }
];

const euro = value => new Intl.NumberFormat('it-IT', {
  style: 'currency',
  currency: 'EUR',
  maximumFractionDigits: 0
}).format(value);

function ensureChoices(form) {
  const grid = form.querySelector('.s90g-choice-grid');
  if (!grid) return;

  choiceDefinitions.forEach(choice => {
    if (grid.querySelector(`input[value="${choice.slug}"]`)) return;

    const label = document.createElement('label');
    label.className = 's90g-choice';

    const input = document.createElement('input');
    input.type = 'radio';
    input.name = 'kitchen_situation';
    input.value = choice.slug;

    const copy = document.createElement('span');
    const title = document.createElement('strong');
    const description = document.createElement('small');
    title.textContent = choice.title;
    description.textContent = choice.description;
    copy.append(title, description);
    label.append(input, copy);
    grid.appendChild(label);
  });
}

function init() {
  const form = document.getElementById('s90g-kitchen-path');
  if (!form) return;

  ensureChoices(form);

  const options = [...form.querySelectorAll('input[name="kitchen_situation"]')];
  const result = document.getElementById('s90g-path-result');
  const cta = document.getElementById('s90g-result-cta');

  const renderList = (id, items) => {
    const node = document.getElementById(id);
    node.innerHTML = items.map(item => `<li>${item}</li>`).join('');
  };

  const buildTarget = service => {
    if (!portalConfig.enabled || !portalConfig.url) return '/contatti.html';

    const target = new URL(portalConfig.url);
    const source = new URL(window.location.href);

    target.searchParams.set('requester_role', service.requesterRole || 'private');
    target.searchParams.set('service', service.serviceId);
    target.searchParams.set('units', '1');
    target.searchParams.set('source_page', source.searchParams.get('source_page') || 'analisi-preventiva');
    target.searchParams.set('content_type', source.searchParams.get('content_type') || 'guided-path');
    target.searchParams.set('cta_position', source.searchParams.get('cta_position') || 'result');

    [
      'utm_source',
      'utm_medium',
      'utm_campaign',
      'utm_content',
      'utm_term',
      'case_id',
      'problem'
    ].forEach(key => {
      const value = source.searchParams.get(key);
      if (value) target.searchParams.set(key, value);
    });

    return target.toString();
  };

  const showResult = slug => {
    const service = services[slug];
    if (!service) return;

    document.getElementById('s90g-result-code').textContent = service.serviceId;
    document.getElementById('s90g-result-title').textContent = service.title;
    document.getElementById('s90g-result-description').textContent = service.description;
    document.getElementById('s90g-result-price').textContent = euro(service.price);
    document.getElementById('s90g-result-time').textContent = service.time;
    renderList('s90g-result-checks', service.checks);
    renderList('s90g-result-deliverables', service.deliverables);
    renderList('s90g-result-limits', service.limits);

    cta.href = buildTarget(service);
    cta.dataset.service = service.serviceId;
    cta.dataset.finalPortal = 'true';
    cta.dataset.portalEnabled = String(Boolean(portalConfig.enabled && portalConfig.url));
    cta.querySelector('span').textContent = portalConfig.enabled && portalConfig.url ? 'Inizia la richiesta' : 'Contatta Sistema 90G';

    result.hidden = false;
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });

    const url = new URL(window.location.href);
    url.searchParams.set('service_hint', slug);
    url.hash = 'risultato';
    history.replaceState({}, '', url);

    document.dispatchEvent(new CustomEvent('s90g:path-result', {
      detail: {
        role: service.requesterRole || 'private',
        service: service.serviceId,
        units: '1'
      }
    }));
  };

  options.forEach(option => option.addEventListener('change', () => showResult(option.value)));

  const initial = new URL(window.location.href).searchParams.get('service_hint');
  if (initial && services[initial]) {
    const input = options.find(option => option.value === initial);
    if (input) {
      input.checked = true;
      showResult(initial);
    }
  }
}

document.addEventListener('DOMContentLoaded', init);
})();