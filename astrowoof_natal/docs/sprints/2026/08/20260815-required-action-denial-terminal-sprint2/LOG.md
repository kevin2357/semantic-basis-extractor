# Required-Action Denial Terminalization Sprint 2 Log

2026-08-15

- Received the API handoff describing a retained run whose required creative-retry
  actions were atomically denied providerlessly while native closeout continued to
  report blocking local authoring work.
- Reviewed SBE 0.4.1 lifecycle inspection, local-dependency synthesis, closeout,
  denial contracts/tests, consumer handoff, and the preceding atomic batch-denial
  sprint.
- Preliminary code inspection found the reported contradiction is structurally
  plausible: denied actions cease to be necessary, but the unchanged `AUTHORING`
  run status independently creates `retry_preparation / authoring_continuation`.
- Drafted a state-transition-centered sprint plan. It deliberately does not treat
  closeout suppression alone as the fix and does not yet freeze the terminal
  vocabulary before API review.
- No implementation, fixture, test execution, provider operation, build, commit,
  release, or tag has begun. Status is proposed pending Kevin's review.
- Kevin supplied the remainder of the API handoff. It confirms the behavior loops
  across ordinary resumes, applies to fresh required-action refusals, recommends
  `BUDGET_EXHAUSTED` as the clearest current status, requires zero provider/local
  dependencies at terminal closeout, and explicitly preserves optional-stage skip
  semantics and provider-safety refusals.
- Revised the leading contract proposal to `BUDGET_EXHAUSTED` with a distinct
  machine-readable external-authority cause, while retaining a Slice 1 comparison
  against a separate policy-stop status. No implementation has begun.
- Kevin approved the plan. Committed and pushed the planning package as `f8d4851`;
  Sprint 2 entered `in_progress` and Slice 0 began.
- Added provider-free baselines for one authorized required creative retry, an
  atomic two-action required batch, and a real bounded prepared required action.
- Single and batch `external_authority_denied` operations persist exact
  `DENIED_PROVIDERLESS` action evidence and replay correctly, but leave the parent
  `AUTHORING` status unchanged. Inspection then reports no provider continuation,
  blocking local retry preparation, and a nonterminal outcome; closeout returns
  `continuation_required` with no unresolved action IDs.
- The bounded runner reproduces the shared problem from a real frozen profile:
  denial/replay and snapshot validation pass, inspection/closeout remain
  nonterminal, and a subsequent normal resume returns to
  `AwaitingSpendAuthorization` for the denied action. Provider submissions remain
  zero.
- Focused denial/batch/bounded tests passed all 38 tests. The complete repository
  suite passed all 296 tests in 137.913 seconds.
- Slice 0 is complete and paused for review. No runtime fix, terminal status,
  schema vocabulary, recovery mutation, provider call, build, release, or tag was
  introduced.
- Kevin approved Slice 0. Committed and pushed the regression baseline as
  `80ca0b7`; Slice 1 began.
- Drafted the complete required-denial terminal contract without changing runtime
  schemas or mutation behavior before consumer review.
- The leading mapping uses `BUDGET_EXHAUSTED` plus a closed external-spend cause
  for `external_authority_denied` and `reservation_unavailable`. It proposes
  `POLICY_STOPPED` for product denial/cancellation, preserves frozen optional-stage
  skips and accepted-delivery precedence, and treats every accepted denial as
  final rather than a temporary reservation delay.
- Proposed v0.2 single/batch success results with required `run_transition`
  evidence, one coherent batch consequence, runner short-circuiting, closed
  terminal closeout, and narrowly verified automatic reconciliation for affected
  retained 0.4.1 workspaces on normal resume/closeout.
- Slice 1 is paused at its planned Kevin/API-agent review gate. No production
  contract resource, state mutation, provider operation, build, release, or tag
  has been introduced.
- The AstroWoof API agent accepted all seven contract questions without a blocker:
  familiar spend status plus exact cause, distinct `POLICY_STOPPED`, final denial
  semantics, v0.2 transition results, mixed-batch precedence, narrow retained-run
  reconciliation, and closed non-delivery capacity release.
- The API requested one provenance clarification: a mixed-batch transition must
  separately expose all ordered `denied_action_ids` and the causal ordered subset
  `required_action_ids`. Incorporated that distinction into the contract, schema,
  fixture, and tests.
- Added strict packaged v0.2 success-result schemas while retaining historical
  v0.1 result schemas, two sanitized fixtures, closed transition outcome/trigger/
  reason vocabularies, and catalog entries. Requests remain v0.1.
- Focused lifecycle contract tests passed all 16 tests. The complete repository
  suite passed all 298 tests in 129.648 seconds.
- Slice 1 is implementation-complete and paused for Kevin's gate approval. No
  denial mutation, run transition, recovery mutation, provider operation, build,
  release, or tag has begun.
- Kevin approved Slice 1. Committed and pushed the API-approved v0.2 contract as
  `984d3fc`; Slice 2 began.
- Implemented locked run-consequence derivation and same-revision terminalization
  for new single and batch denials. Required spend refusals use
  `BUDGET_EXHAUSTED`; product/cancellation refusals use `POLICY_STOPPED`; mixed
  batch precedence and dual denied/required causal lists match the approved
  contract.
- Added durable terminal authority to private state, bounded cause/outcome to
  public state, terminal-aware status recomputation, exact inspection/closeout
  mapping, and early exact/bounded runner return before paid work.
- Preserved accepted delivery and first terminal authority. Added a real bounded
  optional-polish denial test that skips the stage and reaches delivery without a
  second provider submission.
- The first full-suite run exposed three expected consumer-smoke compatibility
  assertions: new success schema v0.2 and the new terminal event. Updated installed
  smoke and CLI consumer expectations, while ensuring only first terminalization
  emits the event. The corrected focused ladder passed 70 tests.
- The corrected complete repository suite passed all 301 tests in 121.713 seconds.
- Slice 2 is complete and paused for review. Retained 0.4.1 reconciliation and
  exhaustive new-transition failure injection remain explicitly assigned to
  Slice 3. No provider operation, paid work, build, release, or tag occurred.
- Kevin approved Slice 2. Committed and pushed atomic terminalization as
  `16465fe`; Slice 3 began.
- Added a narrow native reconciler for retained 0.4.1 single and batch denial
  evidence. It validates the complete snapshot, exact legacy denial artifact and
  binding, provider absence, native requiredness, and competing terminal/review
  conditions before committing one terminal transition and one reconciliation
  evidence artifact.
- Wired reconciliation into normal exact resume before provider-capable work,
  bounded resume, and closeout. Exact replay is nonmutating; accepted delivery is
  preserved; optional-only or contradictory legacy evidence fails closed.
- Added failure injection at artifact staging, state persistence, artifact
  promotion, and snapshot publication. Recovery permits only the declared native
  write set and refuses an unrelated workspace member.
- Retained single and batch fixtures, provider-evidence refusal, closeout
  auto-reconciliation, and interrupted bounded-resume recovery all pass with zero
  provider submissions.
- Focused recovery tests passed all 49 tests. After the pre-provider resume-order
  adjustment, the final complete repository suite passed all 309 tests in 133.040
  seconds.
- Slice 3 is complete and paused for Kevin's gate
  review. No paid operation, API key, build, release, or tag was used.
- Kevin approved Slice 3. Committed and pushed retained-workspace reconciliation
  as `f62e559`; Slice 4 began.
- Added the supported provider-free `reconcile-required-denial` lifecycle CLI. It
  returns a typed fresh inspection and supports ordinary JSON or event-plus-result
  JSONL transport. The matching Python reconciler accepts an optional event
  emitter.
- Reconciliation emits the existing redacted `terminal.transitioned` observation
  only on first mutation; exact replay emits no duplicate transition event.
- Updated the packaged contract catalog to identify v0.2 as the current successful
  single/batch result and v0.1 explicitly as historical reader compatibility.
- Expanded installed lifecycle smoke with terminal result schema, outcome,
  quiescence, and dependency checks. Updated the consumer handoff with exact API
  sequence, causal-member mapping, terminal reason mapping, optional/delivery
  precedence, and retained 0.4.1 recovery instructions.
- Focused consumer/lifecycle tests passed all 79 tests. The complete repository
  suite passed all 310 tests in 134.137 seconds.
- Built and installed a fresh Windows Python 3.11 qualification wheel outside the
  source import path. Installed smoke passed; installed inspect returned a valid
  terminal/quiescent state; CLI help exposed the new command. The temporary wheel
  SHA-256 was `12f91c8a7c61612ee901726c444ee130004e0765933b375d165527b37c4c145e`.
  The qualification tree was removed afterward.
- Slice 4 is complete and paused for Kevin's review. No provider operation, paid
  work, API key, release, tag, or publication occurred.
- Kevin approved Slice 4. Committed and pushed the consumer interfaces and handoff
  as `50051cd`; Slice 5 began.
- Built the unchanged Slice 4 source twice with the source commit timestamp as
  `SOURCE_DATE_EPOCH`. Both wheels were byte-identical at SHA-256
  `a344dfedf3b71beef52006ed7f19037d5c001cadc583f9d88026c05d4067f296`.
- Installed the exact candidate into a fresh Windows Python 3.11 venv and a cached
  `python:3.11-slim` Linux container with networking disabled. Both installed
  lifecycle smokes passed and loaded from site-packages.
- Inspected wheel contents for `py.typed`, the lifecycle schema/catalog, and the
  v0.2 single/batch fixtures. All required members were present.
- Removed both temporary build trees, the Windows venv, and both smoke workspaces
  after retaining compact evidence. No qualification output remains in the tree.
- Published the complete response to the source handoff, including new-denial
  semantics, retained 0.4.1 recovery, provider-safety refusals, ownership boundary,
  consumer sequence, and qualification result.
- Sprint exit criteria pass. The recommendation is a separately authorized
  pinnable 0.4.2 patch built from the eventual exact closeout commit. No version
  bump, release artifact, tag, or publication occurred.
