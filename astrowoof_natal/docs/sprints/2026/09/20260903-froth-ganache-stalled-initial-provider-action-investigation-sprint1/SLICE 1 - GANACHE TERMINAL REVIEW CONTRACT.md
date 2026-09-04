# Slice 1 — Ganache terminal-review contract

**Status:** proposed contract freeze; runtime implementation has not started.

## Scope

This is a narrow exact-interactive reconciliation boundary for a deterministic
`AssemblyContractError` that occurs only after SBE has adopted the exact
completed provider evidence and all native provider custody is final. It does
not change Froth, initial-wave admission, Batch, bounded routing, generic
exception handling, or API-owned scheduling.

## Trigger

The bridge applies only when all of these are true under the reconciliation
writer fence:

1. The selected provider response has already been retrieved and its exact
   identity and binding have been accepted into the corresponding native
   action/pass truth.
2. Every action disposition is terminally accounted for: no action remains
   provider-pending, provider-custodied, ambiguous, providerless-unresolved,
   or locally runnable.
3. The final deterministic native assembly step raises `AssemblyContractError`.

The bridge must not convert a transport, provider, snapshot, integrity, or
arbitrary reconciliation exception into a terminal-review result. A remaining
provider-custody item also prevents sealing: reconciliation remains the
selected path until the custody is resolved.

## Native result and invocation outcome

Reuse the existing public terminal-review contracts; no new schema version is
needed.

- Persist the existing `FAILED_REQUIRES_REVIEW` terminal transition under the
  writer, with terminal outcome `review_required` and closed cause
  `finalization_contract_invalid`.
- Publish `astrowoof.native_execution_result.v0.2` with
  `command_kind=provider_reconciliation`, the invocation identity, the exact
  pre-checkpoint snapshot identity, complete action dispositions/inventory,
  and final custody closure.
- Publish the existing native receipt. Its digest-bound post-transition
  snapshot identity, result identity, receipt identity, and invocation join
  provide the required post-checkpoint binding.
- Return the existing invocation-bound
  `astrowoof.terminal_review_command_result.v0.1` envelope, then exit 2.
  The envelope's sealed result/receipt identifiers and hashes are authoritative
  for API ingestion; API must consume it before interpreting the exit status.

`review_required` is deliberate, not an inferred terminal-failure label. It
means native editorial/finalization review is required after native custody is
closed. API still owns settlement, delivery, resource release, and its own job
terminalization policy.

## Refusal and replay posture

- A non-final action inventory remains on the ordinary reconciliation path;
  this bridge publishes nothing and performs no extra provider operation.
- An exception outside the exact deterministic `AssemblyContractError` trigger
  retains its existing failure behavior; this patch is not a catch-all error
  translator.
- Once sealed, an exact replay must return the same immutable result/receipt
  join and cannot create, submit, retrieve, or revive generic retry work.
- A later action must originate from a new lawful native/API decision, never
  from mutating the sealed invocation.

## Provider-free qualification matrix

| Case | Expected evidence |
| --- | --- |
| Completed adopted final action + deterministic assembly error | v0.2 `review_required` result, `finalization_contract_invalid`, receipt and command envelope; no transport call or provider create |
| Same sealed invocation replay | exact immutable result/receipt; no transport call or generic retry publication |
| A second unresolved provider-custody action | no terminal seal; reconciliation custody remains selected |
| Non-assembly exception | no conversion to `finalization_contract_invalid` |
| Rehashed/mismatched action or receipt join | closed validation refusal, not a terminal result |

The positive fixture begins with complete provider evidence already adopted, so
the terminal-failure/seal interval itself is provider-free. A later public
reconciliation fixture may separately prove adoption, but must not obscure this
no-new-I/O contract.

## Existing-suite observation

Before Slice 2 source work, the focused terminal-review set produced 32 passes,
two expected optional-schema skips, and one unrelated expectation mismatch:
`test_custody_successor_preserves_and_orders_review_lineage` expects a later
mixed-custody successor to remain `review_required`, while the current reducer
correctly reports `provider_pending` when provider custody remains. No runtime
source was changed for this sprint before that observation. Slice 2 should
either revise that fixture to its custody-precedence meaning or isolate it from
this narrow terminal-seal qualification.
