# Slice 2 — same-checkpoint witness and precedence finding

## Status

Provider-free witness implemented and passing. API review is required before
deciding whether a packaged wrapper is needed.

## Witness

`test_legacy_upgrade_witness_joins_v05_v07_v08_on_one_checkpoint` constructs one
production-shaped exact-interactive workspace with:

- one completed creative-retry provider response whose deterministic fan-in is
  executable;
- one separate creative-retry provider identity whose retrieval is pending and
  not due; and
- no provider transport invocation.

Against that same workspace and observation time, it proves:

1. the released public v0.5 validator accepts the document;
2. the only additional API predicate failure is the empty
   `local_dependencies` count;
3. the released public v0.7 and v0.8 validators accept their documents;
4. run ID, operator revision, snapshot digest, and logical root agree across all
   three versions;
5. v0.8 contains the exact v0.7 local-work inventory;
6. v0.8 retains both provider-custody action identities; and
7. no create, retrieval, mutation, or retained-QA access occurs.

## Precedence refinement discovered by the witness

The pre-Slice 2 expectation that v0.8 must always select reconciliation for any
mixed custody was too broad.

Released v0.8 distinguishes two safe cases:

- **pending custody is due:** SBE selects the bounded reconciliation cycle;
- **pending custody is not due and lineage is consistent:** SBE may select the
  exact deterministic fan-in operation for already completed provider evidence,
  while retaining the other provider custody and permitting no provider create.

The witness reaches the second case and selects:

```text
selected_command     = ordinary_resume
capacity_disposition = continue_local_cycle
eligible_now         = true
local operation      = provider_result_fan_in_and_retry_evaluation
source actions       = completed provider action only
```

This does not violate the provider-custody fence. `ordinary_resume` consumes
already durable provider evidence and performs deterministic native work; it
does not create new provider work. The still-pending provider identity remains
in custody and can only be retrieved through a later SBE-selected reconciliation
cycle.

Lineage conflict is stricter: with retained provider custody, v0.8 permits only
reconciliation and forbids forward dispatch; after custody clears, it selects
typed review.

## API implication

The compatibility adapter should:

- treat v0.8 as the final authority for the mixed-custody case;
- execute an exact advertised local operation when v0.8 selects it;
- preserve the unrelated provider custody and consumer authority;
- never infer that `ordinary_resume` authorizes provider creation; and
- invoke reconciliation only when the v0.8 temporal decision selects the
  run-level reconciliation command.

API should continue to rely on SBE's validators for the action/binding/provider
joins and independently compare only the stable shared identities frozen in
Slice 1.

## Packaging assessment

The runtime readers and validators needed for the witness are already public in
0.4.31. The existing packaged qualifications prove v0.7 progression and v0.8
lineage separately, but no single packaged receipt currently presents this
three-version same-checkpoint witness.

Pause for API review to choose between:

1. consuming the released readers directly in its provider-free fixture; or
2. requesting one additive SBE qualification wrapper/receipt in Slice 3.

No runtime lifecycle correction is indicated by this finding.
