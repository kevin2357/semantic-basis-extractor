# API review — promotion batch 11 collision qualification

## Decision

Approved to promote exactly these seven collision-qualified modules from
`provisional` to `parallel_safe`:

- `test_provider_reconciliation_precedes_authority_slice0.py`;
- `test_operator_disposition_cross_route_slice3.py`;
- `test_post_fan_in_retry_contract_slice1.py`;
- `test_native_transition_availability.py`;
- `test_initial_wave_public_contract.py`;
- `test_axis_aware_policy.py`; and
- `test_lifecycle_inspection.py`.

The retained post-fan-in Slice 0 module and every other provisional module are
outside this decision.

## Evidence accepted

Three controlled two-copy repetitions produced 42 clean secret-scrubbed
receipts. The per-copy inventories remained exactly 5/0, 4/0, 9/1, 5/1, 9/0,
5/0, and 7/0 tests/skips. There were no failures, errors, unexpected outcomes,
nonzero child exits, coordinator stderr, persisted failure logs, or external
provider/R2/Render/QA/production activity.

The real assertions remain active: custody-before-new-authority, cross-route
operator classification, consumed-work replay refusal, native-result
availability fences, initial-wave joins, deterministic axis-aware extraction,
and read-only lifecycle inspection.

## Required next boundary

Move only these seven rows, pass the runner and manifest-inventory checks, then
run repeated concurrent actual-manifest `parallel_only` stress. Require exact
matching identity/outcome/manifest digests, complete expected inventory, and
empty stderr. Pause for Batch 11 completion review before selecting Batch 12.
