# Slice 5 Public Interfaces and Handoff

Date: 2026-08-17  
Status: complete; awaiting gate review  
Provider operations: 0  
Paid spend: `$0`

## Outcome

Route-parity reconciliation is now available through supported, typed Python and
CLI consumer surfaces. The API can dispatch exact Responses, exact Batch, and
bounded-Natal Responses from validated native identity without parsing private
state or selecting route code itself.

## Public Python surface

The package root exports:

- `ProviderReconciliationAdapters`; and
- `reconcile_authoring_provider_cycle()`.

The dispatcher validates lifecycle inspection v0.3, native route, mechanism,
snapshot, action binding, and required adapters before invoking a route-specific
cycle. Mixed mechanisms, missing adapters, contradictory identity, and bounded
Batch fail closed before provider activity.

## CLI surface

Both supported authoring commands now expose:

```text
--provider-reconciliation-cycle --observed-at <UTC instant>
```

The exact command supports Responses and Batch. The bounded command supports
Responses and rejects Batch. Both reject new-run use, fake providers, simultaneous
spend-authority mutation, and missing decision time.

The historical exact-only `--bounded-provider-reconciliation` option remains as a
deprecated compatibility alias. It retains its prior implicit current-time
decision and interactive-only behavior; it does not mean bounded Natal. New
consumers must use the neutral spelling.

Nonterminal reconciliation exits with code 3. Consumers distinguish `not_due`,
pending, authority, progress, review, and unsupported states from the JSON result
and embedded inspection, never from the exit code alone.

## Contracts, fixtures, typing, and events

- Public imports carry runtime annotations and remain covered by packaged
  `py.typed`.
- The installed lifecycle smoke now requires the public symbols and the packaged
  transition-oracle fixture.
- Added packaged
  `route-parity-transition-oracle.v1.json` for API transition-oracle adoption.
- Added the closed `provider.reconciliation_observed` event. It exposes only
  action ID, native route family, provider mechanism, outcome, and optional Batch
  member count.
- Retrieved operations emit the observation before `run.detached` and
  `checkpoint.committed`. `not_due` and retrieval-free replay do not duplicate
  retrieval events. All events remain non-authoritative, redacted, and
  sink-failure-isolated.

## Consumer handoff

Published
[Provider Reconciliation Route Parity Handoff](../../../../../post_extraction_authoring/Provider%20Reconciliation%20Route%20Parity%20Handoff.md)
with:

- complete route/mechanism support matrix;
- Python and CLI examples;
- timing, custody, consumer-authority, and outcome mapping;
- exact Batch membership/replay semantics;
- compatibility and bounded-Batch deferral;
- workspace cleanup restrictions; and
- an API adoption checklist referencing the packaged oracle fixture.

The established lifecycle consumer handoff links directly to the new guide.

## Tests

Focused public dispatcher, lifecycle contract, event, exact Batch, exact
interactive, bounded interactive, CLI discovery, and smoke coverage passed all 71
tests in 38.361 seconds. The provider-free lifecycle smoke passed with the public
surface and packaged-resource checks enabled.

The complete repository suite passed all 355 tests in 247.940 seconds.

Installed-wheel and cross-platform qualification remain intentionally assigned to
Slice 6. No network transport, API key, provider endpoint, build, version bump,
release, or tag operation was used.

## Gate conclusion

The API now has one neutral, strict, typed dispatch boundary and packaged adoption
evidence for every supported route/mechanism. Bounded Batch remains unambiguously
unsupported at construction, inspection, dispatch, and CLI boundaries.
