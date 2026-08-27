# API Slice 3 Review — Native Progress and Safety Oracle

## Assessment

The Slice 3 structure is sound and is ready to remain the native-side oracle
foundation: classification is derived rather than trusted from fixture labels;
stutter and recurrence are history-sensitive; contradictory evidence remains
distinct from a valid refusal; and the two digest roles correctly separate exact
stale-authority fencing from semantic progress.  In particular, a checkpoint or
snapshot rewrite must remain able to invalidate stale authority without being
mistaken for useful lifecycle progress.

One correction is required before claiming the current provider-create rule proves
the plan's **create-at-most-once by action/binding** invariant.

## Required correction: bind provider observations to one action inventory member

`provider_fixture.operations` presently contains only opaque correlation IDs and
states.  `adversarial_safety_violations()` consequently treats *any* prior durable
provider identity plus *any* subsequent scripted create as
`provider_identity_recreated`.

That is too broad for the supported initial wave and reconciliation topology.  A
normal 4+2 sequence may retain four known/completed provider members while lawfully
creating the other two distinct, still-unentered action bindings.  The current rule
would call that expected progression a duplicate.

Please either:

1. extend the closed redacted public trace shape so every operation and scripted
   create/retrieval is joined to one ordered opaque action/binding identity (for
   example an opaque action ref plus a binding digest); then enforce at-most-once
   only per identical action/binding; or
2. narrow the v1 claim and remove this global rule until that join is publicly
   expressible.

The first option is preferable: it enables a genuine create-once check without
exposing provider IDs, prompts, packets, or private workspace facts.  It should
also make the planned 4+2 route/adversarial traces precise rather than relying on a
global provider-state heuristic.

## Approval condition

With that action/binding join (or an explicitly narrowed claim), I approve the
native progress/fingerprint approach and SBE may proceed to Slice 4.  No API code,
provider work, retained-QA recovery, deployment, or release is requested by this
review.
