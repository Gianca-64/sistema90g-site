(() => {
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
    nav.addEventListener('click', event => {
      if (event.target.closest('a')) close();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') close();
    });
    const current = location.pathname.split('/').pop() || 'index.html';
    nav.querySelectorAll('a[href]').forEach(link => {
      if (link.getAttribute('href').split('#')[0] === current) link.setAttribute('aria-current', 'page');
    });
  }

  const page = location.pathname.split('/').pop() || 'index.html';
  const version = '20260704-image-audit2';

  const pageVisuals = {
    'index.html': ['homepage-approvata.svg', '90g-style-conflitto.svg'],
    'analisi-preventiva.html': ['hero-analisi-90g.jpg', '90g-style-preventivo.svg'],
    'controllo-mirato.html': ['90g-style-hero.svg'],
    'analisi-completa.html': ['90g-style-planimetria.svg'],
    'progetto-da-zero.html': ['hero-progetto-zero-90g.jpg'],
    'chi-e-sistema90g.html': ['hero-casa90g.jpg'],
    'casi-analizzati.html': ['hero-casi-90g-2026.jpg'],
    'controllo-progetto-cucina.html': ['hero-controllo-progetto-cucina.svg', '90g-style-conflitto.svg'],
    'analisi-preventivo-cucina.html': ['hero-analisi-preventivo-cucina.svg', '90g-real-preventivo.svg'],
    'verifica-planimetria-distribuzione-casa.html': ['hero-verifica-planimetria-casa.svg', 'hero-planimetria-90g.jpg'],
    'scelta-finiture-casa.html': ['hero-scelta-finiture-casa.svg', '90g-style-finiture.svg'],
    'render-fotorealistici-interni.html': ['90g-real-kitchen.svg', 'hero-finiture-90g.jpg'],
    'agenzie-immobiliari.html': ['hero-agenzie-90g.jpg', '90g-style-agenzie.svg'],
    'professionisti.html': ['90g-style-planimetria.svg', 'hero-verifica-planimetria-casa.svg'],
    'caso-lavastoviglie-passaggio-cucina.html': ['caso-lavastoviglie-passaggio.svg', '90g-style-conflitto.svg'],
    'caso-ingresso-tavolo-living.html': ['caso-ingresso-tavolo-living.svg'],
    'caso-cucina-piccola-tre-lati.html': ['caso-cucina-piccola-tre-lati.svg'],
    'caso-preventivo-cucina-sconto-valore.html': ['caso-preventivo-sconto-valore.svg'],
    'caso-isola-passaggi-cucina.html': ['caso-isola-passaggi-2026.jpg'],
    'caso-secondo-bagno-impianti-spazio.html': ['caso-secondo-bagno-2026.jpg'],
    'caso-open-space-tv-divano-passaggi.html': ['caso-open-space-tv-2026.jpg'],
    'caso-lavello-sotto-finestra-aperture.html': ['caso-lavello-finestra-2026.jpg'],
    'caso-scala-interna-terrazzo-planimetria.html': ['caso-scala-planimetria-2026.jpg'],
    'caso-open-space-percorso-centrale.html': ['caso-percorso-centrale-2026.jpg'],
    'caso-terza-camera-zona-giorno.html': ['caso-terza-camera-2026.jpg'],
    'caso-cucina-profondita-75-angolo.html': ['caso-profondita-angolo-2026.jpg'],
    'caso-bagno-lavatrice-dieci-centimetri.html': ['caso-bagno-lavatrice-10cm-90g.svg'],
    'caso-cabina-armadio-camera-irregolare.html': ['caso-cabina-armadio-camera-irregolare-90g.svg'],
    'caso-divano-letto-soggiorno-tre-persone.html': ['caso-divano-letto-soggiorno-tre-persone-90g.svg'],
    'micro-caso-frigo-apertura.html': ['frigo-apertura-insufficiente.svg'],
    'micro-caso-passaggio-bloccato.html': ['hero-controllo-passaggio.svg'],
    'scena-frigo-vicino-parete.html': ['frigo-apertura-insufficiente.svg'],
    'scena-isola-sgabelli-passaggio.html': ['90g-real-kitchen.svg'],
    'scena-lavastoviglie-aperta-passaggio.html': ['90g-style-conflitto.svg'],
    'scene-reali-cucina.html': ['90g-real-kitchen.svg'],
    'caso-open-space.html': ['90g-real-open-space.svg'],
    'caso-passaggio-lavastoviglie.html': ['hero-controllo-passaggio.svg'],
    'caso-verificato-isola-forno-passaggi.html': ['90g-real-kitchen.svg'],
    'centro-casi-reali.html': ['hero-analisi-90g.jpg'],
    'errori-trovati-davvero.html': ['90g-style-conflitto.svg'],
    'metodo-sistema90g.html': ['homepage-approvata.svg'],
    'progetto-preventivo.html': ['90g-real-preventivo.svg'],
    'tutto-sembrava-corretto-finche.html': ['90g-style-conflitto.svg', 'hero-controllo-passaggio.svg']
  };

  const contentImages = [...document.querySelectorAll('main img')].filter(img => !img.closest('.brand'));
  const sequence = pageVisuals[page];
  if (sequence) {
    contentImages.forEach((image, index) => {
      const file = sequence[index];
      if (!file) return;
      image.src = `images/${file}?v=${version}`;
      image.removeAttribute('srcset');
    });
  }

  if (page === 'casi-analizzati.html') {
    const cards = {
      'caso-lavastoviglie-passaggio-cucina.html': 'caso-lavastoviglie-passaggio-2026.jpg',
      'caso-ingresso-tavolo-living.html': 'caso-ingresso-living-2026.jpg',
      'caso-cucina-piccola-tre-lati.html': 'caso-cucina-tre-lati-2026.jpg',
      'caso-preventivo-cucina-sconto-valore.html': 'caso-preventivo-valore-2026.jpg',
      'caso-isola-passaggi-cucina.html': 'caso-isola-passaggi-2026.jpg',
      'caso-secondo-bagno-impianti-spazio.html': 'caso-secondo-bagno-2026.jpg',
      'caso-open-space-tv-divano-passaggi.html': 'caso-open-space-tv-2026.jpg',
      'caso-lavello-sotto-finestra-aperture.html': 'caso-lavello-finestra-2026.jpg',
      'caso-scala-interna-terrazzo-planimetria.html': 'caso-scala-planimetria-2026.jpg',
      'caso-open-space-percorso-centrale.html': 'caso-percorso-centrale-2026.jpg',
      'caso-terza-camera-zona-giorno.html': 'caso-terza-camera-2026.jpg',
      'caso-cucina-profondita-75-angolo.html': 'caso-profondita-angolo-2026.jpg',
      'caso-bagno-lavatrice-dieci-centimetri.html': 'caso-bagno-lavatrice-2026.jpg',
      'caso-cabina-armadio-camera-irregolare.html': 'caso-cabina-armadio-2026.jpg',
      'caso-divano-letto-soggiorno-tre-persone.html': 'caso-divano-letto-2026.jpg'
    };
    document.querySelectorAll('article').forEach(article => {
      const link = article.querySelector('a.text-link[href]');
      const image = article.querySelector('img.case-card-image');
      if (!link || !image) return;
      const target = link.getAttribute('href').split('#')[0];
      const file = cards[target];
      if (file) image.src = `images/${file}?v=${version}`;
    });
  }
})();
