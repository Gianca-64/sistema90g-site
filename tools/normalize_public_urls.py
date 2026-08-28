#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


TARGET = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")

if not TARGET.is_dir():
    raise SystemExit(f"ERRORE: directory non trovata: {TARGET}")

LEGACY_ROUTE_MIGRATIONS = {
    "acquisto-assistito-cucina": "sviluppo-avanzato-progetto-cucina",
}

# Cloudflare Workers Static Assets usa di default html_handling=auto-trailing-slash:
# /pagina.html -> /pagina. Il contenuto pubblico deve quindi dichiarare e collegare
# direttamente l'URL pulito, evitando canonical/sitemap che puntano a una redirect.
ABSOLUTE_HTML_URL = re.compile(
    r"https://sistema90g\.it/(?P<path>[A-Za-z0-9_./~-]+)\.html(?P<suffix>[?#][A-Za-z0-9_=&%./:~+,-]*)?"
)
ROOT_HTML_URL = re.compile(
    r"(?P<path>/(?!/)[A-Za-z0-9_./~-]+)\.html(?P<suffix>[?#][A-Za-z0-9_=&%./:~+,-]*)?"
)


def clean_public_text(text: str) -> str:
    # La home resta semplicemente '/'.
    text = text.replace("https://sistema90g.it/index.html", "https://sistema90g.it/")
    text = text.replace("/index.html", "/")

    for old_slug, new_slug in LEGACY_ROUTE_MIGRATIONS.items():
        text = text.replace(old_slug, new_slug)

    def absolute_repl(match: re.Match[str]) -> str:
        suffix = match.group("suffix") or ""
        return f"https://sistema90g.it/{match.group('path')}{suffix}"

    text = ABSOLUTE_HTML_URL.sub(absolute_repl, text)

    def root_repl(match: re.Match[str]) -> str:
        suffix = match.group("suffix") or ""
        return f"{match.group('path')}{suffix}"

    return ROOT_HTML_URL.sub(root_repl, text)


changed = 0
for pattern in ("*.html", "*.xml"):
    for path in TARGET.rglob(pattern):
        original = path.read_text(encoding="utf-8", errors="strict")
        updated = clean_public_text(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1

# Anche i due runtime che classificano le pagine servizio devono conoscere il nuovo slug.
for runtime_name in ("navigation-conversion.js", "privacy-consent.js"):
    runtime = TARGET / runtime_name
    if runtime.is_file():
        original = runtime.read_text(encoding="utf-8", errors="strict")
        updated = original
        for old_slug, new_slug in LEGACY_ROUTE_MIGRATIONS.items():
            updated = updated.replace(old_slug, new_slug)
        if updated != original:
            runtime.write_text(updated, encoding="utf-8")
            changed += 1

# Nei redirect manteniamo la sorgente legacy (.html), ma portiamo la destinazione
# direttamente all'URL pulito per evitare catene 301 -> 307.
redirects = TARGET / "_redirects"
if redirects.exists():
    lines = []
    redirects_changed = False
    for raw_line in redirects.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            lines.append(raw_line)
            continue

        parts = raw_line.split()
        if len(parts) >= 2:
            target = parts[1]
            if target == "/index.html":
                parts[1] = "/"
            elif target.startswith("/") and ".html" in target:
                base, sep, fragment = target.partition("#")
                query_base, query_sep, query = base.partition("?")
                if query_base.endswith(".html"):
                    query_base = query_base[:-5]
                    rebuilt = query_base
                    if query_sep:
                        rebuilt += "?" + query
                    if sep:
                        rebuilt += "#" + fragment
                    parts[1] = rebuilt
            updated_line = " ".join(parts)
            redirects_changed = redirects_changed or updated_line != raw_line
            lines.append(updated_line)
        else:
            lines.append(raw_line)

    for old_slug, new_slug in LEGACY_ROUTE_MIGRATIONS.items():
        for source in (f"/{old_slug}", f"/{old_slug}.html"):
            rule = f"{source} /{new_slug} 301"
            if rule not in lines:
                lines.append(rule)
                redirects_changed = True
        legacy_file = TARGET / f"{old_slug}.html"
        if legacy_file.exists():
            legacy_file.unlink()
            changed += 1

    if redirects_changed:
        redirects.write_text("\n".join(lines) + "\n", encoding="utf-8")
        changed += 1

# Gate: nessun URL canonico/sitemap o link interno pubblico deve ancora dichiarare
# un percorso .html. I file fisici restano .html: è solo la forma pubblica dell'URL
# a essere normalizzata.
residuals: list[str] = []
checks = (
    re.compile(r"https://sistema90g\.it/[^\s\"'<>]+\.html(?:[?#][^\s\"'<>]*)?"),
    re.compile(r"(?:href|action)=[\"']/[^\"']+\.html(?:[?#][^\"']*)?[\"']", re.I),
)
for pattern in ("*.html", "*.xml"):
    for path in TARGET.rglob(pattern):
        text = path.read_text(encoding="utf-8", errors="strict")
        for check in checks:
            match = check.search(text)
            if match:
                residuals.append(f"{path.relative_to(TARGET)}: {match.group(0)}")
                break

if residuals:
    print("ERRORI URL PUBBLICI:", file=sys.stderr)
    for item in residuals:
        print(f"- {item}", file=sys.stderr)
    raise SystemExit(1)

print(f"URL pubblici normalizzati: {changed} file aggiornati")
