/* Sistema 90G — configurazione unica del portale pubblico */
(() => {
  window.S90G_PORTAL_CONFIG = Object.freeze({
    enabled: true,
    status: 'active',
    trialHosting: false,
    url: 'https://portale.sistema90g.it/portal.html',
    displayHost: 'portale.sistema90g.it',
    message: 'Il portale raccoglie la richiesta iniziale. Allegati, pagamento e consegna saranno gestiti separatamente finché le relative funzioni non saranno attive.',
    capabilities: Object.freeze({
      initialRequest: true,
      attachments: false,
      payments: false,
      delivery: false
    })
  });
})();
