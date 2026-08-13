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

# Guard rail semantico: il sito pubblico deve comunicare esclusivamente cucina.
# Ripulisce residui storici nei metadati/schema di pagine ancora utili e indicizzabili.
find "$DIST" -type f -name '*.html' -print0 | while IFS= read -r -d '' file; do
  sed -i.bak \
    -e 's/Tecnico indipendente per analisi preventiva di progetti casa e cucina/Tecnico indipendente per analisi preventiva di progetti cucina/g' \
    -e 's/Analisi preventiva indipendente per progetti, spazi, preventivi e cucine\./Analisi preventiva indipendente per progetti, preventivi, spazi e scelte della cucina./g' \
    "$file"
  rm -f "$file.bak"
done

# Guard rail: i materiali operativi non devono comparire nell'output Pages.
for forbidden in \
  '.git' '.github' 'tools' '.htaccess' 'CNAME' 'README.md' \
  'AUDIT_PRELIMINARE_SITO_2026-08-04.md' 'BASE_ORIGINALE_PRESERVATA.txt'; do
  if [ -e "$DIST/$forbidden" ]; then
    echo "ERRORE: file interno presente in dist: $forbidden" >&2
    exit 1
  fi
done

# Requisiti minimi del sito pubblico.
for required in index.html robots.txt sitemap.xml guide-cucina-sitemap.xml image-sitemap.xml _headers _redirects privacy-policy.html cookie-policy.html; do
  test -f "$DIST/$required" || { echo "ERRORE: manca $required in dist" >&2; exit 1; }
done

echo "Cloudflare Pages dist pronta: $(find "$DIST" -type f | wc -l | tr -d ' ') file pubblici"
