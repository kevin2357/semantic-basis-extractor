# Slice 4 — retired-intent contract and runtime-integration design

## Decision

The correction can remain an internal native-state evolution. Existing public
v2 command-result semantics already express all consumer-visible outcomes:

- a fresh authority either commits and dispatches normally or refuses;
- an exact replay returns the existing closed `exact_replay` outcome; and
- pending, partial, ambiguous, conflicting, or malformed custody remains
  non-retirable and continues through its existing reconciliation/review paths.

No lifecycle, authority-request, grant, provider-dispatch-result, or API state
version needs to change merely to make the live intent slot truthful.

## Exact normal integration point

The first complete native checkpoint is the coordinator-owned quiescent
checkpoint after `SpendController.settle_active()` has made every member of one
v2 intent `REPORTED` and the provider response/reconciliation evidence is
durable.

For the reproduced creative-retry path, that is the `save_state()` checkpoint
inside `checkpoint_spend_boundary()` as the completed retry is adopted and the
command unwinds at its next authority/quiescence boundary. Worker-thread
`persist_state()` calls are not complete workspace checkpoints and are not the
retirement boundary.

The implementation should introduce one writer-fenced quiescent-checkpoint
helper used by the ordinary exact-interactive command:

1. acquire `_exclusive_lifecycle_lock(run_dir)`;
2. re-read or join the coordinator's current state without accepting a stale
   competing revision;
3. validate the complete live-intent terminal join described below;
4. when complete, append exactly one retired record and remove the singleton
   live intent in memory;
5. persist the state/journal and publish the workspace snapshot while the same
   native writer is held; and
6. validate the resulting snapshot before releasing the writer.

The helper is called for both exceptional paid-stage handoff checkpoints and
normal final/quiescent checkpoints. Retirement is therefore caused by terminal
native truth, not by the arrival of a future request.

This patch initially targets ordinary exact-interactive Response actions—the
route reproduced by Delerium. Initial-wave and Batch intent models are distinct.
Bounded ordinary-v2 applicability must be characterized before sharing the hook;
it must not be enabled merely because the internal record is route-neutral.

## Complete terminal join

Retirement is permitted only if one strict validator proves all of the following
for the complete ordered intent inventory:

- intent schema/state/cursor/active-call fields are closed and internally
  coherent;
- every ordered action exists exactly once in the ledger;
- complete action binding, authorization document identity, and consumption
  identity join the intent request/grant/member records;
- every action is `REPORTED`;
- every provider identity is durable, unique, and exactly equals the ordered
  intent provider-operation identity;
- reconciliation timing records `last_outcome=completed` with no remaining
  `resume_not_before`;
- reported usage/billing evidence is present, preserving unavailable distinctly
  from zero where the existing disposition permits it;
- the snapshot-declared retained reconciliation response exists, is strict JSON,
  carries the exact provider identity and `status=completed`, and its artifact
  digest is included in the terminal-evidence basis; and
- no ambiguity, identity conflict, partial cursor, missing member, duplicate
  evidence, unsupported mechanism, or contradictory action state exists.

The validator is all-or-none. A multi-member intent cannot retire member by
member.

## Closed internal retired record

Successful retirement appends one record to the existing
`external_authority_v2_dispatch_history` list:

```text
schema_version
outcome
request_schema_version
request_sha256
checkpoint_basis_sha256
grant_schema_version
grant_sha256
api_decision_id
ordering_semantics
ordered_action_ids
ordered_authorization_document_sha256s
provider_bound_action_ids
provider_operation_ids
prepared_create_records
terminal_action_records
terminal_evidence_sha256
retirement_state_revision
retirement_record_sha256
```

Normative values:

- `schema_version = astrowoof.external_authority_v2_retired_invocation.v1`
- `outcome = provider_completed`
- ordered inventories preserve the exact `lexical_action_id_ascending` intent
  order;
- each `terminal_action_record` contains only safe identity/digest facts:
  action ID, binding digest, authorization-document digest/reference,
  consumption digest, provider kind/ID, reconciliation-evidence digest,
  reported-evidence digest, and retained-response artifact path/bytes/digest;
- `terminal_evidence_sha256` commits to the complete ordered terminal-action
  record inventory; and
- `retirement_record_sha256` commits to every record field except itself.

The record contains no request payload, prompt, provider response body, authored
content, subject data, credentials, or API-global reservation/lease/capacity
claim.

`retirement_state_revision` is the revision produced by the state persistence
that adds the record and removes the live slot. Embedding that same snapshot's
SHA-256 inside `run.json` would be self-referential, so it is intentionally not
claimed. Instead, the validated workspace snapshot inventories the retired
record in `run.json`; replay returns its existing public post-snapshot identity.
No new publication receipt is necessary.

## Replay precedence

The existing CLI already defers intent revalidation when the supplied action is
provider-bound/reported, then asks the dispatch layer for exact replay. Extend
the dispatch history lookup as follows:

1. validate the current workspace snapshot;
2. search exact `(request_sha256, grant_sha256)` history;
3. duplicated or contradictory matches → `native_evidence_invalid`;
4. an exact pre-provider-refusal record retains its existing replay behavior;
5. an exact `provider_completed` retired record returns the existing v3
   `exact_replay` result with `provider_identity_durable`, `replayed`, the exact
   ordered provider inventory, and zero provider I/O; and
6. absent exact history proceeds only through a current live intent.

A fresh successor request/grant never borrows, aliases, or reopens predecessor
authority. It requires a fresh current inspection and the ordinary constrained
commit fence.

## Historical compatibility

Steady-state runtime must retire at its terminal quiescent checkpoint. A
historical workspace may already contain a complete terminal intent stranded in
the live slot.

Compatibility repair, if implemented in this patch, must:

- run only under the same writer and exact terminal validator;
- append the identical closed retired record and remove the live slot;
- perform zero provider I/O and consume no new authority;
- invalidate the caller's prior inspection/basis and require a fresh inspection
  and fresh API decision before successor dispatch; and
- emit a typed native diagnostic distinguishing compatibility repair from normal
  retirement.

It must not retire pending, partial, ambiguous, conflicting, unjoinable, or
malformed history. Delerium itself remains an unauthorized investigation object;
this design does not authorize repairing or resuming it.

## Failure atomicity

- Before state persistence: no retired record and live slot remains.
- After state persistence but before snapshot publication: the workspace is
  snapshot-invalid and must fail closed; it cannot dispatch a successor.
- After snapshot publication: record and slot removal are visible together.
- Event/log sink failure cannot change retirement, replay, snapshot, or provider
  behavior.
- Repeating normal retirement is idempotent: exactly one history record, no live
  slot, no provider I/O.

## Runtime test matrix for Slice 5

1. Real scripted v2 create → real reconciliation/adoption/reporting → exact
   retirement at the coordinator checkpoint.
2. After that checkpoint, no live intent exists and exactly one strict retired
   record does.
3. Exact predecessor request/grant replay returns `exact_replay`, zero create.
4. Fresh successor inspection/request/grant commits a distinct live intent and
   performs exactly one successor create.
5. Pending, partial, ambiguous, conflicting, missing-response, wrong-response-ID,
   unsupported-status, malformed-artifact, and multi-member partial-terminal
   cases retain the live slot and permit zero successor creates.
6. Failure before persistence, between state and snapshot, and after snapshot
   proves the atomicity classifications above.
7. Privacy sentinel absent from record, events, logs, public output, and fixtures.

## Oauf-paws 5

Pause for API/owner approval before runtime mutation.
