(() => {
  'use strict';

  function ensureBanner() {
    const existing = document.getElementById('cookie-banner');
    if (existing) return existing;

    const banner = document.createElement('section');
    banner.id = 'cookie-banner';
    banner.className = 's90g-consent-banner';
    banner.hidden = true;
    banner.setAttribute('role', 'region');
    banner.setAttribute('aria-labelledby', 's90g-consent-title');
    banner.innerHTML = `
      <div class="s90g-consent-copy">
        <strong id="s90g-consent-title">Privacy e cookie</strong>
        <p>Usiamo cookie tecnici necessari al funzionamento del sito. Solo con il tuo consenso attiviamo la misurazione statistica delle visite per capire quali contenuti sono utili.</p>
        <p class="s90g-consent-links"><a href="/privacy-policy.html">Privacy</a><a href="/cookie-policy.html">Cookie policy</a></p>
      </div>
      <div class="s90g-consent-actions">
        <button type="button" data-cookie-choice="reject">Rifiuta</button>
        <button type="button" class="primary" data-cookie-choice="accept">Accetta</button>
      </div>`;
    document.body.appendChild(banner);
    return banner;
  }

  function ensureSettingsLink() {
    if (document.querySelector('[data-cookie-settings]')) return;
    const links = document.querySelector('.s90g-footer-links,.footer-links');
    if (!links) return;
    const link = document.createElement('a');
    link.href = '#cookie-banner';
    link.dataset.cookieSettings = 'true';
    link.textContent = 'Gestisci cookie';
    links.appendChild(link);
  }

  ensureBanner();
  ensureSettingsLink();

  document.addEventListener('click', event => {
    const trigger = event.target.closest('[data-cookie-settings]');
    if (!trigger) return;
    requestAnimationFrame(() => {
      const banner = document.getElementById('cookie-banner');
      if (!banner || banner.hidden) return;
      banner.querySelector('[data-cookie-choice]')?.focus();
    });
  });
})();
