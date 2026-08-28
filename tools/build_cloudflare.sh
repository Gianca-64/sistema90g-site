#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="$ROOT/dist"

rm -rf "$DIST"
mkdir -p "$DIST"

# File pubblici di primo livello. Non copiare Markdown, .htaccess, CNAME,
# strumenti di sviluppo, workflow o altri materiali interni del repository.
find "$ROOT" -maxdepth 1 -type f \( \
  -name '*.html' -o \
  -name '*.css' -o \
  -name '*.js' -o \
  -name '*.xml' -o \
  -name '*.webmanifest' -o \
  -name 'robots.txt' -o \
  -name 'humans.txt' -o \
  -name '_headers' -o \
  -name '_redirects' \
\) -exec cp {} "$DIST/" \;

for dir in images editoriale approfondimenti .well-known; do
  if [ -d "$ROOT/$dir" ]; then
    cp -R "$ROOT/$dir" "$DIST/$dir"
  fi
done

# Due PNG storici molto pesanti non sono referenziati dal sito pubblico.
# Restano nel repository come materiale storico, ma non devono entrare nel deploy.
rm -f \
  "$DIST/images/02_HOME_SCENA_PROBLEMA.png" \
  "$DIST/images/04_HOME_COSTO_TARDIVO.png"

# Perimetro pubblico: esclusivamente cucina.
# Manteniamo solo i sei casi reali cucina attualmente approvati; tutti gli altri
# vecchi casi casa/soggiorno/camere/bagno/garage/terrazzo vengono esclusi dal deploy.
case_keep='^(caso-cucina-piccola-tre-lati|caso-cucina-profondita-75-angolo|caso-isola-passaggi-cucina|caso-lavastoviglie-passaggio-cucina|caso-lavello-sotto-finestra-aperture|caso-preventivo-cucina-sconto-valore)\.html$'
find "$DIST" -maxdepth 1 -type f -name 'caso-*.html' -print0 | while IFS= read -r -d '' file; do
  base="$(basename "$file")"
  if ! printf '%s\n' "$base" | grep -Eq "$case_keep"; then
    rm -f "$file"
  fi
done

# Le vecchie raccolte extra-cucina non devono essere pubblicate come pagine autonome.
rm -f \
  "$DIST/casi-camere-contenimento.html" \
  "$DIST/casi-distribuzione-casa.html" \
  "$DIST/casi-soggiorno-open-space.html" \
  "$DIST/casi-spazi-servizio.html" \
  "$DIST/verifica-planimetria-distribuzione-casa.html" \
  "$DIST/scelta-finiture-casa.html" \
  "$DIST/agenzie-immobiliari.html" \
  "$DIST/analisi-unita-varianti.html" \
  "$DIST/studio-preliminare-spazi.html"

# Se un vecchio URL HTML ha gia un redirect 301 esplicito, rimuoviamo il file fisico
# dall'output cosi il redirect non puo essere mascherato da una risorsa statica omonima.
# index.html fa eccezione: serve come documento home del Worker, mentre /index.html -> /
# resta una regola canonica per le richieste esplicite al vecchio URL.
while read -r source target status rest; do
  [ "${status:-}" = "301" ] || continue
  case "$source" in
    /index.html)
      ;;
    /*.html)
      legacy="${source#/}"
      rm -f "$DIST/$legacy"
      ;;
  esac
done < "$DIST/_redirects"

# Guard rail semantico: il sito pubblico deve comunicare esclusivamente cucina.
# Ripulisce residui storici nei metadati/schema e collega direttamente all'hub casi canonico.
find "$DIST" -type f -name '*.html' -print0 | while IFS= read -r -d '' file; do
  sed -i.bak \
    -e 's/Tecnico indipendente per analisi preventiva di progetti casa e cucina/Tecnico indipendente per analisi preventiva di progetti cucina/g' \
    -e 's/Analisi preventiva indipendente per progetti, spazi, preventivi e cucine\./Analisi preventiva indipendente per progetti, preventivi, spazi e scelte della cucina./g' \
    -e 's/casi-cucina\.html/casi-analizzati.html/g' \
    "$file"
  rm -f "$file.bak"
done

# Cloudflare Workers Static Assets espone i file HTML con URL pubblici senza .html.
# Allineiamo quindi canonical, sitemap, link interni e destinazioni dei redirect
# alla forma realmente servita, evitando canonical verso redirect e catene 301 -> 307.
python3 "$ROOT/tools/normalize_public_urls.py" "$DIST"

# P2: i rich result FAQ non sono piu mostrati da Google. Manteniamo le domande
# visibili per le persone ma rimuoviamo dal solo output pubblico il vecchio FAQPage,
# evitando markup inutile o divergente dal contenuto effettivamente mostrato.
python3 "$ROOT/tools/normalize_public_search_semantics.py" "$DIST"

# P2: Home e Free Entry devono portare vicino alla decisione una prova concreta
# di identita, indipendenza e casi verificabili, senza cambiare il funnel.
python3 "$ROOT/tools/inject_public_trust_bridge.py" "$DIST"

# P2: prima del punto di invio il Free Entry deve chiarire cosa succede dopo,
# senza promettere tempi o canali operativi non verificati.
python3 "$ROOT/tools/inject_public_free_entry_expectation.py" "$DIST"

# Ogni pagina di contenuto deve avere una UI di consenso funzionante prima che
# privacy-consent.js inizializzi lo stato analytics. Il componente non duplica
# eventuali banner storici gia presenti nel markup.
python3 "$ROOT/tools/inject_public_consent_ui.py" "$DIST"

# Ogni CSS/JS locale riceve nel solo output pubblico una query v= derivata
# dal contenuto reale del file. La sorgente resta leggibile e ogni modifica futura
# invalida automaticamente la cache browser senza bump manuali.
python3 "$ROOT/tools/version_public_static_assets.py" "$DIST"

# Il Portale pubblico accetta soltanto il Free Entry. Ogni CTA pubblica deve quindi
# usare esplicitamente service=valutazione-iniziale; i servizi a pagamento vengono
# proposti solo dopo la qualificazione del caso.
python3 "$ROOT/tools/test_public_portal_entry_contract.py" "$DIST"

# L'offerta pubblica deve restare allineata al listino canonico anche nelle
# pagine dedicate a professionisti e rivenditori.
python3 "$ROOT/tools/test_public_commercial_contract.py" "$DIST"

# La cache lunga immutable e consentita solo se tutti i riferimenti CSS/JS pubblici
# portano la versione automatica basata sul contenuto.
python3 "$ROOT/tools/test_public_static_asset_versioning.py" "$DIST"

# Il consenso deve restare negato di default e ogni pagina pubblica deve esporre
# una UI accessibile per accettare, rifiutare e riaprire le preferenze.
python3 "$ROOT/tools/test_public_consent_contract.py" "$DIST"

# P2: la prova di fiducia deve essere presente una sola volta sulla Home e prima
# del punto di invio nel Free Entry.
python3 "$ROOT/tools/test_public_trust_bridge_contract.py" "$DIST"

# P2: il Free Entry deve spiegare invio, prima lettura e assenza di acquisto automatico.
python3 "$ROOT/tools/test_public_free_entry_expectation_contract.py" "$DIST"

# P2 SEO/AEO: struttura tecnica leggibile, JSON-LD valido e coerente, canonical
# puliti e sitemap canonica; niente markup FAQ obsoleto usato come scorciatoia AEO.
python3 "$ROOT/tools/test_public_search_semantics_contract.py" "$DIST"

# Controlli statici ad alta confidenza sul solo output realmente pubblicato:
# lingua/titolo, alt, ID duplicati, etichette, pulsanti e ordine tastiera.
python3 "$ROOT/tools/test_public_accessibility_contract.py" "$DIST"

# Un'immagine raster referenziata da HTML/metadata pubblici non deve superare 1 MB.
# Il gate evita regressioni pesanti senza imporre conversioni a immagini gia efficienti.
python3 "$ROOT/tools/test_public_image_performance_contract.py" "$DIST"

# Gli URL creati a runtime devono funzionare anche sulle pagine annidate sotto
# /approfondimenti/: CSS, fallback immagini e CTA non possono essere page-relative.
python3 "$ROOT/tools/test_public_runtime_root_paths.py" "$DIST"

# Il vecchio percorso guidato con catalogo/prezzi legacy resta nel repository solo
# come debito storico di sviluppo. Controlliamo le sole pagine che sopravvivono nel
# perimetro pubblico, poi rimuoviamo gli asset legacy dall'output.
if grep -R -n -E 'role-case-path\.(js|css)' "$DIST" --include='*.html' >/tmp/s90g-role-path-references.log 2>/dev/null; then
  echo "ERRORE: una pagina pubblica dipende ancora dal catalogo legacy role-case-path" >&2
  cat /tmp/s90g-role-path-references.log >&2
  exit 1
fi
rm -f "$DIST/role-case-path.js" "$DIST/role-case-path.css"

# Guard rail: nessuna pagina extra-cucina nota puo rientrare accidentalmente nel deploy.
for forbidden_public in \
  'casi-camere-contenimento.html' 'casi-distribuzione-casa.html' \
  'casi-soggiorno-open-space.html' 'casi-spazi-servizio.html' \
  'verifica-planimetria-distribuzione-casa.html' 'scelta-finiture-casa.html'; do
  if [ -e "$DIST/$forbidden_public" ]; then
    echo "ERRORE: pagina extra-cucina presente in dist: $forbidden_public" >&2
    exit 1
  fi
done

# Guard rail: i materiali operativi non devono comparire nell'output Pages.
for forbidden in \
  '.git' '.github' 'tools' '.htaccess' 'CNAME' 'README.md' \
  'AUDIT_PRELIMINARE_SITO_2026-08-04.md' 'BASE_ORIGINALE_PRESERVATA.txt' \
  'role-case-path.js' 'role-case-path.css'; do
  if [ -e "$DIST/$forbidden" ]; then
    echo "ERRORE: file interno presente in dist: $forbidden" >&2
    exit 1
  fi
done

# Requisiti minimi del sito pubblico.
for required in index.html robots.txt sitemap.xml guide-cucina-sitemap.xml image-sitemap.xml _headers _redirects privacy-policy.html cookie-policy.html; do
  test -f "$DIST/$required" || { echo "ERRORE: manca $required in dist" >&2; exit 1; }
done

# Verifica finale dei casi pubblicati: devono essere esattamente i sei casi cucina approvati.
case_count="$(find "$DIST" -maxdepth 1 -type f -name 'caso-*.html' | wc -l | tr -d ' ')"
if [ "$case_count" -ne 6 ]; then
  echo "ERRORE: attesi 6 casi cucina pubblici, trovati $case_count" >&2
  exit 1
fi

echo "Cloudflare Pages dist pronta: $(find "$DIST" -type f | wc -l | tr -d ' ') file pubblici"
