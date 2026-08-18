# Slice 3 — Shared Pass Seam and Exact Compatibility

Date: 2026-08-18  
Status: complete; awaiting gate review

## Outcome

Exact and bounded authoring can now traverse one small transport-neutral pass
identity seam without sharing or weakening their semantic adapters. Exact retains
its ZIP/workspace prompts, schemas, reconstruction, and assembly. Bounded retains
its JSON packet, invariant-only authority, minimized provider view, validation, and
authority hydration.

The seam does not execute provider work and does not decide between interactive
Responses and Batch. It freezes the logical request that either transport must
carry later.

## Logical binding

`astrowoof.authoring.logical_pass_request.v1` binds:

- semantic route family and route contract;
- assignment, pass number/count, and pass ID;
- attempt and stage;
- resource identity;
- complete logical prompt identity;
- output-schema identity; and
- maximum output tokens.

`astrowoof.authoring.logical_pass_result.v1` binds returned output to that exact
request, route, pass, and attempt. Exact replay is stable; a changed prompt, schema,
stage, attempt, resource, maximum output, or route produces a different identity.

## Route boundary

- Exact interactive builds its existing request first, then validates that request
  through the shared seam. Its provider envelope and idempotency behavior are
  unchanged.
- Exact Batch does the same for each existing Batch member and now explicitly binds
  the scheduler's actual attempt number.
- Bounded adapts its strict Slice 2 pass packet into the seam and revalidates the
  packet digest before binding it.
- Bounded card schemas admit exactly ten assigned claim IDs and no summaries.
- The bounded summary schema admits exactly four assigned summary IDs and no cards.
- Exact-shaped evidence is rejected by bounded hydration, and a bounded result
  cannot validate against an exact request identity.

## Evidence

```text
Shared protocol + complete exact semantic-closure suite:
Ran 90 tests in 214.081s
OK

Focused bounded protocol/provider/packet suite:
Ran 21 tests in 1.215s
OK

Python 3.11 Linux worker focused gate:
Ran 10 tests in 1.881s
OK
```

No public lifecycle state or provider mechanism changed in this slice. Bounded v2
interactive execution begins only after the Slice 3 gate is accepted.

Provider operations: 0. Spend: USD 0.
