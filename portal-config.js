/* Sistema 90G — configurazione unica del portale pubblico */
(() => {
  window.S90G_PORTAL_CONFIG = Object.freeze({
    enabled: true,
    status: 'active',
    trialHosting: false,
    url: 'https://portale.sistema90g.it/portal.html',
    displayHost: 'portale.sistema90g.it',
    message: 'Il portale raccoglie la richiesta iniziale, consente l’invio degli allegati e gestisce la consegna. Il pagamento resta separato finché la relativa funzione non sarà attiva.',
    capabilities: Object.freeze({
      initialRequest: true,
      attachments: true,
      payments: false,
      delivery: true
    })
  });
})();
