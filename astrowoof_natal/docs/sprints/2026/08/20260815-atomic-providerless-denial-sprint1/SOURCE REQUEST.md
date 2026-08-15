# Source Request: Atomic Providerless-Denial Batch Lifecycle Support

## Observed scenario

An SBE run reached `DELIVERY_COMPLETE` with two remaining providerless,
API-authorized creative-retry actions. The API inspected once, then called the
single-action `deny_providerless_action()` twice using that same observation. The
first call correctly mutated native state and refreshed the state revision and
snapshot; the second correctly failed closed because its observation was stale.

The stale protection behaved correctly. The integration seam is that one logically
atomic terminal cleanup currently crosses the API/SBE boundary as several
individual mutations.

## Requested capability

Design and implement a supported operation conceptually shaped as:

```python
deny_providerless_actions(run_dir, request)
```

One request should:

- identify one native run and one observed lifecycle/snapshot identity;
- carry an ordered bounded set of exact action denial requests;
- validate every member before mutation;
- apply all eligible denials together or none;
- write one coherent new `run.json` and snapshot;
- return a typed result with per-action outcomes and a shared checkpoint;
- support exact idempotent replay;
- fail closed on stale observation, binding mismatch, provider evidence, ambiguous
  submission, unknown/duplicate actions, or mixed applicability; and
- emit useful typed per-action and batch-level lifecycle events.

SBE remains authoritative for native workspace state, snapshot identity, denial
eligibility, and native mutation. The API remains authoritative for its PostgreSQL
paid-action ledger, reservations, and capacity allocations.

## Questions to decide and document

1. Is `DELIVERY_COMPLETE` a supported context for denial of previously authorized
   but never provider-bound actions?
2. Must every member be independently providerless-denial eligible, with all-or-none
   preflight?
3. What exact result and per-action fields distinguish application, replay, stale
   observation, provider evidence, ambiguity, binding mismatch, and other refusal?
4. Does the existing single-action operation remain supported unchanged?
5. Can this operation run and replay against a retained terminal workspace without
   submitting provider work?

## Acceptance expectations

- Public consumer-facing Python and CLI contract packaged in the wheel.
- Strict schema validation and deterministic/idempotent behavior.
- Tests for two successful denials, replay, stale observation, zero mutation on one
  ineligible member, duplicate/unknown/binding mismatch, terminal delivery with
  unused authorized actions, event emission, and installed-wheel smoke where
  appropriate.
- API handoff with exact request/result examples and migration/compatibility notes.

The request is limited to SBE's native lifecycle contract. API adoption, release of
matching API authority, delivery publication, and audited recovery of affected API
runs remain API work.
