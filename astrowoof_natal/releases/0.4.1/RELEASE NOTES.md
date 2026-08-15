# AstroWoof Natal Authoring 0.4.1

Status: published under immutable annotated tag
`astrowoof-natal-authoring-v0.4.1`.

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

## Qualification

- complete repository suite: 294 passed;
- two independent fixed-epoch builds were byte-identical;
- wheel SHA-256:
  `5bbb2317fbb314d22a6407a75ce03e0a406a928bdaa8160eed51682318650351`;
- wheel bytes/entries/resources/cache entries: 720149 / 82 / 42 / 0;
- fresh installed lifecycle smoke passed on Windows CPython 3.12 and Linux CPython
  3.11 using the exact candidate bytes; and
- artifact source commit:
  `1fa1151ab1e72b768697674b17c295c32a8ba78f`.

Publication is complete. Authenticated download verification matched the qualified
wheel SHA-256. The immutable tag identifies release-record commit
`b9aa4af11fbe9d83099474646a288842285860e6`; this post-publication evidence does
not move that tag.
