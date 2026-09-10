# SBE 0.4.59 Release-Lock Qualification

## Decision

SBE `0.4.59` is technically qualified at the pre-tag/release boundary, pending
the ordinary installed-wheel API consumer review and final publication approval.

## Immutable candidate coordinates

- release-lock/tag-target commit:
  `e5127caea466b12340472eee48b2563abfd68650`
- component tag, if later authorized:
  `astrowoof-natal-authoring-v0.4.59`
- `SOURCE_DATE_EPOCH`: `1789062636`
- wheel: `astrowoof_natal_authoring-0.4.59-py3-none-any.whl`
- size: `1,376,264` bytes
- SHA-256:
  `9211b7a7fd2e1a10a42cfe6bf47cafd749fa2076767b2dd7500621a93d9cbe92`
- wheel members: `307`

## Retained consumer artifact and toolchain

The exact first qualified wheel is retained for API consumer qualification at:

`C:\tmp\astrowoof_natal_authoring-0.4.59-e5127ca-qualified-py3-none-any.whl`

That handoff copy is 1,376,264 bytes and independently rehashes to the candidate
SHA-256 above. It is a renamed byte-for-byte copy of the first qualification
wheel, not a rebuild. Publication must use the canonical wheel filename stated
above.

The reproducibility pair was built with:

- Python `3.12.14`
- pip `26.2.1`
- setuptools `84.0.0`
- wheel `0.48.0`
- command frontend: `python -m pip wheel --no-deps --no-build-isolation`
- fixed `SOURCE_DATE_EPOCH=1789062636`

An independent build made with another toolchain may be semantically equivalent
but is not the qualified publication artifact unless its bytes match this digest.

Two independent clean `git archive` exports of the exact lock commit produced
identical filenames, sizes, member inventories, and wheel bytes. The wheel has
zero detected cache, bytecode, private-key, or test members.

## Qualification gates

- focused source qualification: 24 passed, 4 skipped
- supported broad/full coordinator: 1,167 passed, 60 skipped
- test inventory SHA-256:
  `c5c2fcbe8cd3e8a474d4422ce193382c6f3f7da5916c23c9e93e4b7b875bcd3e`
- clean exact-wheel `pip check`: pass
- installed import/version/site-packages boundary: pass (`0.4.59`)
- installed release smoke: pass, 193 resources
- installed adversarial qualification: pass, 32 invariants, 22 route cells,
  zero provider/network calls and zero spend
- Alloy impact: none; no model change or rerun required

## Tag fence

If later authorized, tag only
`e5127caea466b12340472eee48b2563abfd68650`. This qualification record is a
later evidence-only commit and must not become the tag target. Upload only the
exact wheel identified above; do not rebuild or substitute another artifact.

No tag, push, GitHub release, controlled live run, or publication occurred.
