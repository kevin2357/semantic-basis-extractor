# Slice 7 — Public Lifecycle, Fixtures, Oracle, and Handoff

Status: complete; awaiting API consumer review

## Result

Bounded interactive and Batch route parity is now exposed through strict installed
consumer evidence without adding public lifecycle states. The public lifecycle
runtime remains inspection v0.3 and reconciliation-cycle result v0.2; the new
resources provide route-specific adoption evidence over that existing vocabulary.

The installed package now includes:

- `astrowoof.route_parity_transition_oracle.v2`;
- `astrowoof.bounded_route_parity_traces.v1`;
- strict typed Python readers and validators; and
- the provider-free `astrowoof-route-parity-evidence` CLI.

The oracle and traces are sanitized consumer fixtures, not native run authority.
Actual authority remains the validated native workspace, snapshot, lifecycle
inspection/cycle result, transition journal, immutable execution result, and
publication receipt.

## Coverage

The evidence includes bounded interactive multi-pass continuation and retry plus
bounded Batch authorization, pending, early nonmutating `not_due`, due reclaim,
partial-member pass-local retry, usage unavailable after retrieval, ambiguous
submission, terminal provider failure, and final delivery.

It explicitly proves that retrieved terminal files can end provider retrieval
custody while integrity or billing conditions retain API consumer authority. It
also preserves one reservation per Batch round, never per member.

## Verification

- Focused strict reader/catalog tests: 34 passed, 6 optional `jsonschema` tests
  skipped in the lean desktop runtime.
- Desktop bounded/lifecycle/native-transition gate: 132 passed in 156.449 seconds,
  with the same 6 optional skips.
- Python 3.11 Linux read-only-container gate: 132 passed in 19.832 seconds, with the
  same 6 optional skips.
- Lifecycle installed-resource smoke: pass.
- Provider operations: 0.
- Provider spend: USD 0.

The sprint now pauses at the required API review gate before Slice 8 installed
qualification and release recommendation.
