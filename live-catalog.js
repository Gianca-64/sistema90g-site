const S90G_CONSOLE_URL = 'https://sistema90g-console.sistema90g.workers.dev';

const S90G_LEVEL_IMAGES = {
  finiture: 'images/17_SERVIZI_FINITURE.jpg?v=20260716b',
  'check-up-progetto': 'images/14_SERVIZI_CONTROLLO_MIRATO.jpg?v=20260716b',
  restyling: 'images/16_SERVIZI_PROGETTO_DA_ZERO.png?v=20260716b',
  redistribuzione: 'images/15_SERVIZI_ANALISI_COMPLETA.jpg?v=20260716b',
  'progetto-completo': 'images/03_HOME_METODO.jpg?v=20260716b',
};

const S90G_FALLBACK_LEVELS = [
  {
    slug: 'finiture',
    name: 'Finiture arredo',
    short_label: 'Scelte materiali e colori',
    price_label: '47 euro',
    delivery_time: '72 ore',
    problem: 'Per scegliere finiture, colori, materiali e abbinamenti evitando un risultato incoerente.',
    required_inputs: 'Foto dell’ambiente, materiali, render o progetto disponibili ed elementi già scelti.',
    deliverable: 'Lettura del rischio estetico e indicazioni per coordinare le finiture.',
    includes: 'Abbinamenti, materiali, colori e percezione generale dell’ambiente.',
    excludes: 'Progettazione completa, redistribuzione ed esecutivi tecnici.',
  },
  {
    slug: 'check-up-progetto',
    name: 'Verifica progetto',
    short_label: 'Controllo prima della conferma',
    price_label: '127 euro',
    delivery_time: '72 ore',
    problem: 'Per controllare una proposta, un progetto o un preventivo prima di confermare.',
    required_inputs: 'Planimetrie, misure, immagini, render, preventivi o documentazione del progetto.',
    deliverable: 'Analisi dei punti critici, degli aspetti da chiarire e dei rischi nell’uso quotidiano.',
    includes: 'Funzionalità, passaggi, aperture e coerenza tra progetto e uso reale.',
    excludes: 'Nuova progettazione completa o modifica totale degli ambienti.',
  },
  {
    slug: 'restyling',
    name: 'Restyling arredo esistente',
    short_label: 'Aggiornare senza rifare tutto',
    price_label: '79 euro',
    delivery_time: '72 ore',
    problem: 'Per migliorare un ambiente esistente mantenendo parte degli arredi.',
    required_inputs: 'Foto, elementi da mantenere, modifiche desiderate e dati disponibili sugli arredi.',
    deliverable: 'Direzione di restyling con valutazione delle compatibilità e delle priorità.',
    includes: 'Arredi esistenti, modifiche estetiche, aggiornamenti e coerenza generale.',
    excludes: 'Nuovo progetto completo, opere edilizie e gestione dei fornitori.',
  },
  {
    slug: 'redistribuzione',
    name: 'Redistribuzione interni',
    short_label: 'Riorganizzare gli spazi',
    price_label: '147 euro',
    delivery_time: '72 ore',
    problem: 'Per capire come riorganizzare ambienti, funzioni e percorsi che oggi non funzionano.',
    required_inputs: 'Planimetria, misure, vincoli, esigenze familiari e ambienti coinvolti.',
    deliverable: 'Analisi distributiva con direzione progettuale e criticità da verificare.',
    includes: 'Flussi, rapporti tra ambienti, priorità e organizzazione degli spazi.',
    excludes: 'Pratiche edilizie, calcoli tecnici ed esecutivi professionali.',
  },
  {
    slug: 'progetto-completo',
    name: 'Progetto interni da zero',
    short_label: 'Costruire una direzione completa',
    price_label: '797 euro',
    delivery_time: '72 ore per la prima analisi',
    problem: 'Per partire dalle esigenze reali quando non esiste ancora una soluzione definita.',
    required_inputs: 'Planimetrie, misure, esigenze, foto, vincoli, priorità e obiettivi.',
    deliverable: 'Documento guida per impostare il progetto degli interni.',
    includes: 'Logica distributiva, priorità, criteri di scelta e impostazione generale.',
    excludes: 'Pratiche edilizie, direzione lavori ed esecutivi professionali.',
  },
];

let s90gCasesAnalyzed = 188;

function s90gEscape(value) {
  return String(value || '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function s90gLevelCard(level, index) {
  const number = String(index + 1).padStart(2, '0');
  const image = S90G_LEVEL_IMAGES[level.slug] || 'images/13_SERVIZI_HERO.jpg?v=20260716b';
  return `<article class="service-level-card" data-service-level="${s90gEscape(level.slug)}">
    <figure class="service-level-media">
      <img src="${s90gEscape(image)}" alt="${s90gEscape(level.name)}: esempio di analisi Sistema 90G" loading="lazy">
      <span>${number}</span>
    </figure>
    <div class="service-level-body">
      <div class="service-level-heading">
        <small>${s90gEscape(level.short_label)}</small>
      </div>
      <h3>${s90gEscape(level.name)}</h3>
      <div class="service-level-commercial">
        <strong>${s90gEscape(level.price_label)}</strong>
        <span>Consegna: ${s90gEscape(level.delivery_time)}</span>
      </div>
      <p class="service-level-purpose">${s90gEscape(level.problem)}</p>
      <div class="service-level-output">
        <strong>Cosa ricevi</strong>
        <p>${s90gEscape(level.deliverable)}</p>
      </div>
      <details>
        <summary>Cosa serve, cosa include e limiti</summary>
        <p><strong>Da inviare:</strong> ${s90gEscape(level.required_inputs)}</p>
        <p><strong>Include:</strong> ${s90gEscape(level.includes)}</p>
        <p><strong>Non include:</strong> ${s90gEscape(level.excludes)}</p>
      </details>
      <a class="s90g-link service-card-link" data-track-portal href="${S90G_CONSOLE_URL}/richiesta" target="_blank" rel="noopener">Sottoponi il caso <span aria-hidden="true">→</span></a>
    </div>
  </article>`;
}

function s90gRenderCatalog(levels) {
  const section = document.getElementById('servizi');
  if (!section) return;

  section.className = 's90g-services s90g-live-services';
  section.innerHTML = `<div class="s90g-shell">
    <div class="s90g-section-head s90g-live-services-intro">
      <div>
      <p class="s90g-kicker">Cinque livelli chiari</p>
      <h2>Cinque profondità, una sola logica: vedere prima ciò che può diventare un problema.</h2>
      <p>Il livello dipende dalla decisione da proteggere e dal materiale disponibile. Prezzo, tempi, risultato e limiti restano dichiarati prima di iniziare.</p>
      </div>
    </div>
    <aside class="s90g-live-proof" aria-label="Casi analizzati da Sistema 90G" aria-live="polite">
      <strong class="s90g-live-proof-number" data-public-cases-count>${s90gCasesAnalyzed}</strong>
      <div class="s90g-live-proof-copy">
        <span>casi reali raccolti e analizzati</span>
        <p>Cucine, preventivi, finiture, arredi e distribuzioni interne letti prima che la scelta diventi difficile da correggere.</p>
      </div>
      <a class="s90g-link" href="casi-analizzati.html">Scopri i casi pubblicati <span aria-hidden="true">→</span></a>
    </aside>
    <div class="s90g-live-level-grid">
      ${levels.map(s90gLevelCard).join('')}
    </div>
    <div class="s90g-service-catalog-note">
      <strong>La prima lettura è gratuita.</strong>
      <span>Serve a capire se il caso è adatto e quale profondità è davvero necessaria. Il lavoro parte solo dopo conferma.</span>
    </div>
  </div>`;
}

function s90gUpdateCounters(value) {
  const count = Number(value);
  if (!Number.isFinite(count) || count < 0) return;
  s90gCasesAnalyzed = count;
  document.querySelectorAll('[data-public-cases-count]').forEach((element) => {
    element.textContent = new Intl.NumberFormat('it-IT').format(count);
  });
  const heroCounter = document.getElementById('casi-analizzati-90g');
  if (heroCounter) heroCounter.textContent = `${new Intl.NumberFormat('it-IT').format(count)}+`;
}

function s90gAlignLegacyOffer() {
  const delivery = document.getElementById('consegna');
  if (delivery) {
    delivery.innerHTML = `<div class="container">
      <div class="premium-copy wide">
        <p class="eyebrow">Consegna e tempi</p>
        <h2>Ogni livello dichiara prima contenuti, tempi e confini.</h2>
        <p>Il tempo indicato nella scheda decorre dal pagamento e dalla ricezione del materiale completo. Se manca un elemento decisivo, il lavoro non viene simulato: viene richiesto prima di iniziare.</p>
      </div>
      <div class="premium-three">
        <article><span>Formato</span><h3>Un documento da consultare.</h3><p>Trovi il problema, le conseguenze possibili e ciò che conviene chiarire prima della decisione.</p></article>
        <article><span>Decorrenza</span><h3>Dopo pagamento e materiale completo.</h3><p>Il tempo di consegna parte soltanto quando sono disponibili gli elementi necessari.</p></article>
        <article><span>Limiti</span><h3>Nessuna verifica tecnica simulata.</h3><p>Strutture, impianti, autorizzazioni e controlli in cantiere restano di competenza dei professionisti abilitati.</p></article>
      </div>
    </div>`;
  }

  const footer = document.querySelector('.footer-links, .s90g-footer-links');
  if (!footer) return;
  ['controllo-mirato.html', 'analisi-completa.html', 'progetto-da-zero.html'].forEach((href) => {
    footer.querySelectorAll(`a[href="${href}"]`).forEach((link) => link.remove());
  });
  if (!footer.querySelector('a[href="index.html#servizi"]')) {
    const link = document.createElement('a');
    link.href = 'index.html#servizi';
    link.textContent = 'I cinque livelli';
    footer.prepend(link);
  }
}

async function s90gLoadPublicStats() {
  try {
    const response = await fetch(`${S90G_CONSOLE_URL}/api/public-stats`, { cache: 'no-store' });
    if (!response.ok) return;
    const payload = await response.json();
    if (payload && payload.ok) s90gUpdateCounters(payload.casesAnalyzed);
  } catch (error) {
    console.warn('Contatore pubblico non disponibile', error);
  }
}

async function s90gLoadServiceLevels() {
  try {
    const response = await fetch(`${S90G_CONSOLE_URL}/api/public-service-levels`);
    if (!response.ok) return;
    const payload = await response.json();
    if (!payload || !payload.ok || !Array.isArray(payload.levels) || payload.levels.length !== 5) return;
    s90gRenderCatalog(payload.levels);
    s90gUpdateCounters(s90gCasesAnalyzed);
  } catch (error) {
    console.warn('Catalogo servizi live non disponibile', error);
  }
}

document.addEventListener('DOMContentLoaded', () => {
  s90gRenderCatalog(S90G_FALLBACK_LEVELS);
  s90gAlignLegacyOffer();
  const services = document.getElementById('servizi');
  if (services) {
    services.addEventListener('click', (event) => {
      const link = event.target.closest('[data-track-portal]');
      if (link && typeof trackLead === 'function') trackLead('public_portal_open', link);
    });
  }
  void s90gLoadPublicStats();
  void s90gLoadServiceLevels();
});
