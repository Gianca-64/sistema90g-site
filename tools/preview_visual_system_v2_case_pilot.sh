#!/bin/bash
set -euo pipefail

BRANCH="visual-system-v2-case-pilot"
PORT="4174"
BASE_URL="http://127.0.0.1:${PORT}"
SAMPLE_PAGES=(
  "caso-lavastoviglie-passaggio-cucina.html"
  "caso-isola-passaggi-cucina.html"
  "caso-preventivo-cucina-sconto-valore.html"
)

current_branch="$(git branch --show-current)"
if [ "$current_branch" != "$BRANCH" ]; then
  echo "ERRORE: questa preview richiede il branch $BRANCH (attuale: $current_branch)."
  exit 1
fi

if [ -n "$(git status --porcelain)" ]; then
  echo "ERRORE: repository non pulito. Nessuna preview avviata."
  git status --short
  exit 1
fi

echo "=== BUILD + CONTRATTI ==="
bash tools/build_cloudflare.sh

echo
echo "=== PREVIEW CASE VISUAL V2 ==="
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory dist >/tmp/s90g-case-v2-preview.log 2>&1 &
server_pid=$!

cleanup() {
  kill "$server_pid" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

first_url="$BASE_URL/${SAMPLE_PAGES[0]}"
for _ in {1..30}; do
  if curl -fsS "$first_url" >/dev/null 2>&1; then
    break
  fi
  sleep 0.2
done

for page in "${SAMPLE_PAGES[@]}"; do
  url="$BASE_URL/$page"
  if ! curl -fsS "$url" >/dev/null 2>&1; then
    echo "ERRORE: preview non raggiungibile su $url"
    exit 1
  fi
done

for page in "${SAMPLE_PAGES[@]}"; do
  open -a "Google Chrome" "$BASE_URL/$page"
done

echo "Preview campione aperta su 3 casi:"
echo " - lavastoviglie: 90G Use"
echo " - isola: 90G Conflict"
echo " - preventivo: 90G Compare"
echo "Nessun deploy eseguito. Premi Ctrl-C in questo Terminale per chiudere il server."
wait "$server_pid"
