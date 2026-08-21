# Cost Tracking and Estimation Sprint 1 Plan

Date: 2026-08-18
Status: discovery draft; implementation slices not yet planned or approved

## Purpose

Investigate whether historical paid-action usage can support tighter OpenAI cost
commitments without weakening SBE's durable per-run enforcement or the AstroWoof
API's account-wide spend authority. The motivating operational goal is to reduce
avoidable over-reservation so limited global spend capacity can support useful
parallelism.

The current findings, storage inventory, candidate cohort identity, and open design
questions are recorded in [BACKGROUND.md](BACKGROUND.md).

The versioned fine-grained realized cost/usage/timing observation and API ingestion
handoff are now planned separately in
`../20260821-silly-owner-wants-accounting-and-performance-visibility-sprint1/PLAN.md`.
This sprint
retains future ownership of estimate calibration, percentile/margin policy, and any
proposal to change commitments.

## Current direction

- Reuse native paid-action/provider evidence and existing API persistence rather
  than create a competing accounting authority.
- Treat an append-only normalized calibration observation as a possible query
  projection, not as settled billing truth.
- Identify observations by route, paid stage, provider/model configuration,
  authoring/profile/resource identity, prompt geometry, price book, and outcome.
- Preserve the distinction between commitment, provider-reported or SBE-estimated
  cost, and API-reconciled account billing.
- Treat cache behavior as measured historical evidence, never as guaranteed savings
  at the provider-submission boundary.
- Keep the fifty-claim semantic basis budget out of this dollar-spend work.

## Ownership boundary to preserve

SBE owns native per-run ceilings, exact paid-action binding, pre-submission checks,
provider-operation evidence, native settlement accounting, and fail-closed
detach/resume behavior. The API owns transactional reservations across runs,
account quotas, global circuit breakers, product policy, capacity allocation, and
authoritative billing reconciliation.

Any future calibration contract must respect that boundary. In particular, a
forecast used to reserve API capacity must not be mistaken for permission to exceed
SBE's frozen native ceiling, and a native estimated cost must not be presented as
account-authoritative billing.

## Before producing an implementation plan

The discovery should establish:

1. the exact native fields available for each paid stage and provider mechanism;
2. the exact normalized and JSON fields already persisted by the API;
3. the usable historical sample size and completeness by cohort;
4. a stable prompt/request-geometry identity that changes with cost-relevant prompt
   assembly changes;
5. evidence-basis and missing-usage semantics;
6. whether a view, an extension, or a new append-only API table is justified;
7. the conservative statistical rule and fallback behavior that could safely inform
   commitments; and
8. the cross-repository qualification and consumer-review boundary.

The bounded final-QA state defect discovered during the live calibration run is
owned and qualified by the concurrent-fan-out sprint, not this cost sprint. Cost
calibration may consume bounded observations only after that fix is released and
must preserve the resulting outcome classification.

## Explicit non-decisions

This draft does not yet:

- define implementation slices or gates;
- authorize source, schema, migration, or runtime changes;
- select production percentile thresholds, margins, ceilings, or dollar defaults;
- promise cache hits or provider idempotency;
- change the current versioned price book or commitment formula;
- move billing reconciliation into SBE; or
- recommend a release version.

After the background and open questions have been reviewed with the API consumer,
this document can be revised into a sliced implementation plan with tests, gates,
evidence artifacts, review pauses, and release criteria.
