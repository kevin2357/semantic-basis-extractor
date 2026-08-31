# API review — Slice 4 and Oauf-paws 6

## Decision

**Approved to implement the narrow native correction in Slice 5.** The proposed
coordinator-owned quiescent `save_state()` boundary is the correct normal
lifecycle point. The closed internal retirement record and existing public v3
`exact_replay` outcome avoid an unnecessary API/public-contract change.

## Conditions carried into implementation

- The real reconciliation/adoption/reporting flow—not a synthetic state edit—
  must invoke the helper and produce a published checkpoint with the retired
  record and no live singleton intent.
- Keep the retirement validator all-or-none for the complete ordered inventory.
  A report-like action label alone is never enough; the exact result artifact,
  provider identity, reconciliation, consumption, and billing joins remain
  mandatory.
- Historical compatibility repair, if included, must remain a separately typed,
  zero-provider-I/O path requiring a new inspection and API decision afterward.
  It must not make Delerium recoverable as an incidental test outcome.
- Preserve the failure matrix: before persistence retains the live slot; after
  persistence/before snapshot fails closed; after publication exposes the
  record-and-slot-removal pair together.
- Verify replay lookup cannot turn the retired record into fresh authority.
  Exact predecessor replay returns only the existing result; a fresh successor
  still requires its own current inspection, request, grant, and writer-fenced
  live intent.

## API boundary

No API consumer change is required for this correction if the documented v3
`exact_replay` result remains structurally identical. Please flag immediately
if implementation proves that a newly observable public field/version is
unavoidable rather than silently widening the result.
