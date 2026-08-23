# API Consumer Handoff — SBE 0.4.16

Consume lifecycle v0.6 as two joined facts:

1. `checkpoint_basis` is immutable native/provider custody evidence. Its digest
   commits to route, mechanism, ordered action inventory, provider identities,
   bindings, authority facts, and custody schedule.
2. `temporal_decision` is SBE's deterministic scheduling conclusion for the exact
   `(checkpoint_basis, observed_at)` pair. The API supplies canonical UTC
   `observed_at`; it may invoke only the supported command selected by SBE.

The API must not choose or reconstruct a due-action subset. SBE may select at most
four due retrievals per cycle. Same basis and time is exact replay; later time may
progress not-due to due. Clock regression, due to not-due regression, or any native
identity/authority/custody change under the same basis must be refused.

External-authority request v2 is a reference joined to a validated lifecycle v0.6
inspection. It is not sufficient by itself to reconstruct or authorize actions.
Its digest is stable while only observation time advances; grants become stale when
their bound basis/request changes, not merely because time passed.

Use the public Python surface `inspect_temporal_lifecycle(...)` or the
`astrowoof-lifecycle inspect-temporal` CLI with explicit trusted time. Continue to
use v0.5 only through its existing contract. Fail closed rather than projecting old
inspection versions into v0.6 semantics.

Full details and examples are in the sprint's
`TEMPORAL LIFECYCLE API CONSUMER HANDOFF.md`.

