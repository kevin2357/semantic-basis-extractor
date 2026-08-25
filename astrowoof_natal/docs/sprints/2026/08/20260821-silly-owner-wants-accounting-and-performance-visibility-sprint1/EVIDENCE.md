# Silly Owner Wants Accounting Visibility — Sprint 1 Evidence

Status: Slice 5 complete; API fixture-adoption review pending before Slice 6

- Provider calls: 0
- Spend: USD 0
- Runtime/source/schema changes: none
- API migration changes: none
- Audit result:
  `results/SLICE 0 - COST AND TIMING EVIDENCE AUDIT.md`
- Representative synthetic discovery shapes:
  `results/slice0-interactive-observation-shape.example.json` and
  `results/slice0-batch-round-observation-shape.example.json`
- Evidence sources inspected:
  - native paid-action ledger and run accounting;
  - exact/bounded interactive and Batch route implementations;
  - Response retrieval diagnostics and provider reconciliation;
  - native transition journal/result/publication receipt;
  - API paid actions, provider operations and append-only observations; and
  - API native execution receipts and billing reconciliation fields.
- API review: `API Agent Slice 0 Review and Suggestions.md`.
- Gate result: Slice 0 PASS; transaction-grained append-only revision direction
  approved for Slice 1 proposal. No schema is frozen yet.
- Slice 1 proposal:
  `PROVIDER ECONOMICS OBSERVATION CONTRACT PROPOSAL.md`.
- Joint review packet:
  `SLICE 1 - JOINT CONTRACT REVIEW REQUEST.md`.
- Branch basis refreshed through published SBE 0.4.19 without changing the proposed
  evidence/authority boundary.
- Proposal examples:
  - `results/slice1-interactive-settlement-revision.proposal.json`;
  - `results/slice1-interactive-editorial-revision.proposal.json`; and
  - `results/slice1-batch-partial-usage-revision.proposal.json`.
- Slice 1 checks: JSON examples parse; documentation whitespace check passes.
- Original proposal gate: passed through joint SBE/API/owner approval.

## Slice 1 implementation evidence in progress

- Joint SBE/API/owner contract gate: approved with API conditions.
- Packaged schema:
  `provider-economics-transaction-revision.v1.schema.json`.
- Public Python surface: transaction/cohort/revision identity derivation, revision
  finalization, strict revision validation, and cumulative sequence validation.
- Lean focused result: 10 passed; one optional-schema skip.
- Schema-enabled focused result: 11 passed.
- Existing contract/publication regressions: 128 passed.
- Provider calls, retrievals, credentials, spend, and API database changes: 0.
- Packaged positive fixtures: 7; closed refusal mutations: 7.
- Fixture manifest:
  `results/slice1-consumer-fixture-manifest.json`.
- Consumer handoff:
  `SLICE 1 - PROVIDER ECONOMICS CONSUMER HANDOFF.md`.
- Slice 1 gate: PASS; API consumer approved the transaction/revision contract.

## Slice 2 — exact native projection

- Public projector:
  `project_exact_provider_economics_revision(state, action, observed_at,
  previous_revision=None)`.
- Input boundary: exact-Natal `astrowoof.semantic_closure_run.v0.9` plus one exact
  spend-ledger action whose binding joins the native run.
- Output boundary: one validated
  `astrowoof.provider_economics_transaction_revision.v1`, or `None` when no newly
  durable consumer fact exists relative to the supplied predecessor.
- Exact interactive cardinality: one native paid action per transaction.
- Exact Batch cardinality: one paid Batch round per transaction, with ordered
  logical members retained only as member-level evidence.
- Provider calls/submissions/retrievals: **0**.
- Native mutations/snapshot writes: **0**; projection operates on supplied values.
- Focused contract and projection suite: **16 passed** with schema validation
  available in the isolated release virtual environment.
- Public-package imports are exercised by the focused projection suite; the broad
  closure suite remains a later release gate because this slice adds no execution
  call site.

## Slice 3 — bounded parity

- Bounded interactive: six independently identified pass/attempt transactions.
- Bounded Batch: one round transaction with six ordered member evidence records.
- Exact/bounded shared settlement semantics: verified.
- Exact/bounded route and cohort identities: verified distinct.
- Legacy bounded v1: typed Python refusal before projection.
- Provider-economics contract + exact + bounded projection suite: **20 passed**.
- Provider calls, retrievals, submissions, and spend: **0**.
- Native writes or snapshot changes: **0**.

## Slice 3 consumer approval

- Review artifact: `API Agent Slice 3 Review and Publication Suggestions.md`.
- Decision: approved to proceed later with timing semantics and public export.
- Frozen Batch rule: one transaction/authority per round; ordered members are
  evidence only and null member usage is never allocated or inferred.
- Frozen legacy rule: bounded v1 fails closed rather than reconstructing topology.
- Remaining release requirements are recorded in PLAN.md, including packaged
  Python and provider-free CLI surfaces, predecessor-checked ingestion, privacy
  scans, member-order refusal, and later-revision monotonicity.
- Resume point: **start of Slice 4 — Timing semantics**.

## Slice 4 — timing semantics

- Review artifact: `SLICE 4 - TIMING SEMANTICS REVIEW.md`.
- Reconciliation checkpoints retain exact bounded retrieval summaries.
- Reference cap: 16 ordered attempt IDs; overflow remains explicit.
- Unknown create/provider compute duration: null, never inferred from pending time.
- Negative/backward timing: refused.
- Provider economics timing suite: **22 passed; 1 optional-schema skip**.
- Provider-pending/temporal/v2 regression: **57 passed; 1 optional-schema skip**.
- Provider calls, spend, credentials, API writes, retained-run access: **0**.
- Slice 4 gate: PASS; Slice 5 public export is next.

## Slice 5 — public export and ingestion handoff

- Public Python seam: `read_provider_economics_export()`.
- Public CLI: `astrowoof-provider-economics-export`.
- Provider-free qualification: `astrowoof-provider-economics-qa`.
- Packaged contracts:
  - `provider-economics-export.v1.schema.json`;
  - `provider-economics-qualification.v1.schema.json`; and
  - existing `provider-economics-transaction-revision.v1.schema.json`.
- Consumer handoff:
  `SLICE 5 - PUBLIC EXPORT AND API INGESTION HANDOFF.md`.
- Focused source result: **28 passed; 1 optional-schema skip**.
- Isolated installed-wheel provider-free qualification: **PASS**.
- Development wheel SHA-256: `5cdc8df44312b21ac228772be6a1d805cd883102b82da8576c29852861b72f22`.
- Qualification receipt SHA-256: `642e48ddd860d7bdf9ba38be62fa4942fae2161c7a31e6f1ddadd1611c1a7ecc`.
- Snapshot-change refusal, canonical-time refusal, output-inside-workspace refusal,
  exact replay, contiguous later revision, predecessor-gap refusal, and all four
  route/mechanism cells: verified.
- External provider I/O, provider creates/retrievals, credentials, spend, API
  database writes, and retained QA access: **0**.
- Gate: awaiting API adoption of packaged fixtures/receipt before Slice 6.
