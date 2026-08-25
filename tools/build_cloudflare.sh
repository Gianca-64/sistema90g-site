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
