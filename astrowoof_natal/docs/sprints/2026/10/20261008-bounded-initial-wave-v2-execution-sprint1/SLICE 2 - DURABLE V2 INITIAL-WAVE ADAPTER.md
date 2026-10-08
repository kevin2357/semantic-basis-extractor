# Slice 2 — Durable v2 Initial-Wave Adapter

## Implementation

`bounded_lifecycle.commit_bounded_initial_wave_v2_dispatch_intent()` is a
separate entry point from the ordinary external-authority v2 dispatcher. It
requires `initial_wave_admission`, re-inspects the exact checkpoint, validates
the v2 grant and six authorization documents, validates the stored bounded
wave/binding bundle/request bytes, and authorizes then begins submission for
all six members in their prepared semantic order.

It writes one `SUBMITTING` constrained intent before provider I/O. The intent
stores only a SHA-256 of its process-local capability. The raw capability is
kept in process memory keyed by workspace/request/grant; after process loss,
the adapter refuses a fresh submission rather than inventing a replacement
provider call.

`dispatch_bounded_initial_wave_v2_intent()` accepts only that exact pair and
delegates to `_execute_bounded_interactive_initial_wave()`. Thus it retains the
existing six-way parallel create, identity checkpoint, and ambiguity behavior.
It does not use the ordinary dispatcher’s lexical ordering or serial payload
resolver.

## Replay and failure boundary

- Repeating the exact commit returns the immutable intent receipt without
  rediscovering a now-stale pre-intent checkpoint and without provider I/O.
- A different request/grant after an intent exists is refused.
- A detached wave returns its existing result and makes no second create.
- Malformed or tampered workspace evidence refuses before intent creation.
- A process restart has no raw capability, so it cannot perform a new create;
  durable provider identity/reconciliation remains the only safe successor.

## Provider-free proof

`test_bounded_initial_wave_v2_contract.py` now proves:

1. one valid v2 grant produces exactly one semantic-order intent;
2. a fake bounded provider receives exactly the six expected creates;
3. commit and dispatch replay cause no duplicate create;
4. descriptor tamper, injected pre-intent failure, and duplicate documents
   fail closed before provider I/O.

The public CLI/result-envelope adaptation is intentionally not frozen by this
slice. Gate C review must choose its exact API-visible result shape before the
adapter is wired into the production command, rather than silently presenting
the bounded semantic order as an ordinary v2 lexical result.
