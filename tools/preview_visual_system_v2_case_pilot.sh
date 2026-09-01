#!/bin/bash
set -euo pipefail

BRANCH="visual-system-v2-case-pilot"
PORT="4174"
URL="http://127.0.0.1:${PORT}/caso-lavastoviglie-passaggio-cucina.html"

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

for _ in {1..30}; do
  if curl -fsS "$URL" >/dev/null 2>&1; then
    break
  fi
  sleep 0.2
done

if ! curl -fsS "$URL" >/dev/null 2>&1; then
  echo "ERRORE: preview non raggiungibile su $URL"
  exit 1
fi

open -a "Google Chrome" "$URL"

echo "Preview aperta: $URL"
echo "Nessun deploy eseguito. Premi Ctrl-C in questo Terminale per chiudere il server."
wait "$server_pid"
