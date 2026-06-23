const GA_ID = 'G-G5D6FNDR00';
const CONSENT_KEY = 's90g_cookie_consent';

function loadAnalytics() {
  if (window.s90gAnalyticsLoaded) return;
  window.s90gAnalyticsLoaded = true;
  window.gtag('consent', 'update', {
    analytics_storage: 'granted',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });
  window.gtag('config', GA_ID);
}

function denyAnalytics() {
  if (typeof window.gtag === 'function') {
    window.gtag('consent', 'update', {
      analytics_storage: 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied'
    });
  }
}

function hideCookieBanner(banner) { if (banner) banner.setAttribute('hidden', ''); }
function showCookieBanner(banner) { if (banner) banner.removeAttribute('hidden'); }
function saveConsent(choice) { window.localStorage.setItem(CONSENT_KEY, choice); }

function trackWhatsAppLead(link) {
  const accepted = window.localStorage.getItem(CONSENT_KEY) === 'accepted';
  if (!accepted || typeof window.gtag !== 'function') return;
  window.gtag('event', 'whatsapp_lead', {
    event_category: 'lead',
    link_url: link.href,
    link_text: link.textContent.trim(),
    transport_type: 'beacon'
  });
}

function injectImageRepairStyles() {
  if (document.getElementById('image-repair-styles')) return;
  const style = document.createElement('style');
  style.id = 'image-repair-styles';
  style.textContent = `
    .premium-hero .premium-image::before,
    .premium-hero .premium-image::after {
      display: none !important;
      content: none !important;
    }
    .premium-hero .premium-image img {
      display: block;
      width: 100%;
      aspect-ratio: 16 / 9;
      object-fit: cover;
    }
  `;
  document.head.appendChild(style);
}

function applyDedicatedPageImages() {
  const pageImages = {
    '/controllo-progetto-cucina.html': 'images/hero-controllo-progetto-cucina.svg?v=20260623e',
    '/analisi-preventivo-cucina.html': 'images/hero-analisi-preventivo-cucina.svg?v=20260623e',
    '/verifica-planimetria-distribuzione-casa.html': 'images/hero-verifica-planimetria-casa.svg?v=20260623e',
    '/scelta-finiture-casa.html': 'images/hero-scelta-finiture-casa.svg?v=20260623e',
    '/casi-analizzati.html': 'images/caso-lavastoviglie.jpg?v=20260623f',
    '/agenzie-immobiliari.html': 'images/agenzie-immobiliari-sopralluogo.jpg?v=20260623f'
  };
  const imagePath = pageImages[window.location.pathname];
  if (!imagePath) return;
  const heroImage = document.querySelector('.premium-hero .premium-image img');
  if (heroImage) heroImage.src = imagePath;
}

function applyAgencySecondaryImage() {
  if (window.location.pathname !== '/agenzie-immobiliari.html') return;
  const secondaryImage = document.querySelector('.premium-split .premium-image img');
  if (secondaryImage) {
    secondaryImage.src = 'images/agenzie-immobiliari-analisi.jpg?v=20260623f';
    secondaryImage.alt = 'Analisi commerciale di un immobile con planimetria, fotografie e documenti';
  }
}

function injectEconomicValueStyles() {
  if (document.getElementById('economic-value-styles')) return;
  const style = document.createElement('style');
  style.id = 'economic-value-styles';
  style.textContent = `
    .economic-value-section { padding: 72px 0; }
    .economic-value-section .economic-intro { max-width: 880px; }
    .economic-value-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px; margin-top: 30px; }
    .economic-value-grid article { padding: 24px; border: 1px solid rgba(22, 43, 35, .14); border-radius: 18px; background: #fff; }
    .economic-value-grid h3 { margin: 0 0 10px; font-size: 1.08rem; }
    .economic-value-grid p { margin: 0; }
    .economic-value-closing { margin-top: 28px; max-width: 880px; font-weight: 700; }
    .service-value-block { padding: 56px 0; }
    .service-value-block .service-value-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; margin-top: 26px; }
    .service-value-block article { padding: 22px; border-radius: 16px; background: rgba(31,122,79,.06); border: 1px solid rgba(31,122,79,.14); }
    .service-value-block h3 { margin: 0 0 8px; font-size: 1rem; }
    .service-value-block p { margin: 0; }
    @media (max-width: 900px) {
      .economic-value-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .service-value-block .service-value-grid { grid-template-columns: 1fr; }
    }
    @media (max-width: 620px) {
      .economic-value-section, .service-value-block { padding: 48px 0; }
      .economic-value-grid { grid-template-columns: 1fr; gap: 14px; }
      .economic-value-grid article, .service-value-block article { padding: 20px; }
    }
  `;
  document.head.appendChild(style);
}

function findSectionByHeading(text) {
  const heading = [...document.querySelectorAll('h2')].find((item) => item.textContent.trim().includes(text));
  return heading ? heading.closest('section') : null;
}

function addHomeEconomicValueSection() {
  const isHome = window.location.pathname === '/' || window.location.pathname.endsWith('/index.html');
  if (!isHome || document.getElementById('economic-value')) return;

  const section = document.createElement('section');
  section.className = 'premium-section economic-value-section';
  section.id = 'economic-value';
  section.innerHTML = `
    <div class="container">
      <div class="premium-copy wide economic-intro">
        <p class="eyebrow">Prima che diventi una spesa</p>
        <h2>Quanto può costare scoprirlo dopo?</h2>
        <p>Prima dell’ordine, modificare una scelta può significare correggere un disegno.<br>Dopo l’ordine può significare cambiare un modulo, rifare un top, spostare un impianto, aggiungere lavorazioni o accettare una soluzione scomoda.<br>Sistema90G interviene quando il problema è ancora una decisione, non una spesa già sostenuta.</p>
      </div>
      <div class="economic-value-grid">
        <article><h3>Elementi da modificare o rifare</h3><p>Moduli, top, pannelli, ante o componenti incompatibili con misure e aperture reali.</p></article>
        <article><h3>Lavori aggiuntivi</h3><p>Prese, scarichi, attacchi, pareti o rivestimenti da correggere quando il progetto è già avanzato.</p></article>
        <article><h3>Costi non chiariti</h3><p>Accessori, lavorazioni, montaggi o componenti indispensabili non evidenziati chiaramente nel preventivo.</p></article>
        <article><h3>Problemi che restano</h3><p>Passaggi scomodi, aperture che interferiscono, poco contenimento o spazi belli nel render ma difficili da usare.</p></article>
      </div>
      <p class="economic-value-closing">Il controllo costa una piccola parte rispetto a ciò che può costare correggere una scelta quando mobili e lavori sono già stati avviati.</p>
    </div>`;

  const servicesSection = findSectionByHeading('Scegli il controllo adatto');
  const anchor = servicesSection || findSectionByHeading('Non guardiamo solo l’estetica');
  if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(section, anchor);
  else document.querySelector('main')?.appendChild(section);
}

function getServiceValueContent(pathname) {
  const blocks = {
    '/controllo-progetto-cucina.html': {
      check: 'Il servizio controlla disposizione, misure, aperture, elettrodomestici, piano utile e uso quotidiano prima dell’ordine.',
      consequence: 'Una criticità scoperta prima dell’ordine può richiedere solo una correzione al progetto. La stessa criticità scoperta dopo può coinvolgere mobili già prodotti, top, impianti o montaggio.',
      comparison: 'Il controllo non elimina ogni rischio, ma aiuta a chiarire i punti critici quando sono ancora modificabili.'
    },
    '/verifica-planimetria-distribuzione-casa.html': {
      check: 'La verifica controlla distribuzione, passaggi, aperture, contenimento e relazione tra gli ambienti prima di demolizioni, impianti e finiture.',
      consequence: 'Un conflitto scoperto tardi può richiedere modifiche a pareti, porte, impianti o lavorazioni già avviate, oppure lasciare un compromesso difficile da correggere.',
      comparison: 'Il costo del controllo riguarda una decisione che può coinvolgere più ambienti e diverse lavorazioni della casa.'
    },
    '/analisi-preventivo-cucina.html': {
      check: 'L’analisi controlla cosa è incluso, cosa manca, quali voci sono poco chiare e quali componenti possono cambiare il costo finale.',
      consequence: 'Il prezzo iniziale non sempre coincide con il costo finale. Elementi esclusi, lavorazioni aggiuntive e componenti indispensabili possono emergere quando la scelta è già stata fatta.',
      comparison: 'L’analisi serve a chiarire il contenuto economico della proposta prima della firma, senza promettere il prezzo più basso.'
    },
    '/scelta-finiture-casa.html': {
      check: 'La verifica controlla coerenza tra materiali, luce reale, manutenzione e continuità tra cucina e ambienti collegati prima dell’ordine.',
      consequence: 'Una scelta poco adatta scoperta dopo può significare sostituire materiali già acquistati, rifare una superficie o accettare un risultato difficile da correggere.',
      comparison: 'Il controllo aiuta a valutare la scelta quando campioni e materiali possono ancora essere confrontati e modificati.'
    }
  };
  return blocks[pathname];
}

function addServiceEconomicValueBlock() {
  const content = getServiceValueContent(window.location.pathname);
  if (!content || document.getElementById('service-economic-value')) return;
  const section = document.createElement('section');
  section.className = 'premium-section service-value-block';
  section.id = 'service-economic-value';
  section.innerHTML = `
    <div class="container">
      <div class="premium-copy wide">
        <p class="eyebrow">Valore del controllo</p>
        <h2>Cosa può succedere se emerge dopo</h2>
      </div>
      <div class="service-value-grid">
        <article><h3>Cosa controlla</h3><p>${content.check}</p></article>
        <article><h3>Se emerge tardi</h3><p>${content.consequence}</p></article>
        <article><h3>Perché farlo prima</h3><p>${content.comparison}</p></article>
      </div>
    </div>`;
  const hero = document.querySelector('.premium-hero');
  if (hero?.parentNode) hero.parentNode.insertBefore(section, hero.nextSibling);
}

function correctEconomicClaims() {
  const replacements = [
    ['Sistema 90G verifica proposte, preventivi, planimetrie e redistribuzioni degli ambienti per capire se rispondono alle tue esigenze e per individuare errori che dopo possono costare tempo, soldi e nervi.', 'Sistema90G controlla progetto, preventivo e scelte prima che un dubbio diventi una modifica, una spesa aggiuntiva o un problema difficile da correggere.'],
    ['Cosa rischi di pagare o subire dopo.', 'Quali conseguenze pratiche o costi aggiuntivi possono emergere dopo.'],
    ['Prima di approvare il progetto o iniziare demolizioni e impianti, quando è ancora possibile correggere la disposizione senza costi aggiuntivi.', 'Prima di approvare il progetto o iniziare demolizioni e impianti, quando una correzione può ancora essere valutata prima di coinvolgere lavori già avviati.']
  ];
  document.querySelectorAll('p, h3').forEach((node) => {
    const text = node.textContent.trim();
    const replacement = replacements.find(([from]) => text === from);
    if (replacement) node.textContent = replacement[1];
  });
}

function buildNavigationLink(href, label) {
  const link = document.createElement('a');
  link.href = href;
  link.textContent = label;
  return link;
}

function applySiteNavigation() {
  const mainNav = document.querySelector('.main-nav');
  if (!mainNav) return;
  const isHome = window.location.pathname === '/' || window.location.pathname.endsWith('/index.html');
  if (isHome) {
    mainNav.replaceChildren(
      buildNavigationLink('#top', 'Home'),
      buildNavigationLink('controllo-progetto-cucina.html', 'Cucina'),
      buildNavigationLink('verifica-planimetria-distribuzione-casa.html', 'Planimetria'),
      buildNavigationLink('analisi-preventivo-cucina.html', 'Preventivo'),
      buildNavigationLink('scelta-finiture-casa.html', 'Finiture'),
      buildNavigationLink('render-fotorealistici-interni.html', 'Render'),
      buildNavigationLink('agenzie-immobiliari.html', 'Agenzie'),
      buildNavigationLink('chi-e-sistema90g.html', 'Chi sono'),
      buildNavigationLink('#contatto', 'Invia il caso')
    );
  }
}

function addAboutLinkToFooter() {
  const footerLinks = document.querySelector('.footer-links');
  if (!footerLinks) return;
  if (!footerLinks.querySelector('a[href="agenzie-immobiliari.html"]')) {
    footerLinks.prepend(buildNavigationLink('agenzie-immobiliari.html', 'Agenzie immobiliari'));
  }
  if (!footerLinks.querySelector('a[href="render-fotorealistici-interni.html"]')) {
    footerLinks.prepend(buildNavigationLink('render-fotorealistici-interni.html', 'Render fotorealistici'));
  }
  if (!footerLinks.querySelector('a[href="chi-e-sistema90g.html"]')) {
    footerLinks.prepend(buildNavigationLink('chi-e-sistema90g.html', 'Chi c’è dietro Sistema 90G'));
  }
}

function addDeliverySection() {
  const isHome = window.location.pathname === '/' || window.location.pathname.endsWith('/index.html');
  if (!isHome || document.getElementById('consegna')) return;
  const faqSection = document.getElementById('faq');
  if (!faqSection) return;
  const section = document.createElement('section');
  section.className = 'premium-section';
  section.id = 'consegna';
  section.innerHTML = `
    <div class="container">
      <div class="premium-copy wide">
        <p class="eyebrow">Consegna e tempi</p>
        <h2>Prima del pagamento sai cosa ricevi, in quale formato e quando sarà pronto.</h2>
        <p>La data di consegna viene comunicata dopo aver verificato che il materiale sia sufficiente e prima della conferma. I tempi dipendono dalla complessità del caso, non da una promessa standard uguale per tutti.</p>
      </div>
      <div class="premium-three">
        <article><span>Formato</span><h3>Analisi scritta e consultabile.</h3><p>Ricevi un documento chiaro con criticità, conseguenze pratiche, punti da chiarire e priorità decisionali. Non sei obbligato a partecipare a una call.</p></article>
        <article><span>Tempi</span><h3>Concordati prima di iniziare.</h3><p>La consegna parte soltanto quando il materiale è completo, il servizio è confermato e il pagamento è ricevuto.</p></article>
        <article><span>Confini</span><h3>Nessuna falsa verifica tecnica.</h3><p>Quando servono controlli edilizi, strutturali, impiantistici o misure in cantiere, vengono indicati come verifiche da affidare ai professionisti competenti.</p></article>
      </div>
    </div>`;
  faqSection.parentNode.insertBefore(section, faqSection);
}

function injectMobileStickyStyles() {
  if (document.getElementById('mobile-sticky-cta-styles')) return;
  const style = document.createElement('style');
  style.id = 'mobile-sticky-cta-styles';
  style.textContent = `
    .mobile-sticky-cta { display: none; }
    @media (max-width: 680px) {
      body { padding-bottom: 84px; }
      .mobile-sticky-cta { position: fixed; left: 12px; right: 12px; bottom: calc(12px + env(safe-area-inset-bottom)); z-index: 999; display: block; }
      .mobile-sticky-cta a { display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: 58px; padding: 14px 18px; border-radius: 18px; background: #1f7a4f; color: #ffffff; text-decoration: none; box-shadow: 0 16px 42px rgba(7, 19, 26, 0.28); border: 1px solid rgba(255,255,255,0.18); }
      .mobile-sticky-cta span { font-size: 12px; text-transform: uppercase; letter-spacing: .08em; opacity: .8; }
      .mobile-sticky-cta strong { font-size: 17px; }
      .cookie-banner:not([hidden]) ~ .mobile-sticky-cta { display: none; }
    }
  `;
  document.head.appendChild(style);
}

function addMobileStickyCta() {
  if (document.querySelector('.mobile-sticky-cta')) return;
  const sourceLink = document.querySelector('a[data-track-whatsapp]');
  if (!sourceLink) return;
  const wrapper = document.createElement('div');
  wrapper.className = 'mobile-sticky-cta';
  const link = document.createElement('a');
  link.href = sourceLink.href;
  link.target = '_blank';
  link.rel = 'noopener';
  link.dataset.trackWhatsapp = '';
  link.setAttribute('aria-label', 'Invia il caso su WhatsApp');
  link.innerHTML = '<span aria-hidden="true">WhatsApp</span><strong>Invia il caso</strong>';
  wrapper.appendChild(link);
  document.body.appendChild(wrapper);
}

document.addEventListener('DOMContentLoaded', () => {
  injectImageRepairStyles();
  injectEconomicValueStyles();
  applyDedicatedPageImages();
  applyAgencySecondaryImage();
  correctEconomicClaims();
  addHomeEconomicValueSection();
  addServiceEconomicValueBlock();
  applySiteNavigation();
  addAboutLinkToFooter();
  addDeliverySection();
  injectMobileStickyStyles();
  addMobileStickyCta();

  const banner = document.getElementById('cookie-banner');
  const savedChoice = window.localStorage.getItem(CONSENT_KEY);
  if (savedChoice === 'accepted') {
    hideCookieBanner(banner);
    loadAnalytics();
  } else if (savedChoice === 'rejected') {
    hideCookieBanner(banner);
    denyAnalytics();
  } else {
    showCookieBanner(banner);
  }

  document.querySelectorAll('[data-cookie-choice]').forEach((button) => {
    button.addEventListener('click', () => {
      const accepted = button.dataset.cookieChoice === 'accept';
      saveConsent(accepted ? 'accepted' : 'rejected');
      hideCookieBanner(banner);
      if (accepted) loadAnalytics(); else denyAnalytics();
    });
  });

  document.querySelectorAll('[data-cookie-settings]').forEach((control) => {
    control.addEventListener('click', (event) => {
      event.preventDefault();
      showCookieBanner(banner);
    });
  });

  document.querySelectorAll('[data-track-whatsapp]').forEach((link) => {
    link.addEventListener('click', () => trackWhatsAppLead(link));
  });
});