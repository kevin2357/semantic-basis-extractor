# API Agent Process-Orchestration Brief

**Prepared:** 2026-08-15  
**Scope:** proposed SBE/API coordination improvement; not yet a sprint plan or a request to change provider semantics.

## Why this brief exists

The AstroWoof API just completed a two-run, two-worker staging qualification cohort using SBE `0.4.2`.  One run completed and published normally.  The other completed its initial submission and most later work, then remained provider-dependent for an extended period while three known provider actions were unresolved.

The important observation is not that an OpenAI response can be slow.  It is that the current API/SBE boundary treats a run with remote work pending as occupying one of the scarce SBE capacity slots for its entire wait.  With two capacity slots, two slow external runs can prevent a third independent reading from beginning, even though the local worker processes are doing only brief reconciliation cycles.

This is a throughput and control-surface issue, not an invitation to weaken durable authority, duplicate provider work, or make logs authoritative.

## Evidence from the qualification cohort

The successful run reached `ready` with 8 paid actions and reported spend `$0.905005`.

The delayed run:

- submitted 10 paid actions and reported `$0.997800`;
- retained three active, already-authorized provider-dependent actions;
- made no additional spend while waiting;
- repeatedly ran short SBE reconciliation cycles, with durable checkpoints and `native.quiescent` outcomes;
- correctly released individual worker leases between cycles; but
- retained an active API `sbe_capacity_allocation`, consuming its slot throughout the provider wait.

This is encouraging: SBE already persists and resumes the semantic closure correctly.  The bottleneck is principally how API capacity models that externally pending state.

## Current shared process

```text
API intent
  -> deterministic worker: AGF canonical graph + four SPC projected graphs
  -> API accepts deterministic checkpoint / queues SBE authoring
  -> SBE worker claims run and invokes closure
  -> SBE submits authoring/provider actions
  -> SBE reaches quiescent checkpoint when provider work is unresolved
  -> API defers the job and later resumes SBE
  -> SBE assembles, validates, polishes/critiques as required, and publishes
```

SBE owns native closure semantics, provider idempotency, authoritative native checkpoint state, and determination of what can proceed.  The API owns user-facing reading state, durable queue/lease/capacity state, artifact custody, cross-run spend authority, and publication delivery.

That ownership split remains sound.

## Proposed incremental target

Do **not** replace SBE with a general workflow engine.  Preserve one logical native closure run, its checkpoints, and its provider action identities.

Instead, make the boundary distinguish three concepts that are currently too close together:

1. **Local execution capacity** — a short-lived worker claim to submit, reconcile, assemble, validate, or publish.
2. **Provider-pending custody** — a durable native/API state in which known provider actions are outstanding and the next reconciliation is due later.
3. **Spend authority** — reservations and reported spend that remain in force while authorized provider work is outstanding.

The desired handoff is:

```text
SBE reaches provider-dependent quiescence
  -> native checkpoint accepted atomically
  -> provider action identities and API spend reservations retained
  -> short local execution slot released
  -> one delayed reconciliation becomes eligible at next_due_at
  -> a worker later claims a short resume cycle
```

This lets an unrelated reading use local execution capacity while a prior reading waits on OpenAI, without forgetting the earlier reading's financial exposure or allowing duplicate submission.

## What SBE might need to expose or clarify

The API agent requests an SBE planning assessment of the smallest supported surface that would allow the target above.  Questions include:

- Does the current public lifecycle already make a machine-readable distinction between provider-pending quiescence and other local-continuation-required quiescence?
- Can SBE provide a recommended next reconciliation/backoff time, rather than relying on the API to infer a tight poll loop?
- Can SBE declare whether a quiescent checkpoint has any local-only continuation requirement that genuinely prevents release of API execution capacity?
- Can the consumer safely resume the same native run after a provider-pending checkpoint from a fresh short-lived worker, provided it preserves the existing run directory/checkpoint artifacts exactly as specified?
- Is any lifecycle state currently held only in the process/workspace such that API cannot safely release the short execution slot before the next resume?
- Which native action states should be treated as still carrying provider/spend exposure, even after a lease is released?

The expected answer may be that most required information already exists in `public-run.json`, `run.json`, and checkpoint metadata, with a narrow additive lifecycle field or recommended-delay signal.  This brief does not prescribe a schema before SBE assesses it.

## API-side companion work anticipated

The corresponding API sprint would likely:

- decouple `sbe_capacity_allocations` from provider-pending custody;
- preserve global spend reservations for unresolved authorized actions;
- schedule one delayed reconciliation per native run rather than a message per action;
- let a due reconciliation reclaim only short local execution capacity;
- keep PostgreSQL authoritative for queue, run, reservation, and capacity state;
- keep SBE checkpoint/action state authoritative for native closure semantics; and
- expose honest user/operator state such as `authoring_waiting_for_provider`, not a misleading active-compute label.

## Future queue/orchestrator direction

A later dedicated scheduler/orchestrator could represent each due local action as a durable queue task, use dependency queries as fan-in barriers, and retain provider actions as child records.  That architecture remains worth keeping in mind, especially for cancellation, global admission policy, and higher throughput.

It is not required for this incremental improvement.  The present goal is to stop equating an external provider wait with a scarce local worker slot while retaining every current correctness property:

- no duplicate provider submission;
- no lost native state;
- no release of reserved spend merely because a worker lease ends;
- no inference of authoritative state from logs;
- explicit retry/backoff and terminalization; and
- restartable execution from durable artifacts.

## Non-goals

- Changing authoring editorial behavior or SBE claim/deck semantics.
- Replacing native checkpointing with API-owned pseudo-checkpoints.
- Making provider polling log-driven.
- Implementing a generic external workflow platform before this narrow boundary is understood.
- Removing per-run or global spend controls.

## Requested next step

Please assess this brief against SBE `0.4.2`, identify any lifecycle/schema constraints, and propose a sliced `PLAN.md` for an SBE-owned incremental improvement.  The plan should call out every API contract addition or change explicitly, so API can plan the companion work without guessing at native closure invariants.
