# Investigation Log

- Sprint opened from two independent fresh QA `0.4.57` runs that both reached
  final-QA failure and a first-polish boundary before API terminalization.
- Initial scope is read-only reconstruction. No retained-workspace coordinate
  packet has been issued yet.
- Slice 0 reconstructed both runs from the contiguous Better Stack cohort.
  Both create a first polish action after identical final-QA counts, but their
  observable endings differ: Ada's provider-reconciliation closure converts
  `awaiting_external_authority` to `review_required`; Aldus emits an awaiting
  spend boundary and later fails API's terminal-review action-inventory guard.
- Trace emission alone cannot prove a sealed authority request. Slice 0
  therefore assigns no final owner and requests coordinates for only Ada's
  accepted generation 6 and Aldus's accepted generation 11 SBE checkpoints.
- Slice 0 completed in `SLICE 0 - FROZEN TRACE RECONSTRUCTION AND COORDINATE
  REQUEST.md`. No R2 read, provider operation, retained-workspace mutation, or
  runtime change occurred.
- API approved Slice 0 and supplied two hash-verified coordinate packets. Kevin
  separately authorized exactly one conditional HEAD and one bounded GET for
  each named object.
- Slice 1 consumed that closed budget. Both ETags, byte sizes, archive hashes,
  inventory hashes, archive member inventories, and every member hash passed.
  No listing, write, delete, provider operation, execution, recovery, or
  workspace mutation occurred.
- Both immutable checkpoints contain one exact first-polish request sidecar
  whose action and binding equal the corresponding PREPARED ledger action and
  satisfy API's released prepared-action reader shape.
- Ada's sealed v0.1 result includes the polish action and correctly says
  `awaiting_external_authority`; SBE's enclosing command nevertheless returns
  `review_required`. Aldus's sealed v0.2 terminal result instead classifies his
  same live PREPARED request as `providerless_denial_required`, despite no
  denial evidence.
- Slice 1 assigns the primary defect to SBE's first-polish spend-boundary /
  terminal-review selection. API's Aldus inventory rejection remains a correct
  downstream guard. Findings are in `SLICE 1 - IMMUTABLE FIRST-POLISH AUTHORITY
  FINDINGS.md`.
- Governance clarification: the API packets did not authorize storage access,
  but Kevin's immediately following SBE-thread message explicitly authorized
  one HEAD and one GET per run before execution. `OWNER ACCESS AUTHORIZATION
  CLARIFICATION.md` records that sequence. It grants no further access.
- API approved Slice 1 and authorized the provider-free reproduction while
  preserving ordinary terminal paths and its strict inventory guard.
- Slice 2 reproduced the defect with a minimal exact-route state and no
  provider: `FINAL_QA_FAILED` dominates a matching live PREPARED polish request,
  causing `none` / `retain_for_review` and hiding the authority request. The
  existing `FINAL_QA_WARN` control selects authority correctly. Classification
  and the narrow correction seam are in `SLICE 2 - PROVIDER-FREE REPRODUCTION
  AND CONTRACT CLASSIFICATION.md`.
- API and Kevin approved Slice 2's implementation fence: `FINAL_QA_FAILED` is
  provisional only for one exact, live, eligible interactive first-polish
  request; contradictory or genuinely terminal evidence remains closed.
- Slice 3 added a fail-closed lifecycle predicate joining the sole PREPARED
  polish action to its submitted attempt and exact current-revision request
  sidecar. It does not change schemas, workspace state, provider behavior, API
  guards, or batch/bounded route families.
- Focused and impacted qualification passed 63 tests with 6 skips. A raw
  repository discovery run executed 1,110 tests with 57 skips and 18 harness
  errors: 17 were missing source-package/subprocess path setup, and the one
  change-owned manifest error was corrected by classifying the new regression.
  The manifest and impacted suite then passed together.
- API's Slice 3 review identified one ambiguity fence: the predicate accepted
  more than one otherwise matching submitted polish attempt. The join now
  requires exactly one; a duplicate-matching-attempt regression proves that
  zero or multiple matches retain closed/review posture.
- API re-review approved the exact-one correction after independently running
  the two provider-free regressions. The fresh release candidate identity is
  frozen as `0.4.58`; lifecycle/authority blast radius selects the broad/full
  coordinator gate under the Maintainer Release Playbook.
- The release-bound focused matrix passed 82 tests with 7 skips. The supported
  one-worker broad coordinator then passed all 1,163 tests with 60 skips and no
  failures in 942.577944 seconds. The exact receipt hashes and no-Alloy-impact
  rationale are recorded in `results/SLICE 4 - 0.4.58 BROAD RELEASE GATE.md`.
- Committed artifact source as `6a66c7a5d2c162ea5c17cf0a7a5dcad79cefdec1`.
  Two clean archive builds at epoch `1789054339` produced byte-identical
  1,376,041-byte wheels with SHA-256 `d509b1747c1fac5bd27dfec257d06be4cf933b79190391edc1df770405cb8d21`
  and equal 307-member inventories.
- Clean installed qualification passed `pip check`, installed release smoke,
  installed adversarial QA, installed polish handoff QA, and a direct installed
  failed-QA exact-request/duplicate-attempt probe. All provider-free checks
  reported zero external calls and spend.
- Release-lock commit `ae993c68013b3a9a31b70f95e8eac51dd7f8a52c` was
  rebuilt twice at epoch `1789054729`. Both exact wheels are 1,376,041 bytes,
  contain the same 307 members, and have SHA-256
  `a8b131e36accb6bead912f208271bc81b76827cddcc94f77de5fc8bcbbf61871`.
  A second fresh installed environment repeated every package and feature gate
  successfully. The candidate is paused for API and owner tag/release approval;
  no tag, push, publication, or live provider run occurred.
- API and Kevin approved exact publication. Pushed `main`, created and pushed
  annotated tag `astrowoof-natal-authoring-v0.4.58` at the lock commit, and
  published GitHub release `RE_kwDOToQdE84XCFRP` with only the exact wheel and
  `SHA256SUMS.txt`.
- Fresh-download verification reproduced the qualified wheel size and SHA-256,
  the checksum line, and the remote peeled tag target. Publication evidence is
  recorded in `POST-RELEASE - 0.4.58 PUBLICATION EVIDENCE.md`.
