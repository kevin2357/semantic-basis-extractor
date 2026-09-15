# SBE pre-tag review — 0.4.63 Python 3.11 resource compatibility

## Decision

SBE 0.4.63 is technically qualified for API consumer and final owner review.
No tag, publication, deployment, or live witness has occurred or is authorized
by this record.

## Immutable release coordinates

- Release target commit:
  `ceb0dc5a28b81cff91a4a985edb4cf6ff3217e24`
- Required annotated tag: `astrowoof-natal-authoring-v0.4.63`
- Canonical filename:
  `astrowoof_natal_authoring-0.4.63-py3-none-any.whl`
- Byte size: `1,385,639`
- SHA-256:
  `fe0fba0c0be87ec25257a9b9c8c5f6e0166f9544df99fc8f940b20109ea1e355`
- Recorded build epoch: `1789481170`
- Retained qualified wheel:
  `C:\dev\github\semantic-basis-extractor\.release-work\0.4.63\lock-final-a\dist\astrowoof_natal_authoring-0.4.63-py3-none-any.whl`

Tag only `ceb0dc5a...`, never the later documentation commit that records these
completed exact-lock checks.

## Qualification summary

- Focused release-bound editorial matrix: 45 tests on Python 3.11.15 and 45 on
  Python 3.12.14; one optional skip on each; zero failures.
- Complete maintained suite: 1,200 tests, 60 expected skips, zero failures;
  inventory SHA-256
  `3831ed792e633b43128e611e93738d8da0af9a0ed4b22f192faa853828ce9b9e`.
- Artifact-source and exact-lock build pairs are byte-identical across all four
  qualified builds at the coordinates above.
- Exact-lock inventory: 310 members, 102 contracts, 67 fixtures, all required
  editorial resources present, zero forbidden test/cache/bytecode/private
  members.
- Exact-lock clean installed qualification passed on Python 3.11.15 and
  3.12.14: exact version/site-packages origin, `pip check`, release smoke,
  lifecycle smoke, editorial QA, and 15 installed public capture/diagnostic
  tests on each runtime.
- Editorial accepted-delivery and closeout fixture digests are unchanged.
- Missing/malformed resources retain their failure behavior.
- Provider operations, spend, runtime storage/network/API operations, and
  authoritative workspace mutation: zero.
- Alloy impact: none.

## Build-note disposition

One diagnostic exact-lock pair used the wrong newer epoch and was rejected even
though internally reproducible. The final lock pair retained the frozen
artifact-source epoch and reproduced the previously qualified wheel exactly.
Only the wheel at the immutable coordinates above is publishable.

## Remaining gate

API should install this exact retained wheel, verify its SHA-256 first, and run
the applicable provider-free consumer/host gate. Final review must bind approval
to the exact commit, filename, size, and SHA above.

Explicit owner authorization is still required before creating or pushing the
annotated tag or publishing GitHub release assets.

