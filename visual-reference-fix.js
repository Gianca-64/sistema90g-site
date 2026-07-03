(() => {
  const current = location.pathname.split('/').pop() || 'index.html';
  const heroes = {
    'index.html': 'homepage-approvata.svg',
    'controllo-progetto-cucina.html': 'hero-cucina-conflitto-90g.jpg',
    'verifica-planimetria-distribuzione-casa.html': 'hero-planimetria-90g.jpg',
    'analisi-preventivo-cucina.html': 'hero-preventivo-90g.jpg',
    'casi-analizzati.html': 'hero-analisi-90g.jpg',
    'chi-e-sistema90g.html': 'hero-analisi-90g.jpg',
    'caso-lavastoviglie-passaggio-cucina.html': 'hero-cucina-conflitto-90g.jpg',
    'caso-ingresso-tavolo-living.html': 'hero-open-space-90g.jpg',
    'caso-cucina-piccola-tre-lati.html': 'hero-progetto-zero-90g.jpg',
    'caso-preventivo-cucina-sconto-valore.html': 'hero-preventivo-90g.jpg',
    'caso-isola-passaggi-cucina.html': 'hero-cucina-conflitto-90g.jpg',
    'caso-secondo-bagno-impianti-spazio.html': 'hero-analisi-90g.jpg',
    'caso-open-space-tv-divano-passaggi.html': 'hero-open-space-90g.jpg',
    'caso-lavello-sotto-finestra-aperture.html': 'hero-finiture-90g.jpg',
    'caso-scala-interna-terrazzo-planimetria.html': 'hero-planimetria-90g.jpg',
    'caso-open-space-percorso-centrale.html': 'hero-analisi-90g.jpg',
    'caso-terza-camera-zona-giorno.html': 'hero-planimetria-90g.jpg',
    'caso-cucina-profondita-75-angolo.html': 'hero-progetto-zero-90g.jpg',
    'caso-bagno-lavatrice-dieci-centimetri.html': 'hero-analisi-90g.jpg',
    'caso-cabina-armadio-camera-irregolare.html': 'hero-livelli-90g.jpg',
    'caso-divano-letto-soggiorno-tre-persone.html': 'hero-open-space-90g.jpg'
  };
  const cards = {
    'caso-lavastoviglie-passaggio-cucina.html': 'hero-cucina-conflitto-90g.jpg',
    'caso-ingresso-tavolo-living.html': 'hero-open-space-90g.jpg',
    'caso-cucina-piccola-tre-lati.html': 'hero-progetto-zero-90g.jpg',
    'caso-preventivo-cucina-sconto-valore.html': 'hero-preventivo-90g.jpg',
    'caso-isola-passaggi-cucina.html': 'hero-cucina-conflitto-90g.jpg',
    'caso-secondo-bagno-impianti-spazio.html': 'hero-analisi-90g.jpg',
    'caso-open-space-tv-divano-passaggi.html': 'hero-open-space-90g.jpg',
    'caso-lavello-sotto-finestra-aperture.html': 'hero-finiture-90g.jpg',
    'caso-scala-interna-terrazzo-planimetria.html': 'hero-planimetria-90g.jpg',
    'caso-open-space-percorso-centrale.html': 'hero-analisi-90g.jpg',
    'caso-terza-camera-zona-giorno.html': 'hero-planimetria-90g.jpg',
    'caso-cucina-profondita-75-angolo.html': 'hero-progetto-zero-90g.jpg',
    'caso-bagno-lavatrice-dieci-centimetri.html': 'hero-analisi-90g.jpg',
    'caso-cabina-armadio-camera-irregolare.html': 'hero-livelli-90g.jpg',
    'caso-divano-letto-soggiorno-tre-persone.html': 'hero-open-space-90g.jpg'
  };
  const hero = document.querySelector('main .premium-hero .premium-image img');
  if (hero && heroes[current]) hero.src = `images/${heroes[current]}?v=20260704-reference`;
  document.querySelectorAll('article').forEach(article => {
    const link = article.querySelector('a.text-link[href]');
    const image = article.querySelector('img.case-card-image');
    if (!link || !image) return;
    const target = link.getAttribute('href').split('#')[0];
    if (cards[target]) image.src = `images/${cards[target]}?v=20260704-reference`;
  });
})();
