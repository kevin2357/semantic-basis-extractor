# Sprint 1 Log

## 2026-08-23 — Planning created

- Companion to API Sprint 36.
- No retained run or provider operation touched.

## 2026-08-23 — SBE pre-sprint review and plan refinement

- Confirmed the current failure mechanism: API persists one full inspection per
  snapshot and rejects a valid later clock-relative scheduling decision.
- Corrected the conceptual model: actual provider result/status evidence cannot
  evolve through provider-free lifecycle inspection; supported reconciliation
  must observe and durably checkpoint it.
- Split the proposed contract into immutable checkpoint basis and temporal
  scheduling decision, each with a canonical digest.
- Kept append-only temporal history and trusted clock ordering API-owned while
  preserving SBE ownership of native evidence and due-member selection.
- Added external-authority request timestamp/digest churn to the explicit audit.
- Expanded provider-free gates, cross-route compatibility, installed-wheel
  qualification, privacy, and retained-run non-mutation boundaries.
- No source, schema, provider, retained-run, spend, or API database changes.
- Paused before Slice 0 for owner and API review.

## 2026-08-23 — API contract review incorporated

- Accepted canonical normalized-UTC `observed_at` supplied by the API trusted
  clock for persisted sequencing.
- Froze custody schedule and `resume_not_before` into the immutable checkpoint
  basis.
- Narrowed temporal changes to eligibility/reason, supported command, SBE-owned
  bounded due subset, and derived `not_before`.
- Adopted the preferred stable external-authority request binding: immutable
  basis plus exact ordered action inventory, not incidental observation time.
- Clarified decision-relevant append-only persistence with an explicit API
  retention policy rather than unbounded storage of harmless polls.
- Clarified that lease/custody controls prevent duplicate invocation and that
  retrieval/checkpointing creates a new basis.
- Retained the pre-Slice-0 joint schema/semantic review gate.
- Recorded that `capacity_disposition` is native/local SBE scheduling evidence,
  never API-global admission, slot, reservation, or spend-capacity state.

## 2026-08-23 — Slice 0 complete

- Added a provider-free six-member fixture reproducing two valid lifecycle v0.5
  projections from one byte-identical workspace and snapshot.
- Proved `t0` not-due then `t1` due, with the due command naming SBE's bounded
  four-of-six subset.
- Proved same checkpoint plus same canonical time is exact replay.
- Froze the exact v0.5 changed-path inventory and published the candidate field
  classification and transition matrix.
- Verified that inspection performs no workspace mutation and that all native
  and provider facts remain stable under the checkpoint.
- Focused tests: 32 passed.
- Gate: paused before Slice 1 for SBE/API review.

## 2026-08-23 — Slice 1 complete

- Added strict lifecycle inspection v0.6 projection with separately canonicalized
  checkpoint-basis and temporal-decision digests.
- Structurally removed copied observation time and native due subset from the
  immutable basis.
- Added canonical whole-second UTC normalization and validation.
- Added pure single-document and prior/current transition validators with closed
  regression reasons.
- Added a v2 external-authority request identity bound to basis digest and exact
  ordered action inventory, independent of observation time.
- Added packaged JSON schemas and root-package public exports.
- Focused tests: 39 passed, 1 skipped because the lean host lacks `jsonschema`;
  both packaged schema documents parsed successfully.
- Gate: paused before Slice 2 for joint schema/semantic review.

## 2026-08-23 — Slice 1 API review corrections

- Removed duplicate v2 authority constants/builders/validators and added a
  root-package import/export smoke test.
- Added strict deep semantic validation for native observation identity, route,
  terminal/quiescence, dependencies, ordered action inventory and complete
  bindings, custody operations and schedule, consumer authority, and closed
  vocabularies/joins.
- Added negative cases for rehashed invalid route, provider identity, binding,
  and consumer-authority facts.
- Added
  `validate_external_authority_request_v2_against_inspection()` and proved that
  a changed member binding makes the original request fail its basis join.
- Clarified that a standalone request is a reference, never authorization or
  sufficient reconstruction material.
- Focused tests: 42 passed, 1 environment-dependent schema test skipped.
- Gate remains paused before Slice 2 for API confirmation.

## 2026-08-23 — Slice 1 primitive-validator parity

- Added Python-level nonempty run-ID and lowercase 64-hex digest validation.
- Added the closed v2 request-kind vocabulary.
- Added canonical `paid_[0-9a-f]{24}` validation across request, checkpoint
  inventory, custody, consumer-authority, blocking, and due-subset identities.
- Added lean-host negative tests for rehashed null run identity, unknown request
  kind, malformed action IDs, and uppercase/noncanonical digest identity.
- Focused tests: 43 passed, 1 optional-`jsonschema` case skipped.
- Gate remains paused before Slice 2 for API confirmation.

## 2026-08-23 — Slice 2 complete

- Extended the installed provider-pending qualification through v0.6 not-due,
  due, real reconciliation, and changed-checkpoint evidence.
- Added pre/post checkpoint-basis hashes to the qualification receipt.
- Proved six unique creates, bounded four-plus-two retrieval, six durable response
  artifacts, and no duplicate create or retrieval.
- Added focused proof that a second reconciliation makes zero retrieval calls
  once completed evidence is durable.
- Added fresh-process reconstruction of the exact new basis.
- Added refusal of a rehashed/reordered due subset.
- Focused tests: 47 passed, 1 optional-`jsonschema` test skipped.

## 2026-08-23 — Slice 3 complete

- Proved lifecycle v0.6 not-due/due parity for exact interactive, exact Batch,
  bounded interactive, and bounded Batch v2.
- Proved enabled polish/critic/candidate response-stage projection for exact and
  bounded routes.
- Preserved explicit refusal for actions that claim unsupported Batch transport
  on optional stages.
- Fixed bounded Batch dispatch to require the actual bounded v2 native contract,
  not merely a v2-shaped action route string.
- Proved legacy bounded v1 Batch fails closed.
- Focused temporal/provider-pending tests: 50 passed, 1 optional-schema skip.
- Existing production bounded Batch detach/retrieve and retrieval-only tests: 2
  passed.
- Gate: paused for API fixture/compatibility review before Slice 4.

## 2026-08-23 — Slice 4 complete

- Added supported read-only `inspect_temporal_lifecycle()` and CLI
  `inspect-temporal`, requiring explicit trusted observation time.
- Preserved existing v0.5 `inspect` behavior unchanged.
- Added public packaged-schema readers and source/CLI read-only tests.
- Built preliminary candidate wheel SHA-256
  `0385b61614e654f05b711ae6aed0418d4094b5413b91bf877103ad106f7d9ea7`;
  superseded by the post-cleanup candidate below.
- Installed the wheel into an isolated target and ran provider-pending
  qualification successfully: six creates, six retrievals, distinct pre/post
  basis hashes, packaged schema readable.
- Verified both packaged schema readers, the inspection/join exports, and the
  installed module CLI's `inspect-temporal` command.
- Focused source tests: 54 passed, 1 optional-schema skip.
- Published API consumer handoff and compact installed-wheel receipt.
- Reordered Slice 1 primitive parity evidence chronologically.
- Gate: final API consumer review before version bump/release recommendation.

## 2026-08-23 — Slice 4 release-blocking reader cleanup

- Removed duplicate definitions of the temporal inspector and both schema
  readers, retaining one canonical public definition each.
- Added an AST-level singular-definition regression in addition to public
  import/export smoke.
- Focused tests: 55 passed, 1 optional-schema skip.
- Rebuilt candidate wheel SHA-256
  `e77b370926ce96df548331e3aa18a14632b80d479d5aafe4ff2eb132d5450fd3`.
- Reinstalled the wheel in a fresh isolated target; provider-free qualification
  passed with six creates, six retrievals, distinct pre/post bases, and singular
  installed reader definitions.
- Gate: ready for version bump/release recommendation after owner authorization.

## 2026-08-23 — 0.4.16 immutable artifact qualification

- API and owner approved the fresh patch release.
- Bumped distribution version to `0.4.16` and committed artifact source as
  `9591385fccfcf635d8371b12135a4d25c654166a`.
- Complete source suite passed: 583 tests with 28 existing environment-dependent
  skips.
- Built the exact wheel twice with the source commit epoch; both builds produced
  SHA-256 `56e26d82bb4689907dc830903721acf34a4c385557c7825c3ece19297f48d339`.
- Fresh-venv installed release smoke and provider-pending qualification passed.
- No provider network call, credential, paid work, or retained QA workspace was
  used.

## 2026-08-23 — 0.4.16 publication

- Created and pushed annotated tag `astrowoof-natal-authoring-v0.4.16` at
  `21705500a3aa6c5f3310a0aaee8aee8a71e4bdac`.
- Published GitHub release `375150470` with the qualified wheel and checksums.
- GitHub reports wheel asset `525987851` at 893028 bytes with SHA-256
  `56e26d82bb4689907dc830903721acf34a4c385557c7825c3ece19297f48d339`.
- Published digest matches the local qualified artifact exactly.
- This post-publication documentation commit does not move the immutable tag.
