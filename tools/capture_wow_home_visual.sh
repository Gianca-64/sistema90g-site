#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT="$HOME/Desktop/Sistema90G-WOW-Home-Visual"
ZIP="$HOME/Desktop/Sistema90G-WOW-Home-Visual.zip"
TARGET_URL="${1:-http://127.0.0.1:4173/}"

if [ ! -x "$CHROME" ]; then
  echo "ERRORE: Google Chrome non trovato in $CHROME" >&2
  exit 1
fi
if ! command -v node >/dev/null 2>&1; then
  echo "ERRORE: Node.js non trovato" >&2
  exit 1
fi
NODE_MAJOR="$(node -p 'process.versions.node.split(".")[0]')"
if [ "$NODE_MAJOR" -lt 22 ]; then
  echo "ERRORE: serve Node.js 22 o successivo (trovato $(node -v))" >&2
  exit 1
fi
if ! /usr/bin/curl -fsS "$TARGET_URL" >/dev/null 2>&1; then
  echo "ERRORE: preview non raggiungibile: $TARGET_URL" >&2
  echo "Avvia prima bash tools/preview_visual_system_v1.sh e lascia aperto quel Terminale." >&2
  exit 2
fi

rm -rf "$OUT" "$ZIP"
mkdir -p "$OUT"
node "$ROOT/tools/capture_wow_home_visual.mjs" "$CHROME" "$OUT" "$TARGET_URL"

cat > "$OUT/README.txt" <<EOF
Sistema 90G — verifica visuale Home WOW
Sorgente verificata: $TARGET_URL

Contenuto:
- visual-proof-desktop.png
- visual-proof-mobile.png
- situation-selector-desktop.png
- situation-selector-mobile.png
- home-full-desktop.png
- home-full-mobile.png
- metrics.json

Controllare:
- nessun overflow orizzontale;
- marker leggibili e non sovrapposti;
- immagini non deformate;
- card visuali desktop 2 colonne / mobile 1 colonna;
- selettore situazione leggibile;
- CTA e cookie banner non coprono contenuti essenziali.
EOF

(
  cd "$HOME/Desktop"
  /usr/bin/zip -qr "$(basename "$ZIP")" "$(basename "$OUT")"
)

echo
echo "PACCHETTO WOW CREATO: $ZIP"
echo "Sorgente: $TARGET_URL"
echo "Il repository resta pulito: il pacchetto e' stato salvato sul Desktop."
