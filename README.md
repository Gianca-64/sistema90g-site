# sistema90g-site

Sito pubblico B2C di Sistema 90G dedicato alla cucina.

`servizi.html` presenta i sei servizi canonici con i relativi prezzi.
`analisi-preventiva.html` è il Free Entry: il Portale riceve la richiesta
di valutazione iniziale gratuita. Un eventuale servizio a pagamento viene
proposto soltanto dopo la qualificazione del caso; nessun acquisto è automatico.

Verifiche locali:

```bash
python3 tools/verify_home_acquisition_v1.py
python3 tools/verify_services_acquisition_v1.py
python3 tools/audit_release.py
node tools/test_guided_pricing.js
bash tools/build_cloudflare.sh
```
