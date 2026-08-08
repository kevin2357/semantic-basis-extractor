# Next-Release Sprint Log

## 2026-08-07 — Planning only

- Reviewed `docs/sprints/README.md` and the complete 2026-08-05 v0.1
  release-engineering sprint record, including its plan, chronological log,
  slice reports, package manifest, smoke reports, live summary, consumer
  handoff, publication verification, and post-sprint audit.
- Drafted the next-release sprint plan around the already implemented identity,
  spend-enforcement, provider-disclosure, and durable-workspace contracts.
- Preserved the prior sprint's gated progression from deterministic evidence to
  installed artifact, controlled live QA, final handoff, and publication.
- Added explicit approval boundaries for version selection, billable provider
  work, final tagging, and publication.
- Marked unknown-time suppression, variable basis sizes, Quick/Complete,
  hierarchy redesign, and critic product policy out of scope.
- No sprint slice has started. No tests, builds, live calls, version changes,
  release artifacts, tags, or publication actions have been performed under
  this sprint.

Next action: obtain explicit approval to start Slice 0.

## 2026-08-07 — Sprint start and Slice 0 authorization

- User approved the plan and authorized sprint execution through the Slice 0
  gate.
- Committed the unchanged planning scaffold as `edb6c93` before starting work.
- Changed sprint status to `in_progress`; live provider work and publication
  remain unauthorized.
- Began the read-only baseline, release-coordinate, compatibility-tuple, and
  change-since-v0.1.0 audit. No package version, tag, or artifact changed.

## 2026-08-07 — Slice 0 audit complete; gate pending

- Resolved the v0.1.0 tag to
  `8fdad164b151c87f77dfc416f6efb754cf00fd7b` and recorded `4ea2e17` as the
  pre-sprint runtime baseline.
- Audited the 32-file change set since v0.1.0, current package metadata,
  contract catalog, release playbook, provider routes, and price book.
- Inspected the published AGF 0.6.0 and SPC 0.10.0 tags, manifests, wheel
  checksums, canonical graph boundary, profile, four contexts, and projected
  registry identities.
- Recommended `astrowoof-natal-authoring==0.2.0` and tag
  `astrowoof-natal-authoring-v0.2.0`; these coordinates remain unapproved and
  no package metadata changed.
- Found that the current installed smoke fixture is SPC 0.10 / canonical graph
  1.3 but retains `natal:bre`. Slice 1 therefore needs exact pinned-boundary
  evidence with an opaque UUID-style identity rather than claiming the old
  fixture proves the evolved identity contract.
- Wrote `results/SLICE 0 - Baseline and Release Coordinate Audit.md` and paused
  at the required gate. No test suite, build, live call, tag, or publication
  was required or performed in this audit slice.

Next action: obtain explicit approval for the Slice 0 gate recommendations.

## 2026-08-07 — Slice 0 approved

- User approved distribution version `0.2.0`, annotated tag
  `astrowoof-natal-authoring-v0.2.0`, the recorded AGF 0.6.0 / SPC 0.10.0
  artifact and semantic-resource tuple, CPython 3.12.13 as the reproducible
  build interpreter with the `>=3.11` floor, and creation of exact opaque-ID
  compatibility evidence in Slice 1.
- Updated only the sprint coordinates. Package metadata remains unchanged
  until Slice 3 as planned.
- Slice 0 is approved for commit; Slice 1 may begin after that commit.

## 2026-08-07 — Slice 1 contract and integration qualification

- Committed approved Slice 0 as `9ac90de` and began Slice 1 without changing
  package metadata.
- Downloaded the published AGF 0.6.0 and SPC 0.10.0 wheels. Their SHA-256
  values exactly matched the approved release records.
- Confirmed the local CPython 3.12 Windows environment cannot install the
  qualified Swiss-Ephemeris dependency without native compilation. Preserved
  that limitation rather than claiming a fresh AGF live calculation.
- Added deterministic UUID identity derivation to the packaged smoke input and
  recorded the pinned upstream artifact hashes and changed identity carriers.
- Extended smoke checks through the authoring packet, selected claims,
  syntheses, delivered deck, operator provenance, and delivery provenance.
- Added a machine-outcome matrix covering eight distinct run result classes.
- The first full suite exposed a concurrent snapshot-attestation race. Changed
  worker saves to persist state atomically while reserving whole-directory
  snapshot attestation for the quiescent coordinator; crash behavior remains
  fail closed. Added the boundary to durable documentation.
- Focused release-contract tests passed (12), UUID source smoke reached
  `DELIVERY_COMPLETE`, and the full repository suite passed (136).
- Wrote the Slice 1 human and machine reports. No OpenAI call, version change,
  wheel build, tag, or publication occurred.

Next action: Slice 1 gate review and approval before commit or Slice 2.

## 2026-08-07 — Slice 1 approved; Slice 2 safety qualification

- Committed approved Slice 1 as `44adeb5` and began Slice 2.
- Added a binding matrix for interactive initial, Batch initial, creative
  retry, polish, qualitative critic, and qualitative candidate actions.
- Added failure injection after provider creation but before provider-ID state
  persistence; the action becomes machine-distinguishable ambiguity and is not
  replayed.
- Confirmed polling known provider work creates no new action or commitment.
- Expanded snapshot negatives to missing, changed, additional, and truncated
  members; relocation and successful exact-path cases remain covered.
- Reconfirmed minimized disclosure for every provider route while protected
  local provenance remains separate.
- Focused regressions passed (14), the repository suite passed (140), and
  `git diff --check` passed. No live provider call occurred.
- Wrote the Slice 2 human report and machine-readable safety matrix.

Next action: Slice 2 gate review and approval before commit or Slice 3.

## 2026-08-07 — Slice 2 approved; Slice 3 candidate artifact

- Committed approved Slice 2 as `f60b95c` and began Slice 3.
- Updated the approved distribution version from 0.1.0 to 0.2.0.
- Fixed `SOURCE_DATE_EPOCH=1786156755` and built twice with CPython 3.12.13,
  setuptools 83.0.0, wheel 0.47.0, and pip 26.0.1.
- The first pair was reproducible but rejected during content inspection: the
  runtime-required Kevin editorial reference retained protected birth and
  location values.
- Cleared only those six protected reference fields, added a regression, and
  rebuilt twice. Replacement wheels were byte-identical at 623,605 bytes with
  SHA-256 `799307597fb33e5717112e0c772983bca2dd78bd193b999a5286e4476f2b4ea4`.
- Audited all 40 wheel members: 16 source, 19 resource, and five distribution
  metadata members. No unsafe path, unexpected member, secret, protected
  subject value, cache, run artifact, or provider artifact remained.
- Recorded resource-set SHA-256
  `439c8771fe7944ddb1b5b83465b7d2f76f252340624f1b85c85f9278fba55404`.
- Complete repository tests passed (140), then focused release-contract tests
  passed (13) after the audit regression. `git diff --check` passed.

Next action: Slice 3 gate review and approval before commit or Slice 4.

## 2026-08-07 — Slice 3 approved; Slice 4 installed smoke

- Committed approved Slice 3 as `a8fbf05` and began Slice 4.
- Created a fresh CPython 3.12 virtual environment under `C:\tmp`, installed
  only candidate wheel SHA-256
  `799307597fb33e5717112e0c772983bca2dd78bd193b999a5286e4476f2b4ea4`,
  and confirmed version 0.2.0 resolves from site-packages outside the checkout.
- Ran `astrowoof-release-smoke --require-installed` from outside the repository.
  It reached `DELIVERY_COMPLETE` with 50 cards, four summaries, the forced
  two-attempt retry, matching delivery hashes, and successful cleanup.
- The installed smoke retained the Slice 1 opaque UUID, approved AGF/SPC wheel
  hashes, and Slice 3 resource-set identity.
- Exercised installed prepare/authorize state without provider submission:
  pending authorization was durable and public, exact authorization persisted,
  and legacy state without a ledger failed closed.
- Complete repository tests passed (141); `git diff --check` passed. No live
  provider call, tag, or publication occurred.
- Wrote the Slice 4 human and machine-readable reports.

Next action: Slice 4 gate review. Slice 5 cannot begin without explicit live
provider authorization and a real approved spend policy.
