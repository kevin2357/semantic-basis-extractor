# Slice 1 - Quiescent Checkpoint Architecture

Status: complete; gate approval pending.

## Result

State/ledger persistence is now separate from complete-workspace checkpoint
publication.

`persist_state()` atomically advances and writes operator state, public state,
and authorization requests without changing `workspace-snapshot.json`.
`save_state()` remains the coordinator operation: on the main thread it first
persists state and then inventories the quiescent workspace. Worker-thread
saves are persistence-only.

Every `SpendController` transition now uses persistence-only writes. This keeps
commitment, authorization consumption, provider identity, waiting/ambiguity,
and reported usage durable at the earliest safe point without falsely
attesting that surrounding request, response, QA, final, or subject artifacts
have settled.

Known spend-control pauses in interactive/Batch authoring and optional final
stages unwind through `checkpoint_spend_boundary()`. After the orchestrated
mutation returns or raises awaiting authorization, budget exhaustion, or
ambiguous submission, the coordinator persists the complete state and
publishes one snapshot before returning control to the consumer.

`finalize_subjects()` now installs a newly assembled subject record into
`state["subjects"]` before entering resumable polish. Attempt results mutate
that state-owned object, so an attempt-2 authorization exception can no longer
discard attempt-1 state and provider metadata.

The API remains responsible for one exclusive run lease and for copying worker
scratch only after the SBE invocation exits. SBE's spend-consumption lock still
serializes authorization consumption. The failure-injection slice will audit
and harden process interruption on both sides of every provider/checkpoint
boundary; this slice does not claim that an arbitrary mid-transition crash has
become automatically resumable.

## Contract consequence

A durable ledger write is not necessarily a restorable workspace checkpoint.
The consumer-visible snapshot is authoritative only after the coordinator has
published it at a quiescent exit. Documentation now makes that distinction
explicit for ordinary author workers and optional paid stages.

The run schema and snapshot schema versions remain unchanged in this slice.
No new public state is needed for a normal authorization pause: its existing
`AWAITING_SPEND_AUTHORIZATION` state is now accompanied by a coherent snapshot.
Any new incomplete-transition or repair classification is deferred to the
failure-injection/recovery slices and will require its own gate review.

## Verification

- State-owned polish record across attempt-2 authorization pause: pass.
- Persistence-only write leaves prior snapshot unchanged: pass.
- Coordinator spend-pause unwind publishes a validating snapshot: pass.
- Mixed-generation inventory reproduction remains active: pass.
- Complete semantic-closure suite: 71 passed in 67.046 seconds.
- Spend-enforcement plus installed-smoke regression modules: 19 passed in
  26.003 seconds.
- `git diff --check`: pass.
- Provider requests, authorization consumption, and incremental spend: zero.
- Retained acceptance run mutation: none.

Next action: approve the production persistence/checkpoint/subject-state diff
before Slice 2 provider-interruption and boundary failure injection.
