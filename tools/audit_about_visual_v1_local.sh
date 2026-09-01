#!/usr/bin/env bash
set -euo pipefail

BRANCH="visual-system-v6-about-pilot"
PORT="4178"
BASE_URL="http://127.0.0.1:${PORT}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$HOME/Desktop/Sistema90G-About-Visual-V1-Audit"
ZIP="$HOME/Desktop/Sistema90G-About-Visual-V1-Audit.zip"
PAGE="chi-e-sistema90g.html"

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

echo "=== 1/4 BUILD + CONTRATTI ==="
bash tools/build_cloudflare.sh

echo
echo "=== 2/4 SERVER LOCALE ==="
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory dist >/tmp/s90g-about-v1-audit-preview.log 2>&1 &
server_pid=$!
cleanup(){ kill "$server_pid" >/dev/null 2>&1 || true; }
trap cleanup EXIT INT TERM

for _ in {1..30}; do
  if /usr/bin/curl -fsS "$BASE_URL/$PAGE" >/dev/null 2>&1; then break; fi
  sleep 0.2
done
if ! /usr/bin/curl -fsS "$BASE_URL/$PAGE" >/dev/null 2>&1; then
  echo "ERRORE: server locale non raggiungibile su $BASE_URL/$PAGE"
  exit 1
fi

echo "OK server locale raggiungibile."

echo
echo "=== 3/4 CATTURA AUTOMATICA DESKTOP/MOBILE ==="
rm -rf "$OUT" "$ZIP"
mkdir -p "$OUT"
node "$ROOT/tools/capture_visual_page.mjs" "$CHROME" "$OUT" "$BASE_URL" "$PAGE" "about"

cat > "$OUT/README.txt" <<EOF
Sistema 90G — About Visual V1 audit locale
Branch: $BRANCH
Pagina: $BASE_URL/$PAGE

Catture automatiche:
- desktop 1440x1100
- mobile 390x844

Gate automatici:
- pagina raggiungibile
- H1 presente
- immagini caricate
- nessun overflow orizzontale

File:
- about-full-desktop.png
- about-full-mobile.png
- metrics.json
EOF
(
  cd "$HOME/Desktop"
  /usr/bin/zip -qr "$(basename "$ZIP")" "$(basename "$OUT")"
)

echo
echo "=== 4/4 STATO REPOSITORY ==="
if [ -n "$(git status --porcelain)" ]; then
  echo "ERRORE: il repository si e' sporcato durante l'audit."
  git status --short
  exit 1
fi

echo "OK repository pulito."
echo
echo "ABOUT VISUAL V1: GATE LOCALE COMPLETATO."
echo "Pacchetto unico da condividere: $ZIP"
echo "Nessun deploy eseguito e nessuna modifica a main."
