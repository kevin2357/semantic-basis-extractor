# API Consumer Handoff — SBE 0.4.19

The supported public surfaces are:

- `astrowoof-operator-retirement build-request`
- `astrowoof-operator-retirement dry-run`
- `astrowoof-operator-retirement execute`
- `astrowoof-operator-retirement-qa --require-installed`

The API must establish an operator-retirement-pending custody fence before invoking
SBE. It must validate the exact dry-run/request evidence, invoke execute without a
long database transaction, ingest the sealed result transactionally, and release
API-owned resources only for a fully validated `applied`, `exact_replay`, or
compatible `already_retired` result.

The terminal pair is explicitly `POLICY_STOPPED / operator_retired`. Successful
evidence binds the native run, exact-Natal route, logical workspace root, request
digest, pre/post revisions and snapshots, complete action-closure digest, native
result/receipt identities, and freshly derived false provider/local-continuation
assertions.

Refusal never authorizes API resource release. Providerless actions must first be
resolved through the existing providerless-denial contract. SBE does not assert API
lease, capacity, reservation, account, entitlement, or publication state.

The detailed contract and examples are in the sprint handoff:
`docs/sprints/2026/08/20260824-operator-stuck-run-native-retirement-patch-sprint1/OPERATOR RETIREMENT API CONSUMER HANDOFF.md`.
