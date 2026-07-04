(() => {
  const page = location.pathname.split('/').pop() || 'index.html';
  if (page !== 'casi-analizzati.html') return;

  const collection = document.querySelector('#raccolta .container');
  if (!collection || collection.querySelector('a[href="caso-due-appartamenti-accessi-disimpegni.html"]')) return;

  const hero = document.querySelector('.premium-hero .premium-copy');
  if (hero) {
    const intro = hero.querySelector('h1 + p');
    if (intro) intro.textContent = 'Sedici casi anonimizzati e semplificati, con scene concrete, criticità, conseguenze e limiti dichiarati.';
    const meta = hero.querySelector('.case-meta');
    if (meta) meta.innerHTML = 'Analisi di <a href="chi-e-sistema90g.html">Gian Carlo Primo</a> · 16 casi pubblicati · Aggiornato il 4 luglio 2026';
  }

  const collectionTitle = collection.querySelector('.premium-copy h2');
  if (collectionTitle) collectionTitle.textContent = 'Sedici criticità diverse, ciascuna legata a una decisione reale.';

  const row = document.createElement('div');
  row.className = 'premium-three cases';
  row.innerHTML = '<article><img class="case-card-image" src="images/final/case-16-two-apartments-access.svg?v=20260704-case16" alt="Planimetria divisa in due appartamenti con accessi e disimpegno da verificare"><span>Divisione immobiliare</span><h3>Due appartamenti: il corridoio è davvero spazio perso?</h3><p>Prima di eliminarlo va verificato se serve a rendere indipendenti i due accessi.</p><a class="text-link" href="caso-due-appartamenti-accessi-disimpegni.html">Leggi il caso</a></article>';

  const finalLink = collection.querySelector(':scope > p:last-of-type');
  if (finalLink) collection.insertBefore(row, finalLink);
  else collection.appendChild(row);

  const description = document.querySelector('meta[name="description"]');
  if (description) description.setAttribute('content', 'Sedici casi pratici analizzati da Sistema 90G: problemi nascosti in cucine, planimetrie, open space, camere e preventivi.');

  const structured = document.querySelector('script[type="application/ld+json"]');
  if (structured) {
    try {
      const data = JSON.parse(structured.textContent);
      if (data?.mainEntity?.['@type'] === 'ItemList') data.mainEntity.numberOfItems = 16;
      data.dateModified = '2026-07-04';
      structured.textContent = JSON.stringify(data);
    } catch (_) {}
  }
})();
