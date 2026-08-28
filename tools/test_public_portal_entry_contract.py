#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PORTAL_HOST = "portale.sistema90g.it"
PUBLIC_SERVICE = "valutazione-iniziale"


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "dist")
    if not root.is_dir():
        print(f"ERRORE: directory pubblica non trovata: {root}", file=sys.stderr)
        return 2

    errors: list[str] = []
    checked = 0

    for html in sorted(root.rglob("*.html")):
        text = html.read_text(encoding="utf-8", errors="replace")
        marker = "https://portale.sistema90g.it/"
        start = 0
        while True:
            pos = text.find(marker, start)
            if pos < 0:
                break
            end_candidates = [p for p in (text.find('"', pos), text.find("'", pos), text.find("<", pos)) if p >= 0]
            end = min(end_candidates) if end_candidates else len(text)
            raw = text[pos:end].replace("&amp;", "&")
            start = max(end, pos + len(marker))

            parsed = urlparse(raw)
            if parsed.hostname != PORTAL_HOST:
                continue
            checked += 1
            service = parse_qs(parsed.query).get("service", [""])[0]
            if service != PUBLIC_SERVICE:
                rel = html.relative_to(root)
                errors.append(f"{rel}: CTA Portale pubblica con service={service or '<mancante>'}: {raw}")

    if errors:
        print("ERRORE: il Portale pubblico accetta solo la Valutazione iniziale gratuita.", file=sys.stderr)
        for error in errors:
            print(f" - {error}", file=sys.stderr)
        return 1

    print(f"OK public Portal entry contract: {checked} CTA, solo {PUBLIC_SERVICE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
