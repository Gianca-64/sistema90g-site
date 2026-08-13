# Sistema 90G — Audit finale e migrazione Cloudflare Pages

**Data:** 13 agosto 2026  
**Repository:** `Gianca-64/sistema90g-site`  
**Baseline:** `main` — commit `3d4526bb21ac2fba23771545a3ecefcb37553e02`  
**Obiettivo:** verificare la readiness del sito corrente e predisporre una migrazione reversibile verso Cloudflare Pages.

## Esito sintetico

**PRONTO PER DEPLOY DI STAGING SU CLOUDFLARE PAGES.**

Il cambio del dominio `sistema90g.it` deve avvenire soltanto dopo il deploy di staging e la verifica dei record DNS, in particolare MX/TXT collegati alla posta elettronica.

## Audit precedente: stato dei blocchi

### Privacy — RISOLTO

La Privacy Policy corrente dichiara correttamente che il portale raccoglie la richiesta iniziale e i dati essenziali, mentre caricamento allegati, pagamento e consegna non sono ancora disponibili nel portale pubblico.

### Quality gate GitHub — RISOLTO

È presente la workflow `.github/workflows/site-quality-gate.yml`, eseguita sulle pull request verso `main`, con audit release, responsive, navigazione, prezzi e contratti pubblici. Questa migrazione aggiunge anche la verifica dell'output Cloudflare.

### PR #15 professionisti — ISOLATA

La PR #15 resta Draft, non è stata fusa in `main` e mantiene disattivata la funzione inbound professionisti. Non blocca il trasferimento dell'attuale sito pubblico.

## Compatibilità Cloudflare Pages

Il sito è statico e quindi adatto a Cloudflare Pages. I redirect Apache sono stati tradotti nel file `_redirects`; la regola legacy per gli URL `blog/7-errori...` è stata aggiunta in forma compatibile con Pages.

Gli header di sicurezza sono gestiti tramite `_headers`. È stato rimosso il caching `immutable` generico su `/assets/*`: nel repository corrente gli asset principali non sono organizzati in quella cartella e molti nomi non sono fingerprintati. Si mantiene quindi la rivalidazione standard, evitando versioni obsolete dopo i deploy.

Gli URL tecnici `*.pages.dev` ricevono `X-Robots-Tag: noindex, nofollow` per prevenire duplicazioni SEO rispetto al dominio canonico.

## Confine di pubblicazione

Cloudflare Pages non interpreta `.htaccess`. Pubblicare direttamente la root del repository potrebbe quindi rendere raggiungibili file tecnici o documentali che sul vecchio hosting erano protetti da regole Apache.

È stato introdotto `tools/build_cloudflare.sh`, che genera `dist/` copiando soltanto:

- pagine HTML pubbliche;
- CSS e JavaScript pubblici;
- sitemap, robots, manifest e humans.txt;
- `_headers` e `_redirects`;
- immagini, approfondimenti, feed editoriale e `.well-known`.

Restano fuori dall'output almeno:

- `.git`, `.github` e `tools`;
- `.htaccess`;
- `CNAME` del precedente hosting;
- README, audit e documentazione Markdown;
- file operativi non destinati al pubblico.

## Configurazione Cloudflare Pages da usare

- Repository: `Gianca-64/sistema90g-site`
- Production branch: `main`
- Build command: `bash tools/build_cloudflare.sh`
- Build output directory: `dist`
- Framework preset: nessuno / statico

Non sono necessarie Pages Functions per il sito corrente.

## Passaggio dominio

Per `sistema90g.it` (dominio apex) il dominio deve essere aggiunto come zona Cloudflare e i nameserver devono essere spostati su Cloudflare. Prima del cambio verificare che nella zona siano presenti tutti i record DNS esistenti, soprattutto:

- record del sito;
- MX della posta;
- SPF, DKIM e DMARC;
- eventuali record di verifica o servizi esterni.

Dopo il deploy di staging:

1. verificare Home, pagine servizio, percorso guidato, Privacy, Cookie e Innovazioni;
2. verificare sitemap e robots;
3. provare i redirect storici;
4. collegare `sistema90g.it` al progetto Pages;
5. attivare HTTPS e mantenere `sistema90g.it` come host canonico;
6. gestire `www.sistema90g.it` con redirect permanente verso il dominio senza `www`;
7. ricontrollare il sito pubblico dopo la propagazione DNS;
8. mantenere il vecchio hosting disponibile come rollback finché la verifica post-cutover è conclusa.

## Criterio di chiusura

La migrazione è conclusa solo quando:

- il quality gate della PR di migrazione è verde;
- il progetto Pages di staging serve correttamente `dist/`;
- DNS email e servizi esterni sono preservati;
- il dominio personalizzato risponde in HTTPS;
- `www` converge sul dominio canonico;
- redirect storici, sitemap, robots e pagine principali sono verificati dal runtime Cloudflare.
