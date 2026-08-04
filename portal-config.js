/* Sistema 90G — configurazione unica del portale pubblico */
(() => {
  window.S90G_PORTAL_CONFIG = Object.freeze({
    enabled: false,
    status: 'verification',
    trialHosting: false,
    url: 'https://portale.sistema90g.it/portal.html',
    displayHost: 'portale.sistema90g.it',
    message: 'Il portale per l’invio della richiesta è sospeso fino alla verifica del dominio, del modulo pubblico e della destinazione effettiva dei dati. Il percorso guidato continua a mostrare servizio, prezzo, tempi e limiti senza raccogliere dati personali o allegati.',
    capabilities: Object.freeze({
      initialRequest: false,
      attachments: false,
      payments: false,
      delivery: false
    })
  });
})();
