#!/usr/bin/env python3

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]

build = (
    ROOT
    / "tools/build_cloudflare.sh"
).read_text(
    errors="replace"
)

editorial = (
    ROOT
    / "tools/test_public_editorial_copy_contract.py"
).read_text(
    errors="replace"
)

errors = []


legacy_build_calls = [
    "inject_public_wow_situation_selector.py",
    "inject_public_trust_bridge.py",
    "inject_public_free_entry_expectation.py",
    "test_public_wow_situation_selector_contract.py",
    "test_public_trust_bridge_contract.py",
    "test_public_free_entry_expectation_contract.py",
]

for filename in legacy_build_calls:

    if filename in build:

        errors.append(
            f"legacy build dependency remains: {filename}"
        )


modern_contracts = [
    "verify_home_acquisition_v1.py",
    "verify_free_entry_acquisition_v1.py",
    "verify_cases_acquisition_v1.py",
    "verify_services_acquisition_v1.py",
    "verify_global_public_alignment_v1.py",
]

for filename in modern_contracts:

    if build.count(filename) != 1:

        errors.append(
            f"modern build contract count != 1: {filename}"
        )


legacy_editorial_markers = [
    'data-s90g-wow-situation-selector="true"',
    "A che punto sei con la tua cucina?",
    "Consulenza 90G · 79 €",
    "'quale lavoro è utile e quanto costa',",
    "'prima di iniziare sai che cosa verrà fatto e quanto costa',",
    "Home instradata dalle 6 situazioni",
]

for marker in legacy_editorial_markers:

    if marker in editorial:

        errors.append(
            f"legacy Home assertion remains in editorial contract: "
            f"{marker}"
        )


if errors:

    print(
        "CURRENT PUBLIC BUILD ARCHITECTURE V1: FAIL"
    )

    for error in errors:
        print(
            "FAIL —",
            error,
        )

    sys.exit(1)


print(
    "PASS — build no longer invokes legacy Home injectors"
)

print(
    "PASS — build no longer runs obsolete WOW/trust/Free Entry contracts"
)

print(
    "PASS — current acquisition contracts guard canonical source"
)

print(
    "PASS — editorial contract no longer owns legacy Home architecture"
)

print(
    "CURRENT PUBLIC BUILD ARCHITECTURE V1: PASS"
)
