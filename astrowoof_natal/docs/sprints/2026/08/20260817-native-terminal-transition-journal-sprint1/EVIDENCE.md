# Native Terminal Transition Journal Sprint 1 Evidence

Status: planning baseline only; no implementation or qualification evidence yet.

## Source material

- AstroWoof API Sprint 26 `BACKGROUND.md`: retained Aster chronology, authority
  limits, and historical non-repair posture.
- AstroWoof API Sprint 26 `PLAN.md`: joint contract freeze, API ingestion and
  terminal-first classification, SBE journal/publication work, oracle, and QA seam
  qualification.
- SBE 0.4.4: lifecycle inspection v0.3, reconciliation-cycle result v0.2, strict
  route/mechanism identity, custody/consumer-authority projection, and supported
  exact Responses / exact Batch / bounded Responses reconciliation.

## Planning assertions to prove

- A valid native review terminal is durable and ingestible before any generic
  subprocess fallback.
- Provider-operation observations are append-only and cannot be overwritten beneath
  one logical action.
- Ordinary authoring and reconciliation share the same native result boundary.
- Logs are unnecessary to explain or prevent the provider-free Aster-shaped trace.
- SBE never claims API database, queue, reservation, billing, or publication
  authority.

Provider operations: `0`

Paid spend: `$0`

## API planning review

The API agent reported no blocker and accepted the ownership split, use of SBE
0.4.4 route-parity contracts as substrate, ordinary-authoring coverage, and Aster
historical preservation. Required planning refinements were incorporated:

- explicit API review after Slice 0;
- explicit API fixture-contract review after Slice 5; and
- precise atomic-publication language in which only a jointly validated journal
  range, snapshot identity, and hash set makes a result visible/valid.

## Slice 0 evidence

- Sanitized characterization fixture:
  `fixtures/aster-shaped-authoritative-gap.v0.json`.
- Focused reproduction: 1 test passed in 1.256 seconds.
- Complete repository suite: 357 tests passed in 237.475 seconds.
- Native final truth present: operator/public state, provider metadata, complete
  snapshot, and inspection v0.3 review terminal.
- Native handoff truth absent: append-only transition/provider-operation history
  and invocation result bound to the exact journal range and snapshot.
- Exact ordinary CLI: terminal snapshot, diagnostic event/stdout, then exit 2.
- Bounded ordinary CLI: public state output without equivalent explicit review exit
  conversion.
- Neutral reconciliation: typed v0.2 result returned/printed but not preserved as a
  complete ordinary-plus-reconciliation invocation history.
- Provider operations: 0. Paid spend: `$0`. Historical Aster records changed: no.
- Required next gate: API review of reproduction, missing facts, crash windows, and
  five questions in the Slice 0 result.

## Slice 0 API gate

The in-repository `API Agent Slice 0 Review and Responses.md` records
`approved-for-slice-1-contract-freeze`. It confirms all five answers and adds the
following binding requirements for Slice 1:

- immutable per-invocation result identity and artifact;
- journal range/digest plus run identity as replay basis;
- SBE provider-observation record identity, closed kind, and `observed_at`;
- frozen request/profile digests;
- versioned price/usage evidence reference for reported cost;
- provider external ID absent until genuinely recorded; and
- no second distinct provider ID while supersession remains unsupported.

API ingestion acknowledgement remains outside SBE authority.

## Slice 1 contract proposal evidence

- Proposal: `NATIVE TRANSITION CONTRACT PROPOSAL.md`.
- Draft strict schema: `fixtures/native-transition-contracts.proposal.schema.json`.
- Canonical examples: one completed-provider journal record and one ordinary
  review-terminal immutable invocation result.
- Proposal validation: 3 tests passed in 0.020 seconds.
- Proposal plus inspection v0.3/current lifecycle compatibility: 33 tests passed in
  0.377 seconds.
- Checkpoint-basis digest avoids self-reference; full snapshot still includes and
  protects every publication artifact.
- Runtime/package mutation: none. Provider operations: 0. Paid spend: `$0`.
- Required next gate: Kevin/API answer the six decisions in the Slice 1 result and
  approve the complete cross-repository contract before Slice 2.

## Slice 1 API gate

`API Agent Slice 1 Review and Responses.md` approves the corrected contract for
implementation. The checkpoint-basis protocol, idempotency key plus canonical
result hash, outcome/cause vocabulary, and no-compaction posture are accepted.

The frozen corrections are:

- exact reconciliation v0.2 cost disposition spellings, including pending;
- no SBE API-acknowledgement field; and
- no predecessor/supersession fields until a later real recovery contract.

Provider operations remain 0 and paid spend remains `$0`.

## Slice 2 implementation evidence

- Packaged contracts: journal record v0.1, immutable execution result v0.1, and
  derived result index v0.1.
- Packaged hash-valid canonical review-terminal fixtures and strict JSON Schema.
- Public package boundary: explicit-result bounded reader and journal validator;
  no public mutation API.
- Native focused tests: 11 passed in 0.870 seconds.
- Native plus lifecycle/snapshot/consumer compatibility: 57 passed in 3.865 seconds.
- Cross-process contention: losing writer failed without journal mutation.
- Integrity refusals: sequence/hash corruption, unknown kind, missing provider ID,
  fabricated unavailable cost, changed result, partial snapshot, relocation,
  unbounded range, and oversized record.
- Provider-bound runtime integration: not started. Provider operations: 0. Paid
  spend: `$0`.

## Slice 3 provider-operation integration evidence

- Integration boundary: `persist_state()` projects the already-durable native
  spend ledger before any enclosing command publishes a workspace snapshot.
- Covered stages: initial authoring, creative retry, polish, qualitative critic,
  and qualitative candidate.
- Covered mechanisms: exact interactive Responses, exact Batch rounds, and bounded
  interactive Responses. Unsupported bounded Batch remains fail-closed.
- Durable observations: prepare, authorize, consume, submission start, provider ID,
  pending retrieval, completed/failed/cancelled/expired, usage reported/unavailable,
  submission ambiguity, identity-conflict refusal, and providerless denial.
- Cost evidence preserves the frozen four-value lifecycle vocabulary. Missing usage
  remains billing-reconciliation-pending and is never represented as zero.
- Exact semantic replay emitted no duplicate records. A second public writer still
  failed without mutation under cross-process contention.
- Failure injection after durable state but before journal append recovered from the
  authoritative ledger on the next synchronization, exactly once.
- Focused native transition tests: 14 passed in 1.412 seconds.
- Broad no-provider compatibility gate: 145 passed in 182.359 seconds.
- Provider operations: 0. Paid spend: `$0`.

## Slice 4 terminal result and receipt evidence

- Publication order: terminal journal range, immutable result, complete snapshot,
  then immutable publication receipt.
- Narrow exclusion: only `native-publication-receipts/` is omitted from native
  snapshot inventory. Result and journal remain ordinary authoritative members.
- Receipt contract: `astrowoof.native_publication_receipt.v0.1`, content-addressed
  and bound to result, full snapshot, checkpoint basis, journal range, run,
  invocation, and logical root identities.
- Retained evidence: exact published snapshot manifest and checkpoint-basis object
  accompany each receipt inside the same narrow namespace.
- Public reader refuses missing/tampered receipt, changed result/range/basis,
  incomplete current workspace, or relocated logical root.
- Interrupted result-before-snapshot publication repaired the exact orphan result;
  the result index remained one member and no replacement operation was minted.
- Historical specified-result validation remained valid after a later publication.
- External spend denial retained `budget_exhausted` plus
  `external_spend_authority_denied`; policy stops and native ceilings remain
  distinguishable.
- Route coverage: exact ordinary authoring, bounded ordinary authoring, exact
  Response/Batch reconciliation, and bounded Response reconciliation. `not_due`
  remains strictly nonmutating.
- Providerless-denial crash recovery accepts the added journal member only when the
  complete chain validates and contains each exact persisted denied action ID.
- Focused native publication tests: 19 passed in 3.098 seconds.
- Both normal and orphan-repair publication validate the freshly written full
  snapshot against actual workspace bytes before calculating or sealing its hash.
- Injected post-manifest workspace mutation was refused before receipt creation;
  restoration permitted exact-orphan repair without replacement publication.
- Post-correction route and crash-recovery compatibility: 50 passed in 11.778
  seconds.
- Broad compatibility and recovery gate: 197 passed in 204.543 seconds.
- Provider operations: 0. Paid spend: `$0`.
