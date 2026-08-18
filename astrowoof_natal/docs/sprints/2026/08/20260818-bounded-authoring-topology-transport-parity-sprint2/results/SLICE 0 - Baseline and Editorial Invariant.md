# Slice 0 — Baseline and Editorial-Invariant Evidence

Date: 2026-08-18
Status: complete; awaiting gate review
Provider operations: 0
Spend: USD 0

## Outcome

The baseline supports the sprint direction.

Exact Natal already treats interactive Responses and Batch as transports over the
same six logical pass requests. Bounded Natal currently does not share that topology:
its 50 claims and four summaries are presented through one pass and one whole-deck
Responses operation, while Batch is rejected before submission.

No new public lifecycle vocabulary is indicated. A new bounded run/route contract,
six-pass identity, and supported bounded-Batch trajectories are required. Legacy
one-operation bounded workspaces cannot be safely reinterpreted and should fail
closed.

## Exact assignment baseline

`stratified-v1` is deterministic for a frozen selected packet, subject, and policy
identity. It:

- assigns every priority ID 1-50 exactly once;
- produces five card passes of ten claims;
- balances claim types, categories, behavioral domains, and priority bands;
- orders each pass to reduce adjacent semantic similarity;
- persists policy, algorithm version, replay seed, and ordered membership; and
- reassembles accepted authoring workspaces in canonical selected-claim order.

It is not an unrecorded random shuffle. Different selected bases or an explicit
future policy/seed version may produce different assignments.

## Exact transport-parity proof

The added regression constructs one frozen exact pass and captures its interactive
Responses request. With explicit cache controls disabled, removing the interactive-
only `background` envelope field makes the request exactly equal to the Batch JSONL
member body produced for the same provider, pass, workspace, and feedback.

Equality covers:

- model and reasoning effort;
- system instruction bytes;
- ordered static, subject, and pass-assignment user segments;
- strict writable-field schema;
- maximum output tokens; and
- optional safety identifier.

Batch intentionally omits interactive prompt-cache controls. That is a documented
transport difference, not an editorial packet difference.

The existing fake-provider baselines additionally prove six interactive passes and
six Batch members reach accepted pass state. Batch detach/resume retains one round
and one attempt per pass.

## Current bounded baseline

The compiled bounded provider fixture contains:

- 50 invariant claims;
- four summaries; and
- authoring packet contract `astrowoof.bounded_natal.authoring_packet.v1`.

Current `create_bounded_run()` nevertheless creates one pass record:

```text
pass_id = <subject>_bounded
pass_number = 1
```

`resume_bounded_run()` then calls `_execute_stage()` once for the full
`authoring_initial` payload, or once more for a whole-deck `creative_retry`. The
provider serializes the complete bounded authoring packet and requests all cards and
summaries in one structured response. Hydration correctly restores immutable claim
authority after provider output, but the model-context topology does not preserve the
exact route's anti-templating fan-out.

`OpenAIBoundedLifecycleProvider(service_level="batch")` raises before transport
construction can submit work. The packaged route-parity oracle v1 consequently
contains `bounded_batch_rejected` with outcome `unsupported`.

## Shared-engine seam inventory

### Reusable provider-transport mechanics

- versioned request/action digest binding;
- Files API JSONL upload;
- Batch creation, ID persistence, and detach;
- due-time polling and terminal-state retrieval;
- output/error File identity and durable download;
- strict unique `custom_id` correlation;
- known-provider no-resubmit behavior;
- Batch-round aggregate commitment and settlement;
- missing-usage cost disposition and consumer-authority retention;
- snapshot/journal/result publication; and
- bounded reconciliation-cycle timing and custody projections.

### Exact-route mechanics that must remain behind an adapter

- `PassSpec` and source ZIP discovery;
- Markdown story-workspace rendering;
- writable marker enumeration and authored-field application;
- exact pass acceptance scripts and metadata repair;
- accepted workspace copying; and
- exact final-deck assembly.

### Bounded-route mechanics that must remain behind an adapter

- invariant-only packet admission and provider minimization;
- bounded assignment feature mapping;
- bounded pass packet/schema construction;
- deterministic reattachment of invariant authority and projected terms;
- bounded pass/final validation; and
- bounded delivery/provenance assembly.

The recommended seam is a transport-neutral logical pass request/result protocol
with route-specific construction, hydration, validation, and assembly adapters. The
Files/Batch machinery should be generalized once, not copied into bounded code.

## Lifecycle and authority implications for Slice 1

- Bounded interactive requires one action per route/pass/attempt.
- Bounded Batch requires one action/global reservation per round and member audit
  beneath it.
- The run remains constrained by immutable aggregate and stage ceilings in both
  modes.
- A frozen assignment must bind route, policy/seed, ordered membership, resource and
  schema identities.
- New six-pass state must use a new explicit contract identity.
- Existing one-operation bounded state fails closed rather than receiving fabricated
  pass history.
- Existing waiting, pending, `not_due`, continuation, review, budget, ambiguity,
  policy-stop, provider-failure, and delivery vocabularies appear sufficient.

## Focused verification

The focused provider-free suite passed 36 tests in 23.412 seconds. It covered the
assignment, request, exact interactive/Batch, bounded provider, and provider-pending
baseline areas named in `EVIDENCE.md`.

One test was added:

```text
TestSemanticClosure.test_exact_live_and_batch_share_logical_pass_request
```

No source runtime behavior, schema, provider payload, authorization, network call,
or release artifact changed in Slice 0.
