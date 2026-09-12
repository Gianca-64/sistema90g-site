#!/usr/bin/env python3

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

LEGACY = {
    "professionisti",
    "professionisti-progetto-cucina",
    "agenzie-immobiliari-cucina",
    "rivenditori-cucine",
    "studio-preliminare-spazi",
    "verifica-planimetria-distribuzione-casa",
}

redirects_text = (
    ROOT
    / "_redirects"
).read_text(errors="replace")

redirected_source_files = set()

for raw_line in redirects_text.splitlines():
    line = raw_line.strip()

    if not line or line.startswith("#"):
        continue

    parts = line.split()

    if len(parts) < 3:
        continue

    source, _, status = parts[:3]

    if status != "301" or "*" in source:
        continue

    source = source.split("?", 1)[0]

    if source.endswith(".html"):
        redirected_source_files.add(
            source.lstrip("/")
        )

errors = []

slug_pattern = "|".join(
    re.escape(x)
    for x in sorted(
        LEGACY,
        key=len,
        reverse=True,
    )
)

link_re = re.compile(
    rf'href=["\']/?(?:{slug_pattern})(?:\.html)?'
    rf'(?:[#?][^"\']*)?["\']',
    re.I,
)

role_re = re.compile(
    r'(?:requester_role|requesterRole)='
    r'(?!private(?:[&#"\']|$))',
    re.I,
)

role_hint_re = re.compile(
    r'data-role-hint=["\']'
    r'(?:retailer|professional|technician|agency|company)'
    r'["\']',
    re.I,
)

for path in ROOT.rglob("*.html"):
    if any(
        part in {
            ".git",
            "node_modules",
            "dist",
        }
        for part in path.parts
    ):
        continue

    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(errors="replace")

    # Files intercepted by an exact permanent redirect
    # are not part of the effective public HTML surface.
    if rel not in redirected_source_files:
        if link_re.search(text):
            errors.append(
                f"{rel}: public link to retired B2B route"
            )

        if role_re.search(text):
            errors.append(
                f"{rel}: non-private requester role exposed"
            )

        if role_hint_re.search(text):
            errors.append(
                f"{rel}: B2B role hint exposed"
            )

free_entry = (
    ROOT
    / "analisi-preventiva.html"
).read_text(errors="replace")

if "requester_role=private" not in free_entry:
    errors.append(
        "analisi-preventiva.html: "
        "private Free Entry contract missing"
    )

if "service=valutazione-iniziale" not in free_entry:
    errors.append(
        "analisi-preventiva.html: "
        "Free Entry service contract missing"
    )

redirects = redirects_text

for slug in LEGACY:
    for route in (
        f"/{slug}",
        f"/{slug}.html",
    ):
        pattern = re.compile(
            rf'^{re.escape(route)}\s+'
            r'/[^\s]+\s+301\s*$',
            re.M,
        )

        if not pattern.search(redirects):
            errors.append(
                f"_redirects: missing 301 for {route}"
            )

for sitemap in ROOT.glob("sitemap*.xml"):
    text = sitemap.read_text(errors="replace")

    for slug in LEGACY:
        if re.search(
            rf'https?://[^<]+/{re.escape(slug)}'
            rf'(?:\.html)?(?:<|$)',
            text,
            re.I,
        ):
            errors.append(
                f"{sitemap.name}: legacy B2B URL {slug}"
            )

if errors:
    print("B2C-ONLY PUBLIC SURFACE: FAIL")
    for error in errors:
        print(f"FAIL — {error}")
    sys.exit(1)

print("PASS — Free Entry is private-only")
print("PASS — no public internal links to retired B2B offers")
print("PASS — no B2B requester roles or role hints")
print("PASS — all retired B2B URLs have 301 redirects")
print("PASS — retired B2B URLs absent from sitemaps")
print("B2C-ONLY PUBLIC SURFACE: PASS")
