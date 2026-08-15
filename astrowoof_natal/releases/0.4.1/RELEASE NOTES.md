# AstroWoof Natal Authoring 0.4.1

Status: release candidate pending exact-artifact qualification and publication.

This patch release adds an atomic providerless-denial batch lifecycle operation
for API-owned terminal cleanup. It preserves all 0.4.0 exact-Natal, bounded-Natal,
spend, snapshot, delivery, and single-action lifecycle contracts.

## Added

- public `deny_providerless_actions()` Python operation;
- `deny-providerless-batch` under `astrowoof-authoring-lifecycle`;
- strict v0.1 batch request/result schemas and four packaged fixtures;
- one-lock, all-or-none preflight and mutation for at most 32 exact actions;
- exact digest-bound idempotent replay and constrained interrupted-write recovery;
- typed provider-safety, staleness, binding, eligibility, and exclusivity refusals;
- ordered, redacted, non-authoritative per-action and batch lifecycle events; and
- installed-wheel smoke coverage plus API migration guidance.

Terminal `DELIVERY_COMPLETE` workspaces may disposition previously authorized but
never provider-bound actions. The operation cannot submit, poll, reconcile, or
cancel provider work. The existing single-action operation remains supported.

Provider operations and provider spend during implementation and qualification:
zero / `$0`.
