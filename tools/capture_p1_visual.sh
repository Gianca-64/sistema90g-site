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
  local screenshot="$OUT/${name}-${suffix}.png"

  rm -rf "$profile" "$screenshot"
  mkdir -p "$profile"
  echo "Cattura ${name}-${suffix}..."

  python3 - "$CHROME" "$profile" "$width" "$height" "$screenshot" "$url" <<'PY'
import os
import pathlib
import shutil
import signal
import subprocess
import sys

chrome, profile, width, height, screenshot, url = sys.argv[1:]
screenshot_path = pathlib.Path(screenshot)
profile_path = pathlib.Path(profile)

common = [
    "--disable-gpu",
    "--hide-scrollbars",
    "--disable-extensions",
    "--disable-background-networking",
    "--disable-component-update",
    "--disable-sync",
    "--metrics-recording-only",
    "--no-first-run",
    "--no-default-browser-check",
    f"--user-data-dir={profile}",
    f"--window-size={width},{height}",
    "--virtual-time-budget=5000",
    "--run-all-compositor-stages-before-draw",
    f"--screenshot={screenshot}",
    url,
]

last_output = ""
for headless_mode in ("--headless=new", "--headless"):
    if screenshot_path.exists():
        screenshot_path.unlink()
    cmd = [chrome, headless_mode, *common]
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    timed_out = False
    try:
        output, _ = proc.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(proc.pid, signal.SIGKILL)
        output, _ = proc.communicate()
    last_output = output or ""

    # Chrome puo lasciare lo screenshot valido pochi istanti prima di terminare.
    if screenshot_path.is_file() and screenshot_path.stat().st_size > 10_000:
        shutil.rmtree(profile_path, ignore_errors=True)
        sys.exit(0)

    if timed_out:
        print(f"Tentativo {headless_mode} scaduto dopo 20 secondi.", file=sys.stderr)
    else:
        print(f"Tentativo {headless_mode} terminato senza screenshot valido (exit {proc.returncode}).", file=sys.stderr)

shutil.rmtree(profile_path, ignore_errors=True)
print("ERRORE: Chrome non ha prodotto lo screenshot.", file=sys.stderr)
if last_output.strip():
    print("Ultime righe Chrome:", file=sys.stderr)
    print("\n".join(last_output.strip().splitlines()[-12:]), file=sys.stderr)
sys.exit(1)
PY

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
