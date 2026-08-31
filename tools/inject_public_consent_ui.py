#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

TECHNICAL_PAGES = {Path('consent-bridge.html')}
INLINE_CSS_MARKER = 'data-s90g-consent-ui-style'
JS_TAG = '<script defer src="/consent-ui.js" data-s90g-consent-ui></script>'
PRIVACY_TAG = '<script defer src="/privacy-consent.js"></script>'

css_asset = root / 'consent-ui.css'
if not css_asset.is_file():
    raise SystemExit('ERRORE: consent-ui.css mancante nell\'output pubblico')
css_text = css_asset.read_text('utf-8', errors='strict').strip()
INLINE_CSS_TAG = f'<style {INLINE_CSS_MARKER}>{css_text}</style>'

external_css_re = re.compile(r'<link\b[^>]*href=["\'][^"\']*consent-ui\.css(?:\?[^"\']*)?["\'][^>]*>', re.I)
inline_css_re = re.compile(r'<style\b[^>]*data-s90g-consent-ui-style[^>]*>.*?</style>', re.I | re.S)
ui_js_re = re.compile(r'<script\b[^>]*src=["\'][^"\']*consent-ui\.js(?:\?[^"\']*)?["\'][^>]*>\s*</script>', re.I)
privacy_re = re.compile(r'<script\b[^>]*src=["\'][^"\']*privacy-consent\.js(?:\?[^"\']*)?["\'][^>]*>\s*</script>', re.I)

issues: list[str] = []
changed = 0
privacy_added = 0
checked = 0

for page in sorted(root.rglob('*.html')):
    rel = page.relative_to(root)
    if rel in TECHNICAL_PAGES:
        continue
    checked += 1
    text = page.read_text('utf-8', errors='ignore')
    original = text

    # Il CSS del banner e molto piccolo e deve essere disponibile subito, ma non
    # giustifica una richiesta render-blocking separata. Lo incorporiamo quindi
    # nel documento mantenendo identico il comportamento visivo e senza FOUC.
    text = external_css_re.sub('', text)
    if not inline_css_re.search(text):
        if '</head>' not in text.lower():
            issues.append(f'{rel}: </head> mancante per iniezione Consent UI inline')
        else:
            text = re.sub(r'</head>', INLINE_CSS_TAG + '</head>', text, count=1, flags=re.I)

    privacy_match = privacy_re.search(text)
    ui_match = ui_js_re.search(text)
    if not ui_match:
        if privacy_match:
            text = text[:privacy_match.start()] + JS_TAG + text[privacy_match.start():]
        elif '</body>' in text.lower():
            text = re.sub(r'</body>', JS_TAG + PRIVACY_TAG + '</body>', text, count=1, flags=re.I)
            privacy_added += 1
        else:
            issues.append(f'{rel}: nessun privacy-consent.js e </body> mancante')

    if text != original:
        page.write_text(text, 'utf-8')
        changed += 1

if issues:
    print('ERRORE: impossibile integrare Consent UI pubblico:', file=sys.stderr)
    for issue in issues:
        print(f' - {issue}', file=sys.stderr)
    raise SystemExit(1)

print(
    f'Consent UI pubblico integrato: {checked} pagine di contenuto, '
    f'{changed} aggiornate, CSS inline, privacy-consent aggiunto a {privacy_added}'
)
