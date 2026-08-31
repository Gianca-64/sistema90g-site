#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlsplit
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('dist')
if not root.is_dir():
    raise SystemExit(f'ERRORE: directory pubblica non trovata: {root}')

TECHNICAL_PAGES = {Path('consent-bridge.html')}
attr_re = re.compile(r'''(?:src|href)\s*=\s*["']([^"']+)["']''', re.I)
inline_css_re = re.compile(r'<style\b[^>]*data-s90g-consent-ui-style[^>]*>(.*?)</style>', re.I | re.S)
issues: list[str] = []
checked = 0

for page in sorted(root.rglob('*.html')):
    rel = page.relative_to(root)
    if rel in TECHNICAL_PAGES:
        continue
    checked += 1
    text = page.read_text('utf-8', errors='ignore')
    refs = [urlsplit(m.group(1).strip()).path for m in attr_re.finditer(text)]

    def count_suffix(name: str) -> int:
        return sum(1 for ref in refs if ref.endswith('/' + name) or ref == name)

    for name in ('consent-ui.js', 'privacy-consent.js'):
        count = count_suffix(name)
        if count != 1:
            issues.append(f'{rel}: atteso 1 riferimento a {name}, trovati {count}')

    if count_suffix('consent-ui.css') != 0:
        issues.append(f'{rel}: consent-ui.css non deve generare una richiesta esterna')

    inline_matches = inline_css_re.findall(text)
    if len(inline_matches) != 1:
        issues.append(f'{rel}: atteso 1 blocco CSS Consent UI inline, trovati {len(inline_matches)}')
    elif '.s90g-consent-banner' not in inline_matches[0]:
        issues.append(f'{rel}: CSS Consent UI inline incompleto')

    ui_pos = text.find('consent-ui.js')
    privacy_pos = text.find('privacy-consent.js')
    if ui_pos < 0 or privacy_pos < 0 or ui_pos > privacy_pos:
        issues.append(f'{rel}: consent-ui.js deve precedere privacy-consent.js')

ui_path = root / 'consent-ui.js'
css_path = root / 'consent-ui.css'
privacy_path = root / 'privacy-consent.js'

if not ui_path.is_file():
    issues.append('consent-ui.js: asset pubblico mancante')
else:
    ui = ui_path.read_text('utf-8', errors='ignore')
    requirements = {
        "banner.id = 'cookie-banner'": 'banner cookie non creato',
        'data-cookie-choice="reject"': 'azione Rifiuta mancante',
        'data-cookie-choice="accept"': 'azione Accetta mancante',
        "link.dataset.cookieSettings = 'true'": 'link Gestisci cookie mancante',
        '/privacy-policy.html': 'link Privacy mancante',
        '/cookie-policy.html': 'link Cookie policy mancante',
        "banner.hidden = true": 'banner non inizializzato nascosto',
        "aria-labelledby": 'banner senza etichetta accessibile',
    }
    for token, label in requirements.items():
        if token not in ui:
            issues.append(f'consent-ui.js: {label}')

if not css_path.is_file():
    issues.append('consent-ui.css: asset sorgente pubblico mancante')
else:
    css = css_path.read_text('utf-8', errors='ignore')
    for token, label in {
        '.s90g-consent-banner': 'stile banner mancante',
        '.s90g-consent-banner[hidden]': 'stato hidden mancante',
        '@media(max-width:700px)': 'hardening mobile mancante',
        'min-height:44px': 'target touch minimo mancante',
    }.items():
        if token not in css:
            issues.append(f'consent-ui.css: {label}')

if not privacy_path.is_file():
    issues.append('privacy-consent.js: runtime pubblico mancante')
else:
    privacy = privacy_path.read_text('utf-8', errors='ignore')
    for token, label in {
        "analytics_storage:'denied'": 'analytics non denied di default',
        "c==='accepted'": 'gestione consenso accepted mancante',
        "c==='rejected'": 'gestione consenso rejected mancante',
        "[data-cookie-choice]": 'handler scelte cookie mancante',
        'loadAnalytics()': 'attivazione analytics dopo consenso mancante',
        'denyAnalytics()': 'blocco analytics dopo rifiuto mancante',
    }.items():
        if token not in privacy:
            issues.append(f'privacy-consent.js: {label}')

if issues:
    print('ERRORE: contratto consenso pubblico non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print(
    f'OK public consent contract: {checked} pagine con Consent UI CSS inline + '
    'privacy-consent, analytics denied fino a consenso'
)
