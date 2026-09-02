# Sprint log

## 2026-08-31 — planning

- Read the API-authored background and exact protected checkpoint coordinates.
- Confirmed both native run IDs are present in the supplied full SBE log.
- Generated a fresh diagnostic run-evolution report over the current 2,000-line
  export; parsed 1,641/1,641 marked trace records.
- Identified a plausible shared completed-evidence/local-adoption seam, retained
  only as a hypothesis pending exact checkpoint inspection.
- Prepared an investigation-first plan with four review pauses.
- No R2, provider, retained-workspace, runtime, release, or recovery action.

## 2026-08-31 — Slice 0 evidence freeze

- Incorporated `API REVIEW OF INVESTIGATION PLAN.md`.
- Froze the supplied 2,000-line log identity and its approximately 15:55:44Z
  coverage ceiling; the later reported Biscuit loop is not in this export.
- Recorded a closed diagnostic reporter receipt and source/trace evidence map.
- Traced local dependency selection through v0.7 operation projection,
  ordinary resume, progress sealing, authoring adoption, and polish execution.
- Kept Nori and Biscuit as separate causal candidates:
  - Nori: polish operation may be sealed at the earlier authoring checkpoint;
  - Biscuit: the correct creative-retry consumer runs but adoption remains
    ambiguous after completed retrieval.
- Explicitly did not equate SBE `terminal_closed` with API
  `native.terminal.review_required` without the protected identity joins.
- Stopped at Voof-paws 1. No R2 or retained workspace was accessed.

## 2026-08-31 — Slices 1–2 exact recovery and classification

- Consumed exactly two approved `HEAD` and two ETag-conditional `GET`
  operations; all frozen object identities matched.
- Safely restored both archives into disposable local directories and validated
  archive inventories plus workspace snapshot members without changing logical
  workspace contracts.
- Validated all native result/receipt/journal/retained-snapshot joins offline.
- Proved Nori's v0.2 review result explicitly retains polish reconciliation
  custody, separating SBE sealing from API terminalization.
- Proved Biscuit generation 13 contains completed, statically joinable retry
  evidence but no consumed local-operation history.
- Classified Nori as a combined SBE ordering plus API disposition seam and
  Biscuit as a creative-retry adoption defect candidate plus API no-progress
  loop guard gap.
- Stopped at Voof-paws 2. No retained checkpoint was executed or mutated.

## 2026-09-01 — Slice 3 production-boundary reproduction

- Added provider-free production-shaped tests through public `closure.main()`.
- Reproduced Nori's ordering seam: the first authoring checkpoint seals an
  unchanged completed-polish operation before `finalize_subjects()` reaches its
  stage-specific consumer.
- Proved the sealed v0.2 result truthfully retains reconciliation custody and
  prohibits new provider creation.
- Proved the positive control consumes polish evidence when consumption occurs
  before the first progress seal.
- Preserved not-due provider custody as non-eligible reconciliation with no
  local operation.
- Ran a Biscuit-shaped creative-retry control with its ambiguous-attempt posture;
  current production code adopted the completed response and advanced to fresh
  authority without provider I/O.
- Did not generalize Nori's cause to Biscuit. Paused before Slice 4 design.

## 2026-09-01 — Slice 4 narrow Nori correction

- Incorporated `API REVIEW OF SLICE 3.md` and retained Biscuit as
  evidence-insufficient.
- Added a real `finalize_subjects()` / `polish_subject()` adoption fixture with
  completed persisted response evidence and provider transport forbidden.
- Moved optional-stage-only progress sealing from the earlier authoring
  checkpoint to the existing finalization checkpoint.
- Preserved immediate authoring/creative-retry and mixed-operation checking.
- Reloaded writer-committed local-work progress into coordinator state so later
  checkpoint publication cannot overwrite cumulative consumed keys.
- Proved real polish adoption removes the operation, records its stable key,
  performs no provider I/O, and yields truthful custody-final review rather
  than `local_work_progress_contradiction`.

## 2026-09-01 — Slice 5 focused qualification

- Ran 43 focused tests across production-boundary reproduction, completed
  adoption/replay, final-QA mixed custody, and post-fan-in runtime matrices.
- All 43 passed.
- Diff hygiene passed with only Git's existing LF/CRLF advisory.
- Paused before Slice 6 packaging/release-scope review.

## 2026-09-01 — release-scope separation

- Incorporated `API REVIEW OF SLICES 4-5.md`.
- Removed run-reporter public exports and console-script registrations from the
  Nori patch diff.
- Left the reporter sources, tests, contracts, and sprint documents untracked
  for their own review/commit path; they are excluded from the Nori commit and
  must be excluded from its committed-source wheel build.
- No reporter source was discarded.

## 2026-09-01 — Slice 6 installed-wheel qualification

- Bumped the unreleased candidate version to `0.4.38` before release testing.
- Re-ran the 43-test focused source matrix successfully.
- Rejected two preliminary wheels because stale build metadata retained some
  reporter members despite source staging; neither is a release candidate.
- Built twice from independent clean tracked-source exports with only the Nori
  runtime and version changes overlaid.
- Both accepted wheels are byte-identical at SHA-256 `c50fe0fa...967e5feb`.
- Verified the accepted wheel contains no reporter module, CLI, or schema.
- Installed SBE `0.4.38` with SPC `0.11.1`; `pip check` and generic release
  smoke passed.
- Re-ran the five Nori/Biscuit production-boundary tests against the installed
  package; all passed.
- Restored every reporter source/resource to the working tree.
- Paused for final API and owner release review.
