# Provider-Pending Lifecycle Classification Patch Sprint 3 Log

## 2026-08-19 — 0.4.13 published and independently verified

- Immutable annotated tag `astrowoof-natal-authoring-v0.4.13` points to commit
  `7722077fc015a1f4161ef44c946bffd4a79a84c0`; tag object is
  `2830a679258bdb04b199b91aabead0e22617a6e2`.
- GitHub release 373366994 published at `2026-08-19T21:40:42Z`.
- Independently downloaded wheel: 858,164 bytes, SHA-256
  `4798758f0420d43276efce50c1611db222fba1dc1c2b9446319efe82b089e8f9`.
- Wheel/checksum asset IDs: 521372731 / 521372730.
- GitHub's asset digest and the downloaded checksum both match the qualified
  artifact. Post-publication evidence lands after the tag and does not move it.

## 2026-08-19 — Implementation and provider-free qualification

- Published lifecycle inspection v0.4 with a closed, semantically validated
  `execution_branch`; retained v0.3 as historical input evidence.
- Removed provider retrieval from ordinary local dependencies. Durable provider
  custody now gates retry, assembly, optional-stage, and delivery continuation
  until evidence is ingested.
- Added direct due classification with SBE-owned next-action selection capped at
  four, while preserving the run-level API invocation boundary.
- Added the redacted `lifecycle.branch_selected` diagnostic event and expanded the
  operational log line with command, reason, and eligibility.
- Added provider-free six-member, first-inspection-due, contradiction, four-plus-
  two retrieval, and installed qualification coverage.
- Added `astrowoof-provider-pending-qa`; it accepts no inputs, credentials,
  provider endpoint, spend authority, or production workspace.
- Prepared the candidate as fresh immutable version `0.4.13`; the `0.4.12` tag
  remains unchanged.
- The retained QA cohort was not opened or mutated. Provider creates/retrievals:
  zero real / zero real. Spend: USD 0.

## 2026-08-19 — API contract approval

- The API agent approved lifecycle inspection v0.4 and confirmed that it fixes
  both the provider/local-continuation conflation and first-inspection-already-due
  command-selection gap.
- API review record: commit `4455acc`.
- Incorporated its clarification: SBE may identify only its next bounded retrieval
  subset (maximum four), while the API invokes the supported run-level command and
  must not select members or reconstruct a command from action IDs.
- Sprint remains paused before implementation pending Kevin authorization.

## 2026-08-19 — Sprint proposed

- Kevin supplied the API Sprint 29 incident report from an SBE 0.4.12 QA worker.
- Six exact interactive initial Responses were submitted exactly once and retained
  with durable IDs; the API repeatedly chose ordinary resume and never invoked the
  supported provider reconciliation cycle.
- The QA worker is suspended and the retained cohort is frozen against mutation,
  retrieval, resume, or resubmission during contract work.
- Code inspection found that provider result reconciliation currently contributes
  to `local_continuation_remains`, and that a due inspection uses generic
  `continue_local_cycle/local_work_ready` without a closed command branch.
- Proposed lifecycle inspection v0.4 adds a closed `execution_branch`, separates
  provider-only continuation from ordinary local continuation, and handles a first
  inspection that is already due.
- No implementation, provider request, retained-workspace access, or spend occurred.
