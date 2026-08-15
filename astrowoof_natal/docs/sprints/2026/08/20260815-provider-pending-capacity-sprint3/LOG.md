# Provider-Pending Capacity Release Sprint 3 Log

2026-08-15

- Received the AstroWoof API process-orchestration brief after a two-run staging
  cohort showed remote provider waiting retained scarce API SBE capacity.
- Reviewed SBE 0.4.2 lifecycle inspection, action inventory, interactive Responses
  polling, Batch detach, snapshot publication, local dependency synthesis, and
  fresh-process resume behavior.
- Confirmed that core native state is durable, but the current public projection
  does not distinguish safe local-process release from absence of all native
  continuation. `WAITING_FOR_RESPONSE` currently produces both provider and local
  continuation and public `not_quiescent`.
- Identified bounded poll-once/detach behavior for interactive Responses as the
  main orchestration work beyond an additive schema projection.
- Drafted an eight-slice medium-large SBE sprint with an explicit API review gate,
  one separate API companion sprint, and a shared parallel-cohort qualification.
- No implementation, test mutation, provider operation, build, version bump,
  commit, release, or tag has begun. Status remains proposed for Kevin/API review.
- The API agent approved the overall plan and requested four Slice 1 refinements:
  durable lower-bound `resume_not_before` with typed early `not_due`; native
  custody-retention classification rather than SBE-owned spend exposure; a small
  explicit wall-clock ceiling covering the retrieval HTTP call; and separate SBE
  native versus API operational cohort gates.
- The API agent also cautioned against making Batch, bounded-Natal, and every route
  block the core exact-interactive fix. Kevin and SBE agreed to require the entire
  exact interactive pipeline, including enabled polish/critic/candidate stages,
  while classifying Batch and bounded-Natal explicitly as parity-supported or
  fail-closed/deferred.
- Incorporated all refinements. Kevin approved the revised plan and authorized
  Slice 0. No runtime implementation or provider operation has begun yet.
