# SBE release-lock candidate — 0.4.62 runtime-capture diagnostics

## Decision

The release-lock source is ready to commit. Tagging and publication are not
authorized. The commit containing this record is the intended immutable release
target only after its exact-source rebuild and installed qualification pass.

## Frozen coordinates

- Version: `0.4.62`
- Recorded build epoch: `1789468315`
- Canonical filename:
  `astrowoof_natal_authoring-0.4.62-py3-none-any.whl`
- Expected package bytes from artifact-source qualification: 1,385,622
- Expected SHA-256 from artifact-source qualification:
  `eea9d74ec0ab39cc804ceedb4b00ce8af8cb17ce99c89d6b6276372ba00ab1bb`

The fixed epoch intentionally remains the artifact-source epoch. Sprint review
documents are outside package data, so the exact release-lock rebuild must
reproduce these bytes. Any difference blocks release and requires investigation.

## Accepted evidence

- API approved Gate B and preparation of a fresh-version candidate.
- Focused matrix: 43 passed.
- Full maintained suite: 1,196 tests, three expected skips, zero failures.
- Two artifact-source builds: byte-identical, 310 members.
- Clean installed dependency, release-smoke, lifecycle-smoke, editorial parity,
  and real API `force=False` coexistence gates: passed.
- Provider/network/storage operations, spend, and authoritative mutation: zero.

## Required exact-lock gate

After committing this record:

1. identify the exact commit and verify only documentation changed after the
   artifact-source commit;
2. export and build that commit twice at epoch `1789468315`;
3. require exact expected filename, size, SHA-256, and member inventory;
4. install the exact build outside the checkout and rerun dependency checking,
   public release/lifecycle smokes, installed editorial parity, and API-host
   coexistence; and
5. return the exact commit and wheel coordinates for API final pre-tag review.

Do not tag, publish, deploy, or run a live witness without later explicit owner
authorization.
