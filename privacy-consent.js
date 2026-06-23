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
    '/casi-analizzati.html': 'images/errori-reali-lavastoviglie.jpeg?v=20260623e'
  };
  const imagePath = pageImages[window.location.pathname];
  if (!imagePath) return;
  const heroImage = document.querySelector('.premium-hero .premium-image img');
  if (heroImage) heroImage.src = imagePath;
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
  applyDedicatedPageImages();
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
