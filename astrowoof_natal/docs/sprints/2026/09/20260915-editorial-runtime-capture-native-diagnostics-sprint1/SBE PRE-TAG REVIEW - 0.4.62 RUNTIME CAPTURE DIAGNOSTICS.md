# SBE pre-tag review — 0.4.62 runtime-capture diagnostics

## Decision

SBE `0.4.62` is technically qualified for final API/owner review. No tag,
publication, deployment, or live witness has occurred or is authorized by this
record.

## Immutable release coordinates

- Release target commit:
  `e79a67104fb7704c7f9fdc25724c8062ad0042b6`
- Required annotated tag: `astrowoof-natal-authoring-v0.4.62`
- Canonical filename:
  `astrowoof_natal_authoring-0.4.62-py3-none-any.whl`
- Byte size: `1,385,622`
- SHA-256:
  `eea9d74ec0ab39cc804ceedb4b00ce8af8cb17ce99c89d6b6276372ba00ab1bb`
- Recorded build epoch: `1789468315`
- Retained qualified wheel:
  `C:\dev\github\semantic-basis-extractor\.release-work\0.4.62\lock-build-a\astrowoof_natal_authoring-0.4.62-py3-none-any.whl`

Tag only `e79a671...`. This evidence is intentionally committed afterward and
must not become or move the immutable release target.

## Qualification summary

- Focused release-bound matrix: 43 passed.
- Full maintained suite: 1,196 tests, three expected skips, zero failures;
  inventory SHA-256
  `d85f093e8ebc4e98bbc4508eec4b9f2b5d5e3424b0e468a6c73d47df13110aab`.
- Two pre-lock and two exact-lock builds were byte-identical within each pair;
  exact-lock bytes also matched the pre-lock expected identity.
- Exact-lock inventory: 310 members, all required members present, zero
  forbidden test/cache/bytecode members.
- Exact-lock clean installed dependency check: passed in the API host
  environment.
- Exact-lock installed release smoke: passed.
- Exact-lock installed lifecycle smoke: passed.
- Exact-lock installed editorial runtime/diagnostics matrix: 15 passed.
- Exact-lock real API `force=False` coexistence: passed; existing API handler
  preserved, one SBE handler, valid API and SBE records, distinct failure phases.
- Provider operations, network access, R2/Better Stack access, spend,
  authoritative workspace mutation, deployment, and live QA: zero.
- Alloy impact: none; diagnostics are non-authoritative observations.

## Publication fence

Final review must independently bind the consumer gate to the exact commit,
filename, size, and SHA-256 above. After explicit tag/publication authorization,
publish only these exact retained wheel bytes under the canonical filename and
the matching `SHA256SUMS.txt`; then independently download and verify both.
