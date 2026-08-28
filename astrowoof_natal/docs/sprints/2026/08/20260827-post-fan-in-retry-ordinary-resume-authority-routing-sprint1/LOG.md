# Log — Post-Fan-In Retry Ordinary-Resume Authority Routing SBE Sprint 1

## 2026-08-27 — Planning

- Read and analyzed `Background.md`.
- Traced the lifecycle v0.7 local-work selector into exact and bounded runtime
  entry points.
- Identified a strong exact-route hypothesis: stored completed initial-wave lineage
  is treated too broadly as active initial-wave admission by command guards.
- Preserved uncertainty about native provider-ID/reconciliation state until a
  provider-free production-shaped reproduction proves the exact causal sequence.
- Added the pre-sprint huddle and detailed six-slice plan.
- No code, provider, retained-QA, deployment, or release action occurred.

Current gate: owner/API plan review before Slice 0.

## 2026-08-27 — Slice 0 complete

- Added a sanitized, production-shaped exact-interactive workspace with a complete
  joinable initial wave, terminal initial provider lineage, a retrieved creative
  retry, and the next prepared ordinary retry.
- Drove lifecycle v0.7 and the actual public semantic-closure resume dispatcher.
- Confirmed lifecycle v0.7 correctly selects one local fan-in operation.
- Confirmed exact command routing mistakes stored `DETACHED` initial-wave lineage
  for active initial admission.
- Proved ordinary authorization hits `aggregate_grant_required` without mutation
  or publication.
- Proved omitting authorization still re-enters the initial-wave branch, bypasses
  ordinary fan-in, and publishes unchanged detached-wave meaning.
- Characterized bounded interactive as already state-scoped to active initial-wave
  states; it does not share the exact predicate verbatim.
- Added `SLICE 0 - INCIDENT REPRODUCTION AND CAUSAL FINDINGS.md`.
- Focused characterization/regression run: 7 tests passed.
- Retained QA and provider services remained untouched.

Current gate: owner/API review of Slice 0 before Slice 1 contract freeze.

## 2026-08-27 — API Slice 0 review incorporated

- Added `API SLICE 0 REVIEW.md` to the sprint record.
- API approved the reproduction and exact-runtime causal boundary.
- Expanded Slice 1's matrix to distinguish retrieved completion, local fan-in,
  later ordinary v2 authority, and active initial-wave v1 aggregate authority.
- Froze `DETACHED` and other terminal/historical wave states as lineage only.
- Made ordinary-resume consumption/no-spin behavior explicit.
- Kept provider custody precedence and explicit Batch deferral/non-accidental
  inheritance in the contract gate.

Current gate: Slice 1 may begin; API review is required after Slice 1 before runtime
implementation.

## 2026-08-27 — Slice 1 complete

- Added `POST-FAN-IN ROUTING CONTRACT AND DECISION MATRIX.md`.
- Froze four noninterchangeable phases: v1 initial admission, provider custody,
  provider-free local fan-in, and later ordinary v2 paid continuation.
- Froze the active initial-wave set as `AWAITING_SPEND_AUTHORIZATION`,
  `AUTHORIZED`, and `SUBMITTING`.
- Froze `DETACHED` and `FAILED` as historical lineage; unknown states fail closed.
- Defined consuming ordinary-resume behavior and provider/ambiguity/refusal
  precedence.
- Recorded exact/bounded interactive applicability and deliberate ordinary-v2
  Batch deferral without weakening Batch retrieval custody.
- Concluded lifecycle v0.7 already carries the required public evidence; no schema
  or public command change is proposed.
- Added a closed four-route machine-readable decision fixture and mutation tests.
- Focused Slice 0/1 and post-fan-in matrix suite: 19 tests passed, 1 expected
  optional-schema skip.
- No production runtime, provider, retained-QA, or release action occurred.

Current gate: API contract review before Slice 2 runtime implementation.

## 2026-08-27 — API Slice 1 review incorporated

- Added `API SLICE 1 REVIEW.md`.
- API independently reproduced the 19-pass focused result with one expected
  optional-schema skip.
- Contract approved without schema or command changes.
- Slice 2 conditions confirm one centralized positive active-wave predicate,
  preservation of the v1 active fence, historical-lineage fallthrough to current
  facts, consuming-resume protection, and bounded non-regression.

Current gate: Slice 2 runtime implementation may proceed.

## 2026-08-27 — Slice 2 complete

- Added one centralized positive classifier for active versus historical
  initial-wave state.
- Updated exact ordinary-authorization guarding and initial-wave-mode selection to
  use the positive classifier instead of object presence.
- Updated bounded generic initial-wave fencing to use the same classifier without
  changing its existing active-state behavior.
- Exact stored `DETACHED` lineage now falls through to current local/provider/
  ordinary-authority facts.
- Active initial admission remains aggregate-grant fenced.
- Unknown/malformed stored wave states fail closed as `unsupported_contract`.
- Added nonmutation, active/historical-set, public-dispatch, and bounded parity
  coverage.
- Focused Slice 0–3 route suite: 24 tests passed.
- Wider initial-wave, external-authority, bounded, and Slice 2 suite: 77 tests
  passed.
- Provider/network/spend/retained-QA activity remained zero.

Current gate: Slice 3 composed runtime/failure qualification; API review follows
Slice 3.

## 2026-08-27 — Slice 3 complete

- Added a composed provider-free exact-interactive proof through not-due,
  due retrieval, durable completed evidence, local fan-in, operation consumption,
  ordinary v2 request/grant/intent/dispatch, and exact replay.
- Confirmed not-due reconciliation is byte-identical and retrieval-free.
- Confirmed due reconciliation returns `progressed_local`, accurately separating
  provider retrieval from semantic fan-in.
- Confirmed retained `DETACHED` initial-wave lineage no longer captures the public
  ordinary-resume path.
- Confirmed one scripted ordinary v2 create and zero duplicate creates on replay.
- Re-ran exact/bounded 4+2, all applicable response stages, ambiguity/fence, and
  deliberate Batch-deferral coverage.
- Focused composed/route/failure suite: 44 tests passed.
- Added `SLICE 3 - COMPOSED RUNTIME AND FAILURE QUALIFICATION.md`.

Current gate: API runtime/failure-boundary review before Slice 4.

## 2026-08-27 — API Slice 3 review incorporated

- Added `API SLICE 3 REVIEW.md`.
- API independently reran the focused Slice 1/3 suite: 19 passed with one
  expected optional-schema skip.
- API approved the composed runtime proof and made its promotion to a reusable
  installed-wheel fixture an explicit Slice 4 deliverable.
- The fixture must expose only validated public projections, bind stable fixture
  and receipt identities, and end at an SBE-owned delivery-ready or explicitly
  provider-pending boundary. API persistence, one-slot fairness, and reader
  delivery remain in the joined campaign.

Current gate: Slice 4 public fixture and adversarial qualification may proceed.

## 2026-08-27 — Slice 4 SBE qualification implemented

- Added a stable packaged post-fan-in scenario fixture and strict public reader.
- Added a closed receipt schema, Python runner/validator, and installed CLI entry
  point `astrowoof-post-fan-in-retry-qa`.
- The provider-free runtime materializes a disposable native workspace and proves
  not-due, retrieval, local fan-in, consumed operation, ordinary-v2 authority,
  one dispatch, exact replay, and an explicit provider-pending endpoint.
- Added privacy, mutation, schema, fixture, CLI, and output validation coverage.
- Updated the adversarial simulation playbook and added the API handoff.
- Focused Slice 4 qualification: 5 passed with one expected optional-schema skip.
  Combined Slice 1–4 routing/qualification suite: 25 passed with one expected
  optional-schema skip.

Current gate: API fixture-by-fixture review and joined one-slot campaign.

## 2026-08-27 — API Slice 4 reproducibility correction

- Added `API SLICE 4 REVIEW.md` and accepted its reproducibility finding.
- Replaced full lifecycle/result hashing with closed semantic evidence projections
  that retain route, mechanism, command, capacity, custody, ordered action/local
  work, outcome, and replay facts while excluding ephemeral logical-root,
  snapshot, and wall-clock identities.
- Added a two-invocation regression requiring identical ordered phase digests,
  endpoint digest, receipt digest, and complete receipt bytes.
- Focused qualification: 6 passed with one expected optional-schema skip.
- Combined Slice 1–4 routing/qualification suite: 26 passed with one expected
  optional-schema skip.

Current gate: API Slice 4 re-review before installed-wheel qualification.

## 2026-08-27 — API Slice 4 re-review approved

- Added `API SLICE 4 RE-REVIEW.md`.
- API independently confirmed identical phase, endpoint, and receipt identities
  across fresh temporary workspaces.
- API approved Slice 5 installed-wheel qualification without further contract or
  runtime changes.
- Candidate version advanced to fresh unpublished patch `0.4.27`.

Current gate: Slice 5 installed-wheel and compatibility qualification.

## 2026-08-27 — Slice 5 SBE candidate qualification complete

- Locked candidate source at commit `e1a22ab` with fresh version `0.4.27`.
- Built twice from that source with fixed `SOURCE_DATE_EPOCH=1787844361`.
- Both wheels are byte-identical: 1,048,593 bytes, SHA-256
  `ae8da7a7ce64cd83e1a4444fb8a77587eafb1c1f5a7ff1cc3ac615dfb51e611a`.
- Inspected the wheel and confirmed `py.typed`, the post-fan-in fixture, its
  closed receipt schema, and `astrowoof-post-fan-in-retry-qa` are packaged.
- Installed the candidate outside the checkout with exact SPC `0.11.1`.
- Installed generic release smoke, adversarial qualification, and post-fan-in
  qualification all passed.
- Two fresh installed post-fan-in invocations produced identical receipt bytes,
  SHA-256
  `0db488713ad4711f52431d0a65187d6103f7784e41cd9a2c1d192c5af7eee074`.
- Full source suite: 829 passed, 40 expected environment/opt-in skips.
- External provider/network calls, spend, and retained-QA access remained zero.

Current gate: API/Linux joined-candidate review before Slice 6 release decision.

## 2026-08-27 — API Slice 5 review incorporated

- Added `API SLICE 5 REVIEW.md`.
- API independently ran the installed public runner outside the checkout and
  confirmed its provider-pending endpoint and reproducible receipt/phase evidence.
- API approved source `e1a22ab`, version `0.4.27`, and wheel SHA-256
  `ae8da7a7ce64cd83e1a4444fb8a77587eafb1c1f5a7ff1cc3ac615dfb51e611a`
  as the exact joined-campaign candidate.
- Publication, deployment, provider work, spend, and retained-QA recovery remained
  explicitly unauthorized pending the joined campaign.

## 2026-08-27 — Joined-campaign handoff blocker accepted

- Added `API JOINED-CAMPAIGN BLOCKER REVIEW.md`.
- The existing receipt remains valid SBE qualification evidence, but its opaque
  phase hashes cannot exercise API's real lifecycle translator and scheduler.
- Added corrective Slice 4A for a closed, sanitized, ordered public
  inspection-projection bundle covering the existing seven phases.
- The previously qualified wheel remains historical pre-4A evidence. Slice 5 must
  be repeated from committed 4A source before the joined campaign or release.

Current gate: Slice 4A implementation, followed by API projection-bundle review.

## 2026-08-27 — Corrective Slice 4A implemented

- Added closed contract `astrowoof.post_fan_in_retry_inspection_bundle.v1`.
- Added a packaged schema plus public Python reader, runner, and strict validator.
- Extended the installed qualification CLI with `--inspection-bundle` and
  `--inspection-bundle-schema`.
- Published the seven exact ordered lifecycle projections needed by API while
  excluding private workspace/provider evidence.
- Bound each phase, the complete bundle, the existing fixture, and the existing
  qualification receipt by canonical SHA-256 identities.
- Froze scripted post-dispatch scheduling evidence so independent temporary
  workspaces reproduce exact bundle bytes.
- Focused bundle/receipt suite: 9 tests passed, 1 expected optional-schema skip.
- Adjacent Slice 1–3 regression suite: 20 tests passed.
- External provider/network calls, spend, and retained-QA access remained zero.

Current gate: API Slice 4A contract and fixture review before rebuilding Slice 5.

## 2026-08-27 — API Slice 4A receipt-binding correction

- Added `API SLICE 4A REVIEW.md` and reproduced its integrity finding.
- Refactored shared provider-free artifact construction to avoid recursive public
  validation.
- The public bundle validator now reconstructs the canonical qualification receipt
  and requires the claimed receipt identity to match it exactly.
- Added the requested mutation: replace only the receipt digest, recompute the
  outer bundle digest, and require refusal.
- Focused Slice 4A suite: 10 passed, 1 expected optional-schema skip.
- Adjacent Slice 1–3 suite: 20 passed.

Current gate: commit corrected source, build a fresh post-4A candidate, and repeat
installed qualification before the API joined campaign.

## 2026-08-27 — Fresh post-4A candidate qualified

- Corrected artifact source: `9205235`.
- Rebuilt `0.4.27` twice with fixed `SOURCE_DATE_EPOCH=1787872684`.
- Both wheels are byte-identical: 1,051,330 bytes, SHA-256
  `db5ff09afce53b063dea1b29d8fcb94af581bcf383f7cab5da1d65cc0d4e48ed`.
- Installed outside the checkout with exact SPC `0.11.1`.
- Installed receipt and ordered-bundle commands passed; the bundle's receipt
  reference exactly matched the installed canonical receipt.
- Installed adversarial qualification passed.
- Generic installed release smoke reached `DELIVERY_COMPLETE` and completed
  cleanup successfully.
- Receipt identity:
  `982f8e3044c7e20a9324d44c61867af5e1787d2d996289ad7fe57aff19e6f2b9`.
- Bundle identity:
  `75247d8652698e122c46fc79480bbf5b73fd0671b8cb38cb6aa5671eaab2a8a4`.
- External provider/network calls, spend, and retained-QA access remained zero.

Current gate: API consumes this exact replacement candidate in the joined
campaign; the pre-4A wheel is superseded.

## 2026-08-27 — API Slice 4A re-review approved

- Added `API SLICE 4A RE-REVIEW.md`.
- API independently confirmed the canonical receipt join and requested mutation
  refusal: 10 passed, 1 expected optional-schema skip.
- API approved the replacement wheel SHA-256
  `db5ff09afce53b063dea1b29d8fcb94af581bcf383f7cab5da1d65cc0d4e48ed`
  for the joined provider-free campaign.
- The older pre-4A wheel with the same unpublished version is explicitly
  superseded and must not be selected by version string alone.

Current gate: API/Linux joined campaign against the exact replacement digest.

## 2026-08-27 — API Slice 5 re-review recorded

- Added `API SLICE 5 RE-REVIEW.md`.
- API approved the post-4A wheel digest `db5ff09a...d4e48ed` as the exact joined-
  campaign input and independently confirmed its installed evidence.
- Publication/deployment remained withheld.

## 2026-08-27 — Corrective Slice 4B requested

- Added `API SLICE 4B PUBLIC HAPPY-PATH WITNESS REQUEST.md`.
- Added two representative installed-engine witnesses: two retries with out-of-
  order completion, and retry followed by one supported downstream ordinary stage.
- Preserved the generated simulator as broad combinatorial evidence and the new
  witnesses as narrow claims about real installed SBE behavior.
- Added a production-path characterization requirement before freezing the exact
  downstream stage; no lifecycle/stage prerequisite may be fabricated or weakened.
- The post-4A wheel remains valid historical evidence but is superseded as the
  future joined-campaign artifact because 4B changes the packaged surface.

Current gate: Slice 4B production-path characterization and implementation,
followed by API witness review and another fresh Slice 5 candidate.

## 2026-08-27 — Slice 4B production-path characterization

- Reproduced out-of-order completion with two provider-bound creative retries.
- Found a real mixed-custody branch gap: capacity reports
  `continue_local_cycle/local_work_ready`, but command selection falls through to
  `none` when the older dependency projection is empty.
- Identified the narrow correction: completed provider evidence selects
  `ordinary_resume`; v0.7 remains responsible for a concrete local-work inventory.
- Confirmed retained custody still prevents either prepared successor from
  dispatching until the other provider operation is reconciled.
- Identified the truthful authority shape as distinct exact successor members in
  one aggregate ordinary-v2 action-set request when both become eligible.
- Confirmed polish is the preferred downstream witness only if normal final-
  assembly prerequisites are driven through production orchestration.
- Added `SLICE 4B - PRODUCTION PATH CHARACTERIZATION AND CONTRACT QUESTION.md`.

Current gate: API confirms aggregate-member interpretation before Slice 4B runtime
correction and fixture implementation.

## 2026-08-27 — API interpretation approved; selector corrected

- Added `API SLICE 4B PRODUCTION-PATH INTERPRETATION.md` and the API's clarified
  original request.
- Froze one aggregate `ordinary_action_set` envelope with distinct exact member
  bindings/authorization documents when successors become co-ready.
- Preserved retained provider-custody precedence and all-or-none API admission.
- Corrected mixed-custody command selection so completed provider evidence selects
  `ordinary_resume` even when the older dependency projection is empty.
- Updated v0.5 semantic validation and terminal continuation evidence consistently;
  v0.7 remains the source of the concrete local operation.
- Added a production-shaped regression proving the later retry can complete and
  select its exact local operation while the earlier retry remains retained.

Current gate: public Witness A and Witness B artifact implementation.

## 2026-08-27 — Slice 4B public happy-path witnesses

- Implemented one aggregate ordinary-v2 action-set for co-ready successors while
  preserving separate member bindings, authorization documents, and paid-action
  authority.
- Preserved custody precedence: a prepared successor remains masked until all
  retained provider custody has cleared.
- Added `astrowoof-ordinary-v2-happy-path-qa`, two closed schemas, and a closed
  packaged fixture inventory.
- Added real-engine witnesses for out-of-order two-retry completion and
  retry-to-enabled-qualitative-critic continuation.
- Both witnesses end at truthful detached provider-pending custody and prove exact
  replay without duplicate create or local consumption.
- Public projections use reproducible semantic request/grant digests plus exact
  per-member binding and authorization-document digests.

Current gate: API reviews the Slice 4B public contract and fixture evidence before
installed-wheel/release qualification resumes.

## 2026-08-27 — Slice 4B evidence-scope correction

- Accepted API review's distinction between production-shaped setup and the real
  selector/authority boundary exercised by the witnesses.
- Added the closed `post_fan_in_selector_authority_and_replay` scope to the
  packaged fixture and every public witness projection.
- Added exact machine-readable inventories of fixture-installed precursor facts.
- Narrowed handoff claims: these witnesses prove post-fan-in selection, custody,
  authority, dispatch, and replay; they do not prove upstream semantic evaluation,
  QA acceptance, natural successor generation, or product-policy selection.

Current gate: rerun source and installed-wheel evidence, then API re-review.

## 2026-08-27 — Slice 4B API re-review approved

- Added `API SLICE 4B RE-REVIEW.md`.
- API accepted the closed evidence scope, machine-readable precursor inventory,
  aggregate authority topology, deterministic installed artifacts, and privacy
  boundary without further contract changes.
- Slice 4B is approved for fresh committed-source installed-wheel and release
  qualification.

Current gate: Slice 5 qualification from the committed post-4B source identity.

## 2026-08-27 — Slice 5 adjacent regression corrected

- The broad gate caught an adjacent contradiction in the mixed-custody selector:
  completed provider evidence was marking local continuation while another
  provider action was already due for retrieval.
- Narrowed the rule: completed evidence selects local fan-in only when the run is
  nonterminal and no retained provider action is presently due.
- This preserves the Slice 4B pending/not-due fan-in case, preserves retrieval
  precedence for due custody, and keeps nonblocking completed optional evidence
  from reopening a terminal run.
- Added a regression covering the same workspace at not-due and later-due times.

Current gate: commit the correction, then restart deterministic build and broad
qualification from the new source identity.

## 2026-08-27 — Final post-4B Slice 5 qualification complete

- Final candidate source: `adbbc70`.
- Built twice with `SOURCE_DATE_EPOCH=1787874000`; both wheels are byte-identical
  at 1,060,420 bytes and SHA-256
  `210ed3c98bcc84c2cfe9e9669edebaa56a1780bc1bb8057e61c0fffbd0c4c276`.
- Installed outside the checkout with exact SPC `0.11.1`.
- Generic installed release smoke passed and reached `DELIVERY_COMPLETE`.
- Installed adversarial qualification, post-fan-in retry qualification, and both
  scoped happy-path witnesses passed.
- Two installed happy-path receipts were byte-identical; receipt-file SHA-256
  `31c46af0692d20b8dcecb118b52349b5c5bf5dcde1955e1b9cf37ada710c7588`.
- Full source suite: 839 passed, 41 expected environment/opt-in skips, in
  833.803 seconds.
- `git diff --check` passed.
- External provider/network calls, spend, and retained-QA access remained zero.

Current gate: API consumes the exact final candidate digest in its joined campaign
before Slice 6 release decision.

## 2026-08-27 — API final candidate approval and Slice 6 preparation

- Added `API SLICE 5 FINAL CANDIDATE REVIEW.md`.
- API consumed exact source `adbbc70` / wheel SHA-256 `210ed3c9…c276` and passed
  10 focused installed campaign tests in API commit `abcc024`.
- API approved the candidate for SBE release with no remaining contract changes.
- Prepared the 0.4.27 release notes, compatibility, known-limitations/retained-
  cohort posture, consumer routing handoff, and machine-readable manifest.
- Release records distinguish artifact source from the later release-lock commit.

Current gate: commit release preparation, then explicit owner authorization before
tag or publication.

## 2026-08-27 — Slice 6 final release approval

- Added `API SLICE 6 FINAL RELEASE REVIEW.md`.
- API release-pair coverage passed 23 tests against exact candidate digest
  `210ed3c9…c276`; API commit `8dc7ede`.
- API and owner approvals are unconditional for immutable 0.4.27 tag/publication.
- Release-review checkpoint: `db736e7e8ced31f85f5b1f9d6a8f2746f1ae1dcf`.

Current gate: commit the release lock, rebuild/verify exact artifact bytes, then
tag, publish, download-verify, and record post-publication evidence.

## 2026-08-27 — SBE 0.4.27 published and verified

- Release lock and immutable tag target:
  `f04551e50b19cfe38dae495d008f91287b34132d`.
- Published tag: `astrowoof-natal-authoring-v0.4.27`.
- GitHub release ID: `378229362`; published at `2026-08-28T02:31:44Z`.
- Downloaded the published wheel and checksum asset into a fresh verification
  directory.
- Downloaded wheel size: 1,060,420 bytes.
- Downloaded wheel SHA-256 and GitHub asset digest both equal
  `210ed3c98bcc84c2cfe9e9669edebaa56a1780bc1bb8057e61c0fffbd0c4c276`.
- Published checksum asset SHA-256:
  `bce08ac3d501c7362f87b398183f3617837f6ba6b45cd589d741a3cfdda963e2`.

Status: sprint and immutable 0.4.27 publication complete.
