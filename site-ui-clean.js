(() => {
  const OFFICIAL_EMAIL = 'sistema90g@icloud.com';

  const cleanResidualChat = () => {
    document.querySelectorAll('a').forEach(link => {
      const text = (link.textContent || '').replace(/\s+/g, ' ').trim().toLowerCase();
      const href = (link.getAttribute('href') || '').toLowerCase();
      const isOfficialButton = link.classList.contains('s90g-chat-button');
      const isWhatsapp = href.includes('wa.me') || href.includes('whatsapp');
      const isResidualLabel = text.includes('domande rapide') || text === 'chat whatsapp' || text.includes('domande rapide chat whatsapp');
      if ((isWhatsapp || isResidualLabel) && !isOfficialButton) link.remove();
    });

    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);
    textNodes.forEach(node => {
      const value = node.nodeValue || '';
      if (/domande\s+rapide/i.test(value)) node.nodeValue = value.replace(/domande\s+rapide/gi, '');
    });
  };

  document.querySelectorAll('a[href^="mailto:"]').forEach(link => {
    link.setAttribute('href', `mailto:${OFFICIAL_EMAIL}`);
    if (link.textContent.includes('@')) link.textContent = OFFICIAL_EMAIL;
  });

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const textNodes = [];
  while (walker.nextNode()) textNodes.push(walker.currentNode);
  textNodes.forEach(node => {
    node.nodeValue = node.nodeValue
      .replace(/info@sistema90g\.it/gi, OFFICIAL_EMAIL)
      .replace(/sistema90g@sistema90g\.it/gi, OFFICIAL_EMAIL);
  });

  cleanResidualChat();
  new MutationObserver(cleanResidualChat).observe(document.body, { childList: true, subtree: true, characterData: true });

  const header = document.querySelector('[data-s90g-header]');
  const button = header?.querySelector('.nav-toggle');
  const nav = header?.querySelector('.main-nav');

  if (header && button && nav) {
    const close = () => {
      header.removeAttribute('data-menu-open');
      button.setAttribute('aria-expanded', 'false');
      document.documentElement.classList.remove('s90g-menu-open');
    };

    button.addEventListener('click', () => {
      const open = header.getAttribute('data-menu-open') === 'true';
      if (open) close();
      else {
        header.setAttribute('data-menu-open', 'true');
        button.setAttribute('aria-expanded', 'true');
        document.documentElement.classList.add('s90g-menu-open');
      }
    });

    nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
    document.addEventListener('keydown', event => { if (event.key === 'Escape') close(); });
    window.addEventListener('resize', () => { if (window.innerWidth > 820) close(); });

    const current = location.pathname.split('/').pop() || 'index.html';
    nav.querySelectorAll('a[href]').forEach(link => {
      if (link.getAttribute('href').split('#')[0] === current) link.setAttribute('aria-current', 'page');
    });
  }

  const removeUnapprovedContentImages = () => {
    document.querySelectorAll('main figure.premium-image, main img.case-card-image, main .case-card img, main article > img').forEach(node => {
      if (node.tagName === 'IMG') {
        const figure = node.closest('figure');
        if (figure && figure.querySelectorAll('img').length === 1) figure.remove();
        else node.remove();
      } else {
        node.remove();
      }
    });

    document.body.classList.add('s90g-no-content-images');
  };

  removeUnapprovedContentImages();
  new MutationObserver(removeUnapprovedContentImages).observe(document.body, { childList: true, subtree: true });
})();