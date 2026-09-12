# SBE release lock — 0.4.61 portable snapshot ordering

## Decision

SBE `0.4.61` is technically qualified for API consumer review. Immutable
tagging and publication are not yet authorized.

## Immutable identity

- Commit: `477cfa2491f33377f1a873772c5e465c588f0741`
- Commit epoch: `1789243472`
- Canonical filename:
  `astrowoof_natal_authoring-0.4.61-py3-none-any.whl`
- Byte size: `1,383,877`
- SHA-256:
  `8dd151fced3fc7823ef914c7642798a977eca93d19b1136bf34da55b589ef723`

Tag only the exact commit above. This evidence document is intentionally a
later commit and must never become the release target.

## Qualification

- Focused matrix: 46 passed.
- Full manifest suite: 1,192 tests, 60 expected skips, zero failures.
- Two exact-lock builds: byte-identical; inventories identical, 310 members.
- Clean exact-wheel install and dependency check: passed.
- Installed release smoke and lifecycle smoke: passed.
- Public installed relocated reader against retained Bodoni: passed with exact
  expected assessment, valid authority/wrapper pair, and 387 unchanged files.
- Provider operations: zero.
- External storage reads: zero.
- Live QA mutations: zero.

## Remaining gate

API independently verifies the exact wheel/consumer contract and supplies its
release review. Owner authorization is then required before tag or publication.
