#!/bin/bash
set -euo pipefail

BRANCH="main"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
  echo "STOP: branch corrente non canonico. Atteso: $BRANCH" >&2
  exit 20
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "STOP: working tree non pulito." >&2
  git status --short
  exit 21
fi

export PATH="/opt/homebrew/opt/node@22/bin:$PATH"
if ! node -e 'const m=Number(process.versions.node.split(".")[0]); if(m<22) process.exit(1)'; then
  echo "STOP: Node.js 22 o superiore non disponibile nel PATH previsto." >&2
  exit 22
fi

git fetch origin "$BRANCH"
LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse "origin/$BRANCH")"
if [[ "$LOCAL" != "$REMOTE" ]]; then
  if git merge-base --is-ancestor "$LOCAL" "$REMOTE"; then
    git merge --ff-only "origin/$BRANCH"
  else
    echo "STOP: branch locale e remoto divergenti." >&2
    exit 23
  fi
fi

TMP_REDIRECTS="$(mktemp)"
cp _redirects "$TMP_REDIRECTS"
restore_redirects(){ cp "$TMP_REDIRECTS" _redirects 2>/dev/null || true; rm -f "$TMP_REDIRECTS"; }
trap restore_redirects EXIT

# La build Cloudflare richiede temporaneamente di rimuovere il redirect /index.html.
perl -0pi -e 's#^/index\.html / 301\n##m' _redirects
bash tools/build_cloudflare.sh
cp "$TMP_REDIRECTS" _redirects

# build_cloudflare.sh ha gia normalizzato le destinazioni di dist/_redirects
# alla forma pubblica senza .html. Non sovrascrivere il file normalizzato con
# la sorgente grezza: ripristiniamo nel solo artefatto la regola /index.html
# rimossa temporaneamente prima della build.
python3 - <<'PY_REDIRECTS'
from pathlib import Path

redirects = Path("dist/_redirects")
lines = redirects.read_text(encoding="utf-8").splitlines()

for line in lines:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        continue
    parts = stripped.split()
    if parts and parts[0] == "/index.html":
        raise SystemExit(
            "STOP: /index.html presente in dist/_redirects prima del ripristino controllato."
        )

redirects.write_text(
    "/index.html / 301\n" + "\n".join(lines) + "\n",
    encoding="utf-8",
)
PY_REDIRECTS

# Fail-closed: il deploy non deve mai reintrodurre destinazioni .html,
# che causerebbero una catena 301 -> redirect automatico Cloudflare.
if awk '
  /^[[:space:]]*#/ { next }
  NF >= 2 && $2 ~ /^\/.*\.html([?#].*)?$/ {
    print
    found=1
  }
  END { exit found ? 0 : 1 }
' dist/_redirects; then
  echo "STOP: destinazione .html presente in dist/_redirects." >&2
  exit 24
fi

test -f dist/index.html
test -f dist/_redirects
test -f dist/_headers
test -f dist/cucina-ad-angolo-guida.html
test -f dist/guide-cucina-sitemap.xml
test -f dist/innovazioni.html
test -f dist/approfondimenti/forno-intelligenza-artificiale-telecamera-cosa-cambia.html
test -f dist/approfondimenti/piano-induzione-opaco-antigraffio-cosa-cambia.html
test -f dist/images/editoriale/forno-ai-telecamera-editoriale.webp
test -f dist/images/editoriale/piano-induzione-opaco-editoriale.webp
grep -q 'Novità, tecnologie e soluzioni che migliorano la cucina di ogni giorno' dist/innovazioni.html
grep -q 'forno-ai-telecamera-editoriale.webp' dist/approfondimenti/forno-intelligenza-artificiale-telecamera-cosa-cambia.html
grep -q 'piano-induzione-opaco-editoriale.webp' dist/approfondimenti/piano-induzione-opaco-antigraffio-cosa-cambia.html
grep -q '^/index.html / 301$' dist/_redirects
! test -e dist/casi-camere-contenimento.html
! test -e dist/casi-distribuzione-casa.html
! test -e dist/casi-soggiorno-open-space.html
! test -e dist/casi-spazi-servizio.html

npx --yes wrangler@4 deploy

sleep 5
STAMP="$(date +%s)"
curl --fail --silent --show-error --location --retry 5 --retry-delay 2 "https://sistema90g.it/?verify=$STAMP" > /tmp/s90g-home.html
curl --fail --silent --show-error --location --retry 5 --retry-delay 2 "https://sistema90g.it/innovazioni.html?verify=$STAMP" > /tmp/s90g-innovazioni.html
grep -qi 'Sistema 90G' /tmp/s90g-home.html
grep -q 'Novità, tecnologie e soluzioni che migliorano la cucina di ogni giorno' /tmp/s90g-innovazioni.html


echo
echo "=== P0 LEGACY PUBLIC SURFACE LIVE CERTIFICATION ==="

BASE="https://sistema90g.it"
STAMP="${STAMP:-$(date +%s)}"

check_301() {
  local path="$1"
  local expected="$2"
  local headers
  local status
  local location

  headers="$(mktemp)"

  status="$(
    curl \
      --silent \
      --show-error \
      --dump-header "$headers" \
      --output /dev/null \
      --max-redirs 0 \
      --write-out '%{http_code}' \
      "${BASE}${path}?verify=${STAMP}"
  )"

  location="$(
    awk '
      BEGIN { IGNORECASE=1 }
      /^location:/ {
        sub(/\r$/, "")
        sub(/^[^:]+:[[:space:]]*/, "")
        print
        exit
      }
    ' "$headers"
  )"

  rm -f "$headers"

  if [ "$status" != "301" ]; then
    echo \
      "STOP: $path status=$status, atteso 301" \
      >&2
    exit 31
  fi

  if [ "$location" != "$expected" ] && \
     [ "$location" != "$BASE$expected" ] && \
     [ "$location" != "$expected?verify=$STAMP" ] && \
     [ "$location" != "$BASE$expected?verify=$STAMP" ]; then

    echo \
      "STOP: $path Location=$location, atteso $expected" \
      >&2

    exit 32
  fi

  echo "PASS — $path -> $expected [301]"
}

check_404() {
  local path="$1"
  local outfile
  local status

  outfile="$(mktemp)"

  status="$(
    curl \
      --silent \
      --show-error \
      --output "$outfile" \
      --write-out '%{http_code}' \
      "${BASE}${path}?verify=${STAMP}"
  )"

  if [ "$status" != "404" ]; then
    echo \
      "STOP: $path status=$status, atteso 404" \
      >&2
    rm -f "$outfile"
    exit 33
  fi

  grep -q \
    'VEDERE IL PROBLEMA PRIMA' \
    "$outfile"

  grep -q \
    'MOSTRA IL TUO CASO' \
    "$outfile"

  grep -q \
    'Problemi, verifiche e decisioni sulla cucina' \
    "$outfile"

  if grep -qE \
    'ANALISI PREVENTIVA INDIPENDENTE|VALUTA IL TUO CASO|Acquisto assistito|>Professionisti<|>Rivenditori<' \
    "$outfile"; then

    echo \
      "STOP: $path espone ancora shell legacy" \
      >&2

    rm -f "$outfile"
    exit 34
  fi

  rm -f "$outfile"

  echo "PASS — $path [404 canonica]"
}

check_301 \
  "/professionisti" \
  "/servizi"

check_301 \
  "/professionisti-progetto-cucina.html" \
  "/progetto-cucina-sistema90g"

check_301 \
  "/progetto-preventivo-cucina-90g" \
  "/servizi"

check_301 \
  "/rivenditori-veneta-cucine" \
  "/metodo-sistema90g"

check_404 \
  "/casi-spazi-servizio.html"

check_404 \
  "/caso-garage-apertura-portiere.html"

curl \
  --fail \
  --silent \
  --show-error \
  --location \
  "${BASE}/progetto-cucina-sistema90g?verify=${STAMP}" \
  > /tmp/s90g-p0-project.html

grep -q \
  'Progetto Cucina 90G · 399 €' \
  /tmp/s90g-p0-project.html

if grep -qE \
  'Progetto Cucina 90G · 145 €|117 €|57 € / vista|57 €/vista' \
  /tmp/s90g-p0-project.html; then

  echo \
    "STOP: Progetto Cucina live contiene prezzi legacy" \
    >&2

  exit 35
fi

echo \
  "PASS — Progetto Cucina live = 399 €, nessun vecchio add-on"

curl \
  --fail \
  --silent \
  --show-error \
  --location \
  "${BASE}/servizi?verify=${STAMP}" \
  > /tmp/s90g-p0-services.html

for required in \
  '99 €' \
  '169 €' \
  '199 €' \
  '399 €' \
  '229 €'; do

  grep -q \
    "$required" \
    /tmp/s90g-p0-services.html || {

      echo \
        "STOP: prezzo canonico mancante da /servizi: $required" \
        >&2

      exit 36
    }
done

if grep -qE \
  'Progetto &amp; Preventivo|Progetto & Preventivo|185 €|127 €|97 €|Veneta Cucine' \
  /tmp/s90g-p0-services.html; then

  echo \
    "STOP: /servizi espone ancora contratto legacy" \
    >&2

  exit 37
fi

echo \
  "PASS — /servizi live priva del vecchio contratto commerciale"

echo \
  "P0 LEGACY PUBLIC SURFACE LIVE CERTIFICATION: PASS"

echo "DEPLOY VERIFIED: site $(git rev-parse --short HEAD)"
