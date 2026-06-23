const GA_ID = 'G-G5D6FNDR00';
const CONSENT_KEY = 's90g_cookie_consent';

function loadAnalytics() {
  if (window.s90gAnalyticsLoaded) {
    return;
  }

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

function hideCookieBanner(banner) {
  if (banner) {
    banner.setAttribute('hidden', '');
  }
}

function showCookieBanner(banner) {
  if (banner) {
    banner.removeAttribute('hidden');
  }
}

function saveConsent(choice) {
  window.localStorage.setItem(CONSENT_KEY, choice);
}

function trackWhatsAppLead(link) {
  const accepted = window.localStorage.getItem(CONSENT_KEY) === 'accepted';

  if (!accepted || typeof window.gtag !== 'function') {
    return;
  }

  window.gtag('event', 'whatsapp_lead', {
    event_category: 'lead',
    link_url: link.href,
    link_text: link.textContent.trim(),
    transport_type: 'beacon'
  });
}

function applyDedicatedPageImages() {
  const pageImages = {
    '/controllo-progetto-cucina.html': 'images/hero-controllo-progetto-cucina.svg?v=20260623a',
    '/analisi-preventivo-cucina.html': 'images/hero-analisi-preventivo-cucina.svg?v=20260623a',
    '/verifica-planimetria-distribuzione-casa.html': 'images/hero-verifica-planimetria-casa.svg?v=20260623a',
    '/scelta-finiture-casa.html': 'images/hero-scelta-finiture-casa.svg?v=20260623a'
  };

  const imagePath = pageImages[window.location.pathname];
  if (!imagePath) {
    return;
  }

  document.querySelectorAll('img[src*="90G-hero-v1-open-space-vissuto.png"]').forEach((image) => {
    image.src = imagePath;
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
  if (!mainNav) {
    return;
  }

  const isHome = window.location.pathname === '/' || window.location.pathname.endsWith('/index.html');

  if (isHome) {
    mainNav.replaceChildren(
      buildNavigationLink('#top', 'Home'),
      buildNavigationLink('controllo-progetto-cucina.html', 'Cucina'),
      buildNavigationLink('verifica-planimetria-distribuzione-casa.html', 'Planimetria'),
      buildNavigationLink('analisi-preventivo-cucina.html', 'Preventivo'),
      buildNavigationLink('scelta-finiture-casa.html', 'Finiture'),
      buildNavigationLink('chi-e-sistema90g.html', 'Chi sono'),
      buildNavigationLink('#contatto', 'Invia il caso')
    );
  }
}

function addAboutLinkToFooter() {
  const footerLinks = document.querySelector('.footer-links');
  if (footerLinks && !footerLinks.querySelector('a[href="chi-e-sistema90g.html"]')) {
    footerLinks.prepend(buildNavigationLink('chi-e-sistema90g.html', 'Chi c’è dietro Sistema 90G'));
  }
}

document.addEventListener('DOMContentLoaded', () => {
  applyDedicatedPageImages();
  applySiteNavigation();
  addAboutLinkToFooter();

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

      if (accepted) {
        loadAnalytics();
      } else {
        denyAnalytics();
      }
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
