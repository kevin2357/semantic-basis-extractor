# Plan — force-fence peer resumption contract investigation

## Status

**Active — read-only companion.** This sprint first distinguishes a peer that
is due in the queue from one that is admissible under the deployed active-SBE
capacity policy. API owns any scheduler or operator-policy follow-up; SBE's
role is to determine whether its lifecycle/readiness contract contributed.

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

## Slice 2 — paired classification gate

Review API Slice 0 alongside this sprint and jointly classify the cause as:

- API scheduling/claim behavior;
- an SBE/API handoff gap;
- intended scarce-capacity containment with an incorrectly stated
  peer-isolation expectation; or
- another explicit policy outcome.

Use Q3A-003 as the single-slot containment positive control where relevant.
Do not start runtime/schema work before that gate.
