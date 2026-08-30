# Sprint log

## 2026-08-29 — Slice 8 release qualification

- Recorded API Voof-paws 6 approval and bumped the fresh candidate to `0.4.29`;
  immutable `0.4.28` was not reused.
- The first broad run exercised 879 tests and exposed three release-only/adjacent
  compatibility seams: exact retry enforcement leaked into a bounded route and a
  minimal spend fixture, while the terminal-review fixture still identified
  `0.4.28`.
- Narrowly corrected those three cells and reran each directly: 3 passed.
- Reran the complete suite from corrected source: 879 passed, 44 expected skips.
- Locked artifact source commit `f6a045b`, then produced two byte-identical wheels
  under a fixed source epoch.
- Installed the exact wheel in a fresh Python 3.11 environment; generic release
  smoke, lifecycle smoke, retry-lineage, terminal-review, post-fan-in, and
  adversarial qualifications all passed.

Status: Slice 8 complete; owner/API release approval recorded. Tag and publication
may proceed from the release-lock commit while preserving `f6a045b` as the exact
artifact source identity.

## 2026-08-28 — Slice 7 installed-wheel surface and consumer handoff

- Incorporated API Voof-paws 5 approval and its explicit interactive-only scope.
- Added the closed packaged retry-lineage qualification schema and public Python
  reader/validator/runner exports.
- Added the `astrowoof-retry-lineage-qa` provider-free console command with no
  production inputs and a native-workspace output refusal.
- Added package/schema identity to the qualification receipt and validated it
  against Draft 2020-12 where `jsonschema` is available.
- Added a closed consumer handoff and a hash-bound fixture manifest covering the
  v0.8 root, lineage sub-contract, qualification schema, and mixed-custody fixture.
- Built and installed the candidate wheel into a clean Python 3.11 virtual
  environment and ran the console command plus public readers from site-packages.

Status: Slice 7 complete; paused at Voof-paws 6. Release preparation has not
begun and remains unauthorized.

## 2026-08-28 — Slice 6 provider-free runtime qualification

- Added a deterministic qualification runner over fresh exact- and
  bounded-interactive native workspaces.
- Both routes prove exact replay, provider-custody-first reconciliation, and the
  post-custody `retry_lineage_conflict_requires_review` disposition.
- The qualification executes the forward-create fence against prepared,
  authorized, call-entered, durable-provider-identity, and reported evidence.
- Added a real completed-predecessor/current-incomplete feedback assertion rather
  than declaring that property in the receipt.
- The closed receipt is stable across fresh temporary roots and contains no
  logical paths, payloads, prompts, bindings, provider configuration, or subject
  prose.

Status: Slice 6 complete; paused at Voof-paws 5 for API fixture/runtime review.

## 2026-08-28 — Slices 4–5 runtime correction

- Recorded API barkproval from `API VOOF-PAWS 4 RE-REVIEW.md`.
- Exact retry preparation now selects feedback from completed predecessor
  attempt numbers/states and excludes the incomplete current attempt.
- First preparation persists one attempt key/action/binding/request/payload
  evidence unit; re-entry reuses it instead of minting another action.
- Exact creative-retry forward dispatch now preflights the whole ledger and
  rejects duplicate/conflicting logical lineages before provider I/O.
- Added lifecycle v0.8 runtime inspection and public
  `inspect-retry-lineage` CLI operation.
- Mixed conflict plus provider custody selects retrieval-only reconciliation;
  after custody settles it becomes typed non-dispatching review.

## 2026-08-28 — Slice 3 contract freeze

- Incorporated the complete API Voof-paws 3 review document.
- Froze attempt identity on run/route/stage/pass/attempt only; request and binding
  remain attached evidence.
- Added closed retry-lineage inventory v1 and lifecycle v0.8 contracts.
- Separated forward-dispatch refusal from retrieval-only reconciliation safety.
- Paused before runtime mutation at Voof-paws 4.
- Incorporated Voof-paws 4 corrections: exact whole-inventory/custody joins,
  complete lifecycle-v0.8 schema/reader, and aggregate conflict classification.
  Runtime work remains paused for re-review.

## 2026-08-28 — Planning

- Reviewed the waiting investigation background and the completed terminal-review
  handoff sprint's retained-checkpoint findings.
- Confirmed that the prior inspection proved hash-valid retained workspaces but no
  sealed terminal transition, leaving the editorial cause unresolved.
- Structured an evidence-first investigation with conditional continuation rather
  than presuming a runtime defect.
- Identified controlled read-only R2 inspection as the highest-value first evidence
  step after the protocol is frozen and reviewed.

Status: planning complete; paused before Slice 0 for owner approval.

## 2026-08-28 — Slice 0 evidence map and inspection protocol

- Froze both API/native run identities, active checkpoint generations, archive
  byte counts, and declared member counts from the previously verified inspection.
- Defined an exact protected-authority input requirement so R2 objects cannot be
  guessed from bucket listing, size, recency, or neighboring generations.
- Defined a `HEAD=2`, `GET=2`, all-writes-zero remote boundary and prohibited every
  SBE/provider execution path.
- Defined whole-archive, complete-inventory, path-containment, member-hash, logical
  root, and native-run validation before evidence interpretation.
- Froze exact action/pass/attempt/provider/binding joins, sanitization rules,
  access-receipt fields, refusal posture, and confidence rubric.
- Added `slice0-inspection-manifest.json` binding the incident background and
  inspection protocol.

Status: Slice 0 complete; paused at Voof-paws 1. No retained bytes or credentials
were accessed.

## 2026-08-28 — Voof-paws 1 API approval

- API approved the bounded read-only inspection without widening its remote or
  mutation boundary.
- Added the required claim-level provenance-pointer rule and clarified that the
  authority input must contain actual expected checkpoint-contract and
  compatibility-identity values.
- Corrected the stale pre-Slice 0 evidence status wording.
- Reviewed API Sprint 55 status: released SBE 0.4.28 intake is underway; its newly
  persisted immutable API action-binding projection is an API ingestion
  prerequisite and does not alter this causal investigation.

Status: ready for Slice 1 once exact protected checkpoint authority and temporary
R2 credentials are available.

## 2026-08-28 — Slice 1 first bounded attempt stopped locally

- Validated the uncommitted protected authority document at
  `C:\tmp\astrowoof-sbe-pippin-duchess-checkpoint-authority-20260828.json`;
  authority SHA-256 is
  `1a21adf1b125304e9a1baa7ded358e32eb7f564b2c4489b812e79289462dcbf1`.
- Confirmed exact frozen subject/generation/archive identities, valid archive and
  inventory digests, actual checkpoint contract/compatibility values, and the
  approved two-HEAD/two-GET zero-write boundary.
- The first exact checkpoint passed remote HEAD metadata and downloaded archive
  byte/hash validation.
- Local whole-inventory validation stopped because the inspection script omitted
  the checkpoint archive contract's trailing newline when reproducing the
  canonical inventory digest. The archive was held only in memory and was not
  saved; the second subject was not contacted.
- Remote operations consumed by this failed attempt: HEAD 1, GET 1, list/write 0.
- Fixed the local serializer and proved the validator against an independently
  generated production-format checkpoint archive without remote access.

Status: stopped before exceeding the frozen remote budget. A fresh bounded retry
requires explicit owner/API acknowledgement; no causal inspection has begun.

## 2026-08-28 — Slice 1 retry stopped on path-identity guard

- Owner and API explicitly approved a fresh two-subject retry after the local
  canonicalization correction.
- The first exact object again passed HEAD metadata, archive byte count, and
  archive SHA-256 validation; complete inventory digest validation also passed.
- Validation stopped because the archive's native workspace snapshot logical root
  did not equal the API checkpoint authority's `logical_restore_path`.
- The script still saved only after all semantic checks, so the in-memory archive
  was not retained; Duchess was not contacted.
- Retry remote counts: HEAD 1, GET 1, list/write 0. Cumulative failed-attempt
  counts: HEAD 2, GET 2, list/write/provider/mutation 0.
- Hardened the local tool so any future exact hash-verified download is persisted
  before semantic interpretation and both independently authorized subjects obtain
  a bounded validation result. This prevents another local semantic refusal from
  discarding already verified evidence bytes.

Status: stopped again. The path mismatch is not being waived or normalized; one
final bounded evidence-preserving retry requires explicit acknowledgement.

## 2026-08-28 — Slice 1 completed from verified retained bytes

- Owner explicitly authorized the final two-object QA inspection and clarified
  that diagnosis should not remain blocked by self-imposed restrictions beyond
  the real no-mutation/no-provider boundary.
- Performed exactly two additional HEADs and two GETs. Both archives passed exact
  byte/hash, complete inventory, and declared-member validation and were saved
  for offline read-only interpretation.
- Recorded a real metadata discrepancy rather than normalizing it: API authority
  names the API-run-ID restore path, while both native snapshots bind distinct
  worker-workspace UUID roots.
- Reconstructed both lineages. In both runs, passes 1–5 accepted attempt 1; pass
  6 rejected attempts 1 and 2 with `theme_group_coverage`; attempt 3 remained
  `AWAITING_SPEND_AUTHORIZATION`.
- Both ledgers independently show the same four-retry-action custody pattern:
  an older provider-pending attempt-2 action, a later reported attempt-2 action,
  an authorized/providerless attempt-3 action, and a second prepared attempt-3
  action. The reported attempt-2 action and current prepared attempt-3 action
  share a request digest in each run.
- The retained checkpoint does not contain the later API
  `native.review.requires_review` observation. Its last sealed transition is
  still `provider_pending`; therefore the later API decision cannot be recast as
  a native terminal editorial transition.
- Source inspection explains that later API mapping: v0.7 post-fan-in inspection
  forces any authorized/providerless action to `retain_for_review`, even when
  provider custody and a prepared successor coexist. API maps that nonterminal
  disposition to `native.review.requires_review`.

Status: Slice 1 complete; paused at Voof-paws 2. Slice 2 should reproduce the
exact provider-free lineage and distinguish the stale-authority/request-binding
defect from the broader review/custody projection behavior.

## 2026-08-28 — Owner theme-group policy context

- Recorded that theme groups support an unimplemented filtering concept whose
  current taxonomy is provisional.
- Refined the retained evidence: both failures were `theme_group_coverage`, not
  the narrower `theme_group_balance` predicate.
- Owner clarified that theme-group policy is context, not a sprint priority. The
  investigation remains focused on stable, consistent, reliable state transitions
  across any legitimate retry-triggering failure.
- Theme-group policy was removed as a conditional implementation path. The
  historical code may remain a reproduction trigger, but the correction must be
  failure-modality-independent.

Status: still paused at Voof-paws 2. Slice 2 centers action lineage, binding,
custody precedence, idempotence, and review mapping.

## 2026-08-28 — Slice 2 provider-free causal reproduction

- Reproduced the exact authorized-plus-prepared duplicate attempt-3 topology
  through the production retry loop with zero provider calls.
- Proved the first preparation includes completed predecessor QA feedback, while
  re-entry sees the incomplete attempt as the last record, loses that feedback,
  changes request bytes, and prepares a second action for the same route.
- Proved current v0.7 semantic validation accepts duplicate route identities with
  different bindings and does not enforce one action lineage per pass attempt.
- Proved base lifecycle inspection correctly selects the retained provider action
  for reconciliation, while post-fan-in v0.7 overwrites that decision with
  `none / retain_for_review` because a separate authorized/providerless action
  exists.
- Proved identical lifecycle behavior for historical `theme_group_coverage` and
  a generic legitimate QA-rejection code.
- Ran the focused plus adjacent precedence/matrix suite: 12 passed; zero network,
  provider, spend, or retained-workspace activity.

Status: Slice 2 complete; paused at Voof-paws 3 before freezing implementation
slices.

## 2026-08-28 — SBE implementation continuation drafted

- Incorporated API review that the investigation proves a general QA-retry
  lifecycle defect rather than a one-run or theme-group-specific theory.
- Corrected stale plan/evidence gate wording.
- Added proposed Slices 3–8 covering contract freeze, idempotent attempt binding,
  whole-ledger integrity/custody precedence, holistic provider-free qualification,
  installed-wheel/API handoff, and release preparation.
- Added explicit API review pauses before runtime implementation, after consumer
  fixtures, and before release preparation/adoption.

Status: planning only; paused at Voof-paws 3. No implementation is authorized.
