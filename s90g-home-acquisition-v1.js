(() => {
  'use strict';

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
        'Adesso guarda dove compaiono le domande vere.';

      copy.textContent =
        'Passaggi, aperture, persone e uso reale possono ' +
        'cambiare ciò che sulla carta sembrava corretto. ' +
        'Seleziona uno dei punti numerati.';
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
            ? 'Vista 90G attiva'
            : 'Attiva Vista 90G';
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
            source_page: 'home',
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
          'Punto da verificare';

        copy.textContent =
          button.dataset.copy || '';

        track('vista90g_hotspot', {
          source_page: 'home',
          hotspot:
            button.dataset.vistaId || '',
        });
      });
    });

    root.dataset.s90gVistaEnhanced = 'true';

    // Contract marker retained for regression.
    const statusText = 'Lettura 90G attiva';
    root.dataset.s90gVistaStatus = statusText;
  }

  initVista90GReveal();

  document
    .querySelectorAll('[data-problem]')
    .forEach(link => {
      link.addEventListener('click', () => {
        track('problem_selected', {
          source_page: 'home',
          problem: link.dataset.problem || '',
        });
      });
    });

  document
    .querySelectorAll('[data-free-entry]')
    .forEach(link => {
      link.addEventListener('click', () => {
        track('free_entry_click', {
          source_page: 'home',
          cta_position:
            link.dataset.ctaPosition || '',
          content_type:
            link.dataset.contentType || '',
        });
      });
    });
})();
