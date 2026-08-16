# Slice 4: Exact-Stage Completeness

Status: implementation complete; pending Kevin's Slice 4 gate review.

## Supported production route

Bounded reconciliation now covers every provider stage in the exact interactive
Natal pipeline:

- initial authoring;
- creative retry;
- polish;
- qualitative critic; and
- qualitative candidate generation.

Completed responses are first persisted as immutable private reconciliation
evidence. The ordinary stage implementation then consumes those exact bytes and
runs all newly unblocked local assembly, finalization, validation, and qualitative
review work. No stage performs a second provider GET, and reconciliation-only
spend control prevents every POST/new submission path.

Optional stages are supported only when the frozen generation profile enables
them. A disabled stage with timing-like bytes fails closed instead of inheriting
capacity-release semantics.

## Secondary-route classification

- Interactive exact Natal is parity-supported across all five stages.
- Batch remains explicitly unsupported by this bounded Responses operation.
- Bounded Natal remains explicitly unsupported until it has its own proven
  reconciliation adapter.
- Unsupported routes return a typed `unsupported` result, make no provider call,
  and never advertise `release_until_due`.

The route check is bound to the exact native run schema, interactive service
level, frozen optional-stage policy, action stage, snapshot, and lifecycle state.

## Delivery and critic precedence

A completed, publishable delivery may coexist with a nonblocking critic or
candidate Response still pending. Delivery remains publishable, local capacity may
be released until the provider action is due, and the exact provider action stays
in custody with `retain_consumer_authority: true`. Releasing the worker therefore
does not imply releasing API reservation or financial authority.

Review, ambiguity, external authorization, and terminal precedence remain typed
and nonmutating in the low-level cycle result. Pure classification performs no
provider operation.

## Gate evidence

Focused tests cover the five exact stages, enabled/disabled optional policy,
Batch and bounded fail-closed behavior, terminal/result classification,
publishable-delivery plus background-critic custody, and cached response reuse at
all three optional attempt-root layouts.

The focused matrix passed all 22 tests in 5.164 seconds. The complete repository
suite passed all 335 tests in 158.131 seconds.

Provider operations: 0. Paid spend: `$0`. API key used: no. Runtime release remains
0.4.2; no build, version bump, tag, or publication occurred.
