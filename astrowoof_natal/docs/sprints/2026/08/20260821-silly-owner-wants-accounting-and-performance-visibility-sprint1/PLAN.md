# Silly Owner Wants Accounting Visibility — Sprint 1 Plan

Date: 2026-08-21
Status: Slice 6 qualified candidate complete; API adoption/final release review pending

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

Result: complete. Exact interactive actions and exact Batch rounds now project
read-only transaction revisions from durable native state. Publication time alone
does not mint a revision; provider settlement or later editorial/native facts do.

### Slice 3 — Bounded-route parity

- Add equivalent bounded interactive and Batch projections.
- Prove six-pass/member evidence aggregates beneath the correct paid authority:
  per pass/attempt for interactive and per round for Batch.
- Prove route-specific payload differences do not alter shared accounting semantics.

Gate: four-route parity matrix and consumer review.

Result: complete. Bounded interactive and Batch use the same revision semantics as
exact while preserving route-specific cohort identity and the bounded v2 contract.
Legacy bounded v1 workspaces fail closed.

API review: approved. Batch-round authority, evidence-only ordered members,
non-inferred null member usage, bounded-v1 refusal, and the four-route matrix are
frozen for the remaining work.

### Slice 4 — Timing semantics

- Normalize only durable, semantically named timing facts:
  create HTTP duration, retrieval attempt duration, observed pending interval,
  native action span, and provider-reported duration when actually available.
- Preserve null/open boundaries and polling-delay caveats.
- Ensure logs can aid diagnosis without becoming the only timing source.
- Preserve unknown/partial provider usage and timing as null through later
  editorial/native revisions unless genuinely new native evidence becomes durable.
- Prevent later revisions from altering accepted provider settlement identity,
  usage, cost basis, member order, or timing evidence.

Gate: clock/failure injection proves no fabricated or negative durations.

Result: complete. Reconciliation now persists an exact bounded retrieval summary;
projection exposes only explicit durable timing facts and derived SBE-observation
spans. Unknown provider compute/create timing remains null, negative or regressing
durations fail closed, and accepted timing/settlement evidence is monotonic.

### Slice 5 — Public export and ingestion handoff

- Expose snapshot/result-validating Python and CLI readers or include observations
  in the native terminal-transition publication protocol.
- Produce route/stage fixtures and an installed-wheel provider-free qualification.
- Document the API ingestion transaction, transaction/revision idempotency keys,
  monotonic merge rules, reconciliation join, immutable revision retention, and
  recommended current-state projection without implementing API-owned policy.
- Provide both a packaged snapshot-validating Python reader/validator and a
  provider-free CLI validation/export path. Python is the primary ingestion seam;
  CLI output supports installed-wheel qualification and operator diagnostics.
- Require append-only API ingestion keyed by `(transaction_id, revision_number)`,
  exact predecessor continuity, byte-identical replay idempotency, and refusal of
  skipped/conflicting/identity-changing revisions.
- Keep immutable revision history distinct from any API-owned current projection,
  and keep SBE estimate, provider-reported money, and API-reconciled billing as
  separately typed facts.

Gate: API fixture adoption review before release qualification.

Result: complete. A snapshot-validating packaged Python reader and read-only CLI
export newly durable transaction revisions from exact/bounded interactive/Batch
state. A provider-free installed-wheel command emits a closed four-route receipt.
The API handoff freezes immutable predecessor-checked ingestion, semantic nulls,
Batch-round authority, privacy exclusions, and the separation of SBE estimates,
provider reports, and API-reconciled billing.

### Slice 6 — Closeout and pinnable artifact

- Run affected suites, privacy scans, installed-wheel qualification, release smoke,
  reproducible build, and consumer-contract review.
- Record exact compatibility and limitations.
- Recommend a fresh immutable patch/minor version only after explicit approval.

Gate: explicit authorization before tag or publication.

Result: qualification complete. SBE 0.4.21 has a committed source identity, a
passing 683-test full suite, two byte-identical wheels, passing generic installed
smoke, passing installed provider-economics qualification, and a clean exact-pinned
dependency check. API fixture/receipt ingestion and explicit owner authorization
remain required before immutable tagging/publication.

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
- protected subject/prompt sentinel absence;
- Batch member-order mutation with unchanged round identity refusal;
- missing/partial usage remaining null through later editorial revisions; and
- public export exclusion of prompts, response text, subject/location data,
  headers, credentials, full authority bindings, and provider payloads.

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

