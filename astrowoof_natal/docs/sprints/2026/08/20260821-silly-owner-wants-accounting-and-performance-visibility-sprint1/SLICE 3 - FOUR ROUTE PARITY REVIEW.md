# Slice 3 — Four-Route Parity Review

Status: implementation complete; API consumer review requested

## Matrix

| Route | Mechanism | Transaction authority | Member evidence |
|---|---|---|---|
| Exact Natal | Response | one pass/attempt action | none |
| Exact Natal | Batch | one Batch-round action | ordered round members |
| Bounded Natal v2 | Response | one pass/attempt action | none |
| Bounded Natal v2 | Batch | one Batch-round action | ordered round members |

The transport changes transaction cardinality; it does not change the accounting
meaning of usage, estimate, settlement, editorial outcome, or native outcome.
Bounded and exact route-specific cohort bytes intentionally differ.

## Consumer decisions requested

1. Confirm one API provider-operation/accounting authority per Batch-round revision,
   never one per member.
2. Confirm member usage remains reported only when provider-supplied; unavailable
   member attribution remains null and is never proportionally invented.
3. Confirm bounded v1 refusal is preferable to retrospective topology inference.
4. Confirm the four-route matrix is sufficient to proceed into timing semantics and
   the later snapshot-valid public export.
