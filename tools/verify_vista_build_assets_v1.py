#!/usr/bin/env python3

from pathlib import Path
from html.parser import HTMLParser
import sys


ROOT = Path(__file__).resolve().parents[1]

BUILD = (
    ROOT
    / "tools/build_cloudflare.sh"
)

HOME = (
    ROOT
    / "index.html"
)

CLEAN = "02_HOME_SCENA_PULITA.jpg"
ANALYSED = "02_HOME_SCENA_PROBLEMA.jpg"

errors = []


build = BUILD.read_text(
    errors="replace"
)

home = HOME.read_text(
    errors="replace"
)


if (
    "for dir in images editoriale approfondimenti .well-known; do"
    not in build
):
    errors.append(
        "public build no longer copies images directory"
    )


if (
    'cp -R "$ROOT/$dir" "$DIST/$dir"'
    not in build
):
    errors.append(
        "public directory copy implementation missing"
    )


if (
    f'"$DIST/images/{ANALYSED}"'
    in build
):
    errors.append(
        "Vista analysed asset is still deleted from dist"
    )


for filename in (
    CLEAN,
    ANALYSED,
):

    path = (
        ROOT
        / "images"
        / filename
    )

    if not path.is_file():
        errors.append(
            f"source Vista asset missing: {filename}"
        )

    if filename not in home:
        errors.append(
            f"Home does not reference Vista asset: {filename}"
        )


class Parser(HTMLParser):

    def __init__(self):
        super().__init__()
        self.layers = []

    def handle_starttag(
        self,
        tag,
        attrs,
    ):

        if tag != "img":
            return

        data = dict(attrs)

        classes = data.get(
            "class",
            ""
        )

        if (
            "s90g-vista-clean-layer"
            in classes
            or
            "s90g-vista-analysed-layer"
            in classes
        ):
            self.layers.append(
                data
            )


parser = Parser()
parser.feed(home)


if len(parser.layers) != 2:

    errors.append(
        f"expected 2 Vista layers, "
        f"found {len(parser.layers)}"
    )

else:

    clean = next(
        (
            item
            for item in parser.layers
            if "s90g-vista-clean-layer"
            in item.get(
                "class",
                "",
            )
        ),
        None,
    )

    analysed = next(
        (
            item
            for item in parser.layers
            if "s90g-vista-analysed-layer"
            in item.get(
                "class",
                "",
            )
        ),
        None,
    )

    if not clean:

        errors.append(
            "clean Vista layer missing"
        )

    elif not clean.get(
        "alt",
        "",
    ).strip():

        errors.append(
            "clean Vista layer needs descriptive alt"
        )


    if not analysed:

        errors.append(
            "analysed Vista layer missing"
        )

    else:

        if analysed.get(
            "alt"
        ) != "":

            errors.append(
                "analysed layer must keep empty alt"
            )

        if analysed.get(
            "aria-hidden"
        ) != "true":

            errors.append(
                "analysed layer must remain aria-hidden"
            )


if errors:

    print(
        "VISTA BUILD ASSETS V1: FAIL"
    )

    for error in errors:
        print(
            "FAIL —",
            error,
        )

    sys.exit(1)


print(
    "PASS — public build copies images directory"
)

print(
    "PASS — Vista analysed asset is not removed from dist"
)

print(
    "PASS — both canonical Vista source assets exist"
)

print(
    "PASS — Home references both Vista layers"
)

print(
    "PASS — analysed layer keeps intentional accessible semantics"
)

print(
    "VISTA BUILD ASSETS V1: PASS"
)
