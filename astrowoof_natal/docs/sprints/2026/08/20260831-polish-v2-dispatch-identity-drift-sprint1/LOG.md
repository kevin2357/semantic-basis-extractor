# Log — polish v2 dispatch identity drift

## 2026-08-30 — planning

- Read the API-provided background and exact retained coordinates.
- Confirmed the focal boundary is post-authoring polish v2 admission before any
  polish provider call.
- Performed a preliminary source map of the public v2 CLI, writer-fenced intent
  commit, dispatchability checks, strict request/inspection join, and grant
  validation.
- Recorded that several logged digests do not yet prove mutation of one request;
  they may come from different observations or differently named fields.
- Created an investigation-first plan with six review pauses and conditional
  implementation/release slices.
- No R2, provider, retained-workspace, or runtime mutation activity occurred.

## 2026-08-30 — offline-inspector scope check

- Reviewed the prior general checkpoint-inspector background/plan and the Moxie
  incident-local download/publication readers.
- Determined that a trustworthy installed inspector is a separate multi-slice
  capability, not a safe incidental promotion of one parser script.
- Updated this sprint to reuse/adapt local read-only inspection while recording
  Delerium requirements for the dedicated tooling sprint.
- Left a narrow extraction option open only for existing-validator, restored-
  workspace-only helpers that do not delay investigation or imply public support.

## 2026-08-30 — Slice 0 source and trace characterization

- Read and hashed the corrected full SBE Render export at the owner-supplied
  local path. The export is 845,872 bytes, 1,200 lines, and has SHA-256
  `61813d879183d4637553f96875df6459335b2b24a21bd7098ee33df10808e087`.
- Replaced the earlier truncated export as the diagnostic source for this
  slice. No log content or protected payload was copied into the repository.
- Proved from source and trace that the apparent request drift conflated three
  document identities:
  - stable standalone v1 authority request `a838af…`;
  - time-bearing lifecycle-v0.5 embedded v1 requests, including `c5ac68…`;
  - stable constrained-dispatch v2 request `07300bd…`.
- Confirmed repeated attempts used the same v2 request and grant, while the
  lifecycle-v0.5 request digest changed with each new observation time.
- Located the earlier local-progress failure at revision 75:
  `Local-work consumption history is not append-only`.
- Confirmed the v2 intent commit then refused native dispatchability with
  `action_state_or_custody_mismatch`; dispatch found an existing intent whose
  request/grant identity did not match and refused with
  `authorization_mismatch`. No provider create was reached.
- Ran three focused provider-free v2 contract tests; all passed.
- Produced the Slice 0 identity map and a one-object generation-11 access
  manifest. No R2 operation has been performed.

## 2026-08-30 — Slice 1 retained generation-11 inspection

- Incorporated both API wording/reproducibility corrections from Oauf-paws 1.
- Executed the approved exact generation-11 access budget:
  one matching `HEAD`, followed by one matching `GET`; zero list/write/delete.
- Verified ETag, byte length, archive SHA-256, checkpoint contract,
  compatibility identity, generation, complete archive inventory, every member
  digest, and the inner native workspace snapshot inventory.
- Confirmed retained state revision 75 and status
  `AWAITING_SPEND_AUTHORIZATION`.
- Confirmed polish action `paid_c90…` is providerless, unconsumed `PREPARED`
  work with no native authorization applied.
- Found the persisted singleton v2 dispatch intent belongs instead to completed
  creative-retry action `paid_707…`, request `e35ca8…`, grant `e09fbc…`, and
  provider response `resp_014d…`. Its intent state remains `PROVIDER_PENDING`
  while the ledger action is already `REPORTED`.
- Confirmed current source refuses every different request/grant while that
  singleton intent remains and contains no normal reconciliation/fan-in path
  that retires it. This retained contradiction directly explains both observed
  refusal reasons without relying on the separate local-work history failure.
- Did not access generation 10; generation 11 is sufficient for the native/API
  join and causal classification gate.

## 2026-08-30 — Slice 2 classification and invariant freeze

- Incorporated API Oauf-paws 2 approval and its exact-terminal-evidence rule.
- Classified the incident as a general SBE sequential-v2-action lifecycle
  defect with a separate diagnostic-label conflation and an adjacent local-work
  append-only failure.
- Froze the live-intent retirement preconditions, refusal precedence, atomic
  archive/slot-release boundary, and retired-intent exact-replay rule.
- Confirmed generation 10 is unnecessary for this classification and performed
  no additional remote access.
- Paused before provider-free production-path reproduction or runtime mutation.

## 2026-08-30 — Slice 3 sequential-v2 reproduction

- Incorporated API Oauf-paws 3's timing refinement: normal intent retirement
  must be atomic with the terminal reconciliation/reporting checkpoint, not
  delayed until successor admission.
- Added a provider-free sequential-v2 witness through the real intent commit,
  ordered scripted dispatch, temporal inspection, request/grant construction,
  and successor intent/dispatch boundaries.
- Reproduced the retained failure mechanically: complete terminal predecessor
  evidence plus a fresh coherent successor request is blocked by the stale live
  singleton (`action_state_or_custody_mismatch` then
  `authorization_mismatch`), with zero successor creates.
- Ran the new witness with the existing v2 intent-fence matrix: 18 tests passed.
- Made no runtime change and performed no remote/provider operation.
- Paused at Oauf-paws 4 before contract shape or runtime integration.

## 2026-08-30 — Slice 4 contract and integration design

- Incorporated API Slice 3 / Oauf-paws 5 approval and the requirement to hook retirement
  into the real reconciliation/reporting checkpoint.
- Identified the coordinator-owned quiescent `save_state()` checkpoint inside
  `checkpoint_spend_boundary()` as the first complete exact-interactive
  workspace checkpoint after `SpendController.settle_active()` has made the
  full intent inventory terminal.
- Rejected worker-thread `persist_state()` and successor admission as normal
  retirement boundaries.
- Froze a closed internal retired-intent record, complete terminal join, exact
  replay precedence, snapshot-membership rule, historical compatibility posture,
  and interruption matrix.
- Determined that the existing public v3 `exact_replay` result can express the
  consumer outcome; no API/public lifecycle schema change is currently needed.
- Performed no runtime mutation, provider operation, or additional remote access.
- Paused at Oauf-paws 5 for approval before implementation.

## 2026-08-30 — Slice 5 runtime correction

- Incorporated API Slice 4/Oauf-paws 6 implementation approval and its real-
  adoption-path requirement.
- Added a strict all-member completed-intent validator and closed internal
  retirement record.
- Wired retirement into the writer-fenced coordinator quiescent checkpoint
  before local-progress/successor selection; worker persistence remains unable
  to retire independently.
- Extended exact dispatch-history replay using the unchanged public v3
  `exact_replay` result.
- Added provider-free real reconciliation/reporting, exact replay, fresh
  successor, partial completion, identity conflict, interruption, privacy, and
  real creative-retry adoption coverage.
- Focused implementation suite: 5 tests passed.
- Broader affected matrix: 49 tests passed, with one expected optional-schema
  skip.
- No provider/network, retained workspace, R2, or API-global mutation occurred.
- Paused before packaging/release work.

## 2026-08-30 — Slice 6 installed qualification and candidate freeze

- Incorporated API Slice 5 approval for packaged/installed qualification.
- Froze fresh candidate version `0.4.34` before building or running release
  gates.
- Added a first-class provider-free installed qualification command and closed
  receipt schema for the completed-intent retirement invariant.
- The receipt proves the coordinator checkpoint contains the retirement,
  exact predecessor replay performs zero provider calls, a fresh successor
  creates exactly once, and partial or contradictory terminal evidence retains
  the live intent and permits no successor create.
- Strengthened the Python validator to validate every nested evidence cell even
  when optional `jsonschema` is unavailable.
- Focused source qualification: 7 tests passed, one optional-schema skip.
- Final affected source matrix: 49 tests passed, with three expected optional-
  schema skips in the lean host interpreter.
- Built two byte-identical `0.4.34` wheels with SHA-256
  `20a64e366840e143f1f9cb6cd936a7dd15341dc2041562e8f33860eb4ed70b2d`.
- Clean installed environment reports SBE `0.4.34`, SPC `0.11.1`, and a clean
  `pip check`; the qualification ran twice with byte-identical receipt files.
- Installed release smoke, external-authority-v2, post-fan-in-retry, and
  terminal-review qualifications passed.
- No external provider call, spend, R2 access, or retained-run mutation occurred.
- Paused before commit/tag/publication for final API/owner release approval.

## 2026-08-30 — 0.4.34 publication

- Received final API and owner approval.
- Committed release source at `c5ec8c20216971f22da768f827a3602f42f1d04a`.
- Rebuilt from that exact commit and reproduced approved wheel SHA-256
  `20a64e366840e143f1f9cb6cd936a7dd15341dc2041562e8f33860eb4ed70b2d`.
- Pushed `main` and immutable tag `astrowoof-natal-authoring-v0.4.34`.
- Published the GitHub release and downloaded the public asset; GitHub's asset
  digest and the downloaded bytes both match the approved SHA-256.
