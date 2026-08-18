# Native Terminal Transition Journal Sprint 1 Log

Status: planned; implementation has not started.

- Reviewed AstroWoof API Sprint 26 `BACKGROUND.md`, `PLAN.md`, `LOG.md`, and
  `EVIDENCE.md`.
- Confirmed the historical Aster run is a forensic fixture only and must not be
  repaired, mutated, or used to backfill uncertain cost.
- Mapped API Sprint 26's shared Slice 1, SBE Slice 3, and shared Slice 6 into a
  complete SBE-owned implementation and qualification sequence.
- Preserved inspection v0.3 and reconciliation result v0.2 as the route/custody
  substrate rather than proposing a competing vocabulary.
- Planning created no runtime/schema mutation, provider operation, paid spend,
  build, version bump, tag, or release.
- API review approved the ownership, route-parity substrate, historical non-repair,
  and overall slice structure with no blocker.
- Added mandatory API pauses after the Slice 0 reproduction/crash-window inventory,
  the Slice 1 contract freeze, the Slice 5 fixture handoff, and Slice 7 closeout.
- Refined the plan to specify an atomic publication protocol rather than literal
  multi-file filesystem atomicity: result visibility requires matching journal
  range, snapshot identity, and hashes; interrupted partial publication fails
  closed.
- Kevin approved the sprint plan. Committed and pushed planning as `aeaba5b`; Slice
  0 began.
- Traced ordinary exact/bounded authoring and neutral reconciliation through paid-
  action persistence, provider identity/result state, public state, snapshot,
  lifecycle projection, event, stdout, and process-exit boundaries.
- Added sanitized provider-free Aster-shaped fixture
  `fixtures/aster-shaped-authoritative-gap.v0.json` and a characterization test.
  It proves current state/snapshot/inspection preserve final review truth while an
  append-only transition history and invocation-bound terminal result are absent.
- Recorded the precise crash windows. The most important handoff gap occurs after a
  valid terminal snapshot but before/without authoritative consumer ingestion;
  stdout, events, and exit status cannot close it.
- Found a route asymmetry relevant to Slice 1: exact ordinary review exits 2 after
  printing, while bounded ordinary review currently prints public state without an
  equivalent explicit exit conversion. Both require the same durable terminal-
  result meaning regardless of exit code.
- The focused characterization passed in 1.256 seconds. The complete repository
  suite passed all 357 tests in 237.475 seconds.
- A preliminary targeted command included one nonexistent module name after 155
  real tests passed; the resulting harness import error was superseded by the clean
  authoritative full discovery run and is not product evidence.
- Slice 0 is complete and paused for the mandatory API review before Slice 1.
  Provider operations remain 0 and paid spend remains `$0`.
- The API agent approved Slice 0 with no blocker and authorized proceeding to the
  Slice 1 contract freeze.
- Recorded the API refinements: immutable per-invocation result artifacts; SBE
  observation identity/kind/time distinct from provider ID; versioned cost evidence
  references; frozen request/profile binding; non-authoritative latest convenience;
  and refusal of a second distinct provider ID while supersession is unsupported.
- API acknowledgement/ingestion remains an API-owned PostgreSQL receipt. SBE result
  publication must never claim consumer acknowledgement.
- Kevin approved Slice 0. Committed and pushed it as `96e3a92`; Slice 1 began.
- Published the native transition journal and immutable execution-result contract
  proposal with closed vocabularies, canonical hashing, API mapping, retention/
  bounds, compatibility, and six explicit API decisions.
- Resolved the result/snapshot self-reference problem with a stable checkpoint-basis
  digest plus mandatory validation of the ordinary full snapshot that inventories
  the result. Publication namespace exclusion applies only to basis calculation,
  never to restoration or full-snapshot membership.
- Added strict non-packaged proposal schema and canonical journal/result examples.
  Three proposal tests passed in 0.020 seconds; proposal plus current lifecycle
  compatibility passed all 33 tests in 0.377 seconds.
- Slice 1 is complete as a proposal and paused for mandatory Kevin/API contract
  review. No runtime or packaged contract changed; provider operations remain 0 and
  paid spend remains `$0`.
- The API agent approved the publication protocol, idempotency key, closed native
  outcomes/causes, and permanent journal v0.1 no-compaction posture.
- Applied the one required compatibility correction: retained the exact lifecycle
  v0.2 cost vocabulary, adding `not_applicable_provider_pending` and restoring the
  full `provider_usage_unavailable_billing_reconciliation_pending` spelling.
- Removed `api_acknowledgement` and future-only predecessor/supersession fields from
  v0.1. API receipts and future recovery models remain wholly outside this schema.
- Slice 1 is API-approved for implementation and paused for Kevin's commit/proceed
  gate before Slice 2.
- Kevin approved Slice 1. Committed and pushed it as `64d67e4`; Slice 2 began.
- Added the packaged native transition engine with canonical content identities,
  hash-linked whole-file journal publication, bounded range digests, immutable
  result artifacts, derived index repair, checkpoint-basis identity, and strict
  full-snapshot reader validation.
- Reused the native spend-consumption lock for cross-process mutation. Only the
  bounded reader and journal validator are public package-root interfaces; mutation
  remains SBE-internal.
- Added packaged contract catalog entries, Draft 2020-12 schema, and hash-valid
  review-terminal record/result fixtures.
- Native focused coverage passed all 11 tests in 0.870 seconds. The final native,
  lifecycle, snapshot, and consumer compatibility gate passed all 57 tests in 3.865
  seconds.
- Slice 2 is complete and paused for Kevin review. Provider-bound journaling and
  command result publication remain later slices; provider operations remain 0 and
  paid spend remains `$0`.
- Kevin approved Slice 2. Committed and pushed it as `590da05`; Slice 3 began.
- Integrated journal projection at the authoritative durable spend-ledger boundary,
  covering every paid stage across exact Responses, exact Batch, and bounded
  Responses without relying on non-authoritative execution events.
- Added deterministic prepare, authorization, consumption, submission-started,
  identity, pending, terminal provider, usage, ambiguity, identity-conflict, and
  providerless-denial observations. Exact semantic replay appends nothing.
- Preserved the public native writer lock while using a separate internal journal
  publication lock, avoiding recursive spend-lock acquisition during state
  persistence and retaining cross-process refusal for public mutation.
- Added route/stage matrix, unavailable-cost, ambiguity, replay, and interrupted
  journal-publication recovery tests. The interruption case proves durable ledger
  truth can reconstruct missing journal observations exactly once.
- Native focused coverage passed all 14 tests in 1.412 seconds. The broad spend,
  provider-capacity, bounded-provider, and semantic-closure compatibility gate
  passed all 145 tests in 182.359 seconds.
- Slice 3 is complete and paused for Kevin review. No live provider operation was
  made and paid spend remains `$0`.
- During final hygiene, discovered the newly added API Slice 2 review requesting a
  complete snapshot hash inside the result that the snapshot itself inventories.
  Documented the irreducible content-hash cycle and proposed an immutable external
  publication receipt binding result, complete snapshot, checkpoint basis, and
  journal range. This requires API confirmation before Slice 4 implementation but
  does not alter the completed Slice 3 provider-observation boundary.
- The API agent accepted the immutable publication-receipt solution, approved Slice
  3, and clarified that command correlation is the result's bounded journal range,
  not a requirement that action-derived projection records share one invocation ID.
- Committed and pushed the API-approved Slice 3 as `64836b0`; Slice 4 began.
- Implemented the shared result publication protocol: terminal journal records,
  immutable execution result, complete workspace snapshot, then immutable receipt.
  The receipt namespace is the one narrow exclusion from native snapshot inventory.
- The receipt binds result ID/hash, exact complete-snapshot hash, checkpoint-basis
  hash, journal-range hash, run/invocation IDs, and stable logical root. The reader
  now refuses missing, changed, or mismatched receipts before exposing a result.
- Retained each exact historical snapshot manifest and checkpoint-basis document in
  the receipt namespace so older specified results remain verifiable after later
  valid publications. API/R2 retention remains a consumer responsibility.
- Added deterministic recovery for interruption after result publication: the next
  invocation seals the exact orphan result rather than minting a replacement.
- Routed exact and bounded ordinary authoring plus route-neutral provider
  reconciliation through the shared finalizer. Strict reconciliation `not_due`
  remains nonmutating as frozen previously.
- Preserved external denial causes, provider terminal failure, provider identity
  conflict, pending, ambiguity, review, delivery, and continuation as distinct
  machine outcomes. Optional skips do not become required-action terminal failure.
- The broad gate initially found three providerless-denial crash-recovery cases
  where the new derived journal member was outside the legacy declared write set.
  Narrowed recovery to admit only a valid hash-chain denial projection containing
  every exact persisted denied action ID; arbitrary changed bytes remain refused.
- Focused publication coverage passed all 18 tests in 2.848 seconds. The final broad
  authoring, spend, provider-capacity, bounded, closeout, and denial recovery gate
  passed all 197 tests in 204.543 seconds. Provider operations remain 0 and spend
  remains `$0`.
- Slice 4 is complete and paused for Kevin review.
- The API agent approved Slice 4 subject to one publication hardening correction:
  validate the just-written complete snapshot against workspace bytes before
  hashing or sealing it on both normal and orphan-repair paths.
- Added both validations and injected a post-manifest workspace mutation. SBE
  refused publication before creating a receipt, then repaired the exact orphan
  after the authoritative bytes were restored. Focused coverage now passes all 19
  tests in 3.098 seconds.
- The post-correction route, provider-capacity, bounded, and denial-recovery subset
  passed all 50 tests in 11.778 seconds; `git diff --check` remained clean.
- Committed and pushed the snapshot-hardened, API-approved Slice 4 as `8385990`;
  Slice 5 began.
- Added the typed public `NativeTransitionResultView`, authoritative explicit-ID
  reader, explicitly derived latest-result convenience, and provider-free
  `astrowoof-native-transition` CLI. Source tests prove explicit/latest parity and
  byte-for-byte nonmutation with a provider-call sentinel.
- Published a packaged eight-case consumer matrix covering exact Response delivery/
  review/pending/replay, exact Batch provider failure, bounded Response ambiguity,
  malformed hash refusal, and conflicting second-operation review/refusal.
- Published the native transition consumer handoff with transactional ingestion,
  idempotency/cursor rules, outcome mapping, ownership, cost, redaction,
  compatibility, receipt retention, and irreducible recovery limitations.
- Added the non-authoritative `native.result_published` event and synchronized its
  closed vocabulary across code, JSON Schema, payload catalog, and route tests.
- Source contract/route/consumer coverage passed all 101 tests in 44.459 seconds.
  The source lifecycle smoke also passed.
- Built candidate wheel SHA-256
  `ce63937ce6385c7b45fcef069d42b174a976d655c55bab69658f65bd9872711b`,
  installed it outside the checkout, and passed installed lifecycle/resource/type/
  entry-point smoke. The installed explicit-result CLI returned the sealed result
  without changing any run bytes.
- Removed the isolated `C:\tmp\sbe-slice5-8385990` qualification tree after
  recording compact evidence. No provider operation occurred and spend remains
  `$0`.
- Draft 2020-12 meta-schema validation and strict consumer-fixture validation
  passed using an isolated cached `jsonschema` install. The validation dependency
  tree was removed afterward.
- API review accepted the Slice 5 contract with one required read-only hardening:
  a CLI `--output` must resolve outside the native run directory. The corrected
  CLI rejects both the run root and descendants before reading or writing, while
  preserving external consumer-owned export.
- The focused post-correction suite passed all 33 tests in 4.654 seconds. The full
  source contract/route/consumer suite passed all 101 tests in 44.459 seconds,
  including byte-for-byte proof for allowed and refused output paths.
- Rebuilt candidate wheel SHA-256
  `baca8ae1cedb050d15ba2240406b34acd83707e857e31b8e5f03c8a2fc58b2dc`;
  isolated installed-package resource/type/entry-point checks passed.
- Slice 5 is API-approved and complete; Slice 6 joint qualification has not begun.
- Committed and pushed the API agent's final Slice 5 approval as `c25f47e`; Slice 6
  qualification began.
- The first complete-suite run reached all 383 tests and exposed one incompatible
  legacy checkpoint-repair fixture: its paid-action binding used short placeholder
  digest strings that the native journal correctly rejects. Runtime validation
  remains strict; the fixture now uses canonical SHA-256 identities before the
  complete-suite rerun.
- The corrected checkpoint-repair module passed all 8 focused tests; the complete
  suite then passed all 383 tests in 247.272 seconds with four expected skips.
- Two fixed-epoch builds from `c25f47e` used `SOURCE_DATE_EPOCH=1787031309` and
  were byte-identical at SHA-256
  `1fa992b07cef80725829137c4d6f1871f65d0b01e1f53b69d9bf4eaa78c05b26`.
  Both contained the native contracts, consumer fixture, and `py.typed`; neither
  contained source tests.
- Downloaded and verified the exact published SPC 0.11.0 wheel at SHA-256
  `82290df44fe5697e87df2e27eb0aa4bab3b7954c66ce988efda0962964e1366d`.
  Clean Windows CPython 3.11 and Linux `python:3.11-slim` installations passed
  `pip check` and installed lifecycle smoke against that exact dependency.
- The API Sprint 26 validator passed its six focused ingestion tests. A direct
  provider-free check of the packaged SBE matrix through the real API validator
  accepted all seven valid/replay/review cases and rejected the intentionally
  malformed result for invalid native identity.
- SBE-native Slice 6 qualification is complete. The real API worker/PostgreSQL/R2
  terminal-first trace remains API-owned and pending; no SBE claim is made for it.
