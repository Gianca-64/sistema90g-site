from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

IT = (
    ROOT
    / "index.html"
).read_text(
    encoding="utf-8",
)

EN = (
    ROOT
    / "en"
    / "index.html"
).read_text(
    encoding="utf-8",
)

HOME_JS = (
    ROOT
    / "s90g-home-acquisition-v1.js"
).read_text(
    encoding="utf-8",
)

EN_JS = (
    ROOT
    / "s90g-site-en-gb-v1.js"
).read_text(
    encoding="utf-8",
)

def require(
    condition,
    message,
):
    if not condition:
        raise SystemExit(
            f"FAIL — {message}"
        )

require(
    '<html lang="en-GB">'
    in EN,
    "English homepage lang",
)

require(
    '<link rel="canonical" href="https://sistema90g.it/en/">'
    in EN,
    "English self canonical",
)

for value in [
    'hreflang="it-IT"',
    'hreflang="en-GB"',
    'hreflang="x-default"',
]:
    require(
        value in EN,
        f"English homepage missing {value}",
    )

require(
    'property="og:locale" content="en_GB"'
    in EN,
    "English OG locale",
)

require(
    'property="og:locale:alternate" content="it_IT"'
    in EN,
    "English OG alternate locale",
)

require(
    'A kitchen can look perfect.'
    in EN,
    "English acquisition headline",
)

require(
    'Sistema 90G looks for problems, inconsistencies'
    in EN,
    "English problem-first promise",
)

for marker in [
    'A useful answer should show',
    'how certain it is.',
    'VERIFIED',
    'TO CHECK',
    'NOT DETERMINABLE',
    'data-evidence-state="verified"',
    'data-evidence-state="to-check"',
    'data-evidence-state="not-determinable"',
    'href="/en/method.html"',
]:
    require(
        marker in EN,
        f"English evidence differentiation missing: {marker}",
    )

require(
    EN.count('data-evidence-state=') == 3,
    "English homepage must expose exactly three evidence states",
)

require(
    'Free initial assessment'
    in EN,
    "English Free Entry promise",
)

require(
    'Independent'
    in EN
    or 'Independence'
    in EN,
    "independence positioning",
)

require(
    'Italian VAT No. IT02844900221'
    in EN,
    "English VAT identification",
)

for path in [
    '/en/how-it-works.html',
    '/en/services.html',
    '/en/real-kitchen-cases.html',
    '/en/kitchen-guides.html',
    '/en/about.html',
]:
    require(
        path in EN,
        f"English route missing: {path}",
    )

require(
    '/en/how-it-works.html#submit'
    in EN,
    "English Free Entry route",
)

require(
    'portale.sistema90g.it'
    not in EN,
    "homepage must enter Free Entry through English site path first",
)

require(
    'src="images/'
    not in EN,
    "English image paths must be root-relative",
)

require(
    'href="sistema90g-'
    not in EN,
    "English CSS paths must be root-relative",
)

require(
    'src="privacy-consent.js'
    not in EN,
    "Italian consent runtime must not load on English homepage",
)

require(
    'navigation-conversion.js'
    not in EN,
    "Italian navigation runtime must not load on English homepage",
)

require(
    '/s90g-site-en-gb-v1.js'
    in EN,
    "English safe runtime missing",
)

require(
    '/s90g-home-acquisition-v1.js'
    in EN,
    "shared homepage runtime missing",
)

for marker in [
    'Mostra il tuo caso',
    'Casi reali',
    'Come funziona',
    'Servizi e prezzi',
    'Chi sono',
    'Prima valutazione gratuita',
    'Cookie e misurazione',
    '>Accetta<',
    '>Rifiuta<',
    'Partita IVA',
    'Attiva Vista 90G',
]:
    require(
        marker not in EN,
        f"Italian visible marker remains: {marker}",
    )

for us_term in [
    'countertop',
    'cooktop',
    'wall cabinet',
]:
    require(
        us_term.lower()
        not in EN.lower(),
        f"US terminology found: {us_term}",
    )

require(
    'const isEnglish ='
    in HOME_JS,
    "shared Vista runtime missing language gate",
)

for runtime_copy in [
    '90G View active',
    'Activate 90G View',
    'Point to check',
]:
    require(
        runtime_copy
        in HOME_JS,
        f"English Vista runtime copy missing: {runtime_copy}",
    )

require(
    "'en-GB'"
    in EN_JS,
    "English shared runtime locale missing",
)

require(
    "location.pathname === '/en/'"
    in EN_JS,
    "English homepage path special-case missing",
)

require(
    "return 'home-en-gb';"
    in EN_JS,
    "English homepage source identifier missing",
)

require(
    "const sourcePage ="
    in HOME_JS,
    "homepage analytics locale source missing",
)

require(
    HOME_JS.count(
        "source_page: sourcePage,"
    ) == 4,
    "all four homepage analytics events must use locale-aware source",
)

require(
    "source_page: 'home',"
    not in HOME_JS,
    "legacy hard-coded homepage analytics source remains",
)

require(
    "'lang',"
    in EN_JS
    and "'en',"
    in EN_JS,
    "English portal language enforcement missing",
)

require(
    "'locale',"
    in EN_JS
    and "'en-GB',"
    in EN_JS,
    "English portal locale enforcement missing",
)

for value in [
    'hreflang="it-IT"',
    'hreflang="en-GB"',
    'hreflang="x-default"',
]:
    require(
        value in IT,
        f"Italian homepage missing {value}",
    )

require(
    'href="/en/"'
    in IT,
    "Italian homepage EN switch missing",
)

scripts = re.findall(
    r'<script\s+type="application/ld\+json">(.*?)</script>',
    EN,
    re.I | re.S,
)

require(
    len(scripts) == 1,
    "expected one English JSON-LD block",
)

data = json.loads(
    scripts[0],
)

graph = data.get(
    "@graph",
    [],
)

pages = [
    item
    for item in graph
    if item.get("@type")
    == "WebPage"
]

require(
    len(pages) == 1,
    "expected one English WebPage schema",
)

require(
    pages[0].get("url")
    == "https://sistema90g.it/en/",
    "English WebPage schema URL",
)

require(
    pages[0].get("inLanguage")
    == "en-GB",
    "English WebPage schema language",
)

print(
    "PASS — English homepage lang + canonical"
)

print(
    "PASS — paired hreflang + x-default"
)

print(
    "PASS — English UK visible content"
)

print(
    "PASS — English evidence differentiation"
)

print(
    "PASS — UK terminology guard"
)

print(
    "PASS — English internal customer journey"
)

print(
    "PASS — no direct homepage bypass to Portale"
)

print(
    "PASS — root-relative shared assets"
)

print(
    "PASS — Italian runtime excluded from English homepage"
)

print(
    "PASS — Vista 90G bilingual runtime"
)

print(
    "PASS — English safe consent/navigation runtime"
)

print(
    "PASS — English structured data"
)

print(
    "PASS — Italian homepage language switch"
)

print(
    "SITE I18N HOME V1: PASS"
)


# === INTERNATIONAL BRAND PLATFORM V1 — HOME ===
from pathlib import Path as _BrandPath

_brand_root = _BrandPath(__file__).resolve().parents[1]
_brand_home = (
    _brand_root / "en" / "index.html"
).read_text(encoding="utf-8")

for _marker in [
    "Italian method · independent checks · better kitchen decisions",
    "Independent Italian kitchen expertise focused on identifying problems",
]:
    if _marker not in _brand_home:
        raise SystemExit(
            f"FAIL — international Italian brand marker missing from EN home: {_marker}"
        )

if "Made in Italy" in _brand_home:
    raise SystemExit(
        "FAIL — generic Made in Italy claim must not be used on EN home"
    )

print("PASS — intentional Italian brand identity on English homepage")

# VQA-2D — release-critical EN-GB mobile navigation contract.
from pathlib import Path as _S90GNavPath
import re as _s90g_nav_re

_s90g_nav_root = (
    _S90GNavPath(__file__)
    .resolve()
    .parents[1]
)

_s90g_nav_runtime = (
    _s90g_nav_root
    / "s90g-site-en-gb-v1.js"
).read_text(
    encoding="utf-8"
)

_s90g_nav_css = (
    _s90g_nav_root
    / "sistema90g-visual-2026.css"
).read_text(
    encoding="utf-8"
)

if not _s90g_nav_re.search(
    r"""header\.classList\.add\(
\s*['"]s90g-nav-ready['"]\s*,?
\s*\)""",
    _s90g_nav_runtime,
):
    raise SystemExit(
        "FAIL — English runtime does not enter "
        "the managed mobile-navigation state"
    )

if (
    ".s90g-header.s90g-nav-ready "
    ".s90g-nav{display:none}"
    not in _s90g_nav_css
):
    raise SystemExit(
        "FAIL — canonical closed mobile-nav CSS missing"
    )

if (
    ".s90g-header.s90g-nav-ready.is-nav-open "
    ".s90g-nav{display:grid}"
    not in _s90g_nav_css
):
    raise SystemExit(
        "FAIL — canonical open mobile-nav CSS missing"
    )

print(
    "PASS — English mobile navigation is closed by default"
)

# VQA-2E-R2 — disclosure for synthetic Italian Home case imagery.
from pathlib import Path as _S90GDisclosurePath

_s90g_disclosure_root = (
    _S90GDisclosurePath(__file__)
    .resolve()
    .parents[1]
)

_s90g_disclosure_it = (
    _s90g_disclosure_root
    / "index.html"
).read_text(
    encoding="utf-8"
)

_s90g_disclosure_en = (
    _s90g_disclosure_root
    / "en/index.html"
).read_text(
    encoding="utf-8"
)

_s90g_disclosure_images = [
    "s90g-home-case-dishwasher-20260914.webp",
    "s90g-home-case-island-20260914.webp",
    "s90g-home-case-quote-20260914.webp",
]

_s90g_disclosure_label = (
    "Immagine illustrativa"
)

if (
    _s90g_disclosure_it.count(
        _s90g_disclosure_label
    )
    != 3
):
    raise SystemExit(
        "FAIL — Italian illustration disclosure count invalid"
    )

for _s90g_disclosure_image in _s90g_disclosure_images:
    if (
        _s90g_disclosure_it.count(
            _s90g_disclosure_image
        )
        != 1
    ):
        raise SystemExit(
            "FAIL — Italian synthetic image reference invalid"
        )

    if (
        _s90g_disclosure_image
        in _s90g_disclosure_en
    ):
        raise SystemExit(
            "FAIL — Italian synthetic image leaked into English Home"
        )

    _s90g_disclosure_pos = (
        _s90g_disclosure_it.index(
            _s90g_disclosure_image
        )
    )

    _s90g_disclosure_start = (
        _s90g_disclosure_it.rfind(
            '<article class="s90g-proof-case">',
            0,
            _s90g_disclosure_pos,
        )
    )

    _s90g_disclosure_end = (
        _s90g_disclosure_it.find(
            "</article>",
            _s90g_disclosure_pos,
        )
    )

    if (
        _s90g_disclosure_start < 0
        or _s90g_disclosure_end < 0
    ):
        raise SystemExit(
            "FAIL — Italian proof-case boundary missing"
        )

    _s90g_disclosure_card = (
        _s90g_disclosure_it[
            _s90g_disclosure_start:
            _s90g_disclosure_end
        ]
    )

    if (
        _s90g_disclosure_label
        not in _s90g_disclosure_card
    ):
        raise SystemExit(
            "FAIL — synthetic Home image not disclosed"
        )

print(
    "PASS — Italian synthetic home illustrations are explicitly labelled"
)

# VQA-2G — clean language-neutral EN-GB Home case imagery.
from pathlib import Path as _S90GEnCleanAssetPath

_s90g_en_clean_root = (
    _S90GEnCleanAssetPath(__file__)
    .resolve()
    .parents[1]
)

_s90g_en_clean_home = (
    _s90g_en_clean_root
    / "en/index.html"
).read_text(
    encoding="utf-8"
)

_s90g_en_clean_assets = [
    "s90g-home-case-dishwasher-en-gb-20260914.webp",
    "s90g-home-case-island-en-gb-20260914.webp",
    "s90g-home-case-quote-en-gb-20260914.webp",
]

_s90g_en_legacy_assets = [
    "/images/caso-lavastoviglie-passaggio-cucina.jpg?v=20260715b",
    "/images/caso-isola-passaggi-cucina.jpg?v=20260715b",
    "/images/22_CASI_PREVENTIVO.jpg?v=20260715a",
]

if _s90g_en_clean_home.count("Illustrative image") != 3:
    raise SystemExit(
        "FAIL — English Home illustrative disclosure count invalid"
    )

for _s90g_asset in _s90g_en_clean_assets:
    if _s90g_en_clean_home.count(_s90g_asset) != 1:
        raise SystemExit(
            f"FAIL — clean EN Home asset reference invalid: {_s90g_asset}"
        )

    _s90g_file = (
        _s90g_en_clean_root
        / "images"
        / _s90g_asset
    )

    if not _s90g_file.is_file() or _s90g_file.stat().st_size <= 0:
        raise SystemExit(
            f"FAIL — clean EN Home asset missing: {_s90g_asset}"
        )

    _s90g_pos = _s90g_en_clean_home.index(_s90g_asset)

    _s90g_start = _s90g_en_clean_home.rfind(
        '<article class="s90g-proof-case">',
        0,
        _s90g_pos,
    )

    _s90g_end = _s90g_en_clean_home.find(
        "</article>",
        _s90g_pos,
    )

    if _s90g_start < 0 or _s90g_end < 0:
        raise SystemExit(
            f"FAIL — EN proof-case boundary missing: {_s90g_asset}"
        )

    _s90g_card = _s90g_en_clean_home[
        _s90g_start:_s90g_end
    ]

    if "Illustrative image" not in _s90g_card:
        raise SystemExit(
            f"FAIL — EN clean asset is not disclosed: {_s90g_asset}"
        )

for _s90g_legacy in _s90g_en_legacy_assets:
    if _s90g_legacy in _s90g_en_clean_home:
        raise SystemExit(
            f"FAIL — legacy annotated image remains on EN Home: {_s90g_legacy}"
        )

print(
    "PASS — English Home uses clean language-neutral case illustrations"
)
