#!/bin/bash
set -euo pipefail

BRANCH="main"
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"

if [[ "$(git branch --show-current)" != "$BRANCH" ]]; then
  echo "STOP: branch corrente non canonico. Atteso: $BRANCH" >&2
  exit 20
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "STOP: working tree non pulito." >&2
  git status --short
  exit 21
fi

export PATH="/opt/homebrew/opt/node@22/bin:$PATH"
if ! node -e 'const m=Number(process.versions.node.split(".")[0]); if(m<22) process.exit(1)'; then
  echo "STOP: Node.js 22 o superiore non disponibile nel PATH previsto." >&2
  exit 22
fi

git fetch origin "$BRANCH"
LOCAL="$(git rev-parse HEAD)"
REMOTE="$(git rev-parse "origin/$BRANCH")"
if [[ "$LOCAL" != "$REMOTE" ]]; then
  if git merge-base --is-ancestor "$LOCAL" "$REMOTE"; then
    git merge --ff-only "origin/$BRANCH"
  else
    echo "STOP: branch locale e remoto divergenti." >&2
    exit 23
  fi
fi

TMP_REDIRECTS="$(mktemp)"
cp _redirects "$TMP_REDIRECTS"
restore_redirects(){ cp "$TMP_REDIRECTS" _redirects 2>/dev/null || true; rm -f "$TMP_REDIRECTS"; }
trap restore_redirects EXIT

# La build Cloudflare richiede temporaneamente di rimuovere il redirect /index.html.
perl -0pi -e 's#^/index\.html / 301\n##m' _redirects
bash tools/build_cloudflare.sh
cp "$TMP_REDIRECTS" _redirects
cp "$TMP_REDIRECTS" dist/_redirects

test -f dist/index.html
test -f dist/_redirects
test -f dist/_headers
test -f dist/cucina-ad-angolo-guida.html
test -f dist/guide-cucina-sitemap.xml
test -f dist/innovazioni.html
test -f dist/approfondimenti/forno-intelligenza-artificiale-telecamera-cosa-cambia.html
test -f dist/approfondimenti/piano-induzione-opaco-antigraffio-cosa-cambia.html
test -f dist/images/editoriale/forno-ai-telecamera-editoriale.webp
test -f dist/images/editoriale/piano-induzione-opaco-editoriale.webp
grep -q 'Novità, tecnologie e soluzioni che migliorano la cucina di ogni giorno' dist/innovazioni.html
grep -q 'forno-ai-telecamera-editoriale.webp' dist/approfondimenti/forno-intelligenza-artificiale-telecamera-cosa-cambia.html
grep -q 'piano-induzione-opaco-editoriale.webp' dist/approfondimenti/piano-induzione-opaco-antigraffio-cosa-cambia.html
grep -q '^/index.html / 301$' dist/_redirects
! test -e dist/casi-camere-contenimento.html
! test -e dist/casi-distribuzione-casa.html
! test -e dist/casi-soggiorno-open-space.html
! test -e dist/casi-spazi-servizio.html

npx --yes wrangler@4 deploy

sleep 5
STAMP="$(date +%s)"
curl --fail --silent --show-error --location --retry 5 --retry-delay 2 "https://sistema90g.it/?verify=$STAMP" > /tmp/s90g-home.html
curl --fail --silent --show-error --location --retry 5 --retry-delay 2 "https://sistema90g.it/innovazioni.html?verify=$STAMP" > /tmp/s90g-innovazioni.html
grep -qi 'Sistema 90G' /tmp/s90g-home.html
grep -q 'Novità, tecnologie e soluzioni che migliorano la cucina di ogni giorno' /tmp/s90g-innovazioni.html

echo "DEPLOY VERIFIED: site $(git rev-parse --short HEAD)"
