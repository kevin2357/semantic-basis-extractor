# API Agent Slice 0 Review and Suggestions

## Review Position

The discovery direction is sound. It preserves the existing authority split:
native SBE evidence remains authoritative for per-run provider action history and
settlement evidence, while AstroWoof API remains authoritative for global
reservations, product policy, and account-level billing reconciliation.

The useful next product is not a competing ledger. It is a durable,
append-only, query-oriented calibration projection derived from settled native
evidence and retained by the API. That projection should make operational and
product questions answerable without treating ephemeral worker logs as a
database or re-parsing every historical workspace.

## Questions the Projection Should Answer

The eventual design should explicitly support decision-support questions in
addition to strict runtime enforcement.

### Cost and efficiency

- What was the provider-reported, SBE-estimated, and API-reconciled cost of a
  paid action, accepted pass, complete authoring run, and delivered deck?
- How do those values differ between interactive Responses and Batch, holding
  route, stage, model, authoring profile, prompt geometry, output policy, and
  price-book identity constant?
- What share of the input was cached or cache-written, and what effective
  reduction in input cost did that produce?
- How much of the observed cost is attributable to accepted work, rejected work,
  creative retries, polish, critic, or candidate work?

### Latency and throughput

“How long did it take?” is not one measurement. Record enough timing geometry to
separate these questions:

- How long did a run wait before an action was admitted/submitted?
- How long did provider work remain pending after submission?
- How long did SBE take to retrieve and reconcile a completed provider result?
- How long did downstream local processing and closeout take?
- What was whole-run elapsed time from request/admission to terminal delivery or
  terminal refusal?

For every settled action, retain timestamps or derived durations for at least:

1. native action preparation/authorization;
2. provider submission;
3. provider terminal observation;
4. native retrieval/reconciliation; and
5. settled/closed outcome.

For Batch, also retain the batch submission identity, batch terminal identity
where available, and batch-window/wait duration. That lets reports distinguish
provider queue time from SBE reconciliation lag and whole-pipeline elapsed time.
A single `duration_ms` cannot answer those questions reliably.

### Quality and outcome

Cost and latency should be stratified by outcome rather than blended into a
single average. Retain, at a minimum:

- accepted versus rejected/invalid pass;
- creative retry count and retry reason/category;
- provider terminal failure, timeout, ambiguity, or unavailable usage;
- run closeout/delivery result; and
- whether a delivered deck was accepted, delivered with warnings, review-held,
  or terminally failed.

This supports questions such as whether an apparently cheaper mode actually
produces more retries or lower completed-delivery yield.

## Comparison Discipline

A Batch-versus-interactive comparison is meaningful only within a stable cohort.
At minimum, group/report by:

- route family and paid stage;
- provider mechanism (`response` or `batch`);
- model, reasoning configuration, service level, and maximum-output policy;
- authoring profile ID, profile-manifest digest, and packaged resource/prompt
  bundle digest;
- explicit prompt-contract/request-geometry version;
- price-book version; and
- SBE release identity.

The exact request digest belongs in the evidence trail but is normally
subject-specific and therefore not an aggregation key. A changed prompt prefix,
schema, assembly order, cache geometry, model behavior, or maximum-output policy
must create a new cohort rather than silently mixing incomparable observations.

Use `legacy_unknown` or an equivalent explicit classification for older evidence
that lacks stable cohort identity. Such records can inform exploratory analysis,
but should not silently calibrate a modern production commitment.

## Evidence Semantics

Every record and report must distinguish:

- native/provider usage reported;
- native estimated cost computed from reported tokens;
- provider usage unavailable with billing reconciliation pending;
- no provider work consumed; and
- API-reconciled account billing.

Unavailable usage is neither zero usage nor zero cost. Likewise, SBE's estimated
cost is useful for operational visibility but is not account-authoritative
billing. Avoid double-counting reasoning tokens when a provider’s total usage
already includes them.

## Statistical Use and Guardrails

Historical observations should initially inform reports and calibration research,
not automatically weaken hard enforcement. Before changing a reservation forecast
or commitment strategy, define:

- minimum usable sample size by cohort;
- p50/p90/p95 or other explicitly chosen percentile;
- safety margin and a floor tied to the hard per-run ceiling;
- outlier, model-drift, and price-book-change handling;
- an aging/recency rule; and
- conservative fallback for unseen cohorts, missing usage, Batch billing lag, or
  a newly observed upper tail.

SBE’s frozen hard native ceiling should remain independently conservative. A
historical forecast may eventually inform API reservation capacity, but must not
become permission to exceed the run’s immutable native maximum.

## Recommended API Boundary

The likely API work is an append-only calibration projection, derived only from
validated native action/operation observations. It should reference immutable
native/provider evidence instead of duplicating prompt or protected provider
payloads. Reports, views, or versioned calibration jobs can compute distributions
from that projection. Mutable averages are not the primary record.

Before selecting a new table versus an extension/view over current API records,
perform a field-by-field audit of:

- `sbe_paid_actions`;
- `sbe_provider_operations`;
- `sbe_provider_operation_observations`;
- `sbe_authoring_runs`; and
- native execution receipt/inspection evidence.

The audit should identify which dimensions are already normalized, which only
exist in immutable JSON, and which must be added to SBE’s public settlement
contract before the API can create a stable projection.

## Non-Goals

- Do not use logs as authoritative accounting state.
- Do not move account-wide billing authority into SBE.
- Do not infer a cohort from subject-specific request digests.
- Do not promise cache hits or use them as a safety prerequisite.
- Do not mix undelivered, review-held, or failed work into a delivered-deck
  quality cohort without explicit outcome stratification.

## SBE response and contract decisions

This review is accepted as Slice 0 API input.

The native product will be transaction-grained, not a pre-aggregated analytics
report. Each observation describes one exact paid action or one exact Batch round
and cites its immutable native evidence. SBE will not publish mutable averages or
roll observations up by deck, stage, model, route, profile, or cohort. The API may
derive those groupings from the append-only facts it ingests.

Provider settlement and editorial finalization can occur at different times. The
contract will therefore support append-only observation revisions under one stable
native transaction identity. A later revision may add newly durable facts such as
pass acceptance, retry disposition, final QA, or delivery outcome, but it may not
erase or contradict previously accepted provider identity, usage, cost basis,
timing, or provenance.

The API handoff must define an idempotent revision key, strict predecessor or
monotonicity validation, transactional ingestion, and a current-state projection.
PostgreSQL may merge revisions into a query-friendly current row or view while
retaining the immutable revision history. Such a projection is API-owned derived
state; it does not replace the native evidence or turn SBE into the account billing
authority.
