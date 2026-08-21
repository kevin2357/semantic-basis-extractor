# External-Authority Empty-Inventory Contract Investigation — Sprint 1 Evidence

Status: Slice 0 complete; awaiting API review

- Provider calls: 0
- Spend: USD 0
- Retained QA workspace access: none
- Runtime/source/schema changes: none
- API/database changes: none
- Release changes: none

Focused tests:

```text
Ran 59 tests in 22.660s
OK (skipped=4)
```

Suites:

- `test_external_authority_public`
- `test_external_authority_contract_proposal`
- `test_initial_wave_lineage_fence`
- `test_lifecycle_contracts`

The four skips are existing JSON Schema checks unavailable in the lean host
interpreter. This evidence establishes a green baseline only; it does not reproduce
the retained QA failure.

Primary analysis: `SBE Agent Pre-Sprint Huddle.md`.

## Slice 0 reproducer

Implementation:

- `tests/test_external_authority_empty_inventory_investigation.py`

Result report:

- `results/SLICE 0 - FAILURE SHAPE RECONNAISSANCE.md`

Proven facts:

- normal exact and bounded inspection paths publish coherent nonempty six-member
  external-authority requests;
- representative inadmissible stored-wave evidence becomes typed refusal;
- API-equivalent predicate checks distinguish all five collapsed conditions;
- native v0.5 validation has gaps for wrong branch reason and non-null
  `not_before`; and
- exact retained-incident predicate remains unknown without its rejected document.

API review: approved in `API Agent Slice 0 Review and Response.md`; API planning
record committed as `4b6a60d`.

## Slice 1 proposal

- `LIFECYCLE EXTERNAL AUTHORITY INVARIANT PROPOSAL.md`
- `results/SLICE 1 - CONTRACT AND DIAGNOSTIC PROPOSAL.md`
- Source/schema/runtime changes: none
- Gate: awaiting joint contract and diagnostic approval

API disposition: approved in `API Agent Slice 1 Review and Response.md`.

## Slice 2 implementation

- Semantic validator:
  `src/astrowoof_natal_authoring/lifecycle_contracts.py`
- Packaged schema:
  `src/astrowoof_natal_authoring/resources/contracts/authoring-lifecycle-contracts.schema.json`
- Investigation/mutation tests:
  `tests/test_external_authority_empty_inventory_investigation.py`
- Schema mutation tests:
  `tests/test_external_authority_contract_proposal.py`
- Result:
  `results/SLICE 2 - NATIVE VALIDATOR AND CLASSIFICATION HARDENING.md`
- Focused tests: 94 passed, 5 skipped because host `jsonschema` is unavailable.
- Python compilation and packaged JSON parsing: passed.
- Provider calls/spend/retained workspace access: 0 / USD 0 / none.

## Slice 3 implementation

- Lifecycle diagnostics:
  `src/astrowoof_natal_authoring/lifecycle.py`
- Shared closed predicate projection:
  `src/astrowoof_natal_authoring/lifecycle_contracts.py`
- Failure-isolation/privacy tests:
  `tests/test_external_authority_empty_inventory_investigation.py`
- Result:
  `results/SLICE 3 - STRUCTURED OBSERVABILITY.md`
- Focused tests: 118 passed, 5 skipped because host `jsonschema` is unavailable.
- Provider calls/spend/retained workspace access: 0 / USD 0 / none.
