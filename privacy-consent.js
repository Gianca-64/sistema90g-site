const GA_ID = 'G-G5DFNDR00';
const CONSENT_KEY = 's90g_cookie_consent';

function loadAnalytics() {
  if (window.s90gAnalyticsLoaded) {
    return;
  }

  window.s90gAnalyticsLoaded = true;
  window.gtag('consent', 'update', {
    'analytics_storage': 'granted',
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied'
  });
  window.gtag('config', GA_ID, {
    anonymize_ip: true
  });
}

function denyAnalytics() {
  if (typeof window.gtag === 'function') {
    window.gtag('consent', 'update', {
      'analytics_storage': 'denied',
      'ad_storage': 'denied',
      'ad_user_data': 'denied',
      'ad_personalization': 'denied'
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
    denyAnalytics();
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
      } else {
        denyAnalytics();
      }
    });
  });
});
