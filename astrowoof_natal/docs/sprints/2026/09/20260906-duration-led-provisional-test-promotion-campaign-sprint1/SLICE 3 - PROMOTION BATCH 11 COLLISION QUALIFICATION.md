# Slice 3 — promotion batch 11 collision qualification

## Collision result

The seven review-approved modules passed the bounded collision matrix. Three
repetitions ran two independent copies of every candidate in controlled waves
capped at six simultaneous child workers. All 42 secret-scrubbed receipts
passed.

| Module | Exact outcome in every copy | Worker-duration range |
|---|---|---:|
| `test_provider_reconciliation_precedes_authority_slice0.py` | 5 tests, 0 skips | 0.92–1.12 s |
| `test_operator_disposition_cross_route_slice3.py` | 4 tests, 0 skips | 0.79–0.95 s |
| `test_post_fan_in_retry_contract_slice1.py` | 9 tests, 1 optional-schema skip | 0.83–1.03 s |
| `test_native_transition_availability.py` | 5 tests, 1 optional-schema skip | 0.65–0.83 s |
| `test_initial_wave_public_contract.py` | 9 tests, 0 skips | 0.49–0.59 s |
| `test_axis_aware_policy.py` | 5 tests, 0 skips | 0.75–0.96 s |
| `test_lifecycle_inspection.py` | 7 tests, 0 skips | 0.57–0.80 s |

No receipt recorded a failure, error, unexpected skip, expected failure, or
unexpected success. Every child process exited zero. Coordinator stderr was
empty in every copy, and no persisted failure log was produced.

The real tests preserved provider-custody precedence, cross-route operator
classification, consumed-work replay refusal, native-result availability
fences, initial-wave public joins, deterministic axis-aware extraction, and
read-only lifecycle inspection. No provider, R2, Render, QA, production,
package, or release activity occurred.

## Next boundary

Pause for the separate promotion decision. If approved, move only these seven
collision-qualified modules from `provisional` to `parallel_safe`, run the
manifest/inventory guards, and execute the repeated concurrent actual-manifest
stress proof. The retained post-fan-in Slice 0 module and every other remaining
provisional module stay outside this approval.
