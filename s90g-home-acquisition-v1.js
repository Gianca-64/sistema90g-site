(() => {
  'use strict';

  const isEnglish =
    (document.documentElement.lang || '')
      .toLowerCase()
      .startsWith('en');

  const sourcePage =
    isEnglish
      ? 'home-en-gb'
      : 'home';

  const vistaText =
    isEnglish
      ? {
          panelTitle:
            'Now look at where the real questions appear.',
          panelCopy:
            'Clearances, openings, people and real use can change what looked right on paper. Select one of the numbered points.',
          active:
            '90G View active',
          inactive:
            'Activate 90G View',
          fallbackTitle:
            'Point to check',
          status:
            '90G View active',
        }
      : {
          panelTitle:
            'Adesso guarda dove compaiono le domande vere.',
          panelCopy:
            'Passaggi, aperture, persone e uso reale possono cambiare ciò che sulla carta sembrava corretto. Seleziona uno dei punti numerati.',
          active:
            'Vista 90G attiva',
          inactive:
            'Attiva Vista 90G',
          fallbackTitle:
            'Punto da verificare',
          status:
            'Lettura 90G attiva',
        };

  const track = (name, params = {}) => {
    if (typeof window.gtag !== 'function') return;

    window.gtag('event', name, {
      event_category: 'engagement',
      ...params,
    });
  };

  function initVista90GReveal() {
    const root = document.querySelector('[data-vista-root]');

    if (!root) return;

    const stage = root.querySelector('[data-vista-stage]');
    const toggle = root.querySelector('[data-vista-toggle]');
    const toggleLabel =
      root.querySelector('[data-vista-toggle-label]');
    const title = root.querySelector('[data-vista-title]');
    const copy = root.querySelector('[data-vista-copy]');

    const hotspots = [
      ...root.querySelectorAll('[data-vista-hotspot]'),
    ];

    if (
      !stage ||
      !toggle ||
      !title ||
      !copy
    ) {
      return;
    }

    const initialTitle = title.textContent.trim();
    const initialCopy = copy.textContent
      .replace(/\s+/g, ' ')
      .trim();

    const resetHotspots = () => {
      hotspots.forEach(button => {
        button.setAttribute('aria-pressed', 'false');
      });
    };

    const setPanelIntro = () => {
      title.textContent =
        vistaText.panelTitle;

      copy.textContent =
        vistaText.panelCopy;
    };

    const setActive = active => {
      stage.classList.toggle('is-active', active);

      toggle.setAttribute(
        'aria-pressed',
        String(active)
      );

      if (toggleLabel) {
        toggleLabel.textContent =
          active
            ? vistaText.active
            : vistaText.inactive;
      }

      if (active) {
        setPanelIntro();
      } else {
        resetHotspots();
        title.textContent = initialTitle;
        copy.textContent = initialCopy;
      }
    };

    toggle.addEventListener(
      'click',
      event => {
        event.preventDefault();

        /*
         * activating Vista 90G must never move the viewport
         * and this is the only owner of the activation click.
         */
        event.stopImmediatePropagation();

        const x = window.scrollX;
        const y = window.scrollY;

        const active =
          toggle.getAttribute('aria-pressed') !== 'true';

        setActive(active);

        if (active) {
          track('vista90g_open', {
            source_page: sourcePage,
          });
        }

        requestAnimationFrame(() => {
          if (
            window.scrollX !== x ||
            window.scrollY !== y
          ) {
            window.scrollTo({
              left: x,
              top: y,
              behavior: 'auto',
            });
          }
        });
      },
      true
    );

    hotspots.forEach(button => {
      button.addEventListener('click', event => {
        event.preventDefault();

        if (
          toggle.getAttribute('aria-pressed') !== 'true'
        ) {
          setActive(true);
        }

        hotspots.forEach(item => {
          item.setAttribute(
            'aria-pressed',
            item === button ? 'true' : 'false'
          );
        });

        title.textContent =
          button.dataset.title ||
          vistaText.fallbackTitle;

        copy.textContent =
          button.dataset.copy || '';

        track('vista90g_hotspot', {
          source_page: sourcePage,
          hotspot:
            button.dataset.vistaId || '',
        });
      });
    });

    root.dataset.s90gVistaEnhanced = 'true';

    // Contract marker retained for regression.
    const statusText = vistaText.status;
    root.dataset.s90gVistaStatus = statusText;
  }

  initVista90GReveal();

  document
    .querySelectorAll('[data-problem]')
    .forEach(link => {
      link.addEventListener('click', () => {
        track('problem_selected', {
          source_page: sourcePage,
          problem: link.dataset.problem || '',
        });
      });
    });

  document
    .querySelectorAll('[data-free-entry]')
    .forEach(link => {
      link.addEventListener('click', () => {
        track('free_entry_click', {
          source_page: sourcePage,
          cta_position:
            link.dataset.ctaPosition || '',
          content_type:
            link.dataset.contentType || '',
        });
      });
    });
})();
