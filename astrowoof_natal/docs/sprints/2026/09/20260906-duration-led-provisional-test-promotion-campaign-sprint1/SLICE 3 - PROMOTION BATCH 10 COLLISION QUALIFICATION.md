# Slice 3 — promotion batch 10 collision qualification

## Historical witness disposition

The obsolete method
`test_ordinary_retry_cycle_can_republish_same_decision_without_progress` was
removed from routine discovery and preserved verbatim as a non-discoverable
`.py.txt` forensic artifact beside the original 2026-08-25 incident evidence.

The active `test_post_fan_in_retry_matrix_slice0.py` module retains `_workspace`
and its three compatibility/precedence regressions. Those three tests pass
directly after extraction. Characterization-only imports were removed. The
module remains provisional and was not included in the Batch 10 collision
evidence.

The archive points explicitly to current v0.7 regressions proving no-op refusal
and append-only consumed-operation history.

## Collision result

The five review-approved modules passed the bounded collision matrix. Three
repetitions ran two independent copies of every candidate in controlled waves
capped at six simultaneous child workers. All 30 secret-scrubbed receipts
passed.

| Module | Exact outcome in every copy | Worker-duration range |
|---|---|---:|
| `test_external_authority_public.py` | 12 tests, 0 skips | 1.34–1.40 s |
| `test_post_fan_in_mixed_custody_slice4b.py` | 1 test, 0 skips | 1.13–1.21 s |
| `test_operator_disposition_reader_slice2.py` | 6 tests, 0 skips | 0.95–0.99 s |
| `test_post_fan_in_retry_matrix_slice3.py` | 3 tests, 0 skips | 0.96–1.06 s |
| `test_polish_authority_handoff_qa.py` | 4 tests, 1 optional-schema skip | 0.90–1.00 s |

No receipt recorded a failure, error, unexpected skip, expected failure, or
unexpected success. Coordinator invocations returned zero without emitted
stderr or persisted failure logs. The real tests preserved snapshot and
binding fences, mixed-custody precedence, nonmutating exact-result assessment,
the closed post-fan-in matrix, and provider-free polish authority qualification.

## Next boundary

Pause for the separate promotion decision. If approved, move only these five
collision-qualified modules to `parallel_safe`, run manifest/inventory guards,
and execute the repeated concurrent actual-manifest stress proof. The retained
three-test Slice 0 module requires a fresh audit/collision decision if later
promotion is desired.
