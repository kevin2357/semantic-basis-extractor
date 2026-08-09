# Polish Checkpoint and Recovery Sprint Log

## 2026-08-09 - Planning only

- Inspected the retained SBE 0.2.1 acceptance run read-only.
- Confirmed one stable three-file snapshot mismatch: the final deck,
  validation report, and lint report are byte-identical to retained polish
  attempt-1 outputs but differ from their recorded snapshot identities.
- Confirmed polish action 1 is durably reported and action 2 remains prepared,
  unused, provider-less, and exactly bound by its external authorization.
- Confirmed `run.json` lacks the subject record because the authorization pause
  interrupted publication of the locally mutated record.
- Scoped a proposed sprint around quiescent checkpointing, provider-boundary
  failure injection, constrained repair, repaired-copy validation, and an
  optional separately authorized patch release.
- Made no source, test, package, acceptance-run, authorization, provider, tag,
  or release change.

Next action: plan review and explicit approval before Slice 0 begins.

## 2026-08-09 - Slice 0 forensic model and reproduction

- User approved the plan. Committed the planning baseline as `fb44e05` and
  began Slice 0 without changing production runtime code.
- Reconfirmed the retained run's 876-member inventory, exact three-member
  mismatch, empty persisted subjects object, reported action 1, unused prepared
  action 2, and exact external authorization binding.
- Proved every changed final file is byte-identical to its retained native
  attempt-1 output. No arbitrary workspace bytes need to be trusted.
- Added a synthetic regression showing an attempt-2 authorization exception
  bypasses subject-record publication after attempt-1 final mutations.
- Added a controlled regression showing unlocked snapshot inventory can mix
  old final identities with later new attempt identities.
- Classified the transient timing race and stable mixed manifest under one
  missing-quiescence class. Lost subject publication is a second deterministic
  exception-ordering defect at the same orchestration boundary.
- Focused regressions passed (2). No provider request, authorization
  consumption, acceptance-run mutation, or incremental spend occurred.

Next action: Slice 0 gate review before committing the reproduction or changing
production checkpoint orchestration.

## 2026-08-09 - API-agent question register added

- During the Slice 0 review gate, the user requested a dedicated record of the
  API agent's integration questions and a required end-of-sprint response.
- Added `API AGENT QUESTIONS.md`, preserving the defect, snapshot, recovery,
  corrective-deliverable, and production restart questions.
- Amended the plan so final completion requires `API AGENT RESPONSES.md` with a
  direct answer, confidence level, evidence, residual uncertainty, and consumer
  consequence for every question and subquestion.
- Required that response to be delivered with the other important sprint
  artifacts. This documentation refinement does not start Slice 1 or change
  runtime code.
- Received and preserved seven additional AstroWoof API Slice 5 questions about
  the `critic-findings.json` consumer contract: artifact stability, explicit
  schema version, closed vocabularies, guaranteed fields, authoritative
  provenance, private-artifact versus database-index ownership, and Kevin/Ella
  canonical fixture status.
- Required the final response to answer each critic question independently,
  distinguish normative/current/proposed status, cite authority, state
  compatibility behavior, and tell the API whether it can consume the answer
  immediately. No critic contract decision was made by recording the questions.

## 2026-08-09 - Slice 1 quiescent checkpoint architecture

- User approved Slice 0. Committed and pushed its regressions, evidence, plan
  refinement, and API-agent question register as `2df3e33`.
- Split persistence-only state writes from coordinator-owned complete workspace
  checkpoints. Spend callbacks no longer publish snapshots during mutations.
- Added a spend-boundary unwind that checkpoints after known authorization,
  budget, or ambiguity pauses reach the coordinator.
- Installed subject records into operator state before resumable polish begins,
  preserving attempt-1 evidence when attempt 2 pauses.
- Updated durable workspace, runner, and spend-consumer documentation to define
  ledger durability versus a restorable quiescent checkpoint.
- Focused boundary regressions passed. The semantic-closure suite passed (71),
  and spend-enforcement plus installed-smoke modules passed (19).
- Made no acceptance-run change, provider request, authorization consumption,
  schema-version change, or release-coordinate change.

Next action: Slice 1 gate review before commit or Slice 2 failure injection.

## 2026-08-09 - Slice 2 provider interruption and failure injection

- User approved Slice 1. Committed its checkpoint architecture and consumer
  documentation as `e11d59d`, then began Slice 2.
- Changed Responses handling so the validated attempt-local response marker is
  written before ledger provider-ID persistence.
- Added GET-only recovery for a restored `SUBMITTING` action with a matching
  native marker, with no new action, authorization, commitment, or POST.
- Made repeated matching provider identity recording idempotent and conflicting
  marker/ledger identities durably ambiguous.
- Made local polish final-copy or QA installation failure stop before another
  paid attempt can be prepared or submitted.
- Proved an interrupted snapshot publication fails closed until a coordinator
  republishes a complete checkpoint.
- Updated provider-spend and runner documentation without claiming that a
  deterministic idempotency key closes the provider atomicity gap.
- Focused suites passed (91); the complete deterministic repository suite
  passed (157). Fake transports only; no OpenAI call, authorization
  consumption, acceptance-run mutation, or incremental spend occurred.

Next action: Slice 2 gate review before commit or Slice 3 repair tooling.

## 2026-08-09 - Slice 3 constrained repair tooling

- User approved Slice 2. Committed its provider-interruption hardening and
  regression evidence as `2748b44`, then began Slice 3.
- Added the installed `astrowoof-repair-polish-checkpoint` dry-run/apply seam
  for only the proven SBE 0.2.1 three-file polish checkpoint shape.
- Required retained attempt byte equality, provider identity and reported-cost
  consistency, exact attempt-2 request and authorization binding, and an
  entirely unused prepared next action.
- Apply requires a separate byte-identical complete backup, an API exclusive-
  lease reference, and SBE's local spend-consumption lock. It records before
  and after hashes and validates the completed checkpoint.
- Reconstructed the missing attempt as `POLISH_IMPROVED_PARTIAL`, not accepted,
  while preserving all passes, ledger evidence, and the prepared action.
- Added eight synthetic positive/refusal tests and updated durable workspace,
  spend, authorization-consumer, and runner documentation.
- Focused repair/spend/closure suites passed (97); the complete deterministic
  repository suite passed (165). No provider request, authorization
  consumption, incremental spend, or retained-run mutation occurred.

Next action: Slice 3 gate review before commit or any acceptance-copy use.
