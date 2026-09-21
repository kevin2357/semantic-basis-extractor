# Plan — force-fence peer resumption contract investigation

## Status

**Closed — 2026-09-20.** The witnesses exercised only the durable emergency
force-fence primitive, which intentionally retains the active allocation and
does not attempt native suspension, final quarantine, or capacity release.
They are therefore not evidence of an SBE readiness/resumption gap or an API
queue defect. The required product follow-up is a separately scoped,
route-capable transition from active containment to either completed
`operator_quarantined`/released capacity or an explicit unresolved state.

## Slice 0 — exact per-witness SBE chronology

- Read the retained Better Stack worker records for Q5-003 and Mergenthaler.
- Map selected branch, provider-local dependency changes, readiness, capacity
  disposition, reconciliation/fan-in, and the last ordinary SBE event.
- Join each peer's `retry_wait`/due posture to the concurrent active-SBE slot
  inventory and deployed slot limit. Treat **queue due** and **capacity
  admissible** as separate predicates.
- State what SBE had emitted before each peer became/continued `retry_wait`,
  without assuming that a due peer should have been claimable.

**Exit:** one evidence-backed SBE chronology per witness, including whether
the peer was merely queue due or also capacity admissible, with no claim about
API mutation authority.

## Slice 1 — API-consumable contract mapping

- Map each observed SBE event/field to the declared API-facing handoff or
  scheduling meaning.
- Identify any omitted, contradictory, or insufficiently durable signal that
  could prevent ordinary API resumption.

**Exit:** either SBE signal compatibility or one narrow SBE/API ambiguity.

**Disposition:** closed by the Slice 0 evidence and source/contract review.
The peer had already received SBE's explicit local-continuation handoff. The
fenced target's route was deliberately outside the activated cooperative
resolution path, and the Q5 oracle expressly prohibited that path.

## Slice 2 — paired classification gate

Review API Slice 0 alongside this sprint and jointly classify the cause as:

- API scheduling/claim behavior;
- an SBE/API handoff gap;
- intended scarce-capacity containment with an incorrectly stated
  peer-isolation expectation; or
- another explicit policy outcome.

Use Q3A-003 as the single-slot containment positive control where relevant.
Do not start runtime/schema work before that gate.

**Disposition:** closed. The correct classification is intended
scarce-capacity containment under a deliberately durable-only test, paired
with an incomplete end-to-end product route for an actively fenced
reconciliation run. No SBE package or source change is indicated here.
