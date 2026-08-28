#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/p1-visual-capture"
ZIP="$ROOT/p1-visual-capture.zip"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

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
  echo "ERRORE: serve Node.js 22 o successivo per la cattura DevTools (trovato $(node -v))" >&2
  exit 1
fi

rm -rf "$OUT" "$ZIP"
mkdir -p "$OUT"

node "$ROOT/tools/capture_p1_visual.mjs" "$CHROME" "$OUT"

cat > "$OUT/README.txt" <<'EOF'
P1 visual capture Sistema 90G

Screenshot live prodotti con Chrome + DevTools Protocol:
- home: desktop 1440x1100 + mobile reale 390x844
- Free Entry: desktop 1440x1100 + mobile reale 390x844
- servizi: desktop 1440x1100 + mobile reale 390x844
- approfondimento annidato: desktop 1440x1100 + mobile reale 390x844

metrics.json registra per ogni cattura innerWidth, innerHeight, clientWidth e scrollWidth.
Il campo horizontalOverflow permette di distinguere un overflow reale del sito da un semplice ritaglio dello screenshot.

Controllare in particolare:
- header/nav/CTA senza overflow o sovrapposizioni;
- banner cookie e pulsanti visibili;
- chat non sovrapposta al banner;
- testo e CTA leggibili;
- immagini senza tagli anomali;
- pagina /approfondimenti/ con asset e runtime corretti.
EOF

(
  cd "$ROOT"
  /usr/bin/zip -qr "$(basename "$ZIP")" "$(basename "$OUT")"
)

echo
echo "PACCHETTO VISUALE CREATO: $ZIP"
echo "Allega p1-visual-capture.zip alla chat per la verifica finale P1."
