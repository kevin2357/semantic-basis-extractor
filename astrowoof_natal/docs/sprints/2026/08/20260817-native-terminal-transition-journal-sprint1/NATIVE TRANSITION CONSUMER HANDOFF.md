# Native Transition Consumer Handoff

Date: 2026-08-17
Contract status: Slice 5 API-approved

## Supported ingestion boundary

The authoritative Python operation is:

```python
from astrowoof_natal_authoring import read_native_transition_result

view = read_native_transition_result(run_dir, result_id)
```

The return type is `NativeTransitionResultView` with exactly `result`,
`journal_range`, and `receipt`. The reader validates the current restored workspace,
the requested immutable result, its bounded journal range, its retained historical
snapshot and checkpoint basis, and its publication receipt before returning.

The equivalent provider-free CLI is:

```text
astrowoof-native-transition --run-dir /stable/logical/run --result-id nres_...
```

`--latest` exists only as a derived operator convenience. API persistence and replay
must use an explicit result ID obtained from the command handoff. The mutable result
index is not ingestion authority.

When `--output` is used, the resolved output path must be outside the resolved
`--run-dir`. The CLI rejects the run root and every descendant path before reading
or writing. Stdout and direct Python return remain the preferred API-worker paths.

Neither surface accepts a provider, authorization, request body, or retrieval
adapter. Validation/export cannot submit, poll, authorize, deny, reconcile, or
otherwise mutate native state.

## Atomic API ingestion

Within one PostgreSQL transaction, the API should:

1. reject unknown schema versions and extra fields;
2. validate and retain the exact canonical result, bounded journal range, and
   receipt returned by SBE;
3. bind its receipt to `(run_id, result_id, journal_range.range_sha256)` and the
   complete canonical result/receipt hashes;
4. upsert provider-operation rows from action ID plus exact native route/mechanism
   evidence, never from the product job's requested route alone;
5. apply terminal-first job/reading state only after all native evidence is stored;
6. commit provider custody, reservation retention/release, capacity, and public
   status changes in that same API transaction; and
7. capture the complete workspace, including the snapshot-excluded
   `native-publication-receipts/` namespace, in durable R2 storage before deleting
   worker scratch.

If any validation or database operation fails, the API should commit none of the
state transition and retain the complete native workspace for replay/review.

## Idempotency and cursor rules

- Exact ingestion replay key: `(run_id, result_id, journal_range.range_sha256)`.
- Also compare full canonical `result_sha256` and `receipt_sha256`; a matching key
  with different bytes is an integrity conflict, not replay.
- Journal `sequence` is monotonic per native run. Store the accepted end sequence as
  a cursor only after the transaction commits.
- A new result range must start after the last accepted end sequence. Exact replay
  of an already accepted range is allowed. Overlap, gap, or changed prior bytes is
  review-required unless a future versioned recovery contract explicitly permits it.
- Command correlation is the result's bounded journal range. Action-derived records
  may use stable action-derived invocation IDs for crash reconstruction.

## Outcome mapping

| Native outcome | API interpretation |
|---|---|
| `delivery_complete` | Eligible for API delivery/publication policy checks |
| `review_required` | Terminal or retained review according to product policy; never publish automatically |
| `terminal_failure` | Terminal non-delivery; retain financial authority if cost disposition remains unsettled |
| `provider_pending` | Release local capacity, retain provider custody and required consumer authority |
| `continuation_required` | Schedule local continuation; do not infer provider work |
| `awaiting_external_authority` | API reservation/authorization decision required |
| `budget_exhausted` | Terminal non-delivery with cause distinguishing native ceiling from external authority |
| `policy_stopped` | Terminal non-delivery product/cancellation stop |
| `ambiguous_submission` | Fail closed, retain authority, require reconciliation/review |
| `native_evidence_invalid` | Retain workspace and require integrity review |

Optional-stage skipping remains generation-profile policy and must not be mapped to
a required-action terminal failure.

## Provider and cost ownership

SBE records native action binding, provider identity/status, and the closed cost
disposition. `provider_usage_unavailable_billing_reconciliation_pending` is not
zero. A provider-terminal operation may release retrieval custody while the API
continues to retain financial authority for later billing reconciliation.

The API remains authoritative for transactional cross-run reservations, account
quotas, global circuit breakers, entitlements, capacity allocation, billing
reconciliation, and publication policy. SBE journal/events do not claim those
authorities.

## Compatibility and refusal

The new result/journal/receipt reader supports only the published v0.1 native
contracts. Older SBE workspaces lacking those artifacts are not silently upgraded
or inferred. They remain on their previously supported lifecycle/closeout boundary
or require an explicitly qualified migration.

Refuse ingestion for unsupported schema, malformed content identity, changed
receipt/result/range binding, absent retained evidence, invalid current snapshot,
logical-path relocation, unknown route/mechanism, or conflicting provider identity.
Deterministic local keys are not evidence of provider idempotency.

## Packaged fixtures

`resources/fixtures/native_transition/consumer-ingestion-cases.v0.1.json` contains
the frozen consumer matrix:

- exact Response delivery and review;
- exact Batch provider failure;
- exact Response pending custody;
- bounded Response ambiguity;
- malformed-result refusal;
- exact replay; and
- conflicting second-operation refusal/review.

Each accepted case has canonical record, result, range, and receipt identities. The
malformed case intentionally changes the result hash and must be rejected. Fixtures
are token-free and contain no provider credentials or protected subject data.

## Events and redaction

`native.result_published` is a non-authoritative operational event containing only
result ID, receipt ID, and outcome. Events may be dropped and cannot replace the
reader output or API transaction. Journal/result/receipt artifacts contain hashes,
bounded native classifications, provider IDs where already durable, and redacted
operational references; provider-visible subject material remains governed by the
separate disclosure contract.

## Recovery limitations

- SBE can repair one exact incomplete result seal when result and journal/basis
  evidence remain valid.
- Identity-less interrupted provider submission remains ambiguous and fail-closed.
- A conflicting second provider operation is never silently superseded.
- SBE cannot provide literal atomicity across a provider request and local durable
  state when the provider offers no matching transactional/idempotency guarantee.
- The stable logical absolute workspace path remains required.
