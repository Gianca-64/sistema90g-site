#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ "$(git branch --show-current)" != "visual-system-v1" ]]; then
  echo "STOP: esegui il gate dal branch visual-system-v1." >&2
  exit 20
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "STOP: working tree non pulito." >&2
  git status --short
  exit 21
fi

export PATH="/opt/homebrew/opt/node@22/bin:$PATH"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -x "$CHROME" ]; then
  echo "STOP: Google Chrome non trovato in $CHROME" >&2
  exit 22
fi
if ! command -v node >/dev/null 2>&1; then
  echo "STOP: Node.js non disponibile." >&2
  exit 23
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "STOP: python3 non disponibile." >&2
  exit 24
fi

printf '\n=== 1/3 BUILD + CONTRATTI ===\n'
bash tools/build_cloudflare.sh

PORT=4174
URL="http://127.0.0.1:${PORT}/"
LOG="/tmp/s90g-visual-system-v1-audit.log"
python3 -m http.server "$PORT" --bind 127.0.0.1 --directory "$ROOT/dist" >"$LOG" 2>&1 &
SERVER_PID=$!
cleanup(){ kill "$SERVER_PID" 2>/dev/null || true; }
trap cleanup EXIT INT TERM

for _ in {1..30}; do
  if /usr/bin/curl -fsS "$URL" >/dev/null 2>&1; then break; fi
  sleep 0.2
done
if ! /usr/bin/curl -fsS "$URL" >/dev/null 2>&1; then
  echo "STOP: server locale non raggiungibile. Log: $LOG" >&2
  exit 25
fi

printf '\n=== 2/3 PERFORMANCE LOCALE ===\n'
node tools/audit_visual_system_v1_performance.mjs "$CHROME" "$URL"

printf '\n=== 3/3 STATO REPOSITORY ===\n'
if [[ -n "$(git status --porcelain)" ]]; then
  echo "STOP: il gate ha lasciato modifiche nel repository." >&2
  git status --short
  exit 26
fi

echo "OK repository pulito."
echo
echo "VISUAL SYSTEM V1: GATE LOCALE COMPLETATO."
echo "Nessun deploy eseguito e nessuna modifica a main."
