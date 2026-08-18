# SBE 0.4.4 API Consumer Handoff

Require lifecycle inspection v0.3 for capacity decisions. Validate its native
`route_family`, `provider_mechanism`, operation binding, checkpoint, and timing;
do not infer those identities from the API job record.

Supported combinations are exact Natal Responses, exact Natal Batch, and bounded-
Natal Responses. Bounded Batch remains rejected. Invoke the public
`reconcile_authoring_provider_cycle()` function or the neutral
`--provider-reconciliation-cycle --observed-at` CLI only for an existing run with
durable provider identity.

Release a short worker claim only when the closed capacity disposition and
`checkpoint_safe_for_worker_release` permit it. Retain API authority for each exact
action classified `retain_consumer_authority`. A terminal Batch with unavailable
usage can end provider polling while billing reconciliation or integrity review
authority remains retained; unavailable usage is not `$0.00`.

The complete route matrix, result mapping, recovery rules, compatibility behavior,
and adoption checklist are in:

- `docs/post_extraction_authoring/Provider Reconciliation Route Parity Handoff.md`;
- `docs/post_extraction_authoring/Authoring Lifecycle Consumer Handoff.md`;
- `docs/sprints/2026/08/20260816-provider-reconciliation-route-parity-sprint1/FINAL API RESPONSE.md`;
- the packaged contract catalog and lifecycle schema; and
- packaged fixture `route-parity-transition-oracle.v1.json`.

SBE owns native state, provider identities, retrieval timing, snapshots, and local
continuation. The API owns leases, queues, capacity allocation, reservations,
global spend, billing reconciliation, PostgreSQL authority, and publication policy.

