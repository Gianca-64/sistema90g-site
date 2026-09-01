#!/usr/bin/env bash
set -euo pipefail

BRANCH="visual-system-v2-case-pilot"
PORT="4174"
BASE_URL="http://127.0.0.1:${PORT}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$HOME/Desktop/Sistema90G-Case-Visual-V2-Audit"
ZIP="$HOME/Desktop/Sistema90G-Case-Visual-V2-Audit.zip"

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
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory dist >/tmp/s90g-case-v2-audit-preview.log 2>&1 &
server_pid=$!
cleanup(){ kill "$server_pid" >/dev/null 2>&1 || true; }
trap cleanup EXIT INT TERM

for _ in {1..30}; do
  if /usr/bin/curl -fsS "$BASE_URL/caso-lavastoviglie-passaggio-cucina.html" >/dev/null 2>&1; then break; fi
  sleep 0.2
done
if ! /usr/bin/curl -fsS "$BASE_URL/caso-lavastoviglie-passaggio-cucina.html" >/dev/null 2>&1; then
  echo "ERRORE: server locale non raggiungibile su $BASE_URL"
  exit 1
fi

rm -rf "$OUT" "$ZIP"
mkdir -p "$OUT"
node "$ROOT/tools/capture_case_visual_v2.mjs" "$CHROME" "$OUT" "$BASE_URL"

cat > "$OUT/README.txt" <<EOF
Sistema 90G — Case Visual V2 audit locale
Branch: $BRANCH
Sorgente: $BASE_URL

Campioni verificati automaticamente desktop 1440x1100 e mobile 390x844:
- lavastoviglie = 90G Use
- isola = 90G Conflict
- preventivo = 90G Compare

Gate automatici:
- classe Case Visual V2 presente
- hero presente
- modalita 90G attesa presente
- blocco conseguenza presente
- immagini caricate
- nessun overflow orizzontale

Le PNG full-page e consequence servono per il controllo visuale finale.
EOF
(
  cd "$HOME/Desktop"
  /usr/bin/zip -qr "$(basename "$ZIP")" "$(basename "$OUT")"
)

echo
echo "=== 3/3 STATO REPOSITORY ==="
if [ -n "$(git status --porcelain)" ]; then
  echo "ERRORE: il repository si e' sporcato durante l'audit."
  git status --short
  exit 1
fi

echo "OK repository pulito."
echo
echo "CASE VISUAL V2: GATE LOCALE COMPLETATO."
echo "Pacchetto: $ZIP"
echo "Nessun deploy eseguito e nessuna modifica a main."
