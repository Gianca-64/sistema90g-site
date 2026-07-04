(() => {
  const OFFICIAL_EMAIL = 'sistema90g@icloud.com';

  document.querySelectorAll('a[href^="mailto:"]').forEach(link => {
    link.setAttribute('href', `mailto:${OFFICIAL_EMAIL}`);
    if (link.textContent.includes('@')) {
      link.textContent = OFFICIAL_EMAIL;
    }
  });

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const textNodes = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode);
  textNodes.forEach(node => {
    node.nodeValue = node.nodeValue
      .replace(/info@sistema90g\.it/gi, OFFICIAL_EMAIL)
      .replace(/sistema90g@sistema90g\.it/gi, OFFICIAL_EMAIL);
  });

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

    window.addEventListener('resize', () => {
      if (window.innerWidth > 820) close();
    });

    const current = location.pathname.split('/').pop() || 'index.html';
    nav.querySelectorAll('a[href]').forEach(link => {
      if (link.getAttribute('href').split('#')[0] === current) {
        link.setAttribute('aria-current', 'page');
      }
    });
  }

  const page = location.pathname.split('/').pop() || 'index.html';
  const version = '20260704-unique-visuals1';
  const heroMap = {
    'progetto-da-zero.html': ['hero-project-zero-unique.svg', 'Progetto da zero: planimetria, campioni e proposta in sviluppo'],
    'casi-analizzati.html': ['hero-cases-method-unique.svg', 'Metodo di analisi dei casi con percorsi, aperture e funzioni in relazione'],
    'caso-cabina-armadio-camera-irregolare.html': ['case-14-wardrobe-room-unique.svg', 'Camera irregolare con letto, percorso e zona guardaroba'],
    'caso-bagno-lavatrice-dieci-centimetri.html': ['case-13-bath-laundry-unique.svg', 'Bagno compatto con lavanderia e apertura da verificare']
  };

  const hero = heroMap[page];
  if (hero) {
    const section = document.querySelector('main .premium-hero .container');
    if (section) {
      let figure = section.querySelector('figure.premium-image');
      if (!figure) {
        figure = document.createElement('figure');
        figure.className = 'premium-image';
        section.prepend(figure);
      }
      let image = figure.querySelector('img');
      if (!image) {
        image = document.createElement('img');
        figure.appendChild(image);
      }
      image.src = `images/final/${hero[0]}?v=${version}`;
      image.alt = hero[1];
      image.removeAttribute('srcset');
    }
  }

  if (page === 'casi-analizzati.html') {
    const cardMap = {
      'caso-cabina-armadio-camera-irregolare.html': ['case-14-wardrobe-room-unique.svg', 'Camera irregolare con possibile zona guardaroba'],
      'caso-bagno-lavatrice-dieci-centimetri.html': ['case-13-bath-laundry-unique.svg', 'Bagno compatto con lavanderia e apertura da verificare']
    };

    document.querySelectorAll('article').forEach(article => {
      const link = article.querySelector('a.text-link[href]');
      const image = article.querySelector('img.case-card-image');
      if (!link || !image) return;
      const target = link.getAttribute('href').split('#')[0];
      const visual = cardMap[target];
      if (!visual) return;
      image.src = `images/final/${visual[0]}?v=${version}`;
      image.alt = visual[1];
      image.removeAttribute('srcset');
    });
  }
})();