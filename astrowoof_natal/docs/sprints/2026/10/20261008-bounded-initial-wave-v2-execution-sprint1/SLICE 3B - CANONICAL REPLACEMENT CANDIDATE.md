# Slice 3B — Canonical replacement candidate

## Why this candidate replaces the first one

The first unpublished `0.4.72` candidate, source `0b814260`, exposed a broad
suite regression: bounded-v2 initial-wave validation was applied to the
existing exact-natal initial-wave lifecycle path. Commit `986e05ea` restores
the closed route-specific mapping:

- `exact_natal` requires `astrowoof.semantic_closure_run.v0.9`;
- `bounded_natal` requires `astrowoof.bounded_natal.authoring_run.v2`; and
- neither route can satisfy the other route's lifecycle projection.

The original candidate was never tagged, published, deployed, or activated.
It is therefore retired rather than released under a new public version.

## Frozen build coordinates

| Field | Value |
| --- | --- |
| Artifact-source commit | `986e05ea04fc31419d6c0e240ce05d7ba3baa980` |
| Recorded `SOURCE_DATE_EPOCH` | `1791479232` |
| Wheel filename | `astrowoof_natal_authoring-0.4.72-py3-none-any.whl` |
| SHA-256 | `298273523a05c7a72cdd5404ca1727ef3f03c5c922785a7c5ba4da6f2990c364` |
| Byte size | `1,442,607` |
| Wheel members | `330` |
| Retained wheel | `C:\tmp\sbe-0.4.72-regression-candidate\canonical-wheel-a\astrowoof_natal_authoring-0.4.72-py3-none-any.whl` |
| Duplicate build | sibling `canonical-wheel-b` artifact |

Two independent Git archives were created with `core.autocrlf=false` and
`core.eol=lf`, then built using `pip wheel --no-deps --no-build-isolation`.
Their filenames, member inventory, member bytes, sizes, and whole-wheel
SHA-256 values are identical. The 324 packaged text members contain zero CRLF
sequences.

## Installed-package boundary

The retained wheel was installed with the retained
`semantic-projection-core==0.11.1` wheel into an isolated local virtual
environment. Its package resolves from `site-packages` as `0.4.72`; the public
`astrowoof-external-authority-v2` command is present. After installing the
declared `jsonschema` and `tzdata` dependencies into that same disposable
environment, `pip check` reports no broken requirements.

## Qualification and next gate

The manifest-driven broad rerun from `986e05ea` passed with 1,267 tests, 62
expected skips, zero failures/errors, one worker, and 1,345.694 wall seconds.
The retained receipt is
`C:\tmp\sbe-0472-canonical-broad-suite-receipt.json`.

API may now replace—not supplement—its prior `dadd3969…99cb29b` pin with the
SHA above and run the existing joint installed-wheel fixture once. No real
provider, release, deployment, or activation is part of this slice.
