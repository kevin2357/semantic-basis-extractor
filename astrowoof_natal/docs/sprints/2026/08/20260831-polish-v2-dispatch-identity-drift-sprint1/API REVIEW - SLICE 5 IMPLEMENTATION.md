# API review — Slice 5 implementation

## Decision

**Approved to proceed to packaging and installed qualification.** The reviewed
implementation realizes the Slice 4 contract without widening the API-visible
result schema.

## Review findings

- `retire_completed_external_authority_v2_intent()` validates the complete
  terminal inventory before touching the candidate state, constructs a closed
  digest-checked retirement record, and removes the live singleton only after
  that proof.
- The coordinator-owned `checkpoint_spend_boundary()` invokes the writer-fenced
  retirement checkpoint before local-progress/successor selection. Worker
  persistence itself remains unable to retire an intent.
- The replay lookup validates `provider_completed` history and returns the
  unchanged public `exact_replay` disposition with zero provider preparation or
  create work. A distinct successor must still commit its own live intent.
- The Slice 5 tests include a real reconciliation/reporting sequence and a
  `closure.main()` creative-retry-adoption path, in addition to partial,
  conflicting, interruption, replay, successor, and privacy cases.

## Release gate

For installed qualification, retain the exact assertions that:

1. retirement happens in the published coordinator checkpoint, not merely in
   process memory;
2. an exact predecessor replay creates no provider work;
3. a fresh successor creates exactly once; and
4. malformed or incomplete terminal evidence leaves the live intent intact and
   cannot create a successor.

Delerium remains frozen diagnostic evidence. This approval authorizes only
provider-free packaging/qualification and later release preparation; it does
not authorize retained-run recovery or provider work.
