# Sprint commerciale entrate immediate

Questo ramo raccoglie gli interventi destinati ad aumentare la probabilità di vendita nel breve periodo senza dipendere dalla crescita SEO.

Interventi inclusi:

- landing dedicata alla seconda opinione indipendente sulla cucina;
- riposizionamento nel percorso guidato di Controllo mirato e Analisi completa come strumenti di seconda opinione e controllo pre-ordine;
- piano operativo di 7 giorni con canali, KPI e soglie di abbandono;
- tracciato commerciale per misurare contatti, richieste, ricavi, costi e ore;
- preparazione del flusso Payment Links senza introdurre URL di pagamento fittizi;
- attribuzione completa sito → portale → richiesta → Console tramite `request_code`.

## Attribuzione commerciale corrente

Ogni link finale verso `portale.sistema90g.it` viene arricchito automaticamente con pagina di origine, tipo di contenuto, posizione della CTA, ruolo, servizio, valore potenziale del servizio e parametri UTM disponibili.

Il portale aggiunge questi dati alla proprietà `source` della richiesta. Il backend Cloudflare li salva in `source_json` insieme al `request_code`; la Console riceve nuovamente il campo `source` quando importa la richiesta.

Il `request_code` è quindi la chiave primaria operativa per collegare:

1. origine della visita;
2. pagina e CTA utilizzata;
3. ruolo e servizio richiesto;
4. richiesta nel portale;
5. caso importato in Console;
6. esito commerciale;
7. ricavo effettivo.

Nel file `commerciale-tracking.csv`, `valore_servizio_euro` indica il valore nominale/potenziale del servizio richiesto, mentre `ricavo_euro` deve contenere esclusivamente il ricavo effettivamente acquisito. Non usare il valore del lead come fatturato.

## KPI economici principali

Il sito va valutato principalmente su:

- richieste generate per canale e pagina;
- tasso visita → apertura portale;
- tasso apertura portale → richiesta creata;
- tasso richiesta → vendita;
- ricavo per pagina di origine;
- ricavo per canale e campagna;
- ticket medio effettivo;
- ore impiegate per euro di ricavo;
- motivi di perdita più frequenti.

Principio: non creare nuovi servizi quando il bisogno commerciale può essere soddisfatto da un servizio già esistente; cambiare invece il contesto e il momento decisionale con cui il servizio viene presentato.
