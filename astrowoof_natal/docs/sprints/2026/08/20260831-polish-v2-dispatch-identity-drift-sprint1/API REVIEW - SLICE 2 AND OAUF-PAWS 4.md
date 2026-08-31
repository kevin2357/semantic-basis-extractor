# API review — Slice 2 and Oauf-paws 4

## Decision

**Approved to begin the provider-free two-sequential-v2-action reproduction.**
The causal matrix correctly classifies the defect, and its terminal-evidence
preconditions/refusal precedence preserve the safety properties the API needs.

## Required refinement: retirement timing

The normal lifecycle must retire/archive a live v2 intent in the same
writer-fenced checkpoint that first makes its complete terminal reconciliation
evidence durable. It must not wait for a later successor request to trigger
lazy cleanup.

Why this matters: after every member has exact terminal evidence, retaining the
object in the *live* singleton slot falsely represents provider custody and can
mislead ordinary resume/selection even during an interval with no successor.
The terminal checkpoint should contain the immutable retired-intent record and
no live intent. A successor admission may defensively recognize/repair a
historical pre-retirement workspace only if it can perform the same complete
proof, but that is compatibility handling—not the normal steady-state path.

## Slice 3 proof requirements

Please prove both boundaries through the real public path with scripted
transport:

1. first v2 dispatch checkpoints a live intent before the provider call;
2. completed reconciliation/reporting checkpoints the exact retirement record
   and removes the live slot, with zero second provider call;
3. a later fresh v2 authority creates a separate live intent and exactly one
   successor provider call;
4. replay of either retired authority is `exact_replay` and creates nothing;
5. pending, partial, ambiguous, identity-conflicting, or unjoinable evidence
   keeps the live intent and refuses successor creation.

The predecessor's archived evidence must be sufficient for audit and exact
replay but must never be selected as a live authority. No API-side reservation,
lease, or capacity inference is needed or permitted.
