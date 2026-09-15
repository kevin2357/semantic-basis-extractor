# Slice 2 — Causal Reproduction and Correction Fence

## Provider-free reproduction

`slice2_provider_free_reproduction.py` constructs a realistic complete ledger
binding, asks the real terminal-review producer to build its disposition, and
then applies the current capture digest expression.

Two tests pass:

1. the producer's sealed digest equals the closed terminal projection and
   differs from the digest of the complete realistic binding; and
2. every contract-bound field changes the projected digest, while the four
   observed extra ledger fields do not redefine the sealed contract.

This is the same digest-domain split proven across all fifteen retained action
rows. It uses no provider, network, database, R2, or mutable workspace action.

## Ownership and correction boundary

This is an SBE capture-consumer defect. The terminal-review v0.2 producer and
its result validator agree on a closed action-binding projection. Capture must
recompute the same projection rather than hashing the complete ledger mapping.

The narrow correction should expose or centralize one canonical terminal
action-binding projection/digest helper and use it in both:

- `build_terminal_action_dispositions()`; and
- editorial runtime capture's pass and optional-stage disposition joins.

Do not remove the join, accept either digest opportunistically, discover a
latest result, rewrite sealed v0.2 results, or broaden the sealed projection as
an incidental compatibility change.

## Required implementation regressions

- A producer-generated v0.2 result plus a realistic complete ledger binding
  reaches packet construction.
- Both no-polish and multi-polish terminal-review routes are covered.
- Every contract-bound field mutation fails closed.
- Wrong action ID, missing disposition, duplicate disposition, and conflicting
  disposition fail closed.
- Extra non-contract ledger fields do not redefine the producer's digest.
- Existing delivery capture remains byte-compatible.
- Successful review capture emits packet, projections, and the expected
  longitudinal artifact set from the same exact result.
- Any new test module is registered in `test_suite_manifest.json`.

## Alloy ruling

No model update is indicated. The correction aligns two implementations of an
already sealed identity projection; it changes no lifecycle, authority,
eligibility, terminal selection, custody, or artifact chronology rule.

## Review gate C

Investigation is complete and paused for joint API/SBE review. No runtime
implementation, version bump, package qualification, release, deployment, or
live witness is authorized by these findings.

