# Slice 2 — Transport-Neutral Wave Coordinator

Date: 2026-08-18
Status: complete; awaiting gate review
Provider operations: 0
Production route switch: none

## Outcome

Added an internal transport-neutral initial-wave module that admits the Slice 1
contract primitives without switching exact or bounded production orchestration.
The module:

- builds deterministic content-addressed exact or bounded six-member waves;
- validates route, assignment, profile, shared preparation basis, action binding,
  member order, aggregate commitment, timing, and cache policy;
- composes and validates the complete API wave envelope plus six existing exact
  member authorizations;
- makes complete preflight mandatory in the create coordinator itself;
- overlaps only provider create I/O;
- serializes every member outcome persistence callback on the coordinator thread;
- persists each completed identity while other create tasks may still be active;
- restores canonical member order in the aggregate result independently of create
  completion order; and
- classifies provider-bound, definitely unattempted, definitively refused, and
  ambiguous outcomes without claiming provider atomicity.

The new internal module is
`astrowoof_natal_authoring.initial_wave`. It is not exported as a public Python API,
not in the packaged contract catalog, and not called by exact or bounded lifecycle
code yet.

## Preparation and preflight

`build_initial_wave()` is pure. It accepts six route-adapter member specifications
and produces one content-addressed wave. It performs no filesystem write, provider
call, authorization consumption, or spend mutation.

`preflight_wave_authorization()` validates:

- wave and envelope content addresses;
- exact copied wave/run/route/profile/basis/price-book/aggregate identity;
- six ordered unique action and binding identities;
- six existing `astrowoof.provider_spend_authorization.v0.1` documents;
- exact full binding and external authorization reference for every member; and
- exact member-document hashes carried by the envelope.

Partial, reordered, stale, duplicate, or binding-conflicting authority fails before
provider or persistence callbacks can run.

Native action creation, budget classification, and one-lock persistence of the six
prepared actions remain route-integration work for Slices 3 and 4. The coordinator
does not invent a second spend ledger.

## Concurrent I/O and single-writer persistence

`execute_initial_wave_creates()` requires the wave, envelope, and six member
documents and reruns complete preflight internally. It starts up to six create tasks.
Tasks perform no native write. Each task places its closed observation onto a
completion queue.

The caller/coordinator thread consumes that queue and invokes exactly one
`persist_member_outcome` callback per member as soon as the observation arrives.
This gives route integrations the required immediate serialized ledger/journal
durability step while other create operations remain active.

An initial implementation incorrectly waited for all futures before persistence.
The Slice 2 tests exposed that mismatch during review. It was replaced before this
gate with the completion-queue design, and the regression now asserts that at least
one persistence callback occurs while another create remains active.

Only after all six outcomes are durably offered to the single writer does the
coordinator return the canonical aggregate result. Aggregate snapshot/result/receipt
publication remains route-command work and is intentionally absent here.

## Timing and failure behavior

The coordinator passes the frozen 15-second timeout to each create callable and
uses the frozen 20-second provider-I/O wave deadline. A transport that fails to
unwind within that contract produces
`submission_cycle_timeout_with_live_tasks`; the executor is retained until tasks
unwind and no safe aggregate checkpoint is advertised.

Create exceptions are conservative:

- explicit `DefinitelyUnattemptedCreate` → `authorized_unstarted`;
- explicit `ProviderCreateRefused` → `create_refused`;
- valid Response identity → `provider_bound`; and
- every unknown exception or missing/invalid identity → `ambiguous_submission`.

Route integrations remain responsible for consuming authorization immediately
before POST and for converting persistence callback evidence into exact ledger,
journal, timing, snapshot, and lifecycle state.

## Route isolation

The module consumes immutable route/member bindings and knows nothing about prompt
construction, exact versus bounded schemas, protected subject fields, semantic
validation, authority hydration, or final assembly. Exact and bounded wave hashes
differ because route family and contract are content-addressed.

No existing prompt, packet, assignment, provider envelope, Batch JSONL, pass result,
or delivery code was changed in this slice.

## Tests

New tests cover:

- deterministic but route-separated exact/bounded wave identity;
- changed digest, timing, and member-order refusal;
- complete nonmutating preflight;
- partial, reordered, stale-basis, and binding-conflicting authority refusal;
- mandatory preflight inside execution with zero callbacks on failure;
- six-way create overlap;
- coordinator-thread-only persistence;
- persistence while other creates remain active;
- canonical aggregate ordering despite reverse completion order; and
- mixed provider-bound/unstarted/refused/ambiguous classification.

Commands and results:

```text
python -m unittest astrowoof_natal.tests.test_initial_wave
Ran 9 tests in 0.029s
OK

python -m unittest \
  astrowoof_natal.tests.test_initial_wave \
  astrowoof_natal.tests.test_initial_wave_contract_proposal \
  astrowoof_natal.tests.test_spend_enforcement \
  astrowoof_natal.tests.test_provider_pending_capacity \
  astrowoof_natal.tests.test_bounded_topology_contract_proposal
Ran 66 tests in 6.718s
OK

python -m compileall -q \
  astrowoof_natal/src/astrowoof_natal_authoring/initial_wave.py
```

`git diff --check` passes.

## Gate assessment

The shared seam is ready for route integration:

- it cannot initiate create I/O without complete exact wave authority;
- provider I/O overlaps but native persistence is serialized;
- immediate per-ID persistence does not wait for aggregate fan-in;
- exact and bounded semantic adapters remain isolated; and
- existing routes are untouched.

Proceed next to exact interactive integration only after review.

