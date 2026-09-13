(() => {
  'use strict';

  const GA_ID =
    'G-G5D6FNDR00';

  const CONSENT_KEY =
    's90g_cookie_consent';

  const PORTAL_ORIGIN =
    'https://portale.sistema90g.it';

  const CAMPAIGN_KEYS = [
    'utm_source',
    'utm_medium',
    'utm_campaign',
    'utm_content',
    'utm_term',
  ];

  window.dataLayer =
    window.dataLayer || [];

  window.gtag =
    window.gtag ||
    function () {
      window.dataLayer.push(arguments);
    };

  window.gtag(
    'consent',
    'default',
    {
      analytics_storage: 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
    },
  );

  function loadAnalytics() {
    window.gtag(
      'consent',
      'update',
      {
        analytics_storage: 'granted',
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied',
      },
    );

    if (window.s90gAnalyticsLoaded) {
      return;
    }

    window.s90gAnalyticsLoaded = true;

    const script =
      document.createElement('script');

    script.async = true;

    script.src =
      'https://www.googletagmanager.com/gtag/js?id='
      + encodeURIComponent(GA_ID);

    script.dataset.s90gAnalytics = 'true';

    document.head.appendChild(script);

    window.gtag(
      'js',
      new Date(),
    );

    window.gtag(
      'config',
      GA_ID,
      {
        send_page_view: true,
      },
    );
  }

  function denyAnalytics() {
    window.gtag(
      'consent',
      'update',
      {
        analytics_storage: 'denied',
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied',
      },
    );
  }

  function saveConsent(value) {
    window.localStorage.setItem(
      CONSENT_KEY,
      value,
    );

    const secure =
      location.protocol === 'https:'
        ? '; Secure'
        : '';

    document.cookie =
      `${CONSENT_KEY}=${encodeURIComponent(value)}; `
      + 'Path=/; Domain=.sistema90g.it; '
      + 'Max-Age=31536000; SameSite=Lax'
      + secure;
  }

  function ensureCookieBanner() {
    let banner =
      document.getElementById(
        'cookie-banner',
      );

    if (banner) {
      return banner;
    }

    banner =
      document.createElement('aside');

    banner.id =
      'cookie-banner';

    banner.className =
      'cookie-banner';

    banner.hidden = true;

    banner.setAttribute(
      'aria-label',
      'Cookie preferences',
    );

    banner.innerHTML =
      '<div>'
      + '<strong>Cookies and measurement</strong>'
      + '<p>We use essential cookies and, only with your consent, '
      + 'anonymous statistical measurement of visits and use of the '
      + 'initial assessment journey.</p>'
      + '</div>'
      + '<div class="cookie-actions">'
      + '<button data-cookie-choice="accept" type="button">'
      + 'Accept'
      + '</button>'
      + '<button data-cookie-choice="reject" type="button">'
      + 'Reject'
      + '</button>'
      + '</div>';

    document.body.appendChild(
      banner,
    );

    return banner;
  }

  function ensureCookieSettings() {
    document
      .querySelectorAll(
        '.s90g-footer-links',
      )
      .forEach(footer => {
        if (
          footer.querySelector(
            '[data-cookie-settings]',
          )
        ) {
          return;
        }

        const link =
          document.createElement('a');

        link.href = '#';

        link.dataset.cookieSettings = '';

        link.textContent =
          'Cookie settings';

        footer.appendChild(link);
      });
  }

  function pageSlug() {
    if (
      location.pathname === '/en/'
      || location.pathname === '/en'
    ) {
      return 'home-en-gb';
    }

    const parts =
      location.pathname
        .split('/')
        .filter(Boolean);

    const name =
      parts.at(-1) || 'index.html';

    const slug =
      name.replace(
        /\.html$/,
        '',
      );

    return slug === 'index'
      ? 'home-en-gb'
      : `en-${slug}`;
  }

  function prepareJourneyLinks() {
    const current =
      new URL(location.href);

    document
      .querySelectorAll(
        'a[data-start-path]',
      )
      .forEach(
        (link, index) => {
          const raw =
            link.getAttribute('href')
            || '/en/how-it-works.html#submit';

          const target =
            new URL(
              raw,
              location.href,
            );

          target.searchParams.set(
            'source_page',
            link.dataset.sourcePage
              || pageSlug(),
          );

          target.searchParams.set(
            'content_type',
            link.dataset.contentType
              || 'page',
          );

          target.searchParams.set(
            'cta_position',
            link.dataset.ctaPosition
              || (
                link.closest('header')
                  ? 'header'
                  : `inline-${index + 1}`
              ),
          );

          CAMPAIGN_KEYS.forEach(
            key => {
              const value =
                current.searchParams.get(
                  key,
                );

              if (value) {
                target.searchParams.set(
                  key,
                  value,
                );
              }
            },
          );

          link.href =
            target.toString();
        },
      );
  }

  function preparePortalLinks() {
    const current =
      new URL(location.href);

    document
      .querySelectorAll(
        'a[href^="https://portale.sistema90g.it/"]',
      )
      .forEach(
        (link, index) => {
          const target =
            new URL(link.href);

          if (
            target.origin
            !== PORTAL_ORIGIN
          ) {
            return;
          }

          target.searchParams.set(
            'lang',
            'en',
          );

          target.searchParams.set(
            'locale',
            'en-GB',
          );

          if (
            !target.searchParams.get(
              'requester_role',
            )
          ) {
            target.searchParams.set(
              'requester_role',
              'private',
            );
          }

          if (
            !target.searchParams.get(
              'source_page',
            )
          ) {
            target.searchParams.set(
              'source_page',
              pageSlug(),
            );
          }

          if (
            !target.searchParams.get(
              'content_type',
            )
          ) {
            target.searchParams.set(
              'content_type',
              link.dataset.contentType
                || 'page',
            );
          }

          if (
            !target.searchParams.get(
              'cta_position',
            )
          ) {
            target.searchParams.set(
              'cta_position',
              link.dataset.ctaPosition
                || `portal-${index + 1}`,
            );
          }

          CAMPAIGN_KEYS.forEach(
            key => {
              const value =
                current.searchParams.get(
                  key,
                );

              if (
                value
                && !target.searchParams.get(
                  key,
                )
              ) {
                target.searchParams.set(
                  key,
                  value,
                );
              }
            },
          );

          link.href =
            target.toString();
        },
      );
  }

  function initNavigation() {
    const header =
      document.querySelector(
        '.s90g-header',
      );

    const nav =
      header?.querySelector(
        '.s90g-nav',
      );

    if (
      !header
      || !nav
    ) {
      return;
    }

    nav.id =
      nav.id
      || 's90g-main-navigation';

    let toggle =
      header.querySelector(
        '.s90g-menu-toggle',
      );

    if (!toggle) {
      toggle =
        document.createElement(
          'button',
        );

      toggle.type =
        'button';

      toggle.className =
        's90g-menu-toggle';

      toggle.setAttribute(
        'aria-expanded',
        'false',
      );

      toggle.setAttribute(
        'aria-controls',
        nav.id,
      );

      toggle.innerHTML =
        '<span>Menu</span>'
        + '<span aria-hidden="true">☰</span>';

      nav.before(toggle);
    }

    const setOpen =
      open => {
        header.classList.toggle(
          'is-nav-open',
          open,
        );

        toggle.setAttribute(
          'aria-expanded',
          String(open),
        );

        const icon =
          toggle.querySelector(
            '[aria-hidden="true"]',
          );

        if (icon) {
          icon.textContent =
            open
              ? '×'
              : '☰';
        }
      };

    toggle.addEventListener(
      'click',
      () => {
        setOpen(
          toggle.getAttribute(
            'aria-expanded',
          ) !== 'true',
        );
      },
    );

    nav
      .querySelectorAll('a')
      .forEach(link => {
        link.addEventListener(
          'click',
          () => setOpen(false),
        );
      });

    document.addEventListener(
      'keydown',
      event => {
        if (
          event.key === 'Escape'
        ) {
          setOpen(false);
        }
      },
    );
  }

  document.addEventListener(
    'DOMContentLoaded',
    () => {
      initNavigation();
      prepareJourneyLinks();
      preparePortalLinks();

      ensureCookieSettings();

      const banner =
        ensureCookieBanner();

      const consent =
        window.localStorage.getItem(
          CONSENT_KEY,
        );

      if (
        consent === 'accepted'
      ) {
        banner.hidden = true;
        loadAnalytics();
      } else if (
        consent === 'rejected'
      ) {
        banner.hidden = true;
        denyAnalytics();
      } else {
        banner.hidden = false;
      }

      document
        .querySelectorAll(
          '[data-cookie-choice]',
        )
        .forEach(button => {
          button.addEventListener(
            'click',
            () => {
              const accepted =
                button.dataset.cookieChoice
                === 'accept';

              saveConsent(
                accepted
                  ? 'accepted'
                  : 'rejected',
              );

              banner.hidden = true;

              if (accepted) {
                loadAnalytics();
              } else {
                denyAnalytics();
              }
            },
          );
        });

      document
        .querySelectorAll(
          '[data-cookie-settings]',
        )
        .forEach(link => {
          link.addEventListener(
            'click',
            event => {
              event.preventDefault();
              banner.hidden = false;
            },
          );
        });
    },
  );
})();
