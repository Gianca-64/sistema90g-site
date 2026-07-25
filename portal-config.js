/* Sistema 90G — configurazione unica del portale pubblico */
(() => {
  window.S90G_PORTAL_CONFIG = Object.freeze({
    enabled: true,
    status: 'active',
    trialHosting: false,
    url: 'https://portale.sistema90g.it/portal.html',
    displayHost: 'portale.sistema90g.it',
    message: 'Il portale sicuro per l’invio della richiesta è attivo. Gli allegati saranno aggiunti in una fase successiva.'
  });
})();
