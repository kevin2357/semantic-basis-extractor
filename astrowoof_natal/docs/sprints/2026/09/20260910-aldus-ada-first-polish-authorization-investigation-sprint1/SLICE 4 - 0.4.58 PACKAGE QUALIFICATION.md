# Slice 4 — 0.4.58 Package Qualification

## Source candidate

- source commit: `6a66c7a5d2c162ea5c17cf0a7a5dcad79cefdec1`
- version: `0.4.58`
- provisional `SOURCE_DATE_EPOCH`: `1789054339`

The source commit contains only the approved lifecycle correction, exact-one
regression and manifest classification, version freeze, and sprint evidence.

## Reproducible candidate

Two independent clean `git archive` exports of the source commit produced
byte-identical wheels:

- filename: `astrowoof_natal_authoring-0.4.58-py3-none-any.whl`
- size: `1,376,041` bytes
- SHA-256:
  `d509b1747c1fac5bd27dfec257d06be4cf933b79190391edc1df770405cb8d21`
- member count: `307`
- member inventories equal: yes
- forbidden cache/build/private/test members: `0`

These are provisional source-candidate coordinates. The exact release-lock
commit must be rebuilt twice using its own commit timestamp before final review.

## Clean installed qualification

The exact first wheel was installed into a new isolated environment alongside
SPC `0.11.1`, tzdata `2026.3`, and jsonschema `4.26.0`. All imports resolved
from that environment's `site-packages` and the installed version was
`0.4.58`.

- `pip check`: clean
- `astrowoof-release-smoke --require-installed`: pass, 193 resources
- installed adversarial qualification: pass, 32 invariants, 22 route cells,
  zero network/provider calls and zero spend
- installed polish-authority handoff qualification: pass
- installed failed-QA feature probe: exact request selected, exact action
  retained, and duplicate matching attempt remained closed

No controlled live run, tag, push, publication, or retained-workspace access
occurred.
