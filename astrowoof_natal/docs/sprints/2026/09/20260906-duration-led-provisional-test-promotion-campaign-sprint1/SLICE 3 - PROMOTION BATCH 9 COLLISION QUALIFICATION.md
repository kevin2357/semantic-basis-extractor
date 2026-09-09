# Slice 3 — promotion batch 9 collision qualification

## Result

The complete five-module cohort passed the approved bounded collision matrix.
This is evidence for a separate promotion decision; it does not change the live
61/35/36 manifest.

## Matrix

Three repetitions ran two independent copies of every candidate in controlled
waves capped at six simultaneous child workers. All 30 secret-scrubbed worker
receipts passed.

| Module | Exact outcome in every copy | Worker-duration range |
|---|---|---:|
| `test_review_required_pending_retries_investigation_slice2.py` | 4 tests, 0 skips | 2.12–2.36 s |
| `test_spend_enforcement.py` | 18 tests, 0 skips | 1.67–1.94 s |
| `test_external_authority_empty_inventory_investigation.py` | 13 tests, 0 skips | 1.60–1.74 s |
| `test_lifecycle_closeout.py` | 10 tests, 0 skips | 1.67–1.72 s |
| `test_checkpoint_repair.py` | 8 tests, 0 skips | 1.42–1.55 s |

Every copy used the supported provisional-measurement route, an independent
work root, and a separate result receipt. No receipt recorded a failure, error,
skip, expected failure, or unexpected success. Coordinator invocations returned
zero without emitted stderr or persisted failure logs.

The real modules therefore retained their substantive coverage: exact retry
reuse and custody precedence; spend authorization, ambiguity, and doubled
provider-call ordering; closed authority/refusal predicates and diagnostic
non-authority; durable closeout and interruption recovery; and exact,
backup-gated checkpoint repair.

## Next boundary

Pause for the separate promotion decision. If approved, move only these five
modules from `provisional` to `parallel_safe`, run the runner inventory checks,
and then run the repeated concurrent actual-manifest stress proof. No
semantic-closure movement, production/package change, or later provisional
promotion is authorized here.
