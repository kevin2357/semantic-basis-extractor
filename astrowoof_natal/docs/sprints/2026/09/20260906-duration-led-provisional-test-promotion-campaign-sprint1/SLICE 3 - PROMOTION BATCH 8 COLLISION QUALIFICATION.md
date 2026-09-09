# Slice 3 — promotion batch 8 collision qualification

## Result

The complete four-module cohort passed the approved bounded collision matrix.
This is evidence for a separate promotion decision; it does not change the live
57/39/36 manifest.

## Matrix

Three repetitions ran two independent copies of every candidate in controlled
waves capped at six simultaneous child workers. All 24 secret-scrubbed worker
receipts passed.

| Module | Exact outcome in every copy | Worker-duration range |
|---|---|---:|
| `test_post_fan_in_retry_runtime_slice2.py` | 5 tests, 0 skips | 3.27–3.53 s |
| `test_payload_recovery_qa.py` | 2 tests, 0 skips | 2.42–2.53 s |
| `test_operator_disposition_packaging_slice4.py` | 4 tests, 0 skips | 2.61–2.82 s |
| `test_lifecycle_consumer.py` | 4 tests, 0 skips | 2.38–2.51 s |

Every copy used the supported provisional-measurement route, an independent
work root, and a separate result receipt. No receipt recorded a failure, error,
skip, expected failure, or unexpected success. The coordinator invocations
returned zero without emitted stderr or persisted failure logs.

Because the real modules ran, the result retains their substantive assertions:

- v0.5/v0.7 post-fan-in selection, exact/bounded behavior, consumed-operation
  history, no-op refusal, pending-custody precedence, and zero provider work;
- payload-recovery refusal, distinct successor authority, exact inert replay,
  preserved refusal history, and zero external network/spend;
- operator-disposition CLI closure, workspace immutability, recovery-default
  disablement, deterministic replay, schema closure, and mutation refusal; and
- lifecycle smoke events, public v0.5 inspection, typed batch denial, command
  result precedence, and terminal reconciliation inspection.

## Next boundary

Pause for the separate promotion decision. If approved, move only these four
modules from `provisional` to `parallel_safe`, run the runner inventory checks,
and then run the repeated concurrent actual-manifest stress proof. No
semantic-closure movement, production/package change, or later provisional
promotion is authorized here.
