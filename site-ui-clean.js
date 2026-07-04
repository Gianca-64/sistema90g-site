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

  const version = '20260704-audit-images2';
  const page = location.pathname.split('/').pop() || 'index.html';

  const visualMap = {
    'index.html': ['images/hero-home-90g-2026.jpg', 'Analisi preventiva Sistema 90G'],
    'chi-e-sistema90g.html': ['images/hero-chi-sono-90g-2026.jpg', 'Analisi indipendente prima della decisione'],
    'casi-analizzati.html': ['images/hero-casi-90g-2026.jpg', 'Raccolta dei casi analizzati Sistema 90G'],
    'controllo-progetto-cucina.html': ['images/hero-cucina-90g-2026.jpg', 'Controllo preventivo del progetto cucina'],
    'verifica-planimetria-distribuzione-casa.html': ['images/hero-planimetria-90g-2026.jpg', 'Verifica preventiva della planimetria'],
    'analisi-preventivo-cucina.html': ['images/hero-preventivo-90g-2026.jpg', 'Analisi preventiva del preventivo cucina'],

    'caso-lavastoviglie-passaggio-cucina.html': ['images/caso-lavastoviglie-passaggio-2026.jpg', 'Lavastoviglie aperta e passaggio bloccato'],
    'caso-ingresso-tavolo-living.html': ['images/caso-ingresso-living-2026.jpg', 'Ingresso diretto su tavolo e soggiorno'],
    'caso-cucina-piccola-tre-lati.html': ['images/caso-cucina-tre-lati-2026.jpg', 'Cucina compatta su tre lati'],
    'caso-preventivo-cucina-sconto-valore.html': ['images/caso-preventivo-valore-2026.jpg', 'Preventivo cucina e valore reale'],
    'caso-isola-passaggi-cucina.html': ['images/caso-isola-passaggi-2026.jpg', 'Isola, sedute e aperture'],
    'caso-secondo-bagno-impianti-spazio.html': ['images/caso-secondo-bagno-2026.jpg', 'Secondo bagno e vincoli impiantistici'],
    'caso-open-space-tv-divano-passaggi.html': ['images/caso-open-space-tv-2026.jpg', 'TV, divano e percorso principale'],
    'caso-lavello-sotto-finestra-aperture.html': ['images/caso-lavello-finestra-2026.jpg', 'Lavello sotto finestra e apertura dell’infisso'],
    'caso-scala-interna-terrazzo-planimetria.html': ['images/caso-scala-planimetria-2026.jpg', 'Scala interna e distribuzione della casa'],
    'caso-open-space-percorso-centrale.html': ['images/caso-percorso-centrale-2026.jpg', 'Open space con percorso centrale'],
    'caso-terza-camera-zona-giorno.html': ['images/caso-terza-camera-2026.jpg', 'Terza camera e zona giorno residua'],
    'caso-cucina-profondita-75-angolo.html': ['images/caso-profondita-angolo-2026.jpg', 'Cucina profonda e accessibilità dell’angolo'],
    'caso-bagno-lavatrice-dieci-centimetri.html': ['images/caso-bagno-lavatrice-2026.jpg', 'Bagno compatto con lavanderia'],
    'caso-cabina-armadio-camera-irregolare.html': ['images/caso-cabina-armadio-2026.jpg', 'Camera irregolare con cabina armadio'],
    'caso-divano-letto-soggiorno-tre-persone.html': ['images/caso-divano-letto-2026.jpg', 'Divano letto in soggiorno per tre persone']
  };

  const pagesWithoutApprovedHero = new Set([
    'render-fotorealistici-interni.html',
    'agenzie-immobiliari.html',
    'controllo-mirato.html',
    'analisi-completa.html',
    'progetto-da-zero.html'
  ]);

  const setImage = (image, visual) => {
    if (!image || !visual) return;
    image.onerror = () => {
      image.onerror = null;
      image.closest('figure')?.remove();
      document.body.classList.add('s90g-no-hero-image');
    };
    image.src = `${visual[0]}?v=${version}`;
    image.alt = visual[1];
    image.removeAttribute('srcset');
  };

  const heroContainer = document.querySelector('main .premium-hero .container, main .professional-hero .container');

  if (pagesWithoutApprovedHero.has(page)) {
    heroContainer?.querySelector('figure.premium-image')?.remove();
    document.body.classList.add('s90g-no-hero-image');
  } else if (heroContainer && visualMap[page]) {
    let figure = heroContainer.querySelector('figure.premium-image');
    if (!figure) {
      figure = document.createElement('figure');
      figure.className = 'premium-image';
      heroContainer.prepend(figure);
    }
    let image = figure.querySelector('img');
    if (!image) {
      image = document.createElement('img');
      figure.appendChild(image);
    }
    setImage(image, visualMap[page]);
  }

  if (page === 'casi-analizzati.html') {
    document.querySelectorAll('article').forEach(article => {
      const link = article.querySelector('a.text-link[href]');
      const image = article.querySelector('img.case-card-image');
      if (!link || !image) return;
      const target = link.getAttribute('href').split('#')[0];
      setImage(image, visualMap[target]);
    });
  }
})();