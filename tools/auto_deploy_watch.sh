#!/bin/bash
set -euo pipefail

ROOT="${S90G_SITE_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
LOG_DIR="$HOME/Library/Logs/Sistema90G"
mkdir -p "$LOG_DIR"
exec >>"$LOG_DIR/site-autodeploy.log" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] check site"
cd "$ROOT"

if [[ "$(git branch --show-current)" != "main" ]]; then
  echo "STOP: branch non main"
  exit 30
fi
if [[ -n "$(git status --porcelain)" ]]; then
  echo "STOP: working tree non pulito"
  git status --short
  exit 31
fi

git fetch origin main
LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse origin/main)"
[[ "$LOCAL" == "$REMOTE" ]] && { echo "Nessun aggiornamento"; exit 0; }

if ! git merge-base --is-ancestor "$LOCAL" "$REMOTE"; then
  echo "STOP: divergenza locale/remoto"
  exit 32
fi

git merge --ff-only origin/main
bash tools/deploy_verified_local.sh
