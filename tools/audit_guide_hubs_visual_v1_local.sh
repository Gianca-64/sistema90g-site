#!/usr/bin/env bash
set -euo pipefail

BRANCH="visual-system-v10-guide-hubs-rollout"
PORT="4182"
BASE_URL="http://127.0.0.1:${PORT}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$HOME/Desktop/Sistema90G-Guide-Hubs-Visual-V1-Audit"

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
echo "=== 2/3 AUDIT VISUALE AUTOMATICO DEI 4 HUB ==="
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory dist >/tmp/s90g-guide-hubs-v1-audit-preview.log 2>&1 &
server_pid=$!
cleanup(){ kill "$server_pid" >/dev/null 2>&1 || true; }
trap cleanup EXIT INT TERM

for _ in {1..30}; do
  if /usr/bin/curl -fsS "$BASE_URL/preventivo-acquisto-cucina-guide.html" >/dev/null 2>&1; then break; fi
  sleep 0.2
done
if ! /usr/bin/curl -fsS "$BASE_URL/preventivo-acquisto-cucina-guide.html" >/dev/null 2>&1; then
  echo "ERRORE: server locale non raggiungibile su $BASE_URL"
  exit 1
fi

mkdir -p "$OUT"
find "$OUT" -mindepth 1 -maxdepth 1 -exec rm -rf {} +

capture_hub(){
  local rel="$1"
  local key="$2"
  local dir="$OUT/$key"
  mkdir -p "$dir"
  node "$ROOT/tools/capture_visual_page.mjs" "$CHROME" "$dir" "$BASE_URL" "$rel" "$key"
}

capture_hub "preventivo-acquisto-cucina-guide.html" "guide-hub-preventivo"
capture_hub "progettare-cucina-guide.html" "guide-hub-progettazione"
capture_hub "elettrodomestici-impianti-cucina-guide.html" "guide-hub-tecnico"
capture_hub "materiali-finiture-cucina-guide.html" "guide-hub-materiali"

python3 - "$OUT" <<'PY'
import json
import pathlib
import sys
root = pathlib.Path(sys.argv[1])
rows = []
for metrics in sorted(root.glob('*/metrics.json')):
    rows.extend(json.loads(metrics.read_text('utf-8')))
(root / 'metrics-all.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f"OK metriche aggregate: {len(rows)} viewport verificati")
PY

cat > "$OUT/README.txt" <<EOF
Sistema 90G — Guide Hubs Visual V1 audit locale
Branch: $BRANCH

Pagine:
- preventivo-acquisto-cucina-guide.html
- progettare-cucina-guide.html
- elettrodomestici-impianti-cucina-guide.html
- materiali-finiture-cucina-guide.html

Per ogni pagina:
- desktop 1440x1100
- mobile 390x844
- H1 presente
- immagini caricate
- nessun overflow orizzontale

Metriche aggregate: metrics-all.json
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
echo "GUIDE HUBS VISUAL V1: GATE LOCALE COMPLETATO."
echo "Risultati: $OUT"
echo "Nessun deploy eseguito e nessuna modifica a main."
