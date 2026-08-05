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
      'render e fascicolo conclusivo',
      'una revisione circoscritta della direzione concordata'
    ],
    limits: [
      'nessun rilievo o progetto esecutivo',
      'nessun preventivo, ordine, montaggio o collaudo',
      'nessuna seconda composizione completa o revisione illimitata'
    ]
  }
};

const euro = value => new Intl.NumberFormat('it-IT', {
  style: 'currency',
  currency: 'EUR',
  maximumFractionDigits: 0
}).format(value);

function init() {
  const form = document.getElementById('s90g-kitchen-path');
  if (!form) return;

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
    target.searchParams.set('requester_role', 'private');
    target.searchParams.set('case_context', service.serviceId);
    target.searchParams.set('service', service.serviceId);
    target.searchParams.set('service_slug', options.find(x => x.checked)?.value || '');
    target.searchParams.set('service_title', service.title);
    target.searchParams.set('service_price', String(service.price));
    target.searchParams.set('service_currency', 'EUR');
    target.searchParams.set('service_time', service.time);
    target.searchParams.set('source_page', 'analisi-preventiva');
    target.searchParams.set('content_type', 'guided-path');
    target.searchParams.set('cta_position', 'result');
    ['utm_source','utm_medium','utm_campaign','utm_content','utm_term','case_id'].forEach(key => {
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
    cta.querySelector('span').textContent = portalConfig.enabled && portalConfig.url ? 'Inizia la richiesta' : 'Contatta Sistema 90G';
    result.hidden = false;
    result.scrollIntoView({ behavior: 'smooth', block: 'start' });
    const url = new URL(window.location.href);
    url.searchParams.set('service_hint', slug);
    url.hash = 'risultato';
    history.replaceState({}, '', url);
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
