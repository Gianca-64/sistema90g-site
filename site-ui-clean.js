(() => {
  const OFFICIAL_EMAIL = 'sistema90g@icloud.com';

  const cleanResidualChat = () => {
    document.querySelectorAll('a').forEach(link => {
      const text = (link.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase();
      const href = (link.getAttribute('href') || '').toLowerCase();
      const isOfficialButton = link.classList.contains('s90g-chat-button');
      const isWhatsapp = href.includes('wa.me') || href.includes('whatsapp');
      const isResidualLabel = text.includes('domande rapide') || text === 'chat whatsapp' || text.includes('domande rapide chat whatsapp');
      if ((isWhatsapp || isResidualLabel) && !isOfficialButton) link.remove();
    });

    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);
    textNodes.forEach(node => {
      const value = node.nodeValue || '';
      if (/domande\s+rapide/i.test(value)) node.nodeValue = value.replace(/domande\s+rapide/gi, '');
    });
  };

  document.querySelectorAll('a[href^="mailto:"]').forEach(link => {
    link.setAttribute('href', `mailto:${OFFICIAL_EMAIL}`);
    if (link.textContent.includes('@')) link.textContent = OFFICIAL_EMAIL;
  });

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const textNodes = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode);
  textNodes.forEach(node => {
    node.nodeValue = node.nodeValue
      .replace(/info@sistema90g\.it/gi, OFFICIAL_EMAIL)
      .replace(/sistema90g@sistema90g\.it/gi, OFFICIAL_EMAIL);
  });

  cleanResidualChat();
  new MutationObserver(cleanResidualChat).observe(document.body, { childList: true, subtree: true, characterData: true });

  const header = document.querySelector('[data-s90g-header]');
  const button = header?.querySelector('.nav-toggle');
  const nav = header?.querySelector('.main-nav');

  if (header && button && nav) {
    const close = () => {
      header.removeAttribute('data-menu-open');
      button.setAttribute('aria-expanded', 'false');
      document.documentElement.classList.remove('s90g-menu-open');
    };

    button.addEventListener('click', () => {
      const open = header.getAttribute('data-menu-open') === 'true';
      if (open) close();
      else {
        header.setAttribute('data-menu-open', 'true');
        button.setAttribute('aria-expanded', 'true');
        document.documentElement.classList.add('s90g-menu-open');
      }
    });

    nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
    document.addEventListener('keydown', event => { if (event.key === 'Escape') close(); });
    window.addEventListener('resize', () => { if (window.innerWidth > 820) close(); });

    const current = location.pathname.split('/').pop() || 'index.html';
    nav.querySelectorAll('a[href]').forEach(link => {
      if (link.getAttribute('href').split('#')[0] === current) link.setAttribute('aria-current', 'page');
    });
  }

  const version = '20260704-final-reference1';
  const page = location.pathname.split('/').pop() || 'index.html';

  const visualMap = {
    'index.html': ['images/final/hero-home-reference.jpg', 'Analisi preventiva Sistema 90G'],
    'chi-e-sistema90g.html': ['images/final/hero-who-reference.jpg', 'Analisi indipendente prima della decisione'],
    'casi-analizzati.html': ['images/final/hero-cases-reference.jpg', 'Raccolta dei casi analizzati Sistema 90G'],
    'controllo-progetto-cucina.html': ['images/final/hero-kitchen-reference.jpg', 'Controllo preventivo del progetto cucina'],
    'verifica-planimetria-distribuzione-casa.html': ['images/final/hero-plan-reference.jpg', 'Verifica preventiva della planimetria'],
    'analisi-preventivo-cucina.html': ['images/final/hero-quote-reference.jpg', 'Analisi preventiva del preventivo cucina'],
    'render-fotorealistici-interni.html': ['images/final/hero-render-reference.jpg', 'Render e verifica di materiali, luce e proporzioni'],
    'agenzie-immobiliari.html': ['images/final/hero-agency-reference.jpg', 'Analisi preventiva per agenzie immobiliari'],
    'controllo-mirato.html': ['images/final/hero-control-reference.jpg', 'Controllo mirato di un dubbio preciso'],
    'analisi-completa.html': ['images/final/hero-analysis-reference.jpg', 'Analisi completa di progetto, uso reale e vincoli'],
    'progetto-da-zero.html': ['images/final/hero-project-reference.jpg', 'Progetto da zero: esigenze, vincoli e proposta'],

    'caso-lavastoviglie-passaggio-cucina.html': ['images/final/case-01-dishwasher.jpg', 'Lavastoviglie aperta e passaggio bloccato'],
    'caso-ingresso-tavolo-living.html': ['images/final/case-02-entry-living.jpg', 'Ingresso diretto su tavolo e soggiorno'],
    'caso-cucina-piccola-tre-lati.html': ['images/final/case-03-compact-kitchen.jpg', 'Cucina compatta su tre lati'],
    'caso-preventivo-cucina-sconto-valore.html': ['images/final/case-04-quote.jpg', 'Preventivo cucina e valore reale'],
    'caso-isola-passaggi-cucina.html': ['images/final/case-05-island-passages.jpg', 'Isola, sedute e aperture'],
    'caso-secondo-bagno-impianti-spazio.html': ['images/final/case-06-second-bath.jpg', 'Secondo bagno e vincoli impiantistici'],
    'caso-open-space-tv-divano-passaggi.html': ['images/final/case-07-tv-sofa-path.jpg', 'TV, divano e percorso principale'],
    'caso-lavello-sotto-finestra-aperture.html': ['images/final/case-08-sink-window.jpg', 'Lavello sotto finestra e apertura dell’infisso'],
    'caso-scala-interna-terrazzo-planimetria.html': ['images/final/case-09-stair-plan.jpg', 'Scala interna e distribuzione della casa'],
    'caso-open-space-percorso-centrale.html': ['images/final/case-10-central-path.jpg', 'Open space con percorso centrale'],
    'caso-terza-camera-zona-giorno.html': ['images/final/case-11-third-bedroom.jpg', 'Terza camera e zona giorno residua'],
    'caso-cucina-profondita-75-angolo.html': ['images/final/case-12-deep-corner.jpg', 'Cucina profonda e accessibilità dell’angolo'],
    'caso-bagno-lavatrice-dieci-centimetri.html': ['images/final/case-13-bath-laundry.jpg', 'Bagno compatto con lavanderia'],
    'caso-cabina-armadio-camera-irregolare.html': ['images/final/case-14-wardrobe-room.jpg', 'Camera irregolare con cabina armadio'],
    'caso-divano-letto-soggiorno-tre-persone.html': ['images/final/case-15-sofa-bed.jpg', 'Divano letto in soggiorno per tre persone']
  };

  const applyVisual = (container, visual) => {
    if (!container || !visual) return;
    let figure = container.querySelector('figure.premium-image');
    if (!figure) {
      figure = document.createElement('figure');
      figure.className = 'premium-image';
      container.prepend(figure);
    }
    let image = figure.querySelector('img');
    if (!image) {
      image = document.createElement('img');
      figure.appendChild(image);
    }
    image.src = `${visual[0]}?v=${version}`;
    image.alt = visual[1];
    image.removeAttribute('srcset');
  };

  applyVisual(document.querySelector('main .premium-hero .container, main .professional-hero .container'), visualMap[page]);

  if (page === 'casi-analizzati.html') {
    document.querySelectorAll('article').forEach(article => {
      const link = article.querySelector('a.text-link[href]');
      const image = article.querySelector('img.case-card-image');
      if (!link || !image) return;
      const target = link.getAttribute('href').split('#')[0];
      const visual = visualMap[target];
      if (!visual) return;
      image.src = `${visual[0]}?v=${version}`;
      image.alt = visual[1];
      image.removeAttribute('srcset');
    });
  }
})();