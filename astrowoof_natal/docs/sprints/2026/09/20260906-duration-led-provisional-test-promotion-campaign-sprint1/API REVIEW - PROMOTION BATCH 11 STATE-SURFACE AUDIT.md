# API review — promotion batch 11 state-surface audit

## Decision

Approved to run bounded collision qualification for exactly these seven Batch 11
modules:

- `test_provider_reconciliation_precedes_authority_slice0.py`;
- `test_operator_disposition_cross_route_slice3.py`;
- `test_post_fan_in_retry_contract_slice1.py`;
- `test_native_transition_availability.py`;
- `test_initial_wave_public_contract.py`;
- `test_axis_aware_policy.py`; and
- `test_lifecycle_inspection.py`.

No manifest change is approved at this boundary.

## Review

The seven-module adaptive cohort remains compact (5.034 frozen seconds, 44
tests, two known optional-schema skips), while writes, locks, outputs, and
mutation fixtures are temporary-root/process-local. CLI/log patches restore;
resources and examples are read-only; and no external provider/network/database
or fixed shared-output surface was found.

The Slice 0 provider-reconciliation module may proceed: although its framing
records a prior defect, its active assertions prove the corrected
custody-before-new-authority behavior and do not require unsafe historical work
to occur. Likewise, the retained post-fan-in helper is now ordinary
process-local test support, not an obsolete-characterization dependency.

## Collision gate

Run three repetitions of two independent copies per module in controlled waves
of at most six workers. Require exact per-copy outcomes of 5/0, 4/0, 9/1,
5/1, 9/0, 5/0, and 7/0 tests/skips, with no failure, error, unexpected
outcome, coordinator stderr, or external activity. Pause for a separate
promotion decision afterward.
