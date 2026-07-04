(() => {
  const page = location.pathname.split('/').pop() || 'index.html';
  if (page !== 'casi-analizzati.html') return;

  const collection = document.querySelector('#raccolta .container');
  if (!collection || collection.querySelector('a[href="caso-soggiorno-pianoforte-tavolo-divano-tv.html"]')) return;

  const hero = document.querySelector('.premium-hero .premium-copy');
  if (hero) {
    const intro = hero.querySelector('h1 + p');
    if (intro) intro.textContent = 'Diciassette casi anonimizzati e semplificati, con scene concrete, criticità, conseguenze e limiti dichiarati.';
    const meta = hero.querySelector('.case-meta');
    if (meta) {
      meta.textContent = '';
      meta.append('Analisi di ');
      const author = document.createElement('a');
      author.href = 'chi-e-sistema90g.html';
      author.textContent = 'Gian Carlo Primo';
      meta.append(author, ' · 17 casi pubblicati · Aggiornato il 4 luglio 2026');
    }
  }

  const collectionTitle = collection.querySelector('.premium-copy h2');
  if (collectionTitle) collectionTitle.textContent = 'Diciassette criticità diverse, ciascuna legata a una decisione reale.';

  const row = document.createElement('div');
  row.className = 'premium-three cases';
  const article = document.createElement('article');
  const image = document.createElement('img');
  image.className = 'case-card-image';
  image.src = 'images/final/case-17-living-piano.svg?v=20260704-case17';
  image.alt = 'Soggiorno con tavolo, divano, TV e pianoforte verticale';
  const category = document.createElement('span');
  category.textContent = 'Zona giorno';
  const heading = document.createElement('h3');
  heading.textContent = 'Il pianoforte entra, ma serve spazio anche davanti.';
  const summary = document.createElement('p');
  summary.textContent = 'In 4,35 × 3,80 metri tavolo, divano, TV e pianoforte possono contendersi la stessa fascia d’uso.';
  const link = document.createElement('a');
  link.className = 'text-link';
  link.href = 'caso-soggiorno-pianoforte-tavolo-divano-tv.html';
  link.textContent = 'Leggi il caso';
  article.append(image, category, heading, summary, link);
  row.appendChild(article);

  const finalLink = collection.querySelector(':scope > p:last-of-type');
  if (finalLink) collection.insertBefore(row, finalLink);
  else collection.appendChild(row);

  const description = document.querySelector('meta[name="description"]');
  if (description) description.content = 'Diciassette casi pratici analizzati da Sistema 90G: problemi nascosti in cucine, planimetrie, open space, camere e preventivi.';

  const structuredData = document.querySelector('script[type="application/ld+json"]');
  if (structuredData) {
    try {
      const data = JSON.parse(structuredData.textContent);
      if (data && data['@type'] === 'CollectionPage' && data.mainEntity) {
        data.mainEntity.numberOfItems = 17;
        data.dateModified = '2026-07-04';
        structuredData.textContent = JSON.stringify(data);
      }
    } catch (_) {}
  }
})();