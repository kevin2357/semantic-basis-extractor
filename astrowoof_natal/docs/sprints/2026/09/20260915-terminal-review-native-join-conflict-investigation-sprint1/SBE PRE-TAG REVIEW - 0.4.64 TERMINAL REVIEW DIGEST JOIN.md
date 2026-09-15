# SBE Pre-Tag Review — 0.4.64 Terminal Review Digest Join

## Decision

SBE `0.4.64` is technically qualified for API consumer and final owner review.
No tag, publication, deployment, or live witness has occurred or is authorized
by this record.

## Immutable coordinates

- Release target commit:
  `e5ad4cdf3ea3d3fa23d7cc2ab0ad55b0ef15f0ef`
- Required annotated tag: `astrowoof-natal-authoring-v0.4.64`
- Canonical wheel: `astrowoof_natal_authoring-0.4.64-py3-none-any.whl`
- Size: `1,385,707` bytes
- SHA-256:
  `b2f50fb57497c2bdbcadb548b0895fe0b772cba87346189d1daeadac1028984a`
- Normative build epoch: `1789492879`
- Retained qualified wheel:
  `C:\dev\github\semantic-basis-extractor\.release-work\0.4.64\lock-a\dist\astrowoof_natal_authoring-0.4.64-py3-none-any.whl`

Tag only the immutable target above, never the later documentation commit that
records these completed exact-lock checks.

## Qualification summary

- Python 3.11.15 focused source matrix: 66 tests, 5 expected skips, zero
  failures.
- Complete Python 3.12.14 manifest suite: 1,202 tests, 60 expected skips, zero
  failures; inventory SHA-256
  `2b7ef2cce804a16a13fb51b0d5729f06674a468739cfc460993d0473b577436a`.
- Two exact-lock builds have identical filename, size, 310-member inventory,
  and bytes.
- Inventory contains 102 contract and 67 fixture resources, all required
  editorial resources, and zero forbidden test/cache/bytecode members.
- Exact lock-A clean installed gates passed on Python 3.11.15 and 3.12.14:
  exact version/site-packages origin, `pip check`, release smoke, lifecycle
  smoke, editorial-review QA, and 17 installed public runtime/diagnostic tests.
- Accepted-delivery and editorial-closeout fixture digests remained stable.
- Provider operations, spend, runtime storage/API/deployment operations, and
  authoritative workspace mutation: zero.
- Alloy impact: none.

## Remaining gate

API should verify the exact retained wheel SHA before installing it and run the
applicable provider-free consumer/host gate. Approval must bind the exact
commit, filename, size, and SHA above. Explicit owner authorization remains
required before tag creation, push, or GitHub release publication.
