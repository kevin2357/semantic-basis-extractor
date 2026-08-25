# Slice 3 — Provider Dispatch, Replay, and Quiescence Review

Date: 2026-08-24  
Status: implementation complete; API review requested before Slice 4 route qualification

## Outcome

SBE can now dispatch a committed v2 ordinary-action intent through a public Python
boundary while keeping slow provider create I/O outside the native writer. The
persisted intent—not caller-supplied action IDs—selects the complete lexical action
inventory.

The implementation intentionally processes the frozen inventory in order. Before
each provider create it durably publishes `CALL_ENTERED` for that exact member.
After a valid Response identity returns, SBE reacquires the writer and durably
checkpoints that identity, reconciliation timing, cursor advancement, and the
complete snapshot before it permits the next member to enter provider create.

Provider response content is never ingested here. Once identities are durable, the
public lifecycle selects the existing provider-reconciliation cycle.

## Provider atomicity and replay model

| Durable evidence | Behavior |
|---|---|
| Intent cursor before member; no active create | Exact frozen member may dispatch |
| `CALL_ENTERED`; no durable provider ID | Ambiguous/refuse; never create again |
| Returned provider ID checkpointed | Advance cursor; permit only the next member |
| Complete identity inventory | `exact_replay`; zero provider calls |
| Provider identity duplicated across members | Durable ambiguity/review |
| Competing dispatcher while a create is active | Typed ambiguity refusal; zero competing calls |
| Provider callback exception after entry | Durable ambiguity; later members remain uncalled |

The pre-create failure injection point occurs before the durable entered-call
checkpoint and is therefore safely resumable. A process-style interruption after
the checkpoint remains conservatively ambiguous even if the provider call did not
actually begin. This is the irreducible provider atomicity gap; SBE does not claim
provider idempotency from local request identities.

## Public result

`astrowoof.external_authority_provider_dispatch_result.v2` is a packaged, closed
result contract. It binds:

- request/grant/native run identities;
- complete lexical inventory;
- ordered provider-bound and ambiguous members;
- ordered durable provider operation IDs;
- post-state revision and complete snapshot digest;
- outcome: `detached_provider_pending`, `ambiguous_submission`, or `exact_replay`;
  and
- whether this invocation actually performed provider I/O.

Both JSON Schema and the Python validator enforce prefix ordering, closed outcomes,
digest integrity, canonical action IDs, revision shape, and unknown-versus-false
semantics.

## Quiescence and lifecycle behavior

- Before a compatible grant, the existing passive v2 no-grant result remains
  nonmutating and non-dispatching.
- After all identities are durable, a due v0.6 inspection selects
  `provider_reconciliation_cycle` with the exact SBE-selected due subset.
- Generic result ingestion is not added; retrieval/reconciliation remains the sole
  provider-result observation path.
- No SBE artifact asserts API reservations, leases, slots, capacity, or admission.

## Observability and isolation

The constrained boundary emits existing redacted event types for fence validation,
intent commitment, provider-create permission, durable provider identity, and
provider waiting. Event-sink failure is isolated and cannot alter provider calls,
native state, or snapshot validity.

## Evidence

Focused Slice 0–3 plus temporal-lifecycle suite: **50 tests passed** with JSON
Schema enabled. Tests prove:

- writer availability during every provider callback;
- identity checkpoint visibility before the next create;
- exact zero-I/O replay;
- safe resume before create entry;
- durable ambiguity after entered-call exceptions and process-style interruption;
- competing-resumer exclusion;
- partial identity cursor recovery without duplicate create;
- duplicate provider-identity refusal;
- due reconciliation selection;
- strict packaged result validation; and
- event-sink failure isolation.

Provider network calls, OpenAI calls, credentials, spend, and retained-QA workspace
access: **0**. All provider operations were scripted in-process identities.

## Slice 4 review questions

1. Is the durable `CALL_ENTERED` checkpoint an acceptable conservative fence for
   competing resumers and process death?
2. Is ordered one-identity-at-a-time durability the desired v2 ordinary-action
   dispatch rule for the first release?
3. Are the three result outcomes sufficient for API custody/audit mapping?
4. May Slice 4 proceed with exact/bounded applicable-route and holistic 4+2
   qualification using these public primitives?

