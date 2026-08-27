# Evidence — Post-Fan-In Retry Ordinary-Resume Authority Routing SBE Sprint 1

## Planning evidence

- Incident background: `Background.md`.
- Analysis: `SBE AGENT PRE-SPRINT HUDDLE.md`.
- Plan: `PLAN.md`.
- Current SBE release observed in incident: 0.4.26.
- Retained QA cohort: suspended and not accessed or mutated by SBE planning.
- External provider/network calls: 0.
- Provider spend: USD 0.
- Runtime/source/schema changes: none.

## Slice 0 evidence

- Findings: `SLICE 0 - INCIDENT REPRODUCTION AND CAUSAL FINDINGS.md`.
- Public runtime characterization:
  `tests/test_post_fan_in_retry_authority_routing_slice0.py`.
- Existing selector characterization retained:
  `tests/test_post_fan_in_retry_matrix_slice0.py`.
- Focused command:
  `python -m unittest astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 -v`.
- Result: 7 passed.
- Production source/schema changes: none.
- Retained QA access/mutation: none.
- External provider/network calls: 0.
- Provider create/retrieval calls: 0.
- Spend: USD 0.

- API review: `API SLICE 0 REVIEW.md`.
- API disposition: approved to begin Slice 1.

Status: Slice 0 approved; Slice 1 ready to begin.

## Slice 1 evidence

- Normative contract: `POST-FAN-IN ROUTING CONTRACT AND DECISION MATRIX.md`.
- Closed fixture:
  `fixtures/post-fan-in-authority-routing-matrix.v1.json`.
- Contract validator/mutation coverage:
  `tests/test_post_fan_in_authority_routing_contract_slice1.py`.
- Focused command:
  `python -m unittest astrowoof_natal.tests.test_post_fan_in_authority_routing_contract_slice1 astrowoof_natal.tests.test_post_fan_in_retry_authority_routing_slice0 astrowoof_natal.tests.test_post_fan_in_retry_contract_slice1 astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice3`.
- Result: 19 passed; 1 expected optional-schema skip.
- Runtime/source/schema changes: none.
- External provider/network calls: 0.
- Retained QA access/mutation: none.
- Spend: USD 0.

Status: Slice 1 complete; API contract review required before Slice 2.

- API review: `API SLICE 1 REVIEW.md`.
- API disposition: approved for Slice 2 runtime implementation.

## Slice 2 evidence

- Runtime source:
  - `src/astrowoof_natal_authoring/initial_wave.py`
  - `src/astrowoof_natal_authoring/closure.py`
  - `src/astrowoof_natal_authoring/bounded_lifecycle.py`
- Runtime tests:
  - `tests/test_post_fan_in_retry_authority_routing_slice0.py`
  - `tests/test_post_fan_in_retry_routing_runtime_slice2.py`
- Focused route/contract/post-fan-in result: 24 passed.
- Wider initial-wave/external-authority/bounded result: 77 passed.
- External provider/network calls: 0.
- Retained QA access/mutation: none.
- Spend: USD 0.

Status: Slice 2 complete; Slice 3 in progress.

## Slice 3 evidence

- Composed qualification:
  `tests/test_post_fan_in_retry_composed_runtime_slice3.py`.
- Narrative evidence:
  `SLICE 3 - COMPOSED RUNTIME AND FAILURE QUALIFICATION.md`.
- Focused composed/route/failure result: 44 passed.
- Prior wider initial-wave/external-authority/bounded result: 77 passed.
- External provider/network calls: 0.
- Scripted local exact-path retrievals: 1.
- Scripted local exact-path creates: 1.
- Duplicate creates on replay: 0.
- Retained QA access/mutation: none.
- Spend: USD 0.

Status: Slice 3 complete; API review required before Slice 4.

- API review: `API SLICE 3 REVIEW.md`.
- Independent focused result: 19 passed; 1 expected optional-schema skip.
- API disposition: approved for Slice 4 with a required public, provider-free,
  installed-wheel post-fan-in fixture and stable receipt identity.

Status: Slice 3 approved; Slice 4 may begin.

## Slice 4 SBE evidence

- Public fixture:
  `src/astrowoof_natal_authoring/resources/fixtures/post-fan-in-retry-routing.v1.json`.
- Closed receipt schema:
  `src/astrowoof_natal_authoring/resources/contracts/post-fan-in-retry-qualification.v1.schema.json`.
- Public runner/reader/validator:
  `src/astrowoof_natal_authoring/post_fan_in_retry_qa.py`.
- CLI: `astrowoof-post-fan-in-retry-qa`.
- Tests: `tests/test_post_fan_in_retry_qa_slice4.py`.
- Focused result: 5 passed; 1 expected optional-`jsonschema` skip.
- Combined Slice 1–4 result: 25 passed; 1 expected optional-schema skip.
- Scripted local retrievals: 1.
- Scripted local creates: 1.
- Duplicate creates: 0.
- External network/provider calls: 0.
- Spend: USD 0.
- Retained-QA access/mutation: none.

Status: SBE Slice 4 component complete; API joined-campaign review pending.

- API review: `API SLICE 4 REVIEW.md`.
- Reproducibility defect: confirmed and corrected.
- Reproducibility assertion: two independent disposable workspaces produce equal
  phase evidence, endpoint evidence, receipt identity, and receipt value.
- Corrected focused result: 6 passed; 1 expected optional-schema skip.
- Corrected combined result: 26 passed; 1 expected optional-schema skip.

Status: Slice 4 correction complete; API re-review pending.

- API re-review: `API SLICE 4 RE-REVIEW.md`.
- Independent result: receipt, phase evidence, and endpoint evidence reproduce
  exactly across fresh workspaces.
- Disposition: approved for installed-wheel qualification.

Status: Slice 4 approved; Slice 5 in progress.
