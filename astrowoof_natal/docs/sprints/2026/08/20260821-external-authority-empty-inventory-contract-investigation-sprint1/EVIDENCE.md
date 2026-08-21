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
