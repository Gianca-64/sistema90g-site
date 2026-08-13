#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-dist}"

if [ ! -d "$TARGET" ]; then
  echo "ERRORE: directory non trovata: $TARGET" >&2
  exit 1
fi

patterns=(
  'progetti casa e cucina'
  'progetti, spazi, preventivi e cucine'
  'casi-cucina.html'
  'scelta-finiture-casa.html'
)

for pattern in "${patterns[@]}"; do
  if grep -RIl --include='*.html' --include='*.xml' -- "$pattern" "$TARGET" >/dev/null 2>&1; then
    echo "ERRORE: residuo legacy presente: $pattern" >&2
    grep -RIl --include='*.html' --include='*.xml' -- "$pattern" "$TARGET" >&2 || true
    exit 1
  fi
done

case_count="$(find "$TARGET" -maxdepth 1 -type f -name 'caso-*.html' | wc -l | tr -d ' ')"
if [ "$case_count" -ne 6 ]; then
  echo "ERRORE: attesi 6 casi cucina pubblici, trovati $case_count" >&2
  exit 1
fi

echo "OK: perimetro pubblico cucina validato"
