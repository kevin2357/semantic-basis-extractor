# Slice 0 — provisional duration inventory

## Decision summary

The campaign has a useful, sharply concentrated optimization target. All 55
provisional modules passed when measured independently under the runner's
sanitized environment and production quiet/unquiet rules. Their isolated
durations total 520.768 seconds; the two slowest modules account for 46.1% of
that time, the first ten account for 80.4%, and 20 modules finish in under one
second.

Duration is only the ordering signal. No module is promoted by this slice.

## Frozen baseline

- framework/source commit: `d9129f6`
- supported default profile: one worker
- final preceding-suite outcome: 1,118 tests, 58 skips, success
- final preceding-suite wall time: 1,122.983334 seconds
- manifest inventory: 38 parallel-safe, 55 provisional, 36 serial-only
- manifest validation: no missing, duplicate, stale, or multiply classified
  test modules

## Measurement method

`run_test_suite.py --measure-weights` now accepts a closed
`--measure-class` and optional repeated `--measure-module`. This times a module
without changing its manifest classification or admitting it to the parallel
path. Unknown, cross-class, and duplicate named selections fail closed.
Protected logging modules retain their unquiet posture; other modules use the
same quiet child harness and secret-scrubbed environment as a supported suite
run.

Each entry below is one isolated child-process measurement. The two dominant
outliers are being repeated because their combined duration makes their noise
material to the first-batch choice.

## Ranked inventory

| Rank | Module | Tests | Skips | Seconds | Cumulative |
|---:|---|---:|---:|---:|---:|
| 1 | `test_bounded_lifecycle.py` | 39 | 0 | 122.434 | 23.5% |
| 2 | `test_waffle_scone_finalization_slice0.py` | 6 | 0 | 117.633 | 46.1% |
| 3 | `test_happy_path_qa_slice4b.py` | 6 | 1 | 44.831 | 54.7% |
| 4 | `test_adversarial_qa.py` | 5 | 0 | 24.845 | 59.5% |
| 5 | `test_legacy_local_work_upgrade_qa.py` | 9 | 1 | 20.393 | 63.4% |
| 6 | `test_post_fan_in_retry_qa_slice4.py` | 10 | 1 | 19.633 | 67.2% |
| 7 | `test_post_fan_in_retry_composed_runtime_slice3.py` | 7 | 0 | 19.516 | 70.9% |
| 8 | `test_optional_stage_completed_evidence_adoption_slice2.py` | 6 | 0 | 17.683 | 74.3% |
| 9 | `test_final_qa_mixed_custody_qa.py` | 4 | 0 | 16.625 | 77.5% |
| 10 | `test_post_fan_in_retry_routing_runtime_slice2.py` | 9 | 0 | 14.857 | 80.4% |
| 11 | `test_external_authority_v2_route_qualification.py` | 3 | 0 | 12.966 | 82.8% |
| 12 | `test_external_authority_qa.py` | 3 | 1 | 9.806 | 84.7% |
| 13 | `test_bounded_product_qa.py` | 7 | 0 | 7.211 | 86.1% |
| 14 | `test_terminal_review_interruption_slice4.py` | 4 | 0 | 5.870 | 87.2% |
| 15 | `test_completed_retry_duplicate_submission_investigation_slice0.py` | 1 | 0 | 5.822 | 88.4% |
| 16 | `test_batch_negative_authorization.py` | 18 | 0 | 5.513 | 89.4% |
| 17 | `test_external_authority_v2_intent_fence.py` | 17 | 0 | 4.919 | 90.4% |
| 18 | `test_sbe_v03.py` | 52 | 0 | 4.656 | 91.3% |
| 19 | `test_negative_authorization.py` | 20 | 0 | 4.649 | 92.1% |
| 20 | `test_operator_retirement_contract.py` | 26 | 2 | 3.637 | 92.8% |
| 21 | `test_post_fan_in_retry_runtime_slice2.py` | 5 | 0 | 3.386 | 93.5% |
| 22 | `test_payload_recovery_qa.py` | 2 | 0 | 3.126 | 94.1% |
| 23 | `test_operator_disposition_packaging_slice4.py` | 4 | 0 | 2.868 | 94.6% |
| 24 | `test_lifecycle_consumer.py` | 4 | 0 | 2.662 | 95.2% |
| 25 | `test_review_required_pending_retries_investigation_slice2.py` | 4 | 0 | 1.691 | 95.5% |
| 26 | `test_spend_enforcement.py` | 18 | 0 | 1.683 | 95.8% |
| 27 | `test_external_authority_empty_inventory_investigation.py` | 13 | 0 | 1.585 | 96.1% |
| 28 | `test_lifecycle_closeout.py` | 10 | 0 | 1.546 | 96.4% |
| 29 | `test_checkpoint_repair.py` | 8 | 0 | 1.419 | 96.7% |
| 30 | `test_external_authority_public.py` | 12 | 0 | 1.257 | 96.9% |
| 31 | `test_post_fan_in_mixed_custody_slice4b.py` | 1 | 0 | 1.194 | 97.1% |
| 32 | `test_post_fan_in_retry_matrix_slice0.py` | 4 | 0 | 1.138 | 97.4% |
| 33 | `test_operator_disposition_reader_slice2.py` | 6 | 0 | 1.043 | 97.6% |
| 34 | `test_post_fan_in_retry_matrix_slice3.py` | 3 | 0 | 1.029 | 97.8% |
| 35 | `test_polish_authority_handoff_qa.py` | 4 | 1 | 1.026 | 98.0% |
| 36 | `test_provider_reconciliation_precedes_authority_slice0.py` | 5 | 0 | 0.779 | 98.1% |
| 37 | `test_operator_disposition_cross_route_slice3.py` | 4 | 0 | 0.756 | 98.3% |
| 38 | `test_post_fan_in_retry_contract_slice1.py` | 9 | 1 | 0.734 | 98.4% |
| 39 | `test_native_transition_availability.py` | 5 | 1 | 0.716 | 98.5% |
| 40 | `test_initial_wave_public_contract.py` | 9 | 0 | 0.700 | 98.7% |
| 41 | `test_axis_aware_policy.py` | 5 | 0 | 0.680 | 98.8% |
| 42 | `test_lifecycle_inspection.py` | 7 | 0 | 0.669 | 98.9% |
| 43 | `test_polish_authority_handoff_slice0.py` | 6 | 0 | 0.584 | 99.0% |
| 44 | `test_basis_policies.py` | 5 | 0 | 0.546 | 99.1% |
| 45 | `test_bounded_provider.py` | 5 | 0 | 0.541 | 99.2% |
| 46 | `test_test_suite_runner.py` | 14 | 0 | 0.525 | 99.4% |
| 47 | `test_external_authority_v2_contract.py` | 6 | 1 | 0.490 | 99.4% |
| 48 | `test_retry_lineage_contract_slice3.py` | 7 | 0 | 0.469 | 99.5% |
| 49 | `test_provider_economics_export.py` | 4 | 0 | 0.437 | 99.6% |
| 50 | `test_external_authority_v2_execution_gap.py` | 2 | 0 | 0.397 | 99.7% |
| 51 | `test_adversarial_runtime_adapter.py` | 4 | 0 | 0.367 | 99.8% |
| 52 | `test_adversarial_oracle.py` | 7 | 0 | 0.331 | 99.8% |
| 53 | `test_provider_dispatch_result_cli.py` | 3 | 0 | 0.320 | 99.9% |
| 54 | `test_bounded_admission.py` | 6 | 0 | 0.287 | 99.9% |
| 55 | `test_route_parity_resources.py` | 5 | 0 | 0.286 | 100.0% |

## Initial Pareto cut and review questions

The first ten modules are the natural 80% review set, but they should not be
promoted as one batch. The first two deserve individual treatment:

- `test_bounded_lifecycle.py` is a broad 39-case lifecycle module with many
  owned temporary workspaces and at least one concurrency surface. Its duration
  is stable enough to justify a careful Slice 1 audit.
- `test_waffle_scone_finalization_slice0.py` is only six tests yet nearly as
  expensive and materially noisier. Its name and origin also suggest a
  production-shaped investigation witness rather than an ordinary unit module;
  Slice 1 must decide whether it is enduring regression evidence, should be
  decomposed, or should remain serial/provisional.

The remaining eight in the Pareto cut are mostly public qualification and
composed-runtime witnesses. Their subprocess/build/temp-artifact ownership
must be mapped before promotion. The 20 sub-second modules are deliberately
deprioritized: even perfect promotion would have little wall-time value.

## Paws-point

Pause before changing isolation or manifest classification. Review should pick
a deliberately small first audit batch from the Pareto cut and confirm whether
one-off investigation witnesses remain appropriate permanent regressions.
