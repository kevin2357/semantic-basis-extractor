# Slice 4 Terminal Result and Publication Receipt

Date: 2026-08-17
Status: complete; awaiting Kevin review

## Outcome

Supported ordinary authoring and provider-reconciliation commands now seal native
meaning before normal return or spend-control exit conversion. A consumer can
classify delivery, review, failure, pending custody, continuation, authorization,
budget, policy, or ambiguity from validated native evidence rather than stderr or
the process exit code.

## Publication protocol

One native single-writer boundary performs:

1. append invocation finalization and native-transition records;
2. bind all new records since the prior published result as one bounded journal
   range, regardless of action-derived record invocation IDs;
3. publish a content-addressed immutable execution result;
4. publish the complete workspace snapshot inventorying state, journal, result,
   index, and other authoritative members; and
5. publish a content-addressed immutable receipt sealing that exact result/snapshot
   pair.

The receipt is intentionally outside snapshot inventory because embedding either
side's hash in the other would recreate the accepted content-hash cycle. Only the
single `native-publication-receipts/` namespace is excluded.

## Receipt and retained evidence

`astrowoof.native_publication_receipt.v0.1` binds:

- result ID and SHA-256;
- complete snapshot SHA-256;
- checkpoint-basis SHA-256;
- journal-range SHA-256;
- run and invocation IDs; and
- stable logical workspace root.

The same narrow namespace retains the exact published snapshot manifest and
checkpoint-basis document. This permits validation of a specified historical result
after a later valid command updates the live snapshot. The API must retain this
namespace with the rest of its durable R2 capture.

## Failure recovery

An interruption after the result is durable but before snapshot or receipt
publication leaves one recognizable orphan. A later finalization validates its
journal range and checkpoint basis, republishes the complete snapshot, and seals
that exact result. It does not mint a replacement result or provider operation.

Missing, changed, multiply incomplete, or inconsistent evidence fails closed.
Providerless-denial recovery was extended only for a valid hash-linked journal
projection naming every exact persisted denied action ID.

Both normal publication and orphan repair validate the newly written complete
snapshot against actual workspace bytes before hashing or sealing it. A manifest
write alone is never sufficient receipt evidence.

## Route and outcome coverage

- Exact and bounded ordinary authoring.
- Exact interactive and Batch reconciliation.
- Bounded interactive reconciliation.
- Delivery, review, provider failure, provider pending, continuation, awaiting
  authority, budget exhaustion, policy stop, and ambiguous submission.
- External spend denial and native per-run exhaustion retain distinct causes.
- Reconciliation `not_due` remains strictly nonmutating.

## Verification

- Focused terminal/receipt tests: 19 passed in 3.098 seconds.
- Broad compatibility and failure-recovery gate: 197 passed in 204.543 seconds.
- Covered receipt absence/tampering, historical result validation, orphan repair,
  invalid post-manifest workspace mutation, exact denial cause,
  providerless-denial crash cuts, and all supported routes.
- Live provider operations: 0.
- Paid spend: `$0`.

## Deferred to Slice 5

The neutral CLI export surface, complete consumer fixture matrix, installed-wheel
round trips, and API handoff documentation remain Slice 5 work.
