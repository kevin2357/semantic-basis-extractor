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

## 2026-08-24 — Slice 1 contract implementation started

- Added the packaged Draft 2020-12 transaction-revision schema and registered its
  identity in the public contract catalog.
- Added strict Python validation independent of optional `jsonschema`.
- Added canonical native transaction, cohort, and revision identities.
- Enforced interactive-versus-Batch cardinality, conservative partial Batch usage,
  and the prohibition on invented member allocations.
- Added bounded retrieval summaries with 16-reference cap and explicit overflow.
- Added cumulative sequence validation for exact replay, contiguous predecessor
  chains, immutable identities, monotonic settlement/timing evidence, and closed
  provider/editorial/native progressions.
- Added focused contract tests for settlement-to-editorial/native revisions, replay,
  predecessor gaps, contradictions, partial Batch usage, retrieval overflow,
  topology cohort identity, and privacy sentinel absence.
- Initial focused contract result: 7 passed, one optional `jsonschema` check skipped.
- Existing bounded-authoring, native-transition, and semantic-closure regression
  set: 128 passed.
- Static packaged fixture corpus and mutation corpus remain before Slice 1 closeout.

## 2026-08-24 — Slice 1 fixture and closeout completion

- Added seven packaged positive fixtures: settlement, editorial finalization,
  native finalization, partial Batch usage, providerless no-work, ambiguity, and
  legacy-unknown cohort.
- Added a seven-case mutation corpus covering protected/unknown fields, native
  identity, cohort topology digest, invented member cost, false Batch settlement,
  retrieval overflow accounting, and canonical observation time.
- Added closed public fixture/corpus readers and traversal refusal.
- Added pending-to-settled sequence coverage with increasing cumulative timing.
- Schema-enabled focused suite: 11 passed with Draft 2020-12 validation active.
- Existing contract/publication regression suite remains green: 128 passed.
- Published the API consumer handoff and fixture hash manifest.
- Provider/network calls, credentials, workspace mutation, API database changes,
  and spend: 0.
- Slice 1 was approved by the API consumer and Slice 2 proceeded.

## 2026-08-24 — Slice 2 exact-route projection

- Added the read-only `project_exact_provider_economics_revision()` public Python
  surface for exact-Natal v0.9 native actions.
- Projected all five paid-stage classifications: initial authoring, creative retry,
  polish, qualitative critic, and qualitative candidate.
- Preserved one transaction per interactive paid action and one transaction per
  Batch round; ordered Batch members remain evidence beneath round authority.
- Preserved provider-pending, provider usage reported, usage unavailable pending
  reconciliation, providerless no-work, and ambiguous submission as distinct
  settlement dispositions.
- Bound transaction identity to native run/action identity and rejected actions
  whose complete binding does not join the run.
- Made projection cumulative and revision-aware. A later observation timestamp
  with byte-identical consumer facts returns no new revision.
- Added focused exact interactive/Batch, five-stage, replay, settlement, ambiguity,
  no-work, and binding-refusal regressions. No provider transport is reachable.

## 2026-08-24 — Slice 3 bounded-route parity

- Added `project_bounded_provider_economics_revision()` over the same closed
  transaction/revision contract and monotonic comparison as exact-Natal.
- Preserved bounded interactive cardinality as one transaction per pass/attempt.
- Preserved bounded Batch cardinality as one transaction/global authority per
  round, with six ordered members as audit evidence only.
- Kept exact and bounded cohort/route identities distinct even when their durable
  settlement facts are otherwise identical.
- Required the current bounded v2 topology contract. Historical bounded v1 state
  is refused rather than guessed into six-pass accounting.
- Added the four-route parity regressions; all provider economics tests pass with
  no provider transport or state mutation.

## 2026-08-24 — Slice 3 API approval and intentional pause

- Added and reviewed `API Agent Slice 3 Review and Publication Suggestions.md`.
- API approved one transaction/accounting authority per Batch round, ordered
  members as evidence only, null rather than inferred member attribution, bounded
  v1 fail-closed behavior, and the four-route parity boundary.
- Carried immutable-revision ingestion, predecessor/replay, semantic-null, privacy,
  member-order, settlement-monotonicity, packaged Python reader, and provider-free
  CLI requirements into Slices 4–6 and the qualification matrix.
- Sprint is intentionally paused immediately before Slice 4. Resume on branch
  `codex/accounting-performance-visibility` after refreshing it from mainline.

## 2026-08-25 — Slice 4 timing semantics

- Refreshed the branch through published SBE 0.4.20 before resuming.
- Added durable, bounded retrieval summaries to native reconciliation checkpoints:
  attempt count, first/last observation, cumulative HTTP duration, 16 ordered
  diagnostic references, and explicit overflow.
- Projected only explicit native timestamps and two accurately named SBE-observed
  spans; provider-pending wall time is not called provider compute time.
- Preserved unavailable create/provider durations as null and refused negative or
  backward timing.
- Timing-focused economics suite: 22 passed; 1 optional-schema skip.
- Provider-pending/temporal/v2 regression: 57 passed; 1 optional-schema skip.
- Provider/network/spend/retained-run activity: 0.
- Slice 4 gate passed; continuing to Slice 5 public export.

## 2026-08-25 — Slice 5 public export and handoff

- Added a packaged, snapshot-validating Python export that returns only newly
  durable transaction revisions from exact v0.9 or bounded v2 workspaces.
- Added a read-only CLI with canonical observation time, predecessor input, stdout
  support, and refusal to write inside the native workspace.
- Added closed export and qualification schemas and public contract-catalog entries.
- Added a self-contained provider-free four-route qualification receipt suitable
  for installed-wheel/API QA.
- Added snapshot-integrity, replay, predecessor-gap, settlement-revision, CLI
  mutation-safety, four-route cardinality, and privacy checks.
- Published the transaction-tape/API ingestion handoff.
- Focused provider-economics/export/qualification suite: 28 passed; 1 optional
  schema skip on the lean interpreter.
- Isolated installed-wheel qualification passed against the 0.4.20 development
  wheel (`5cdc8df4...b72f22`); its closed receipt was
  `642e48dd...a7ecc`.
- Provider/network/spend/API database/retained-run activity: 0.
- Paused at the planned API fixture-adoption review before Slice 6.

## 2026-08-25 — Slice 5 API adoption approval and Slice 6 start

- API approved the snapshot-validating append-only transaction tape, cardinality,
  predecessor/replay, semantic-null, cost-authority, and privacy boundaries without
  contract correction.
- The remaining consumer condition is API ingestion of the packaged four-route
  fixture/qualification receipt before the resulting release is pinned.
- Opened release qualification and selected fresh immutable version 0.4.21.

## 2026-08-25 — Slice 6 candidate qualification

- Committed the pre-mainline release-candidate source at `fa7f79e` and bumped to
  fresh 0.4.21.
- Full suite: 683 passed; 36 expected environment/opt-in skips.
- Two pre-mainline builds at fixed epoch `1787638617` were byte-identical.
- Installed provider-economics qualification passed with receipt
  `d2cbcdf6...40b8b0` and zero provider I/O.
- Generic installed release smoke passed with 50 cards and four summaries.
- Exact SPC 0.11.0 plus schema dependency environment passed `pip check`.
- No provider/network/spend/retained-run activity occurred.
- Paused for API fixture/receipt ingestion and final release authorization.

## 2026-08-25 — Final release approval

- API approved immediate 0.4.21 publication as an additive, opt-in native release.
- Existing execution/lifecycle/spend/custody/authority contracts remain unchanged;
  bounded retrieval timing is the only native-state addition.
- Product owner authorized tagging and publication.
- API worker pin/deployment remains deferred until its separate ingestion sprint
  qualifies fixture, replay, predecessor, and privacy behavior.

## 2026-08-25 — Final mainline artifact lock

- Fast-forwarded the approved branch into `main` before release tagging.
- Rebuilt from final authorized mainline source `7fae397` with the frozen epoch.
- Two final builds were byte-identical: 969901 bytes, SHA-256
  `44928211...27ade2`.
- Re-ran `pip check`, installed provider-economics qualification, and generic
  installed release smoke against the exact final upload artifact; all passed.
- Final provider-economics receipt remained `d2cbcdf6...40b8b0`.
