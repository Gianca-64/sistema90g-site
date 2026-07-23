/* Sistema 90G — configurazione unica del portale pubblico */
(() => {
  window.S90G_PORTAL_CONFIG = Object.freeze({
    enabled: false,
    status: 'provisioning',
    trialHosting: true,
    url: 'https://portale.sistema90g.it/',
    displayHost: 'portale.sistema90g.it',
    message: 'Il portale sicuro per l’invio di dati, immagini e PDF è in fase di attivazione sul nuovo hosting. Il percorso guidato resta disponibile fino alla visualizzazione del servizio e del prezzo, ma in questa fase non raccoglie dati personali o allegati.'
  });
})();
