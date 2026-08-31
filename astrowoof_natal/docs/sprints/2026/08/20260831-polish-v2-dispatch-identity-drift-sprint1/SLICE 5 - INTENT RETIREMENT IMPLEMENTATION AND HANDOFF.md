# Slice 5 — intent-retirement implementation and handoff

## Outcome

The narrow exact-interactive correction is implemented.

The live ordinary-v2 singleton now retires at the first coordinator-owned
quiescent checkpoint after the complete ordered intent inventory has become
terminally reconciled and reported. The correction does not wait for a later
successor request and performs no provider operation itself.

## Runtime changes

### Strict retirement validator

`retire_completed_external_authority_v2_intent()` validates the complete
all-or-none join across:

- exact intent request/grant/action/authorization inventories;
- authorization documents and consumption identities;
- terminal `REPORTED` ledger state;
- exact ordered provider identities;
- completed reconciliation timing;
- reported usage/billing evidence; and
- exact retained completed-response artifacts.

On success it appends one strict
`astrowoof.external_authority_v2_retired_invocation.v1` record and removes the
live singleton in memory. Pending or partially terminal inventories return
without retirement. Contradictory terminal evidence raises
`native_evidence_invalid` and does not persist the candidate mutation.

### Real checkpoint integration

`checkpoint_spend_boundary()` now publishes a writer-fenced exact-interactive
quiescent checkpoint before its local-progress callback. The checkpoint:

1. validates the persisted revision/run join;
2. builds retirement on a candidate state;
3. persists state/journal;
4. publishes and validates the workspace snapshot; and
5. updates the coordinator's in-memory state only after the valid checkpoint.

The same behavior is used at normal exact-interactive detach/final checkpoints.
Non-main worker persistence remains unchanged and cannot retire an intent by
itself.

### Exact replay

Dispatch history lookup now validates a completed retired record before looking
for a live intent. An exact predecessor request/grant returns the existing
public v2/v3 `exact_replay` result with the original ordered provider identities
and zero provider I/O.

A different successor request does not match that history. It must be produced
from a fresh inspection, receive its own grant/documents, commit a distinct live
intent, and cross its own provider-call fence.

## Provider-free runtime proof

The new Slice 5 fixture proves both the isolated state machine and the actual
creative-retry adoption path.

### Composed retirement/replay/successor trace

1. Commit and dispatch a real ordinary-v2 two-member intent through production
   functions and a scripted create transport.
2. Run the real provider-reconciliation cycle with completed scripted Responses.
3. Run the real `SpendController.settle_active()` reporting transition.
4. Publish the coordinator retirement checkpoint.
5. Prove one strict retired record, no live singleton, and a valid snapshot.
6. Replay the exact predecessor authority and prove `exact_replay` with no
   create.
7. Prepare a fresh successor, obtain a fresh inspection/request/grant, and prove
   exactly one new provider create under its distinct live intent.

### Actual creative-retry adoption trace

A production-shaped exact workspace enters through normal `closure.main()`:

- the reconciled completed response is adopted without provider I/O;
- authoring validation and `SpendController` reporting run normally;
- the coordinator quiescent checkpoint retires the intent before the later
  local-progress decision; and
- the published workspace contains exactly one retirement record and no live
  predecessor singleton.

### Safety cells

- partially terminal multi-member inventory retains the live intent;
- response identity conflict refuses without retirement;
- before-persistence interruption preserves a valid pre-state/live slot;
- after-state/before-snapshot interruption is snapshot-invalid and fail-closed;
- after-snapshot interruption exposes a valid retired-record/no-live-slot pair;
- exact replay performs no prepare/create work; and
- retired evidence contains no prompt, response body, subject parameters,
  credentials, or authorization header material.

## Public/API boundary

- No public schema or lifecycle version changed.
- Existing v3 `exact_replay` bytes retain their existing shape and semantics.
- SBE asserts no API reservation, lease, slot, or global-capacity fact.
- API still supplies every fresh successor inspection/request/grant/document
  set and never decides native retirement.
- Historical compatibility repair was not added. Delerium remains untouched and
  unauthorized for recovery.
- Initial-wave and Batch intent models remain out of scope. Bounded ordinary-v2
  integration remains deferred pending route-specific characterization.

## Verification

- Slice 5 retirement tests: `5 passed`.
- Retirement + sequential-v2 + v2 contracts/routes + intent-fence + Moxie
  adoption + composed post-fan-in matrix: `49 passed, 1 optional-schema skip`.
- External provider/network calls: `0`.
- Retained Delerium/R2 operations during implementation: `0`.

## Review gate

Pause for API implementation review before packaging, installed-wheel
qualification, versioning, or release preparation.
