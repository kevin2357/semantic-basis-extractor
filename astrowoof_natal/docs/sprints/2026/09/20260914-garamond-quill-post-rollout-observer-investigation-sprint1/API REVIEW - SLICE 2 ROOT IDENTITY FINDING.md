# API Review — Slice 2 Root Identity Finding

## Decision

Approved. The two independent exact-workspace reproductions establish an
API-owned workspace-root identity defect.

The decisive property is the paired control: the same verified archive bytes
fail before evidence collection when mounted at API's supplied checkpoint/root
identity, while they each produce one packet, eight projections, and nine
artifacts when mounted at the native durable root. This rules out a native
reader, capture builder, packet, projection, artifact, or HTTP-transport
defect as the first failure.

SBE's strict root validation is correct and must remain fail-closed. Do not
weaken it or add a native-side root-discovery fallback.

## API correction fence

API should open/continue an API-owned implementation slice that:

1. Audits every SBE checkpoint publication and observer preparation path for
   the synthetic API run-label root versus the actual native durable root.
2. Persists/carries one exact native logical workspace root bound to the
   checkpoint and result used by the observer; it may not use a latest-workspace
   lookup or reconstruct an alternate root from a run ID.
3. Supplies that exact identity into the observer after both the initial
   terminal delivery and the carried-forward delivery-validation retry.
4. Adds provider-free regressions for the wrong-root refusal, exact-root
   success, retry carry-forward, and invariant that observation failure cannot
   affect authoritative terminal state, custody, spend, or cleanup.

No SBE runtime, package, schema, or Alloy change is requested. API should stop
for its own implementation/release review before modifying deployed code.
