# API Voof-paws 4 re-review — approved v0.8 contract freeze

## Decision

**Approved: SBE may begin Slice 4 runtime mutation.**

The prior two contract-completeness conditions are satisfied:

1. `validate_lifecycle_inspection_v08()` now invokes an exact retry-lineage to
   checkpoint action-inventory join. Every checkpoint creative-retry action is
   represented once; fabricated/missing action IDs and mismatched provider IDs
   fail closed. Custodial retry entries additionally join the exact custody
   provider identity. The selected due subset remains validated by the prior
   lifecycle contract and remains entirely SBE-selected.
2. The complete lifecycle v0.8 surface is packaged through
   `temporal-lifecycle-contracts.v3.schema.json`,
   `read_lifecycle_inspection_v08_schema()`,
   `validate_lifecycle_inspection_v08()`, and the validated public mixed-custody
   fixture. The retry-lineage resource is linked as a public sub-schema rather
   than asking API to recreate the extension from source.

The added `retry_lineage_conflict_requires_review` classification is a proper
closed machine-readable explanation for the post-custody non-dispatching path.
API will consume it as public evidence; it will not derive the cause from a
state label.

## Verification performed

Ran provider-free focused contract coverage:

```text
python -B -m unittest astrowoof_natal.tests.test_retry_lineage_contract_slice3
Ran 7 tests ... OK
```

No API/provider/R2/queue/deployment activity occurred during this re-review.

## API follow-through

API Sprint 56 Slice 2 may now implement strict v0.8 intake against the
packaged reader/validator. It must keep contradictory input on a typed contract
path before queue failure or capacity release, and only SBE's selected command
may run native work.
