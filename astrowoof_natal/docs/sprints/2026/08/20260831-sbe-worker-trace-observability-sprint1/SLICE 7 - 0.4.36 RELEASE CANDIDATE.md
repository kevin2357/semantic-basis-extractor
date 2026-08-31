# Slice 7 — SBE 0.4.36 release candidate

## Scope

This candidate adds bounded `✨🐶` native state/decision/exit observability and
its provider-free installed qualification. It also contains the narrow
`0.4.35` generic-save correction discovered by the release matrix.

No lifecycle, authority, result, receipt, custody, or scheduling contract is
widened. Trace output remains non-authoritative and privacy bounded.

## Candidate identity

- Version: `0.4.36`
- Reproducible wheel SHA-256:
  `85b94911d82b1dd960c19f72e78ebc4cd6828378dddc8de1bacef3c4aee35841`
- Installed trace receipt SHA-256:
  `82e8aa59c681a7064164569824cefee04fb3ee7473c064b46f1fe3abd81cc7c2`
- Receipt qualification SHA-256:
  `5625a9c2ea879ee4305dab90553873fc2dfd4b6dfbd44dbf9d643e437fc9cc2a`

## Verification

- 58-test bounded/Glimmer/observability matrix passed; one optional schema skip.
- 94 focused modified-boundary tests passed; two optional schema skips.
- Generic installed release smoke passed.
- Installed exact and bounded trace qualification passed.
- Packaged command and schema resource verified.
- Deterministic controlled wheel rebuild passed.
- `git diff --check` and Python compilation passed.
- External provider calls, spend, network, R2, and retained-QA access: zero.

The full repository suite was not rerun. The gate is deliberately focused and
installed-boundary oriented; the 0.4.35 defect was itself found and covered by
the expanded bounded matrix.
