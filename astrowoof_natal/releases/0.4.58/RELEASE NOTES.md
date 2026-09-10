# AstroWoof Natal Authoring 0.4.58

This patch corrects ordinary interactive first-polish authority selection when
whole-deck validation has failed but native state already contains one exact,
live, eligible prepared polish request.

The exception is fail closed. It requires exact agreement among the sole
prepared ledger action, one submitted subject attempt, the current-revision
authorization-request sidecar, route, and binding. Missing, stale,
contradictory, duplicate-attempt, provider-owned, denied, reported, bounded,
batch, or committed-terminal evidence remains in review posture.

There are no public schema, fixture, provider, delivery, API consumer, or Alloy
model changes.
