# Slices 1–2 — Namespace resource compatibility corrections

## Outcome

All four approved Python 3.11-incompatible namespace-package resource readers
now use component-by-component traversal. The six real-runtime-compatible
regular-package calls remain unchanged.

This sprint is ready to hand its source commit back to the predecessor. It does
not build a wheel or run the broad release suite.

## Corrections

- `editorial_review_fixtures.py:628`: chain `fixtures`,
  `editorial_review`, and the closed fixture name.
- `external_authority_v2.py:276`: chain `external-authority-v2` and the
  fixed fixture name.
- `provider_economics.py:570`: chain `provider-economics` and the validated
  closed fixture name.
- `provider_economics.py:578`: chain `provider-economics` and the fixed
  mutation-corpus name.

No fallback lookup, path normalization, exception translation, schema change,
or resource-content change was introduced.

## Regression coverage

Existing manifested modules were extended; no new product test module was
created and `test_suite_manifest.json` required no change:

- `test_editorial_review_contract_fixtures.py`;
- `test_external_authority_v2_contract.py`; and
- `test_provider_economics_contract.py`.

Coverage proves:

- both real editorial v5 fixture resources match their exact recorded bytes and
  parsed values;
- the real external-authority v2 fixture matches exact bytes and parsed value;
- all real provider-economics fixtures and the mutation corpus match their
  parsed values, with the corpus digest pinned;
- unknown/unsafe named-fixture input remains refused;
- missing resources remain `FileNotFoundError`; and
- malformed JSON remains a `ValueError` family failure.

## Two-runtime focused qualification

The same three-module command ran against source on both official runtimes:

- Python 3.11.15: 29 tests, 2 optional skips, success;
- Python 3.12.14: 29 tests, 2 optional skips, success.

The final AST inventory reports:

- six remaining variadic-looking calls;
- all six are the previously proven Python 3.11-compatible regular-package
  controls; and
- zero known unsupported namespace-package paths.

Per owner ruling, broad/full-suite and wheel qualification belong to the
predecessor release-driving sprint and were not duplicated here.

## Handoff

Commit this source-only correction and return its exact identity to
`../20260915-python311-editorial-contract-resource-compatibility-sprint1/`.
That sprint exclusively owns the combined candidate wheel, installed-wheel/API
host gates, release lock, and publication decision.

