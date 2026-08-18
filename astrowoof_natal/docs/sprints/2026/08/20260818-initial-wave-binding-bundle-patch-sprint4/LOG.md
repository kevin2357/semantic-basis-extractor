# Initial-Wave Binding Bundle Patch Sprint 4 Log

## 2026-08-18 — Sprint proposed

- API Slice 2 identified that Initial Authoring Wave v1 exposes binding digests but
  lacks a strict supported public artifact carrying the six complete bindings.
- Confirmed `spend-authorization-requests.json` contains the facts but is not an
  adequate wave-bound closed public contract.
- Proposed a narrow additive binding-bundle v1 contract and fresh immutable 0.4.8.
- Awaiting Kevin approval before Slice 0.

## 2026-08-18 — Slice 0 complete; awaiting contract review

- Inventoried exact and bounded preparation: both create and persist complete native
  action bindings before projecting prepared-wave members.
- Froze `astrowoof.initial_authoring_wave_binding_bundle.v1` and root artifact path
  `initial-authoring-wave-binding-bundle.json`.
- Froze canonical digest, six-member ordering, wave/binding cross-validation,
  snapshot-validating run reader, CLI shape, refusal causes, legacy failure, and
  disclosure inventory.
- Confirmed no lifecycle/oracle vocabulary, Batch authority, editorial, or provider
  request changes.
- Proposal/current-wave suite: 18 passed without skips in offline Linux with
  `jsonschema`; the base Windows environment passed 16 with two expected optional
  `jsonschema` skips.
- Provider operations and spend: zero.

## 2026-08-18 — Slice 0 API review accepted

- API accepted the binding-bundle design with one public-reader completion
  condition.
- Added a closed content-bound authority-inputs wrapper returning the exact
  run-specific prepared wave and binding bundle from one snapshot-validating
  operation.
- Froze root reader `read_initial_wave_authority_inputs(run_dir)` and CLI operation
  `--initial-wave-inputs`; validation failure of either document or their join
  returns neither.

## 2026-08-18 — Slice 1 complete

- Added shared binding-bundle construction, strict validation, canonical digest,
  action-identity validation, and prepared-wave cross-validation.
- Exact and bounded fresh interactive preparation now write one root binding bundle
  from the same authoritative complete bindings used for native action preparation.
- The artifact is included in the complete workspace snapshot. Changed bytes fail
  snapshot validation; restored exact bytes validate again.
- Documented the publication protocol without claiming cross-file filesystem
  atomicity. Interrupted pre-snapshot publication exposes no valid checkpoint.
- Combined wave/exact/bounded suite: 139 passed in 289.799 seconds. Final focused
  regression: 5 passed in 4.810 seconds.
- Provider operations and spend: zero.
