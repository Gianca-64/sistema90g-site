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
    .service-price {
      display: block;
      margin: 10px 0 14px;
      font-size: clamp(1.7rem, 3vw, 2.4rem);
      font-weight: 750;
      line-height: 1;
    }
    .service-meta {
      margin-top: 14px;
      font-size: .94rem;
      opacity: .82;
    }
    .service-boundary {
      margin-top: 14px;
      padding-top: 14px;
      border-top: 1px solid rgba(20, 38, 48, .12);
      font-size: .94rem;
    }
    .social-proof-line {
      margin: 0 auto 34px;
      max-width: 760px;
      padding: 18px 22px;
      border: 1px solid rgba(20, 38, 48, .12);
      border-radius: 18px;
      text-align: center;
      background: rgba(255,255,255,.72);
    }
    .social-proof-line strong { display: block; font-size: 1.2rem; margin-bottom: 4px; }
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
      buildNavigationLink('#servizi', 'Servizi'),
      buildNavigationLink('casi-analizzati.html', 'Casi'),
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

function applyServiceArchitecture() {
  const isHome = window.location.pathname === '/' || window.location.pathname.endsWith('/index.html');
  if (!isHome) return;

  const services = document.getElementById('servizi');
  if (services) {
    services.innerHTML = `
      <div class="container">
        <div class="premium-copy wide">
          <p class="eyebrow">Tre livelli, una scelta più semplice</p>
          <h2>Non devi capire da solo quale servizio acquistare.</h2>
          <p>Invia il caso: dopo una valutazione iniziale gratuita ti indichiamo direttamente il livello corretto, con contenuti, esclusioni, prezzo e tempi chiari.</p>
        </div>
        <div class="social-proof-line">
          <strong>Oltre 60 casi reali analizzati</strong>
          <span>Cucine, preventivi, redistribuzioni e spazi difficili da interpretare.</span>
        </div>
        <div class="premium-three">
          <article>
            <span>01 · Un dubbio preciso</span>
            <h3>Controllo mirato</h3>
            <strong class="service-price">79 €</strong>
            <p>Per una domanda circoscritta su un solo ambiente o punto specifico. Individua la criticità principale, le conseguenze pratiche e ciò che va verificato prima di decidere.</p>
            <p class="service-boundary"><strong>Non comprende:</strong> controllo completo, nuova progettazione, varianti, revisioni o render.</p>
            <p class="service-meta"><strong>Consegna:</strong> entro 72 ore lavorative dal pagamento e dalla ricezione del materiale completo.</p>
          </article>
          <article>
            <span>02 · Prima di firmare o ordinare</span>
            <h3>Analisi completa</h3>
            <strong class="service-price">247 €</strong>
            <p>Per un progetto o una proposta già esistente. Controlla criticità, uso reale, elementi poco chiari e, se disponibile, il preventivo generale prima della decisione.</p>
            <p class="service-boundary"><strong>Non comprende:</strong> nuova progettazione, varianti distributive, rilievi, pratiche, esecutivi o assistenza continuativa.</p>
            <p class="service-meta"><strong>Consegna:</strong> entro 72 ore lavorative dal pagamento e dalla ricezione del materiale completo.</p>
          </article>
          <article>
            <span>03 · Quando serve ripensare tutto</span>
            <h3>Progetto da zero</h3>
            <strong class="service-price">597 €</strong>
            <p>Per una cucina, un ambiente o una zona definita da impostare partendo dalle esigenze reali. Comprende una proposta principale motivata e una revisione circoscritta.</p>
            <p class="service-boundary"><strong>Non comprende:</strong> varianti illimitate, render, rilievi, pratiche edilizie, computi, esecutivi o assistenza senza limite.</p>
            <p class="service-meta"><strong>Prima proposta:</strong> entro 5 giorni lavorativi dal pagamento e dalla ricezione del materiale completo.</p>
          </article>
        </div>
        <div class="premium-copy wide" style="margin-top:34px">
          <p><strong>Approfondimenti solo quando servono.</strong> Restyling, analisi dettagliata del preventivo, confronto tra proposte, finiture, revisioni, capitolato, varianti e render possono essere quotati separatamente. Il render è disponibile su richiesta con preventivo dedicato.</p>
        </div>
      </div>`;
  }

  const how = document.getElementById('come-funziona');
  if (how) {
    how.innerHTML = `
      <div class="container">
        <div class="premium-copy wide">
          <p class="eyebrow">Come funziona</p>
          <h2>Invii il caso. Individuiamo il livello corretto. Poi decidi.</h2>
        </div>
        <div class="premium-three">
          <article><span>1</span><h3>Invia il tuo caso</h3><p>Racconta cosa devi decidere e allega il materiale disponibile: fotografie, planimetria, progetto o preventivo.</p></article>
          <article><span>2</span><h3>Valutazione iniziale</h3><p>Verifichiamo quanto è ampia la richiesta, quale livello è adatto, quali materiali servono e se il caso rientra in Sistema90G.</p></article>
          <article><span>3</span><h3>Proposta chiara</h3><p>Ricevi servizio consigliato, contenuti, esclusioni, prezzo e tempi. Decidi liberamente se procedere.</p></article>
        </div>
        <div class="premium-copy wide" style="margin-top:28px">
          <p>La valutazione iniziale è gratuita, ma non è una consulenza: serve solo a individuare il livello corretto. Il lavoro inizia dopo conferma, pagamento e ricezione del materiale completo.</p>
          <a class="button button-primary" href="#contatto">Invia il tuo caso</a>
        </div>
      </div>`;
  }
}

function applyAgencyOffer() {
  if (window.location.pathname !== '/agenzie-immobiliari.html') return;
  if (document.getElementById('offerta-agenzie')) return;
  const faq = document.getElementById('faq');
  if (!faq) return;

  const section = document.createElement('section');
  section.className = 'premium-section';
  section.id = 'offerta-agenzie';
  section.innerHTML = `
    <div class="container">
      <div class="premium-copy wide">
        <p class="eyebrow">Servizio dedicato</p>
        <h2>Analisi immobile per agenzie</h2>
        <strong class="service-price">290 €</strong>
        <p>Una lettura indipendente dell’immobile per evidenziare punti di forza reali, limiti che possono frenare il compratore, obiezioni prevedibili e potenzialità da approfondire senza promettere trasformazioni non verificate.</p>
      </div>
      <div class="premium-three">
        <article><span>Comprende</span><h3>Analisi e indicazioni operative</h3><p>Distribuzione, criticità, punti di forza, obiezioni, potenzialità e indicazioni per presentazione, annuncio e visite.</p></article>
        <article><span>Non comprende</span><h3>Confini professionali chiari</h3><p>Non è una perizia, una stima, una verifica urbanistica, un progetto edilizio, un preventivo lavori o una garanzia di vendita.</p></article>
        <article><span>Tempi</span><h3>Entro 72 ore lavorative</h3><p>Il tempo decorre dal pagamento e dalla ricezione del materiale completo.</p></article>
      </div>
      <div class="premium-copy wide" style="margin-top:28px">
        <p>Render e visualizzazioni sono disponibili solo su richiesta, con preventivo separato.</p>
      </div>
    </div>`;
  faq.parentNode.insertBefore(section, faq);
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
        <h2>Il tempo parte solo quando il materiale è completo e il pagamento è ricevuto.</h2>
        <p>Controllo mirato e Analisi completa vengono consegnati entro 72 ore lavorative. Per il Progetto da zero, la prima proposta viene consegnata entro 5 giorni lavorativi.</p>
      </div>
      <div class="premium-three">
        <article><span>Formato</span><h3>Analisi scritta e consultabile.</h3><p>Ricevi un documento chiaro con criticità, conseguenze, punti da chiarire e priorità decisionali.</p></article>
        <article><span>Decorrenza</span><h3>Materiale completo e pagamento.</h3><p>Il conteggio non parte finché non sono disponibili tutti gli elementi necessari per lavorare correttamente.</p></article>
        <article><span>Confini</span><h3>Nessuna falsa verifica tecnica.</h3><p>I controlli edilizi, strutturali, impiantistici o in cantiere restano affidati ai professionisti competenti.</p></article>
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
  applyDedicatedPageImages();
  applyAgencySecondaryImage();
  applySiteNavigation();
  addAboutLinkToFooter();
  applyServiceArchitecture();
  applyAgencyOffer();
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