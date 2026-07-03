(() => {
  const header = document.querySelector('[data-s90g-header]');
  const button = header?.querySelector('.nav-toggle');
  const nav = header?.querySelector('.main-nav');
  if (!header || !button || !nav) return;
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
  nav.addEventListener('click', event => {
    if (event.target.closest('a')) close();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') close();
  });
  const current = location.pathname.split('/').pop() || 'index.html';
  nav.querySelectorAll('a[href]').forEach(link => {
    if (link.getAttribute('href').split('#')[0] === current) {
      link.setAttribute('aria-current', 'page');
    }
  });
})();
