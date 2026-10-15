# PR 80 — incarico operativo locale per il collaudo finale

## Obiettivo e stato
Repository: Gianca-64/sistema90g-site.
PR: https://github.com/Gianca-64/sistema90g-site/pull/80
Branch candidato: improve/home-usability-20261015.
Commit applicativo e test verificato: e38ddff6ce8580b3aa599f8f51e9fe229d432387.
La documentazione aggiunta dopo questo commit non cambia gli asset pubblici.
Home IT/EN e Vista 90G sono implementate; controlli statici, build e test DOM simulato passano. Manca il collaudo della versione modificata nel browser. Il sito pubblico non contiene ancora queste modifiche.

## Perimetro
Leggere AGENTS.md e i tre documenti operativi/editoriali richiamati.
Operare solo sul repository Sito. Non modificare Console, Portale, Configuratore, prezzi, AI, destinazioni dei servizi o infrastruttura.
Non chiedere all’operatore di eseguire comandi o copiare errori uno alla volta.
Nessuna nuova modifica applicativa è autorizzata da questo incarico: raccogliere eventuali difetti in un unico rapporto.

## Preparazione
1. Individuare la copia canonica dal remote Git, senza presumere un percorso sul Mac.
2. Verificare main e working tree pulito; fetch e solo aggiornamento fast-forward. Non usare stash/reset/clean/force.
3. Recuperare la PR 80 e verificarne stato, head, base e diff correnti. Se i sorgenti applicativi differiscono dal commit indicato, riportare il delta prima di certificare.
4. Usare una worktree separata per il candidato, anche in detached HEAD. Lasciare la copia canonica su main.
5. Se main è avanzato rispetto alla base della PR, segnalare il fatto: i risultati precedenti non certificano automaticamente l’integrazione.

## Batch locale
Eseguire tutti i controlli indipendenti e raccoglierne gli esiti:
- bash tools/build_cloudflare.sh
- node --check s90g-home-acquisition-v1.js
- node --test tools/test_vista_keyboard_state.cjs
- python3 tools/verify_about_acquisition_v1.py
- python3 tools/test_responsive_contract.py
- python3 tools/test_site_i18n_home_v1.py
- git diff --check

In caso di errore della build, non mostrare dist precedente come anteprima valida.

## Anteprima e collaudo sul Mac
Usare Python 3 e il browser locale già disponibili, senza installazioni.
Dopo build riuscita, avviare un server esclusivamente su 127.0.0.1, su porta libera, dalla directory dist della worktree. Registrare PID, porta, directory servita e commit.
Non eseguire tools/preview_visual_system_v1.sh: è vincolato al vecchio branch visual-system-v1.
Aprire / e /en/; verificare anche /chi-e-sistema90g.html e /en/about.html.
Il server Python non replica redirect e header Cloudflare: non attribuire a questo collaudo una certificazione di tali comportamenti.

Controllare entrambe le Home a 320, 375, 390, 768 e 1440 px:
- apertura leggibile e sei situazioni subito dopo il blocco iniziale;
- assenza di overflow, tagli, sovrapposizioni e deformazioni;
- immagini Vista pulita/analizzata coincidenti e punti coerenti con l’immagine;
- comando Vista e tutti i punti utilizzabili;
- a Vista chiusa i punti invisibili non ricevono Tab;
- a Vista aperta Tab raggiunge i punti, Enter/Spazio li attivano;
- disattivazione senza focus lasciato su un punto nascosto;
- navigazione IT/EN e dicitura della valutazione gratuita corrette.

Salvare screenshot e risultati fuori dai sorgenti versionati, senza sovrascrivere pacchetti esistenti. Mostrare l’anteprima all’operatore per il controllo visivo previsto dal progetto.
Non inviare richieste reali né allegati al Portale durante questo collaudo.
Chiudere soltanto il server creato per questo incarico quando la verifica è terminata.

## Rapporto e pubblicazione
Restituire un solo rapporto con commit esatto, esiti, screenshot, difetti e blocchi. Non dichiarare verificati i controlli non eseguiti.
Questo incarico prepara il collaudo, non esegue merge o pubblicazione in assenza del suo esito.
Dopo esito positivo e revisione finale, integrare soltanto la versione verificata, aggiornare main con fast-forward nella copia canonica pulita ed eseguire esclusivamente bash tools/deploy_verified_local.sh. Se l’integrazione cambia i sorgenti rispetto al candidato, ricontrollare il delta e i relativi test prima del deploy.
Verificare infine sul sito pubblico Home IT/EN, Vista e collegamento alla valutazione gratuita. Riportare commit pubblicato ed esito del deploy.
