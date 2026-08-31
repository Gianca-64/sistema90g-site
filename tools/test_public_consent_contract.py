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
nav_bootstrap_script_re = re.compile(
    r'<script\b[^>]*data-s90g-nav-bootstrap[^>]*>\s*document\.documentElement\.classList\.add\(["\']s90g-js["\']\)\s*</script>',
    re.I,
)
nav_bootstrap_style_re = re.compile(
    r'<style\b[^>]*data-s90g-nav-bootstrap[^>]*>.*?html\.s90g-js\s+\.s90g-header\s+\.s90g-nav\s*\{display:none\}.*?html\.s90g-js\s+\.s90g-header\.is-nav-open\s+\.s90g-nav\s*\{display:grid\}.*?</style>',
    re.I | re.S,
)
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

    for name in ('consent-ui.css', 'consent-ui.js', 'privacy-consent.js'):
        count = count_suffix(name)
        if count != 1:
            issues.append(f'{rel}: atteso 1 riferimento a {name}, trovati {count}')

    script_match = nav_bootstrap_script_re.search(text)
    style_match = nav_bootstrap_style_re.search(text)
    if not script_match:
        issues.append(f'{rel}: bootstrap JS navigazione mobile mancante')
    if not style_match:
        issues.append(f'{rel}: stile bootstrap navigazione mobile mancante')
    first_stylesheet = re.search(r'<link\b[^>]*rel=["\']stylesheet["\'][^>]*>', text, re.I)
    if script_match and first_stylesheet and script_match.start() > first_stylesheet.start():
        issues.append(f'{rel}: bootstrap navigazione deve precedere il primo stylesheet')

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
    issues.append('consent-ui.css: asset pubblico mancante')
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
    print('ERRORE: contratto UI pubblico non rispettato:')
    for issue in issues:
        print(f' - {issue}')
    raise SystemExit(1)

print(
    f'OK public consent contract: {checked} pagine con nav mobile stabile + '
    'Consent UI + privacy-consent, analytics denied fino a consenso'
)
