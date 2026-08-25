# Silly Owner Wants Accounting Visibility — Sprint 1 Plan

Date: 2026-08-21
Status: Slice 1 contract proposal and review packet complete; awaiting joint SBE/API review

## Objective

Create a durable, versioned, privacy-minimized handoff for fine-grained realized
provider cost, usage, outcome, and timing evidence. The result should let the API
build long-term operational/accounting knowledge by route, stage, configuration,
and authoring cohort without parsing private native state or treating SBE estimates
as authoritative billing.

This work was separated from the broader cost-calibration exploration because the
observations are independently useful. The calibration sprint may later consume
this dataset when evaluating safer, tighter commitments.

## Proposed slices

### Slice 0 — Evidence and gap audit

- Inventory exact cost, usage, outcome, timestamp, and duration fields across exact
  and bounded interactive/Batch routes and every paid stage.
- Map those facts to current native journal/results and API tables/JSON.
- Distinguish absent data, duplicated evidence, and fields with incompatible
  semantics.
- Produce a cost/timing evidence matrix and representative sanitized fixtures.

Gate: API review of what already exists before introducing a new schema.

### Slice 1 — Observation contract

- Freeze a closed versioned provider-economics observation.
- Make the native surface transaction-grained: one exact paid action or Batch round
  per observation, never a pre-aggregated deck/stage/model/cohort summary.
- Define a stable transaction identity plus append-only revision identity so later
  editorial outcome facts can join already-durable provider settlement evidence.
- Require revisions to preserve monotonic accepted identity, usage, cost, timing,
  and provenance evidence; contradiction or predecessor gaps fail closed.
- Define action/round/member cardinality, cohort identity, cost basis, timing basis,
  outcome vocabulary, and provenance references.
- Keep API-reconciled billing out of native truth while leaving an exact join seam.
- Publish schema, semantic validator, positive fixtures, and mutation fixtures.

Gate: joint SBE/API schema and ownership approval.

### Slice 2 — Native exact-route projection

- Project initial authoring, creative retry, polish, critic, and candidate evidence
  from exact interactive and Batch native truth.
- Preserve provider usage unavailable, no-work-consumed, partial Batch usage, and
  ambiguous submission as distinct cases.
- Emit only after the referenced ledger/result evidence is durable.

Gate: no projection may change native execution, settlement, or provider behavior.

### Slice 3 — Bounded-route parity

- Add equivalent bounded interactive and Batch projections.
- Prove six-pass/member evidence aggregates beneath the correct paid authority:
  per pass/attempt for interactive and per round for Batch.
- Prove route-specific payload differences do not alter shared accounting semantics.

Gate: four-route parity matrix and consumer review.

### Slice 4 — Timing semantics

- Normalize only durable, semantically named timing facts:
  create HTTP duration, retrieval attempt duration, observed pending interval,
  native action span, and provider-reported duration when actually available.
- Preserve null/open boundaries and polling-delay caveats.
- Ensure logs can aid diagnosis without becoming the only timing source.

Gate: clock/failure injection proves no fabricated or negative durations.

### Slice 5 — Public export and ingestion handoff

- Expose snapshot/result-validating Python and CLI readers or include observations
  in the native terminal-transition publication protocol.
- Produce route/stage fixtures and an installed-wheel provider-free qualification.
- Document the API ingestion transaction, transaction/revision idempotency keys,
  monotonic merge rules, reconciliation join, immutable revision retention, and
  recommended current-state projection without implementing API-owned policy.

Gate: API fixture adoption review before release qualification.

### Slice 6 — Closeout and pinnable artifact

- Run affected suites, privacy scans, installed-wheel qualification, release smoke,
  reproducible build, and consumer-contract review.
- Record exact compatibility and limitations.
- Recommend a fresh immutable patch/minor version only after explicit approval.

Gate: explicit authorization before tag or publication.

## Testing strategy

The minimum matrix should cover:

- exact/bounded × interactive/Batch;
- initial, retry, polish, critic, and candidate stages;
- accepted, rejected, failed, pending, ambiguous, skipped, and terminal outcomes;
- complete usage, missing usage, partial Batch usage, and no provider work;
- cached/uncached input and reasoning/output accounting;
- one Batch round with member evidence but one paid authority;
- fresh execution, detach/reconcile, replay, and restored workspace;
- open/null timestamps and polling-delayed terminal observation;
- mutation of cohort, cost basis, usage reference, timing basis, and provenance;
- initial provider-settlement revision followed by editorial-finalization revision,
  exact replay, skipped predecessor, stale revision, and contradictory revision;
- event/log sink failure with unchanged authoritative evidence; and
- protected subject/prompt sentinel absence.

Tests must prove the observation path is read-only with respect to provider work and
cannot authorize, settle, deny, resubmit, or release anything.

## Deliverables

- evidence-gap matrix;
- versioned observation schema and semantic validator;
- route/stage fixtures and mutation corpus;
- public reader/export surface;
- installed-wheel qualification receipt;
- API consumer handoff with storage/query recommendations;
- explicit transaction-tape and append-only revision semantics;
- compatibility and privacy inventory; and
- sprint log/evidence and release recommendation.

## Explicitly deferred

- changing commitment calculations;
- statistical calibration or cache-hit forecasting;
- dashboards, alerts, and product reporting UI;
- API migrations before the API audit selects a storage form; and
- account-authoritative billing policy.

