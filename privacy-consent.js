const GA_ID = 'G-G5D6FNDR00';
const CONSENT_KEY = 's90g_cookie_consent';
const PUBLIC_PORTAL_URL = 'https://sistema90g-console.sistema90g.workers.dev/richiesta';
const WHATSAPP_CHAT_URL = 'https://wa.me/393275478485?text=Ciao%2C%20ho%20una%20domanda%20rapida%20su%20Sistema%2090G.';

function loadAnalytics() {
  if (window.s90gAnalyticsLoaded) return;
  window.s90gAnalyticsLoaded = true;
  if (typeof window.gtag !== 'function') return;
  window.gtag('consent', 'update', {
    analytics_storage: 'granted',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });
  window.gtag('config', GA_ID);
}

function denyAnalytics() {
  if (typeof window.gtag !== 'function') return;
  window.gtag('consent', 'update', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied'
  });
}

function hideCookieBanner(banner) { if (banner) banner.setAttribute('hidden', ''); }
function showCookieBanner(banner) { if (banner) banner.removeAttribute('hidden'); }
function saveConsent(choice) { window.localStorage.setItem(CONSENT_KEY, choice); }

function trackWhatsAppLead(link) {
  const accepted = window.localStorage.getItem(CONSENT_KEY) === 'accepted';
  if (!accepted || typeof window.gtag !== 'function') return;
  window.gtag('event', 'whatsapp_chat_open', {
    event_category: 'lead',
    link_url: link.href,
    link_text: link.textContent.trim(),
    transport_type: 'beacon'
  });
}

function trackPortalOpen(link) {
  const accepted = window.localStorage.getItem(CONSENT_KEY) === 'accepted';
  if (!accepted || typeof window.gtag !== 'function') return;
  window.gtag('event', 'public_portal_open', {
    event_category: 'lead',
    link_url: link.href,
    link_text: link.textContent.trim(),
    transport_type: 'beacon'
  });
}

function injectSiteStyles() {
  if (document.getElementById('s90g-runtime-styles')) return;
  const style = document.createElement('style');
  style.id = 's90g-runtime-styles';
  style.textContent = `
    .premium-hero .premium-image::before,
    .premium-hero .premium-image::after { display:none!important; content:none!important; }
    .premium-hero .premium-image img { display:block; width:100%; aspect-ratio:16/9; object-fit:cover; }
    .service-price { display:block; margin:10px 0 14px; font-size:clamp(1.7rem,3vw,2.4rem); font-weight:750; line-height:1; }
    .service-meta { margin-top:14px; font-size:.94rem; opacity:.82; }
    .service-boundary { margin-top:14px; padding-top:14px; border-top:1px solid rgba(20,38,48,.12); font-size:.94rem; }
    .service-card-link { display:inline-block; margin-top:16px; font-weight:700; }
    .social-proof-line { margin:0 auto 34px; max-width:760px; padding:18px 22px; border:1px solid rgba(20,38,48,.12); border-radius:18px; text-align:center; background:rgba(255,255,255,.72); }
    .social-proof-line strong { display:block; font-size:1.2rem; margin-bottom:4px; }
    .portal-chat-note { max-width:720px; margin:22px auto 0; font-size:.95rem; opacity:.86; }
    .whatsapp-chat { position:fixed; right:18px; bottom:calc(18px + env(safe-area-inset-bottom)); z-index:998; }
    .whatsapp-chat a { display:flex; align-items:center; gap:11px; min-height:54px; padding:10px 16px 10px 13px; border-radius:999px; background:#1f7a4f; color:#fff; text-decoration:none; box-shadow:0 16px 42px rgba(7,19,26,.28); border:1px solid rgba(255,255,255,.2); transition:transform .18s ease, box-shadow .18s ease; }
    .whatsapp-chat a:hover { transform:translateY(-2px); box-shadow:0 20px 48px rgba(7,19,26,.32); }
    .whatsapp-chat a:focus-visible { outline:3px solid rgba(31,122,79,.3); outline-offset:3px; }
    .whatsapp-chat svg { width:26px; height:26px; flex:0 0 auto; fill:currentColor; }
    .whatsapp-chat-copy { display:flex; flex-direction:column; align-items:flex-start; line-height:1.1; }
    .whatsapp-chat-copy span { font-size:10px; text-transform:uppercase; letter-spacing:.08em; opacity:.82; }
    .whatsapp-chat-copy strong { margin-top:3px; font-size:14px; }
    .cookie-banner:not([hidden]) ~ .whatsapp-chat { display:none; }
    @media (max-width:680px) {
      body { padding-bottom:78px; }
      .whatsapp-chat { right:12px; bottom:calc(12px + env(safe-area-inset-bottom)); }
      .whatsapp-chat a { min-height:52px; padding:10px 14px 10px 12px; }
      .whatsapp-chat-copy span { display:none; }
      .whatsapp-chat-copy strong { margin-top:0; font-size:14px; }
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
  if (!secondaryImage) return;
  secondaryImage.src = 'images/agenzie-immobiliari-analisi.jpg?v=20260623f';
  secondaryImage.alt = 'Analisi commerciale di un immobile con planimetria, fotografie e documenti';
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
  if (!isHome) return;
  mainNav.replaceChildren(
    buildNavigationLink('#top', 'Home'),
    buildNavigationLink('#servizi', 'Servizi'),
    buildNavigationLink('casi-analizzati.html', 'Casi'),
    buildNavigationLink('agenzie-immobiliari.html', 'Agenzie'),
    buildNavigationLink('chi-e-sistema90g.html', 'Chi sono'),
    buildNavigationLink('#contatto', 'Sottoponi il caso')
  );
}

function addFooterLinks() {
  const footerLinks = document.querySelector('.footer-links');
  if (!footerLinks) return;
  const links = [
    ['progetto-da-zero.html', 'Progetto da zero'],
    ['analisi-completa.html', 'Analisi completa'],
    ['controllo-mirato.html', 'Controllo mirato'],
    ['agenzie-immobiliari.html', 'Agenzie immobiliari'],
    ['render-fotorealistici-interni.html', 'Render fotorealistici'],
    ['chi-e-sistema90g.html', 'Chi c’è dietro Sistema 90G']
  ];
  links.forEach(([href, label]) => {
    if (!footerLinks.querySelector(`a[href="${href}"]`)) footerLinks.prepend(buildNavigationLink(href, label));
  });
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
          <h2>La profondità dell’analisi cambia in base alla decisione da proteggere.</h2>
          <p>Invia il caso: dopo una valutazione iniziale gratuita indichiamo il livello corretto, con contenuti, esclusioni, prezzo e tempi chiari.</p>
        </div>
        <div class="social-proof-line">
          <strong>Oltre 170 casi reali raccolti e analizzati</strong>
          <span>Cucine, preventivi, redistribuzioni e spazi difficili da interpretare.</span>
        </div>
        <div class="premium-three">
          <article>
            <span>01 · Un dubbio preciso</span>
            <h3>Controllo mirato</h3>
            <strong class="service-price">127 €</strong>
            <p>Per una domanda circoscritta o un punto specifico. Individua la criticità principale, le conseguenze pratiche e ciò che va chiarito prima di decidere.</p>
            <p class="service-boundary"><strong>Non comprende:</strong> controllo completo, nuova progettazione, varianti, revisioni o render.</p>
            <p class="service-meta"><strong>Consegna:</strong> entro 72 ore lavorative dal pagamento e dalla ricezione del materiale completo.</p>
            <a class="text-link service-card-link" href="controllo-mirato.html">Scopri il Controllo mirato</a>
          </article>
          <article>
            <span>02 · Prima di firmare o ordinare</span>
            <h3>Analisi completa</h3>
            <strong class="service-price">347 €</strong>
            <p>Per un progetto o una proposta già esistente. Mette in relazione criticità, uso reale, vincoli, decisioni aperte e possibili costi tardivi.</p>
            <p class="service-boundary"><strong>Non comprende:</strong> nuova progettazione, varianti complete, rilievi, pratiche, esecutivi o assistenza continuativa.</p>
            <p class="service-meta"><strong>Consegna:</strong> entro 72 ore lavorative dal pagamento e dalla ricezione del materiale completo.</p>
            <a class="text-link service-card-link" href="analisi-completa.html">Scopri l’Analisi completa</a>
          </article>
          <article>
            <span>03 · Quando serve ripensare tutto</span>
            <h3>Progetto da zero</h3>
            <strong class="service-price">797 €</strong>
            <p>Per una cucina, un ambiente o una zona definita da impostare partendo da esigenze, vincoli e uso reale. Comprende una proposta principale motivata e una revisione circoscritta.</p>
            <p class="service-boundary"><strong>Non comprende:</strong> varianti illimitate, render automatici, rilievi, pratiche edilizie, computi, esecutivi o assistenza senza limite.</p>
            <p class="service-meta"><strong>Prima proposta:</strong> entro 5 giorni lavorativi dal pagamento e dalla ricezione del materiale completo.</p>
            <a class="text-link service-card-link" href="progetto-da-zero.html">Scopri il Progetto da zero</a>
          </article>
        </div>
        <div class="premium-copy wide" style="margin-top:34px">
          <p><strong>Approfondimenti invariati e solo quando servono.</strong> Restyling, analisi dettagliata del preventivo, confronto tra proposte, finiture, revisioni, capitolato, varianti e render restano separati e vengono aggiunti soltanto quando il caso lo richiede.</p>
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
          <article><span>1</span><h3>Invia il tuo caso</h3><p>Racconta cosa devi decidere e allega fotografie, planimetria, progetto, render o preventivo.</p></article>
          <article><span>2</span><h3>Valutazione iniziale</h3><p>Verifichiamo ampiezza della richiesta, livello adatto, materiali necessari e coerenza con Sistema 90G.</p></article>
          <article><span>3</span><h3>Proposta chiara</h3><p>Ricevi servizio consigliato, contenuti, esclusioni, prezzo e tempi. Decidi liberamente se procedere.</p></article>
        </div>
        <div class="premium-copy wide" style="margin-top:28px">
          <p>La valutazione iniziale è gratuita, ma non è una consulenza: serve a individuare il livello corretto. Il lavoro inizia dopo conferma, pagamento e ricezione del materiale completo.</p>
          <a class="button button-primary" href="#contatto">Sottoponi il tuo caso</a>
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
        <p>Una lettura indipendente dell’immobile per evidenziare punti di forza reali, limiti, obiezioni prevedibili e potenzialità da approfondire.</p>
      </div>
      <div class="premium-three">
        <article><span>Comprende</span><h3>Analisi e indicazioni operative</h3><p>Distribuzione, criticità, punti di forza, obiezioni, potenzialità e indicazioni per presentazione, annuncio e visite.</p></article>
        <article><span>Non comprende</span><h3>Confini professionali chiari</h3><p>Non è una perizia, una stima, una verifica urbanistica, un progetto edilizio, un preventivo lavori o una garanzia di vendita.</p></article>
        <article><span>Tempi</span><h3>Entro 72 ore lavorative</h3><p>Il tempo decorre dal pagamento e dalla ricezione del materiale completo.</p></article>
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
        <h2>Il tempo parte quando il materiale è completo e il pagamento è ricevuto.</h2>
        <p>Controllo mirato e Analisi completa vengono consegnati entro 72 ore lavorative. Per il Progetto da zero, la prima proposta viene consegnata entro 5 giorni lavorativi.</p>
      </div>
      <div class="premium-three">
        <article><span>Formato</span><h3>Analisi scritta e consultabile.</h3><p>Ricevi un documento chiaro con criticità, conseguenze, punti da chiarire e priorità decisionali.</p></article>
        <article><span>Decorrenza</span><h3>Materiale completo e pagamento.</h3><p>Il conteggio non parte finché non sono disponibili tutti gli elementi necessari.</p></article>
        <article><span>Confini</span><h3>Nessuna falsa verifica tecnica.</h3><p>I controlli edilizi, strutturali, impiantistici o in cantiere restano affidati ai professionisti competenti.</p></article>
      </div>
    </div>`;
  faqSection.parentNode.insertBefore(section, faqSection);
}

function applyPublicPortalCta() {
  const section = document.getElementById('contatto');
  if (!section) return;
  const copy = section.querySelector('.premium-copy');
  if (!copy) return;
  copy.innerHTML = `
    <p class="eyebrow">Portale pubblico</p>
    <h2>Sottoponi il tuo caso in modo ordinato e completo.</h2>
    <p>Nel portale pubblico puoi descrivere cosa devi decidere e allegare foto, planimetrie, render, preventivi e altri documenti in un unico invio.</p>
    <p>La valutazione iniziale serve a verificare se il caso è adatto a Sistema 90G e a indicare il livello corretto. Non è una consulenza e non comporta obbligo di acquisto.</p>
    <p>Se decidi di procedere, ricevi un link personale riservato per consultare la proposta, accettarla, pagare, caricare i materiali, seguire lo stato del lavoro e scaricare la consegna.</p>
    <a class="button button-primary" data-track-portal href="${PUBLIC_PORTAL_URL}" target="_blank" rel="noopener">Apri il portale pubblico</a>
    <p class="portal-chat-note"><strong>Hai solo una domanda rapida?</strong> Usa la chat WhatsApp in basso a destra. Per inviare un caso completo usa sempre il portale.</p>
  `;
}

function addWhatsAppChat() {
  if (document.querySelector('.whatsapp-chat')) return;
  const wrapper = document.createElement('div');
  wrapper.className = 'whatsapp-chat';
  const link = document.createElement('a');
  link.href = WHATSAPP_CHAT_URL;
  link.target = '_blank';
  link.rel = 'noopener';
  link.dataset.trackWhatsapp = '';
  link.setAttribute('aria-label', 'Apri la chat WhatsApp per una domanda rapida');
  link.innerHTML = `
    <svg viewBox="0 0 32 32" aria-hidden="true">
      <path d="M19.11 17.45c-.27-.14-1.6-.79-1.85-.88-.25-.09-.43-.14-.61.14-.18.27-.7.88-.86 1.06-.16.18-.32.2-.59.07-.27-.14-1.14-.42-2.17-1.34-.8-.71-1.34-1.59-1.5-1.86-.16-.27-.02-.42.12-.55.12-.12.27-.32.41-.48.14-.16.18-.27.27-.45.09-.18.05-.34-.02-.48-.07-.14-.61-1.47-.84-2.01-.22-.53-.45-.46-.61-.47h-.52c-.18 0-.48.07-.73.34-.25.27-.95.93-.95 2.27s.98 2.63 1.11 2.81c.14.18 1.92 2.93 4.65 4.11.65.28 1.16.45 1.55.58.65.21 1.24.18 1.71.11.52-.08 1.6-.65 1.83-1.29.23-.64.23-1.19.16-1.29-.07-.11-.25-.18-.52-.32z"/>
      <path d="M16.03 3.2c-7.07 0-12.82 5.75-12.82 12.82 0 2.26.59 4.47 1.71 6.41L3.1 29.08l6.8-1.78a12.79 12.79 0 0 0 6.12 1.56h.01c7.07 0 12.82-5.75 12.82-12.82S23.1 3.2 16.03 3.2zm0 23.5h-.01c-1.91 0-3.79-.51-5.43-1.48l-.39-.23-4.04 1.06 1.08-3.94-.25-.4a10.61 10.61 0 0 1-1.63-5.67c0-5.88 4.79-10.67 10.68-10.67 5.88 0 10.67 4.79 10.67 10.68 0 5.88-4.79 10.66-10.68 10.66z"/>
    </svg>
    <span class="whatsapp-chat-copy"><span>Domande rapide</span><strong>Chat WhatsApp</strong></span>
  `;
  wrapper.appendChild(link);
  document.body.appendChild(wrapper);
}

document.addEventListener('DOMContentLoaded', () => {
  injectSiteStyles();
  applyDedicatedPageImages();
  applyAgencySecondaryImage();
  applySiteNavigation();
  addFooterLinks();
  applyServiceArchitecture();
  applyAgencyOffer();
  addDeliverySection();
  applyPublicPortalCta();
  addWhatsAppChat();

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

  document.querySelectorAll('[data-track-portal]').forEach((link) => {
    link.addEventListener('click', () => trackPortalOpen(link));
  });
});
