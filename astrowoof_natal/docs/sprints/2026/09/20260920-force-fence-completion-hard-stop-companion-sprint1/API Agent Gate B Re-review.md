# API Agent Gate B re-review

## Decision

**Approved.** The revised bounded model and deterministic fixture matrix meet
the Gate B requirements for the initial hard-stop completion design.

## Corrections verified

1. `OrdinaryPrecedence` is now an explicit, inhabited non-final/non-quarantine
   disposition. The model cannot reinterpret an ordinary result that wins the
   race as cooperative completion.
2. `ReplacementFinal` now uses `replacementSafeNonwritingAt`, binding finality
   to target/old-boot identity, pre-inventory admission fence,
   retirement/no-overlap, and new-boot readback rather than an arbitrary child
   exit observation.
3. `currentExitAt` excludes a live observation after the selected exit through
   completion. The deliberately weakened earlier-exit/later-live witness is
   SAT while the full-contract assertion is UNSAT.
4. Cooperative evidence now has `lone` result cardinality per exact force
   fence, while receipt and command remain one-to-one with that result.

The resulting five inhabited outcomes and seven bounded UNSAT checks align
with API's provider-free model at `f01a0c1` and its 17 focused cells.

## Non-blocking implementation-strengthening note

Before the model is reused beyond this bounded campaign, add the direct
identity fact `all i: Invocation | lone f: ForceFence | f.target = i` (or its
equivalent). API persistence already enforces a one-fence-per-target posture;
including that fact makes the Alloy vocabulary mirror its idempotency boundary
outside the explicit one-fence runs. It does not alter this Gate B decision.

## Authorization boundary

SBE and API may now enter their approved runtime/schema design slices. This
approval does **not** authorize a provider call, capacity release, workspace or
R2 mutation, deployment, or live run. Each runtime path must retain the exact
proof/identity checks modeled here and receive its own provider-free
qualification.
