#!/usr/bin/env python3
from __future__ import annotations

import html.parser
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NavParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_nav = False
        self.anchor_href: str | None = None
        self.anchor_text: list[str] = []
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): (value or "") for key, value in attrs}
        if tag.lower() == "nav" and "s90g-nav" in attributes.get("class", "").split():
            self.in_nav = True
        elif tag.lower() == "a" and self.in_nav:
            self.anchor_href = attributes.get("href", "")
            self.anchor_text = []

    def handle_data(self, data: str) -> None:
        if self.anchor_href is not None:
            self.anchor_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "a" and self.anchor_href is not None:
            text = " ".join("".join(self.anchor_text).split())
            self.links.append((self.anchor_href, text))
            self.anchor_href = None
            self.anchor_text = []
        elif tag == "nav" and self.in_nav:
            self.in_nav = False


variants: dict[tuple[tuple[str, str], ...], list[str]] = defaultdict(list)
for path in sorted(ROOT.rglob("*.html")):
    if ".git" in path.parts or path.name.startswith("._"):
        continue
    parser = NavParser()
    parser.feed(path.read_text("utf-8", errors="replace"))
    if parser.links:
        variants[tuple(parser.links)].append(path.relative_to(ROOT).as_posix())

print(f"Navigation variants found: {len(variants)}")
for index, (nav, files) in enumerate(variants.items(), 1):
    print(f"\nVARIANT {index} — {len(files)} page(s)")
    print("Links:")
    for href, text in nav:
        print(f"  - {text}: {href}")
    print("Pages:")
    for filename in files:
        print(f"  - {filename}")
