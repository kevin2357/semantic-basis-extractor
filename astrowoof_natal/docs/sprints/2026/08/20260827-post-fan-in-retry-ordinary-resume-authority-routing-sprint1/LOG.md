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
