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

  if (location.pathname.endsWith('/casi-analizzati.html')) {
    const visuali = {
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
      const file = visuali[target];
      if (file) image.src = `images/${file}?v=20260704-image-audit1`;
    });
  }
})();
