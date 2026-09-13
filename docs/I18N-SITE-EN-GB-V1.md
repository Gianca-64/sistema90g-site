# Sistema 90G — International Website en-GB V1

## Status

Architecture contract for the UK pilot.

This document does not publish the English website.
It defines the rules that every later international website unit must respect.

## Canonical architecture

Italian remains the existing canonical website at the root of:

`https://sistema90g.it/`

English UK lives under:

`https://sistema90g.it/en/`

The existing Italian URLs are not renamed or moved.

No browser-language automatic redirect is permitted.

The visitor may change language explicitly.

## Languages and markets

V1 supports:

- language `it`, locale `it-IT`
- language `en`, locale `en-GB`

Language and country remain separate concepts.

The first international market is the United Kingdom.

English UK is not a generic English implementation and must use UK terminology.

Examples:

- worktop, not countertop
- hob, not cooktop
- wall unit, not wall cabinet
- measurements remain metric

## Currency

V1 remains EUR.

English pages must make the EUR currency explicit where a paid service is shown.

No GBP conversion is introduced in this release.

## Translation rule

Static website copy is controlled editorial content.

It must be deliberately localised into English UK.

Runtime machine translation is not used for published website copy.

The Italian canonical source remains the editorial reference.

## Public scope

Only canonical current B2C pages may receive English equivalents.

Legacy pages, B2B pages and HTML outside the current public architecture are not translated merely because they exist in the repository.

The canonical page mapping is stored in:

`tools/site-i18n-en-gb-manifest.json`

Long-tail Italian guides may remain Italian-only until a controlled English counterpart is produced.

An untranslated Italian page must not advertise a false English alternate.

## URLs

English pages use human-readable English slugs.

Examples:

`/analisi-preventiva.html`
pairs with
`/en/how-it-works.html`

`/verifica-90g.html`
pairs with
`/en/kitchen-review.html`

The mapping must never be inferred from filenames at runtime.

The manifest is authoritative.

## SEO

Each translated Italian/English pair must have:

- a self-referencing canonical
- `hreflang="it-IT"`
- `hreflang="en-GB"`
- `hreflang="x-default"` pointing to the Italian default page
- correct `<html lang>`
- correctly localised title and meta description
- correctly localised Open Graph metadata
- structured data using the correct language where applicable

The English URLs must be included in a controlled sitemap before release.

## Assets

Because English pages live one directory deeper, reusable site assets must use root-relative URLs.

Examples:

`/images/...`

`/sistema90g-visual-2026.css`

English internal navigation must point to `/en/...`.

Italian navigation must continue to point to the current root URLs.

## Language switcher

Every translated pair must expose an explicit language choice.

Italian page:

`EN` -> paired English URL

English page:

`IT` -> paired Italian URL

The switch must not discard the visitor's location in the customer journey when an equivalent translated page exists.

## Free Entry and Portale

The English website must enter Free Entry through the English website path first.

The final Portale link for an English UK visitor must preserve:

`requester_role=private`

`service=valutazione-iniziale`

`lang=en`

`locale=en-GB`

Italian Free Entry remains unchanged.

No B2B role is reintroduced.

## Services

The English website exposes the same current six B2C service families as the Italian website.

The service meaning, scope, price and exclusions must remain semantically equivalent.

Names may be localised for clarity but must not change the commercial contract.

## Customer-first communication

English copy must preserve the current Sistema 90G communication model:

customer -> problem -> discovery -> solution -> service only when useful.

The website must not become a traditional catalogue-led consultancy site.

The positioning remains independent kitchen expertise focused on finding problems, inconsistencies and risky decisions before they become costly or difficult to correct.

Italian origin may support trust but is not the main promise.

## Legal release gate

Privacy and cookie information require English versions.

The audit did not identify a complete dedicated international consumer commercial-terms and cancellation/right-to-cancel page.

Those requirements are release blockers and must be verified before the UK site is opened publicly.

Legal copy must not be fabricated by automatic translation.

## Release rule

No English page is published merely because its translation exists.

The UK release requires all of the following:

- core English customer journey complete
- Free Entry connected to en-GB Portale
- service pages complete
- legal release blockers resolved
- hreflang and canonical checks green
- sitemap checks green
- desktop browser checks green
- mobile browser checks green
- Italian regression checks green
- bilingual end-to-end customer journey green

Only after these gates may push and deploy be considered.
