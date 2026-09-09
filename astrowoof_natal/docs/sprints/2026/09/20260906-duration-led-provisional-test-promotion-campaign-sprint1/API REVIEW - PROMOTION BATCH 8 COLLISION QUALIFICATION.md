# API review — promotion batch 8 collision qualification

## Decision

Approved to promote exactly these four modules from `provisional` to
`parallel_safe`:

- `test_post_fan_in_retry_runtime_slice2.py`;
- `test_payload_recovery_qa.py`;
- `test_operator_disposition_packaging_slice4.py`; and
- `test_lifecycle_consumer.py`.

This decision is restricted to those classification changes and their normal
runner/inventory checks. It does not authorize a later provisional cohort,
semantic-closure movement, product/package work, or a broad speed claim.

## Evidence accepted

The approved matrix completed three repetitions of two independent copies per
candidate, in controlled waves of at most six workers: all 24 receipts passed
with no failure, error, skip, expected failure, unexpected success, stderr, or
persisted failure log. Each copy retained its exact inventory:

| Module | Tests / skips |
|---|---:|
| `test_post_fan_in_retry_runtime_slice2.py` | 5 / 0 |
| `test_payload_recovery_qa.py` | 2 / 0 |
| `test_operator_disposition_packaging_slice4.py` | 4 / 0 |
| `test_lifecycle_consumer.py` | 4 / 0 |

The real assertions remained active: post-fan-in custody and no-provider-work
precedence; recovery's refusal/replay/no-spend behavior; operator CLI
nonmutation and deterministic replay; and lifecycle's public inspection,
batch-denial, and terminal-reconciliation coverage.

## Required next boundary

After moving only those four entries, run manifest/inventory regressions and
the repeated concurrent actual-manifest `parallel_only` stress proof. Require
matching test, outcome, and manifest digests; complete expected inventory; and
empty stderr in every receipt. Pause for Batch 8 completion review before
selecting Batch 9.
