# API review — promotion batch 8 state-surface audit

## Decision

Approved to run the bounded Batch 8 collision qualification for exactly:

- `test_post_fan_in_retry_runtime_slice2.py`;
- `test_payload_recovery_qa.py`;
- `test_operator_disposition_packaging_slice4.py`; and
- `test_lifecycle_consumer.py`.

This is collision-test approval only. The manifest remains unchanged pending
clean collision receipts and a separate promotion review.

## Review

The adaptive four-module cohort is appropriately limited: 15 tests and about
12 frozen seconds, while physical contention stays capped at six workers. The
relevant mutable state is either temporary-root owned or process-local:

- post-fan-in retry restores its CLI/output/callback patches and only imports a
  helper with no import-time output or mutation;
- payload recovery's provider-create count is an injected callback assertion,
  with explicit zero-network/zero-spend coverage;
- packaging/replay CLI work uses owned paths and secret-scrubbed children; and
- lifecycle consumer subprocesses likewise inherit the provider-safe scrubbed
  environment and own their complete run roots.

No finding suggests a database, provider, network, repository, fixed-output,
or cross-worker authority surface. Preserve—not bypass—the assertions that
make these tests valuable: v0.5/v0.7 and custody precedence, exact replay and
refusal nonmutation, CLI workspace immutability, batch denial, and terminal
inspection behavior.

## Collision gate

Run three repetitions of two independent copies of each exact module, in
controlled waves of no more than six child workers. Require per-copy exact
inventories of 5, 2, 4, and 4 tests; no skips beyond the frozen expectation;
empty failure/error sets and stderr; and no substantive test changes. Pause
for a separate review before any classification or actual-manifest stress run.
