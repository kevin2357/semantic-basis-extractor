# API Voof-paws 2 Review — Slice 1 and Slice 2 Contract

Status: Slice 1 approved; Slice 2 contract approved for implementation.

## Slice 1

Approved. The regression proves the actual Waffle-shaped public resume now
reaches `DELIVERY_COMPLETE`, not merely that the former assembly exception is
absent. The coverage/mirroring fixture and unknown-assignment control also
preserve the intended distinction: distribution policy is advisory, while
structural registry and assignment joins remain hard.

No API intake or authority change is required for this policy correction.

## Slice 2 disposition contract

API approves the narrow `AssemblyContractError` approach and the proposed
sealed v0.2 result:

```text
outcome: review_required
cause_code: finalization_contract_invalid
custody_finality: final
new_provider_create_permitted: false
```

The existing API v0.2 terminal-review ingress already supports a closed cause
code with a final custody inventory, provided the publication carries the exact
full action-disposition inventory and its digest, the invocation/result/receipt
bindings validate, and the command is `ordinary_authoring` (or the existing
supported reconciliation command when applicable).

For this cause, API mapping is:

- terminal native review, not retryable dependency failure;
- exact invocation-returned terminal-review command envelope is the primary
  authority for ingress;
- exact sealed result-ID lookup is recovery-only if that envelope was not
  returned; and
- final action custody permits normal terminal closeout, subject to the
  existing API joins and single-writer transaction.

## Required implementation boundaries

1. Catch only the new deterministic native error at the finalization
   coordinator. Do not broaden this into `except ValueError` or process-error
   classification.
2. Emit the sealed native result and its receipt before exit 2. The process
   exit is transport information only; it is not authority for the API mapping.
3. Keep operational `CalledProcessError`, timeout, filesystem, interruption,
   and provider faults untyped unless they independently publish valid native
   evidence. They retain their current conservative behavior.
4. Preserve priority for live provider custody or ambiguity. A native result
   claiming `custody_finality: final` must prove it across every action row.
5. Add an API-shaped consumer fixture in the handoff evidence: a valid sealed
   `finalization_contract_invalid` publication must be accepted by current
   strict API ingress without an API schema relaxation.

With these boundaries, SBE may implement Slice 2 and continue into its runtime
and qualification slices. An API patch is not assumed yet; we will verify the
actual command-envelope handoff against the installed SBE artifact before
calling it unnecessary.
