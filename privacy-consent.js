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

document.addEventListener('DOMContentLoaded', () => {
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
