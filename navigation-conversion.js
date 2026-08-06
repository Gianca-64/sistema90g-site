(() => {
  'use strict';

  const CAMPAIGN_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  const PRIVATE_SERVICE_PAGES = new Set([
    'scelta-finiture-casa',
    'restyling-cucina-esistente',
    'controllo-mirato',
    'analisi-completa',
    'acquisto-assistito-cucina'
  ]);

  const NAV_LINKS = [
    ['services', 'Servizi cucina', '/servizi.html'],
    ['project', 'Verifica progetto', '/analisi-completa.html'],
    ['quote', 'Verifica preventivo', '/analisi-preventivo-cucina.html'],
    ['assisted', 'Acquisto assistito', '/acquisto-assistito-cucina.html'],
    ['problems', 'Problemi ed errori', '/problemi-errori-cucina.html'],
    ['cases', 'Casi reali', '/casi-cucina.html'],
    ['process', 'Come funziona', '/analisi-preventiva.html']
  ];

  const pageSlug = () => {
    const name = (location.pathname.split('/').pop() || 'index.html').replace(/\.html$/, '');
    return name === 'index' ? 'home' : name;
  };

  const activeKey = slug => {
    if (slug === 'servizi' || slug === 'controllo-mirato' || slug === 'scelta-finiture-casa' || slug === 'restyling-cucina-esistente') return 'services';
    if (slug === 'analisi-completa') return 'project';
    if (slug === 'analisi-preventivo-cucina') return 'quote';
    if (slug === 'acquisto-assistito-cucina') return 'assisted';
    if (slug === 'problemi-errori-cucina') return 'problems';
    if (slug === 'casi-cucina' || slug.startsWith('caso-')) return 'cases';
    if (slug === 'analisi-preventiva') return 'process';
    return '';
  };

  const inferRoleHint = slug => PRIVATE_SERVICE_PAGES.has(slug) ? 'private' : '';

  const inferContentType = slug => {
    if (slug.startsWith('caso-')) return 'case';
    if (slug === 'casi-cucina') return 'case-category';
    if (slug === 'problemi-errori-cucina' || slug === 'analisi-preventivo-cucina') return 'guide';
    if (slug === 'servizi' || PRIVATE_SERVICE_PAGES.has(slug)) return 'service';
    return 'page';
  };

  function campaignParams() {
    const current = new URL(location.href);
    const out = {};
    CAMPAIGN_KEYS.forEach(key => {
      const value = current.searchParams.get(key);
      if (value) out[key] = value;
    });
    return out;
  }

  function preserveCampaignParams(scope = document) {
    const params = campaignParams();
    if (!Object.keys(params).length) return;

    scope.querySelectorAll('a[href]').forEach(link => {
      const raw = link.getAttribute('href') || '';
      if (!raw || raw.startsWith('#') || raw.startsWith('mailto:') || raw.startsWith('tel:') || link.hasAttribute('data-no-campaign')) return;

      let target;
      try {
        target = new URL(raw, location.href);
      } catch {
        return;
      }

      if (target.origin !== location.origin) return;
      Object.entries(params).forEach(([key, value]) => target.searchParams.set(key, value));
      link.href = target.toString();
    });
  }

  function preparePathLinks(scope = document) {
    const current = new URL(location.href);
    const slug = pageSlug();
    const defaultRole = inferRoleHint(slug);

    scope.querySelectorAll('a[data-start-path]').forEach((link, index) => {
      const target = new URL(link.getAttribute('href') || '/analisi-preventiva.html#percorso', location.href);
      target.searchParams.set('source_page', link.dataset.sourcePage || slug);
      target.searchParams.set('content_type', link.dataset.contentType || inferContentType(slug));
      target.searchParams.set(
        'cta_position',
        link.dataset.ctaPosition || (link.closest('header') ? 'header' : (link.closest('footer') ? 'footer' : `inline-${index + 1}`))
      );

      if (link.dataset.service) target.searchParams.set('service_hint', link.dataset.service);
      const role = link.dataset.roleHint || defaultRole;
      if (role) target.searchParams.set('role_hint', role);
      if (link.dataset.caseId) target.searchParams.set('case_id', link.dataset.caseId);

      CAMPAIGN_KEYS.forEach(key => {
        const value = current.searchParams.get(key);
        if (value) target.searchParams.set(key, value);
      });

      link.href = target.toString();
    });
  }

  function normalizeActionLabels(scope = document) {
    scope.querySelectorAll('a[data-start-path]').forEach(link => {
      const text = (link.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase();
      if (
        text.includes('invia il tuo caso') ||
        text.includes('sottoponi il caso') ||
        text === 'valuta il caso' ||
        text.startsWith('parliamo del caso')
      ) {
        const arrow = link.querySelector('[aria-hidden="true"]');
        if (arrow) {
          const first = link.querySelector('span:not([aria-hidden])') || link.querySelector('span');
          if (first) first.textContent = 'Individua il servizio';
        } else {
          link.textContent = 'Individua il servizio →';
        }
      }
    });

    scope.querySelectorAll('a.s90g-link').forEach(link => {
      const text = (link.textContent || '').replace(/\s+/g, ' ').trim();
      if (!/^(Scopri|Approfondisci)\s*→?$/i.test(text)) return;
      const card = link.closest('article,.s90g-service-card,.s90g-prof-card');
      const title = card?.querySelector('h2,h3')?.textContent?.trim();
      link.textContent = title ? `Vedi ${title} →` : 'Vedi il servizio →';
    });
  }

  function buildNavigation() {
    const header = document.querySelector('.s90g-header');
    const nav = header?.querySelector('.s90g-nav');
    if (!header || !nav) return;

    const key = activeKey(pageSlug());
    nav.id = 's90g-main-navigation';
    nav.innerHTML = NAV_LINKS.map(([id, label, href]) => (
      `<a data-nav-key="${id}" href="${href}"${id === key ? ' aria-current="page"' : ''}>${label}</a>`
    )).join('');

    let toggle = header.querySelector('.s90g-menu-toggle');
    if (!toggle) {
      toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.className = 's90g-menu-toggle';
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-controls', nav.id);
      toggle.innerHTML = '<span>Menu</span><span aria-hidden="true">☰</span>';
      nav.before(toggle);
    }

    const setOpen = open => {
      header.classList.toggle('is-nav-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.querySelector('[aria-hidden="true"]').textContent = open ? '×' : '☰';
    };

    toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
    nav.addEventListener('click', event => {
      if (event.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && header.classList.contains('is-nav-open')) {
        setOpen(false);
        toggle.focus();
      }
    });
    document.addEventListener('click', event => {
      if (header.classList.contains('is-nav-open') && !header.contains(event.target)) setOpen(false);
    });

    const media = matchMedia('(min-width: 1181px)');
    const reset = () => {
      if (media.matches) setOpen(false);
    };
    media.addEventListener?.('change', reset);
    header.classList.add('s90g-nav-ready');
  }

  function addSkipLink() {
    if (document.querySelector('.s90g-skip-link')) return;
    const main = document.querySelector('main');
    if (!main) return;
    if (!main.id) main.id = 'contenuto-principale';

    const link = document.createElement('a');
    link.className = 's90g-skip-link';
    link.href = `#${main.id}`;
    link.textContent = 'Vai al contenuto principale';
    document.body.prepend(link);
  }

  function enhancePathLinks() {
    const role = inferRoleHint(pageSlug());
    if (!role) return;
    document.querySelectorAll('a[data-start-path]').forEach(link => {
      if (!link.dataset.roleHint) link.dataset.roleHint = role;
    });
  }

  function init() {
    addSkipLink();
    buildNavigation();
    enhancePathLinks();
    normalizeActionLabels();
    preparePathLinks();
    preserveCampaignParams();
    document.dispatchEvent(new CustomEvent('s90g:navigation-ready'));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init, { once: true });
  } else {
    init();
  }
})();