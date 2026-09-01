#!/usr/bin/env bash
set -euo pipefail

BRANCH="visual-system-v15-offer-scope-guide"
PORT="4187"
BASE_URL="http://127.0.0.1:${PORT}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$HOME/Desktop/Sistema90G-Offer-Scope-Guide-Visual-V1-Audit"

current_branch="$(git branch --show-current)"
if [ "$current_branch" != "$BRANCH" ]; then
  echo "ERRORE: questo audit richiede il branch $BRANCH (attuale: $current_branch)."
  exit 1
fi
if [ -n "$(git status --porcelain)" ]; then
  echo "ERRORE: repository non pulito."
  git status --short
  exit 1
fi
if [ ! -x "$CHROME" ]; then
  echo "ERRORE: Google Chrome non trovato in $CHROME"
  exit 1
fi
if ! command -v node >/dev/null 2>&1; then
  echo "ERRORE: Node.js non trovato"
  exit 1
fi
NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
if [ "$NODE_MAJOR" -lt 22 ]; then
  echo "ERRORE: serve Node.js 22 o successivo (trovato $(node -v))"
  exit 1
fi

echo "=== 1/3 BUILD + CONTRATTI ==="
bash tools/build_cloudflare.sh

echo
echo "=== 2/3 AUDIT VISUALE AUTOMATICO DESKTOP/MOBILE ==="
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory dist >/tmp/s90g-offer-scope-guide-v1-audit-preview.log 2>&1 &
server_pid=$!
cleanup(){ kill "$server_pid" >/dev/null 2>&1 || true; }
trap cleanup EXIT INT TERM

for _ in {1..30}; do
  if /usr/bin/curl -fsS "$BASE_URL/voci-escluse-preventivo-cucina.html" >/dev/null 2>&1; then break; fi
  sleep 0.2
done
if ! /usr/bin/curl -fsS "$BASE_URL/voci-escluse-preventivo-cucina.html" >/dev/null 2>&1; then
  echo "ERRORE: server locale non raggiungibile su $BASE_URL"
  exit 1
fi

mkdir -p "$OUT"
find "$OUT" -mindepth 1 -maxdepth 1 -type f -delete
node "$ROOT/tools/capture_visual_page.mjs" "$CHROME" "$OUT" "$BASE_URL" "voci-escluse-preventivo-cucina.html" "offer-scope-exclusions"

cat > "$OUT/README.txt" <<EOF
Sistema 90G — Offer Scope Guide Visual V1 audit locale
Branch: $BRANCH
Pagina: $BASE_URL/voci-escluse-preventivo-cucina.html

Catture automatiche:
- desktop 1440x1100
- mobile 390x844

Gate automatici:
- pagina raggiungibile
- H1 presente
- immagini caricate
- nessun overflow orizzontale

File:
- offer-scope-exclusions-full-desktop.png
- offer-scope-exclusions-full-mobile.png
- metrics.json
EOF

echo
echo "=== 3/3 STATO REPOSITORY ==="
if [ -n "$(git status --porcelain)" ]; then
  echo "ERRORE: il repository si e' sporcato durante l'audit."
  git status --short
  exit 1
fi

echo "OK repository pulito."
echo
echo "OFFER SCOPE GUIDE VISUAL V1: GATE LOCALE COMPLETATO."
echo "Risultati: $OUT"
echo "Nessun deploy eseguito e nessuna modifica a main."
