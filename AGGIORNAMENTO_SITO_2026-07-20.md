# Aggiornamento sito Sistema 90G — 20 luglio 2026

## Base preservata
Lo ZIP originale `sistema90g-site-aggiornato-2026-07-19.zip` non è stato modificato.

## Blocco implementato
- catalogo statico unico a sei servizi;
- nuova homepage orientata a tre situazioni;
- nuova pagina `servizi.html`;
- nuove pagine Restyling e Rivenditori;
- revisione delle altre pagine servizio;
- Acquisto Assistito indipendente dai marchi e articolato in due fasi;
- pagina Come funziona con Console automatica e approvazione umana;
- pagina Professionisti;
- archivio casi organizzato in cinque raccolte;
- menu e footer uniformati;
- vecchia pagina Veneta trasformata in passaggio noindex;
- catalogo dinamico disattivato;
- tracciamento delle CTA con pagina, servizio, tipo contenuto e posizione;
- sitemap aggiornata.

## Dipendenze non implementate in questo repository
- salvataggio dei parametri di provenienza nel portale;
- filtro delle date disponibili;
- registrazione completa delle richieste in Console;
- analisi automatica e bozza da approvare;
- email di notifica;
- gestione privata degli allegati.
Queste funzioni appartengono al progetto Console/portale.

## Completamento conformità Google Search e AI

- JSON-LD statico e coerente su tutte le 56 pagine indicizzabili;
- schema Service sulle offerte, Article sui 27 casi, CollectionPage/ItemList sulle raccolte;
- breadcrumb visibili e strutturati sui casi e sulle categorie;
- Open Graph e Twitter Card completi;
- dimensioni intrinseche e caricamento ottimizzato delle immagini;
- eliminata la possibile duplicazione dinamica dei dati strutturati;
- caricamento differito delle immagini nell’archivio casi;
- 167 CTA verso il portale tutte attribuite;
- audit di rilascio automatico aggiunto in `tools/audit_release.py`;
- rapporto dettagliato in `VERIFICA_CONFORMITA_GOOGLE_AI_2026-07-20.md`.
