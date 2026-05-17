const GA_ID = 'G-G5DFNDR00';
const CONSENT_KEY = 's90g_cookie_consent';

function loadAnalytics() {
  if (window.s90gAnalyticsLoaded) {
    return;
  }

  window.s90gAnalyticsLoaded = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() {
    window.dataLayer.push(arguments);
  };
  window.gtag('js', new Date());
  window.gtag('config', GA_ID, {
    anonymize_ip: true
  });

  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_ID}`;
  document.head.appendChild(script);
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

document.addEventListener('DOMContentLoaded', () => {
  const banner = document.getElementById('cookie-banner');
  const savedChoice = window.localStorage.getItem(CONSENT_KEY);

  if (savedChoice === 'accepted') {
    hideCookieBanner(banner);
    loadAnalytics();
    return;
  }

  if (savedChoice === 'rejected') {
    hideCookieBanner(banner);
    return;
  }

  showCookieBanner(banner);

  document.querySelectorAll('[data-cookie-choice]').forEach((button) => {
    button.addEventListener('click', () => {
      const accepted = button.dataset.cookieChoice === 'accept';
      window.localStorage.setItem(CONSENT_KEY, accepted ? 'accepted' : 'rejected');
      hideCookieBanner(banner);

      if (accepted) {
        loadAnalytics();
      }
    });
  });
});
