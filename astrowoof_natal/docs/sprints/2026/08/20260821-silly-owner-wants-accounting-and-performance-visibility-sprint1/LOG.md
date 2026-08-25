# Silly Owner Wants Accounting Visibility — Sprint 1 Log

## 2026-08-21 — Sprint drafted

- Separated durable realized-cost visibility from the broader estimate-calibration
  exploration.
- Audited the high-level native and API evidence already present.
- Identified that timing exists in attempt metadata, wave results, retrieval
  diagnostics, logs, and API orchestration spans, but not as one normalized
  long-term per-provider-action analytics fact.
- Drafted proposed slices, testing matrix, ownership boundary, and review gates.
- No source, schema, migration, runtime, provider, spend, or release behavior changed.

## 2026-08-21 — Slice 0 evidence and gap audit

- Audited native ledger, attempt metadata, run accounting, Batch rounds/members,
  reconciliation diagnostics, transition journal, and publication receipts.
- Audited API paid-action, provider-operation, provider-observation, execution-
  receipt, and reconciliation persistence.
- Confirmed the missing product is a normalized native observation, not another
  spend-authority or billing ledger.
- Froze no schema. Recorded cost/timing semantic distinctions, route/stage
  cardinality, cohort-identity gap, privacy boundary, and API design questions.
- Added two synthetic shape examples for API review. They are discovery aids, not
  candidate contract fixtures.
- Provider calls: 0. Spend: USD 0. Runtime/source/database changes: none.
- Slice 0 is complete and paused at its planned API review gate.

## 2026-08-21 — Slice 0 API review incorporated

- Moved the API review from the superseded calibration location into this sprint
  and accepted it as Slice 0 input.
- Froze the guiding direction that SBE publishes individual transaction facts, not
  pre-aggregated analytics summaries.
- Selected append-only observation revisions to bridge provider settlement and
  later editorial finalization under one stable transaction identity.
- Required monotonic evidence preservation, exact replay, predecessor validation,
  transactional API ingestion, immutable revision retention, and an API-owned
  current-state projection in the Slice 1/5 gates.
- Reconciled sprint status and evidence bookkeeping. No runtime, schema, provider,
  spend, or API database behavior changed.

## 2026-08-21 — Slice 1 observation contract proposal

- Proposed `astrowoof.provider_economics_transaction_revision.v1` as a closed,
  transaction-grained, cumulative append-only revision contract.
- Kept native run/action identity authoritative: one interactive paid action or one
  Batch round per transaction, with ordered Batch members beneath one authority.
- Defined distinct provider, editorial, and native outcomes; explicit missing,
  partial, estimated, provider-reported, and API-reconciled monetary semantics; and
  multiple named timing bases.
- Proposed exact predecessor/idempotency and monotonic sequence rules plus an API-
  owned immutable revision store/current projection ingestion pattern.
- Added three proposal examples. They are review aids, not packaged schemas or
  accepted fixtures.
- Provider calls: 0. Spend: USD 0. Runtime/source/schema changes: none.
- Paused at the planned joint SBE/API schema and ownership review gate.

## 2026-08-24 — Branch refresh and Slice 1 review packet

- Merged released `main` through SBE 0.4.19 into the accounting/performance branch.
- Rechecked the proposal against the newer lifecycle v0.6, native publication,
  external-authority, provider-reconciliation, and operator-retirement contracts.
- The ownership model still composes: economics revisions observe durable native
  facts but create no execution, spend, custody, scheduling, or billing authority.
- Added a concise joint-review request that freezes the seven decisions needed
  before packaging a schema and validator.
- No runtime, schema, provider, spend, or API database behavior changed.
- Gate remains intentionally paused for SBE/API/owner contract approval.

## 2026-08-24 — Slice 1 joint approval received

- API approved the contract name, cumulative transaction-revision tape, native
  run/action authority, milestone-only emission, Batch-round cardinality,
  `legacy_unknown`, and cohort boundary.
- Added bounded retrieval-summary requirements with explicit reference overflow.
- Added the no-invented-member-allocation rule for Batch.
- Required execution topology in cohort identity and a canonical cohort digest.
- Reaffirmed distinct unknown/zero, estimated/provider/API money, publication time,
  provider completion, and provider-pending wall-time semantics.
- Opened the Slice 1 implementation gate for schema, validators, and fixtures.
