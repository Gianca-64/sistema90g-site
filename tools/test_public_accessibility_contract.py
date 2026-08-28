#!/usr/bin/env python3

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("dist")
if not root.is_dir():
    raise SystemExit(f"ERRORE: directory pubblica non trovata: {root}")


class PageAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang: str | None = None
        self.title_depth = 0
        self.title_text: list[str] = []
        self.main_count = 0
        self.h1_count = 0
        self.ids: list[str] = []
        self.images_without_alt = 0
        self.labels_for: set[str] = set()
        self.controls: list[tuple[str, dict[str, str]]] = []
        self.button_stack: list[dict[str, object]] = []
        self.buttons: list[tuple[dict[str, str], str]] = []
        self.positive_tabindex: list[str] = []

    @staticmethod
    def attrs_dict(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {k.lower(): (v or "") for k, v in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        data = self.attrs_dict(attrs)

        if tag == "html" and self.html_lang is None:
            self.html_lang = data.get("lang", "").strip()
        elif tag == "title":
            self.title_depth += 1
        elif tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "img" and "alt" not in data:
            self.images_without_alt += 1
        elif tag == "label" and data.get("for"):
            self.labels_for.add(data["for"])
        elif tag in {"input", "select", "textarea"}:
            if not (tag == "input" and data.get("type", "").lower() == "hidden"):
                self.controls.append((tag, data))
        elif tag == "button":
            self.button_stack.append({"attrs": data, "text": []})

        if data.get("id"):
            self.ids.append(data["id"])

        tabindex = data.get("tabindex", "").strip()
        if tabindex:
            try:
                if int(tabindex) > 0:
                    self.positive_tabindex.append(f"<{tag} tabindex={tabindex}>")
            except ValueError:
                pass

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title" and self.title_depth:
            self.title_depth -= 1
        elif tag == "button" and self.button_stack:
            item = self.button_stack.pop()
            attrs = item["attrs"]
            text = " ".join(item["text"])
            assert isinstance(attrs, dict)
            self.buttons.append((attrs, text))

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)
        if self.button_stack:
            text_list = self.button_stack[-1]["text"]
            assert isinstance(text_list, list)
            text_list.append(data)


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


issues: list[str] = []
pages = sorted(root.rglob("*.html"))

for page in pages:
    rel = page.relative_to(root)
    parser = PageAudit()
    parser.feed(page.read_text("utf-8", errors="ignore"))

    if not parser.html_lang:
        issues.append(f"{rel}: <html> senza lang")
    if not compact(" ".join(parser.title_text)):
        issues.append(f"{rel}: <title> assente o vuoto")
    if parser.main_count < 1:
        issues.append(f"{rel}: manca <main>")
    if parser.h1_count < 1:
        issues.append(f"{rel}: manca <h1>")
    if parser.images_without_alt:
        issues.append(f"{rel}: {parser.images_without_alt} immagini senza attributo alt")

    seen: set[str] = set()
    duplicates: set[str] = set()
    for element_id in parser.ids:
        if element_id in seen:
            duplicates.add(element_id)
        seen.add(element_id)
    for duplicate in sorted(duplicates):
        issues.append(f"{rel}: id duplicato '{duplicate}'")

    for tag, attrs in parser.controls:
        control_id = attrs.get("id", "")
        labelled = bool(
            attrs.get("aria-label", "").strip()
            or attrs.get("aria-labelledby", "").strip()
            or attrs.get("title", "").strip()
            or (control_id and control_id in parser.labels_for)
        )
        if not labelled:
            name = attrs.get("name") or control_id or "senza id/name"
            issues.append(f"{rel}: <{tag}> '{name}' senza etichetta accessibile")

    for attrs, text in parser.buttons:
        if not (
            compact(text)
            or attrs.get("aria-label", "").strip()
            or attrs.get("aria-labelledby", "").strip()
            or attrs.get("title", "").strip()
        ):
            issues.append(f"{rel}: <button> senza nome accessibile")

    for item in parser.positive_tabindex:
        issues.append(f"{rel}: ordine tastiera forzato con {item}")

if issues:
    print("ERRORE: contratto accessibilità pubblico non rispettato:")
    for issue in issues:
        print(f" - {issue}")
    raise SystemExit(1)

print(f"OK public accessibility contract: {len(pages)} pagine HTML")
