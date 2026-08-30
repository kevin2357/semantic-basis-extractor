# Slice 1 — duplicate-create fence contract proposal

## Status

Approved by API/owner with the typed generic-refusal refinement. Slice 2 implements
that refinement as `astrowoof.generic_provider_dispatch_refusal.v1` and is paused
for implementation review.

## Decision summary

The correction should compose existing public contracts rather than invent another
provider-submission state machine:

1. Lifecycle v0.8 remains the source of exact retry lineage, custody precedence,
   and external-authority selection.
2. External-authority request/grant v2 plus its ordered ordinary authorization
   documents remain the sole complete admission join.
3. The v2 constrained dispatcher remains the create-capable boundary because it
   durably publishes intent and `CALL_ENTERED` before provider I/O.
4. Native result v0.2 remains the no-new-create review/custody result.
5. A new closed review cause, `local_work_progress_contradiction`, should describe
   the specific case where an advertised semantic operation remains unconsumed at
   command closeout.

No new externally visible authoring status is proposed.

## Invariant A — one create boundary

For applicable exact-Natal interactive ordinary actions, including creative retry:

- preparation may occur through ordinary resume;
- lifecycle inspection may export a v2 `ordinary_action_set` request;
- API may make and persist a fresh aggregate authority decision;
- provider creation may occur only through the exact v2 constrained dispatcher;
- generic `--spend-authorization` must fail closed before authorization
  consumption, native mutation, provider I/O, or native-result publication if it
  would make such an action create-capable.

Compatibility aliases may remain readable/non-dispatching. They must not silently
route around the v2 fence.

The prohibited generic invocation returns a closed, nonmutating command conclusion:

- `schema_version = astrowoof.generic_provider_dispatch_refusal.v1`;
- `outcome = pre_provider_refusal`;
- `reason_code = external_authority_v2_dispatch_required`;
- `provider_io_disposition = not_attempted`;
- `new_provider_create_permitted = false`;
- exact run, checkpoint-basis, snapshot, revision, and ordered action identities;
- `next_step = fresh_lifecycle_inspection`.

It exits successfully after printing the typed result, so consumers do not flatten
the safe routing correction into retryable `command_failed`. It does not fabricate
a v2 grant or terminal authoring result.

The initial-wave v1 path is unchanged. Batch and bounded routes remain unchanged
unless Slice 2 source applicability proves they cross the same unsafe generic
boundary and can reuse this contract without semantic widening.

## Invariant B — durable call-entry evidence

The atomic publication protocol under the native writer must make one complete
checkpoint prove either:

- no grant/intent was applied; or
- exact request + grant + ordered inventory + member authorizations + dispatch
  intent are durable together.

Before each create, the dispatcher durably changes the selected member to
`CALL_ENTERED`. It then releases the writer for slow provider I/O. Outcomes retain
the existing closed meanings:

| Evidence | Meaning | Create replay |
| --- | --- | --- |
| `not_attempted` | Refusal occurred provably before provider call entry | Never from the old grant; fresh inspection/authority only |
| `create_entered_unknown` | Provider call entry occurred but identity is absent/uncertain | Prohibited; ambiguity review |
| `provider_identity_durable` | Exact provider identity is durable | Prohibited; reconciliation only |

An identity returned by the provider is checkpointed before another selected
member may enter create.

## Invariant C — post-provider local failure cannot reopen create

`commit_local_work_progress()` may determine that advertised semantic work was not
consumed. That remains a valid safety refusal; the fix must not weaken its
append-only consumed-operation invariant.

Instead of allowing its `ValueError` to bypass public result publication, the
ordinary command boundary should:

1. re-inspect under the native writer;
2. preserve all action/provider/reconciliation/reporting evidence exactly;
3. seal a native result v0.2 with:
   - `outcome = review_required`;
   - `cause_code = local_work_progress_contradiction`;
   - complete action dispositions and inventory digest;
   - `new_provider_create_permitted = false`;
   - exact pre/post checkpoint, journal, result, and receipt bindings;
4. emit an invocation-bound terminal-review command-result envelope; and
5. exit through the supported review-required path.

This is not a claim that the run is editorially terminal. It is a closed native
custody/review disposition: no new provider work may be created until a future,
separately defined recovery contract resolves the contradiction.

## Invariant D — API adoption and retry

API may act only after validating the complete chain:

```text
lifecycle v0.8 inspection
  → external-authority request v2
  → API grant v2 + ordered ordinary authorization documents
  → dispatch intent/result v3
  → command result v2
  → native result + publication receipt + exact checkpoint
```

For a provider-bound or reported action, API persists the exact provider operation
and settlement evidence transactionally before deciding its own lease, capacity,
reservation, or public job state.

An untyped subprocess failure, absent result, stale API action row, or restored
older checkpoint is never authority to recreate provider work. API must re-inspect
and may invoke only the SBE-selected supported command.

## Historical duplicate posture

For Marmalade and any equivalent historical action:

- retain both observed provider identities as contradictory evidence;
- do not select, merge, retrieve, settle, deny, or discard either automatically;
- classify the action/run as provider-submission conflict requiring review;
- prohibit new provider creation;
- do not mutate the frozen workspace during this sprint;
- design recovery only after a separate fixture-backed contract review.

## Refusal precedence

1. Snapshot/journal/result integrity failure.
2. Durable provider identity, provider evidence, consumption, or call-entry
   ambiguity.
3. Retry-lineage conflict or action/binding/inventory mismatch.
4. Stale request/grant/checkpoint basis.
5. Unsupported route/mechanism/stage.
6. Missing compatible grant or generic create-capable invocation.
7. Pre-provider payload/configuration refusal.

Provider safety evidence must not be flattened into stale observation or generic
local failure.

## Required Slice 2 regressions

1. Generic spend authorization for an applicable prepared creative retry refuses
   with zero mutation, provider calls, and result publication.
2. Real v2 request/grant/authorization joins commit intent atomically.
3. The unpatched dispatcher durably records `CALL_ENTERED` before a scripted
   provider adapter is entered.
4. Crash immediately after `CALL_ENTERED` produces ambiguity and never a second
   create.
5. Returned identity is immediately durable and replay is reconciliation-only.
6. Provider completion followed by a genuine local-progress contradiction seals
   review-required v0.2 evidence rather than escaping untyped.
7. Restoring the last API-adoptable checkpoint and replaying the exact command
   cannot produce a second create.
8. Existing initial-wave, provider reconciliation, pre-provider refusal, terminal
   review, and retry-lineage behavior remains unchanged.

## API review questions

1. Approve constrained external-authority v2 as the only create-capable boundary
   for applicable exact-interactive ordinary action sets?
2. Approve `local_work_progress_contradiction` as a new native-result v0.2 review
   cause without a new lifecycle status?
3. Should API map that sealed result directly to stable operator review while
   retaining exact provider/reservation evidence, or is a narrower named API
   disposition required?
4. Approve leaving initial-wave v1, Batch, bounded, and historical recovery outside
   this first runtime slice unless shared-path characterization proves necessary?
