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
    if (meta) {
      meta.textContent = '';
      meta.append('Analisi di ');
      const author = document.createElement('a');
      author.href = 'chi-e-sistema90g.html';
      author.textContent = 'Gian Carlo Primo';
      meta.append(author, ' · 16 casi pubblicati · Aggiornato il 4 luglio 2026');
    }
  }

  const collectionTitle = collection.querySelector('.premium-copy h2');
  if (collectionTitle) collectionTitle.textContent = 'Sedici criticità diverse, ciascuna legata a una decisione reale.';

  const row = document.createElement('div');
  row.className = 'premium-three cases';
  const article = document.createElement('article');
  const image = document.createElement('img');
  image.className = 'case-card-image';
  image.src = 'images/final/case-16-two-apartments-access.svg?v=20260704-case16b';
  image.alt = 'Planimetria divisa in due appartamenti con due cucine e tre bagni';
  const category = document.createElement('span');
  category.textContent = 'Divisione immobiliare';
  const heading = document.createElement('h3');
  heading.textContent = 'Due appartamenti: prima dei corridoi, dove vanno cucine e bagni?';
  const summary = document.createElement('p');
  summary.textContent = 'Due cucine e tre bagni possono decidere la distribuzione più dei metri apparentemente persi.';
  const link = document.createElement('a');
  link.className = 'text-link';
  link.href = 'caso-due-appartamenti-accessi-disimpegni.html';
  link.textContent = 'Leggi il caso';
  article.append(image, category, heading, summary, link);
  row.appendChild(article);

  const finalLink = collection.querySelector(':scope > p:last-of-type');
  if (finalLink) collection.insertBefore(row, finalLink);
  else collection.appendChild(row);

  const description = document.querySelector('meta[name="description"]');
  if (description) description.content = 'Sedici casi pratici analizzati da Sistema 90G: problemi nascosti in cucine, planimetrie, open space, camere e preventivi.';
})();
