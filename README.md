# sistema90g-site

Connessione GitHub attiva.
## Percorso guidato ruolo, situazione e prezzo — 2026-07-20

Il sito pubblico instrada ora le richieste attraverso `analisi-preventiva.html#percorso`.
I prezzi vengono visualizzati dinamicamente soltanto al terzo passaggio e non sono pubblicati nelle pagine descrittive o nei dati strutturati.

Verifiche locali:

```bash
python tools/audit_release.py
node tools/test_guided_pricing.js
```
