# Sistema 90G — International Markets Roadmap V1

Status: canonical roadmap  
Date: 2026-09-13

## 1. Purpose

This document defines how Sistema 90G expands from the Italian market
to international markets without confusing language, locale, country
and commercial market.

The current international pilot remains the United Kingdom.

The United States is the next international market after the UK pilot
has completed its full release and end-to-end verification.

This roadmap does not activate the United States today.

## 1A. Brand identity invariant

Sistema 90G remains explicitly Italian as it expands internationally.

The `.it` domain, Italian origin and the concept of an `Italian method`
are deliberate brand signals rather than temporary limitations.

The international positioning is not generic Italian design, luxury or
style. Italian identity represents attention to function, detail,
everyday use, the relationship between decisions and their practical
consequences, and the principle of identifying problems before they
become costly mistakes.

The brand promise must remain subordinate to the customer's real
problem:

customer -> problem -> understanding -> useful next step -> service only
when useful.

Localisation remains mandatory. Italian identity does not justify using
the same terminology, legal rules, measurements, currency presentation
or commercial wording in every country.

---

## 2. Canonical principle

Language, locale, country and market are separate concepts.

They must never be treated as interchangeable.

Example:

- language: `en`
- locale: `en-GB`
- country: `GB`
- market: `GB`

is different from:

- language: `en`
- locale: `en-US`
- country: `US`
- market: `US`

Both customers use English, but terminology, units, commercial rules,
legal information, SEO and customer-facing outputs may differ.

---

## 3. Operator-language invariant

The customer works in their own language.

Gian Carlo works in Italian.

Sistema 90G manages translation, localisation and semantic control
between the two.

Canonical operator workflow:

1. customer source is preserved unchanged;
2. customer language, locale, country and market are recorded;
3. an Italian operational translation is produced;
4. analysis and approval are performed in Italian;
5. the approved Italian answer is localised into the customer locale;
6. the target-language answer is back-translated into Italian;
7. semantic coherence is checked;
8. only then may the customer-facing technical answer become sendable.

A translated technical answer must not be sent when the system cannot
demonstrate sufficient semantic coherence with the approved Italian
version.

Uncertainty must remain uncertainty.

Examples that must preserve their meaning:

- da verificare;
- incompatibile;
- potrebbe interferire;
- misura non confermata.

---

## 4. Market rollout sequence

### M0 — Italy

Active market.

- language: `it`
- locale: `it-IT`
- country: `IT`
- market: `IT`
- public URL family: Italian root URLs
- primary operator language: Italian

### M1 — United Kingdom

Current international pilot.

- language: `en`
- locale: `en-GB`
- country: `GB`
- market: `GB`
- public URL family: `/en/`
- units: metric
- terminology: UK English
- launch currency: EUR
- Italian operator workflow remains unchanged

UK examples:

- worktop
- hob
- wall unit
- tap
- extractor hood

The UK pilot must be completed before the United States is activated.

### M2 — United States

Next international market after successful UK release.

Planned contract:

- language: `en`
- locale: `en-US`
- country: `US`
- market: `US`
- planned public URL family: `/en-us/`
- terminology: US English
- customer-facing measurement presentation:
  US customary units where appropriate
- original customer measurements:
  preserved unchanged
- derived conversions:
  allowed only as clearly derived operator/customer aids
- commercial/legal localisation:
  US-specific review required
- currency:
  separate release decision required before public US launch

US examples:

- countertop
- cooktop / range
- wall cabinet
- faucet
- range hood
- toe-kick

The United States must not simply reuse `en-GB` pages unchanged.

`en-US` is a separate localisation.

---

## 5. Measurement integrity

Original measurements are source-of-truth data.

They must never be destructively converted.

For United States cases:

- the original value remains stored exactly as received;
- derived metric or US-customary equivalents may be displayed;
- every derived conversion must remain distinguishable from the source;
- drawings, plans and uploaded documents remain original;
- model numbers, product codes and manufacturer dimensions are never
  silently converted or rewritten.

A conversion must not create false precision.

---

## 6. Terminology localisation

English is not one commercial/technical locale.

A terminology layer must be locale-aware.

Examples:

| Concept | en-GB | en-US |
| --- | --- | --- |
| work surface | worktop | countertop |
| cooking appliance | hob | cooktop / range |
| upper cabinet | wall unit | wall cabinet |
| water fitting | tap | faucet |
| extraction | extractor hood | range hood |
| cabinet base detail | plinth | toe-kick |

Terminology localisation must not alter technical meaning.

---

## 7. Currency strategy

### UK pilot

Current launch contract:

- currency displayed: EUR;
- no GBP conversion in V1;
- prices must explicitly identify EUR.

### United States

No USD launch decision has been made yet.

Before US public release, Sistema 90G must choose one controlled model:

1. continue selling in EUR with explicit EUR disclosure; or
2. introduce a real USD commercial price list and payment contract.

Automatic visual conversion of EUR prices into USD is not sufficient
to establish a USD commercial offer.

Currency and payment authority must remain server-side.

---

## 8. Commercial and legal localisation

A market must not be launched merely because its language pages exist.

Before US release, review at minimum:

- customer terms;
- cancellation/refund information;
- consumer disclosures;
- privacy wording where market-specific treatment is required;
- tax/invoicing presentation;
- currency/payment presentation;
- service availability;
- delivery-time wording;
- limitation and scope wording;
- professional/technical disclaimers where applicable.

Legal/commercial material for the UK must not automatically be assumed
valid for the United States.

---

## 9. SEO contract

Locale pages receive hreflang only when the corresponding page actually
exists and is release-ready.

Current active pair:

- `it-IT`
- `en-GB`
- `x-default` -> Italian canonical page

Future US expansion:

- add `en-US` only after real `/en-us/` pages exist;
- never advertise an `en-US` alternate that returns a missing,
  incomplete or placeholder page;
- use self-canonical URLs for each locale;
- maintain reciprocal hreflang between real translated/localised pairs.

There must be no automatic language redirect.

---

## 10. Website URL architecture

Current:

- Italy: root URL family
- UK: `/en/`

Planned:

- US: `/en-us/`

The UK `/en/` family must not be repurposed as generic international
English.

It represents the `en-GB` localisation.

---

## 11. Portal contract

Current UK release contract remains:

- `requester_role=private`
- `service=valutazione-iniziale`
- `lang=en`
- `locale=en-GB`

The future US contract will require:

- `requester_role=private`
- `service=valutazione-iniziale`
- `lang=en`
- `locale=en-US`
- country `US`
- market `US`

where country and market must be resolved and persisted according to
the Portal's canonical data model.

The Portal must continue rejecting unsupported locale combinations
until that locale has been intentionally released.

Therefore `en-US` remains unsupported during the UK pilot.

---

## 12. Release gate before starting US implementation

US public implementation must not start until the UK pilot has passed:

1. complete controlled en-GB website launch set;
2. UK SEO completion;
3. UK commercial/legal completion;
4. website -> Portal en-GB journey complete;
5. Portal international changes integrated and deployed;
6. real-customer bilingual D9 end-to-end verification;
7. controlled website/Portal release;
8. production verification;
9. no unresolved critical internationalisation defect.

Only after these gates may `/en-us/` become an active implementation
scope.

---

## 13. Future candidate markets

After UK and US, candidate English-language markets are:

### Canada

Planned locale candidate:

- `en-CA`

Requires its own review of:

- terminology;
- currency;
- tax/commercial presentation;
- consumer/legal rules;
- possible French-language requirements depending on market strategy.

### Australia

Planned locale candidate:

- `en-AU`

Requires its own localisation and commercial/legal review.

### New Zealand

Planned locale candidate:

- `en-NZ`

Requires its own localisation and commercial/legal review.

No candidate market is considered active merely because it appears in
this roadmap.

---

## 14. Current implementation boundary

As of this roadmap:

ACTIVE:

- `it-IT`
- `en-GB`

PLANNED, NOT ACTIVE:

- `en-US`

FUTURE CANDIDATES:

- `en-CA`
- `en-AU`
- `en-NZ`

Do not yet:

- create `/en-us/`;
- add `en-US` hreflang;
- add US pages to sitemap;
- accept `locale=en-US` in production Portal;
- introduce USD prices;
- convert the UK site into generic English;
- widen the current UK release scope.

---

## 15. Strategic sequence

Canonical market expansion sequence:

Italy
-> United Kingdom pilot
-> UK end-to-end validation
-> United States
-> Canada / Australia / New Zealand as separately approved markets

The expansion principle is:

**validate one complete international market before multiplying markets.**
