# API Agent Gate B Review

## Decision

**Revision requested before Gate B approval.** The model is a strong and very
useful bounded design artifact: it correctly separates scheduling allocation
from retained custody, requires API-parent evidence in addition to a
cooperative SBE handoff, models the replacement/collateral boundary, and
retains the peer/global-budget distinction. Its intended direction is aligned
with API's provider-free model (`f01a0c1`).

Three small but material relational corrections are needed so the Alloy
artifact actually proves the stated safety rules rather than an approximation.

## Required corrections

### B1 — Make ordinary-result precedence inhabitable

`FullContract` requires exactly one `Completion` per `ForceFence`, but
`CompletionClassification` gives no possible `CompletionKind` to a completion
that carries `ordinary`. `CooperativeFinal`, `ParentFinal`, and
`ReplacementFinal` each require `no c.ordinary`; `Escalating` does as well.
Consequently the stated “ordinary lifecycle wins” cell cannot be an inhabited
world under `FullContract`.

Choose either:

1. add an explicit `OrdinaryPrecedence` completion/disposition kind that is
   non-final and non-quarantine; or
2. allow a force fence to have no completion while ordinary lifecycle owns the
   prior ordinary result.

Then add an explicit inhabited ordinary-precedence run and a check that it
cannot become cooperative/quarantine completion.

### B2 — Treat platform replacement as its own non-writing proof

`ReplacementFinal` currently also requires `childExitedAt[target, c.at]`.
That is correct for the cooperative and API-parent proof classes, but it
silently makes a separate child-observation record mandatory for the platform
replacement class. The approved replacement proof is instead target/old-boot
binding, no-new-child admission fence, complete collateral inventory/recovery,
old-worker retirement/no-overlap, and new-boot readback.

Model a shared `safeNonwritingAt` predicate whose alternatives are explicit:

- cooperative/parent finals require exact parent-bound exit of the original
  invocation/process group; and
- replacement final requires its complete platform retirement/no-overlap proof
  for the target's old boot.

Do not let an arbitrary, otherwise unbound `ChildObservation` become the
authority that finishes a replacement.

### B3 — Forbid a later-live child after a claimed exit

`childExitedAt` currently means “some `ChildExited` observation occurred at or
before the completion moment.” It permits another `ChildLive` observation for
the same invocation at that moment or later. The model needs a current/
monotonic exit condition (for example: an exit observation exists and no live
observation exists at or after it through the completion), or an explicit
single-child lifecycle ordering fact.

Add a deliberately weakened witness for “earlier exit plus later live child
still releases allocation,” and require the full contract to reject it.

## Additional bounded-cardinality refinement

The prose says the existing SBE v1 handoff publishes one indexed
result/receipt/command for the exact request. Add the relevant per-fence or
per-invocation cardinality (`lone` / exact one where its route applies), so the
model cannot accept two distinct cooperative results for one request merely
because one happens to be selected for `Completion`.

## What is already approved in direction

- no silence/timeout/unsupported SBE release;
- reconciliation’s pre-GET and durable post-response-checkpoint cells;
- cooperative evidence plus API-parent exit, rather than SBE evidence alone;
- parent-only exact exit as a separate final proof class;
- target-scoped / worker-scoped platform replacement with no-new-child fence,
  collateral handling, old-boot exclusion, and new-boot readback;
- retained provider/spend/workspace/native custody distinct from scheduling;
  and
- peer admission only after a final target completion and absent an independent
  peer global-budget block.

After B1–B3 and the cardinality refinement, API expects to approve Gate B and
continue into the non-runtime API completion/disposition design.
