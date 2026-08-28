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

rm -rf "$OUT" "$ZIP"
mkdir -p "$OUT"

PAGES=(
  "home|https://sistema90g.it/"
  "free-entry|https://sistema90g.it/analisi-preventiva.html"
  "servizi|https://sistema90g.it/servizi.html"
  "approfondimento|https://sistema90g.it/approfondimenti/colonna-lavanderia-a-piena-capacita-con-comandi-ad-altezza-accessibile-1ff0f9c.html"
)

capture() {
  local name="$1" url="$2" width="$3" height="$4" suffix="$5"
  local profile="$OUT/profile-$suffix-$name"
  mkdir -p "$profile"
  "$CHROME" \
    --headless=new \
    --disable-gpu \
    --hide-scrollbars \
    --disable-extensions \
    --no-first-run \
    --no-default-browser-check \
    --user-data-dir="$profile" \
    --window-size="$width,$height" \
    --virtual-time-budget=5000 \
    --screenshot="$OUT/${name}-${suffix}.png" \
    "$url" >/dev/null 2>&1
  rm -rf "$profile"
  echo "OK ${name}-${suffix}.png"
}

for item in "${PAGES[@]}"; do
  name="${item%%|*}"
  url="${item#*|}"
  capture "$name" "$url" 1440 1100 desktop
  capture "$name" "$url" 390 844 mobile
done

cat > "$OUT/README.txt" <<'EOF'
P1 visual capture Sistema 90G

Screenshot live prodotti con Chrome headless:
- home: desktop + mobile
- Free Entry: desktop + mobile
- servizi: desktop + mobile
- approfondimento annidato: desktop + mobile

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
