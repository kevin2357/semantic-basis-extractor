# Background — duration-led provisional test promotion campaign Sprint 2

## Inherited context

This sprint continues the campaign closed at Batch 11 in
`../20260906-duration-led-provisional-test-promotion-campaign-sprint1/`.
The split creates a clean checkpoint while an editorial-review packet release
is being developed concurrently in the same working tree.

Sprint 1 established the deterministic manifest runner and promotion evidence
path. Its final live manifest is:

- 78 `parallel_safe` modules;
- 18 `provisional` modules; and
- 36 `serial_only` modules.

Batch 11's paired actual-manifest proof passed 625 tests with 49 expected skips
and exact matching test, outcome, and manifest digests. No Batch 12 work was
started.

## Inherited provisional tail

- `test_test_suite_runner.py`
- `test_adversarial_oracle.py`
- `test_adversarial_runtime_adapter.py`
- `test_basis_policies.py`
- `test_bounded_admission.py`
- `test_bounded_provider.py`
- `test_editorial_review_contract_foundation.py`
- `test_editorial_review_contract_fixtures.py`
- `test_editorial_review_contract_qualification.py`
- `test_editorial_review_runtime.py`
- `test_external_authority_v2_contract.py`
- `test_external_authority_v2_execution_gap.py`
- `test_polish_authority_handoff_slice0.py`
- `test_post_fan_in_retry_matrix_slice0.py`
- `test_provider_dispatch_result_cli.py`
- `test_provider_economics_export.py`
- `test_retry_lineage_contract_slice3.py`
- `test_route_parity_resources.py`

The four editorial-review modules are a moving test family until their owning
sprint freezes them. They must remain provisional during that work and then be
audited coherently as one family.

## Governing boundary

Duration prioritizes review but never proves isolation. Every future promotion
still requires an explicit state-surface audit, bounded collision evidence,
separate promotion approval, manifest guards, and repeated actual-manifest
stress proof. Package behavior, provider activity, external systems, and release
authority remain out of scope unless separately authorized.
