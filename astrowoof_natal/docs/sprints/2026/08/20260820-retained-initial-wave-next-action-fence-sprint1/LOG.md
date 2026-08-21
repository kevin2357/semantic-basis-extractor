# Retained Initial-Wave Next-Action Fence Sprint 1 Log

## 2026-08-20 — Sprint proposed

- Read the API Sprint 33 next-action contract request and surrounding Background,
  Plan, Log, and Evidence documents.
- Confirmed SBE 0.4.13 publishes an empty branch action inventory for
  `await_external_authority` and does not bind generic resume to a public request.
- Confirmed the existing fresh exact-interactive route can infer initial-wave mode
  from empty pass-attempt state without first excluding historical spend/provider
  lineage.
- Proposed lifecycle inspection v0.5, an independently versioned external-authority
  request, a single-writer constrained continuation fence, and strict initial-wave
  anti-reentry policy.
- No implementation, retained-workspace access, provider call, or spend occurred.
- Sprint is paused for Kevin/API plan review.

## 2026-08-20 — API plan review incorporated

- Preserved the API agent's detailed review as a sprint artifact.
- Accepted inline lifecycle v0.5 request publication, a closed aggregate API grant,
  lexical ordinary-action ordering, semantic initial-wave ordering, and the typed
  `initial_wave_lineage_unjoinable` refusal.
- Fixed the intended single-writer boundary through durable pre-submit intent while
  explicitly excluding slow provider I/O from the lock.
- Retained the irreducible post-intent/pre-identity provider gap as fail-closed
  ambiguity rather than overstating aggregate-grant atomicity.
- No runtime implementation, retained-workspace access, provider call, or spend
  occurred. Sprint remains paused for Kevin authorization to begin Slice 0.

## 2026-08-20 — Final planning clarification and approval

- Made `external_authority_refusal` an explicit closed lifecycle v0.5 companion
  object rather than requiring consumers to infer refusal from a null request.
- Added mutual-exclusion and cross-field schema requirements for request, refusal,
  and non-applicable lifecycle states.
- Kevin and the API agent approved the revised sprint direction.
- No implementation, retained-workspace access, provider call, or spend occurred.

## 2026-08-20 — Slice 0 reproduction and mutation map

- Added a provider-free characterization using the production exact-wave
  preparation, authorization, and concurrent create coordinator with a scripted
  transport.
- Added the requested public-path control through the actual `closure.main()`
  resume dispatcher: one generic resume prepares the inferred wave and a second
  generic resume applies the existing v1 authority documents and performs six
  scripted creates without the proposed constrained grant.
- Proved that retained historical initial actions/provider IDs plus empty current
  pass attempts can produce a distinct second six-member inventory in 0.4.13.
- Mapped preparation, authorization, durable all-member intent, provider I/O,
  identity persistence, snapshot, and result-publication boundaries.
- Located the last safe new fence before preparation mutation under the shared
  cross-process writer, with writer release only after durable pre-submit intent.
- Focused controls passed: 3 tests.
- Provider network calls: 0. Retained Aster access: none. Spend: USD 0.
- Paused for API review before Slice 1 schema freeze.

## 2026-08-20 — Canonical nomenclature huddle

- Canonicalized `RIWNAFS` as **ree-WOOF-naffs**.
- Preserved **Native Authority** as the intentional second-layer reading of `NA`,
  while retaining **Next Action** as the formal sprint expansion.
- Recorded complete, compact, and angsty-teen emoji forms.
- Documented the independently verified Norwegian waffle/krumkake and Swedish
  `nafs` linguistic-pastry adjacency.
- Confirmed that the tiny Scandinavian dog-waffle guardian is binding for morale
  and non-authoritative for runtime behavior.

## 2026-08-20 — Slice 1 external-authority contract proposal

- Added the packaged closed-world request/refusal/grant schema and declared
  lifecycle inspection v0.5 without changing the implemented catalog default.
- Froze complete binding disclosure, route-sensitive canonical ordering, canonical
  SHA-256 construction, exact all-or-none grant membership, and initial-wave
  context repetition.
- Froze the lifecycle request/refusal/null branch matrix and separated a native
  inability to publish one exact request from execution-time stale/grant refusals.
- Clarified that requests require a complete valid snapshot while a no-create
  refusal may truthfully report snapshot invalidity or absent exclusivity.
- Kept the six ordinary per-action spend authorization documents as member
  authorities; proposed the new grant as their observation-bound invocation
  envelope on the v0.5 constrained path.
- Documented positive grant versus withheld authority/providerless denial and the
  irreducible post-intent/pre-provider-ID ambiguity boundary.
- Added sanitized initial-wave request/grant/refusal and ordinary-action fixtures
  plus digest, ordering, all-or-none, closed-schema, and observation tests.
- Focused installed-environment result: 9 tests passed with real Draft 2020-12
  schema validation. Provider/network calls: 0. Spend: USD 0.
- Paused for the required API contract review before Slice 2/runtime work.

## 2026-08-20 — Slice 1 API review corrections

- Added full lifecycle-level request and native-refusal fixtures rather than
  relying only on standalone authority objects.
- Added semantic validation for exact outer lifecycle/request/refusal run,
  observation revision, snapshot, logical-root, and execution-branch joins.
- Added mutations for every cross-boundary identity, branch action inventory, and
  invalid request/refusal combinations.
- Strengthened aggregate-grant validation to validate each complete ordinary
  authorization document's closed shape, schema, action ID, exact binding, digest,
  and reference.
- Added digest-consistent wrong-action and wrong-binding attacks to prove that a
  self-consistent grant cannot bless a mismatched member authorization.
- Focused Linux QA result: 16 tests passed. Provider/network calls and spend: zero.
- Slice 1 remains paused for final API contract approval.

## 2026-08-20 — Slice 1 approved and Slice 2 completed

- Committed and pushed the approved Slice 1 contract as `01b8aee`.
- Added a provider-free root-level Python builder, semantic validator,
  snapshot-validating reader, schema reader, and `astrowoof-external-authority` CLI.
- Joined exact and bounded initial waves through the existing public prepared-wave
  and binding-bundle validators; ordinary actions use lexical action-ID order.
- Made unchanged-checkpoint exports deterministic by using the snapshot-bound native
  update time rather than reader wall-clock time.
- Revalidated complete workspace state after request construction and refused a
  simulated coherent writer update during the read.
- Rejected CLI output under the native run directory and kept all reader/validation
  operations free of provider access and state mutation.
- Focused suite: 33 tests passed on the lean host, with four optional JSON Schema
  tests skipped consistently with Slice 1. Offline wheel build and isolated Python
  3.11 install succeeded; the installed CLI read the packaged v1 schema.
- Provider/network calls: 0. Spend: USD 0. Retained Aster access: none.

## 2026-08-21 — Slice 7 holistic runtime correction

- Replaced the in-memory coordinator qualification with a real snapshot-valid
  exact-Natal run prepared through supported runtime code.
- Read the exact authority through lifecycle inspection v0.5 and the public reader,
  persisted request/grant/member documents outside the workspace, then invoked the
  constrained continuation in a fresh Python process with the scripted production
  Responses transport.
- Reopened the workspace again for retained replay and the real route-neutral
  reconciliation entry point; proved six POSTs total and a bounded GET-only due
  subset with no seventh create.
- Exercised typed unjoinable lineage through lifecycle inspection and an ordinary
  prepared action through the actual snapshot-validating reader.
- The holistic test exposed and corrected a lifecycle-observation join gap:
  constrained execution now rebinds the public reader to the supplied observation
  only after every safety-bearing snapshot field matches current native truth.
- The earlier Slice 7 wheel/hash evidence is superseded pending a fresh build.
- Combined authority/lineage/lifecycle/event gate: 80 tests passed in 76.954
  seconds with five optional schema skips.
- Fresh Python 3.11 installed-wheel holistic command and public receipt validator
  passed from outside the repository; candidate SHA-256
  `32f6572ae26af19ebd687548a87dbd8bfc4ac8d1a81ee1408c1377440a52057b`.
- Corrected an implementation-shape ambiguity before handoff: action preparation
  revision may precede the later lifecycle observation revision after persistence.
  Tests now use `prepared=N`, `observed=N+1`; only a future action revision fails.

## 2026-08-20 — Slice 2 API fail-closed correction

- Restricted initial-wave request publication to a stored wave whose state is
  exactly `AWAITING_SPEND_AUTHORIZATION`.
- Resolved all six semantic wave members against the durable ledger and required
  exactly one matching `PREPARED`, providerless, unconsumed, binding-identical
  action for every member.
- Added production-shaped ledger fixtures and refusal coverage for authorized
  waves, stale wave labels with provider identity/consumption, changed bindings,
  and duplicate action records.
- Focused host result: 36 tests passed with four optional schema tests skipped;
  Linux QA result: all 36 passed with Draft 2020-12 validation active.

## 2026-08-20 — Slice 3 constrained continuation fence

- Added strict runtime validation of the closed aggregate grant and all six complete
  member authorization documents against the current snapshot-bound request.
- Added the supported exact-interactive constrained execution path and CLI inputs:
  `--external-authority-request`, `--external-authority-grant`, and the six existing
  ordered `--spend-authorization` documents.
- Held native single-writer control through current-request reconstruction, exact
  grant validation, all-or-none ledger authorization, and one durable all-member
  `SUBMITTING` intent checkpoint; released it before slow provider creates.
- Reacquired cross-process single-writer control for every returned identity or
  ambiguity outcome and published a complete workspace snapshot after each.
- Removed the legacy public initial-wave authorization route and rejected loose
  initial-wave member authorizations without the snapshot-bound aggregate grant.
- Proved that interruption after durable intent makes replay fail closed before any
  create, while an injected provider-return/identity-persistence gap becomes six
  durable ambiguous submissions and never creates again.
- Focused results: 33 authority tests passed with four optional schema tests skipped
  on the lean interpreter; 40 existing initial-wave/spend tests passed; two targeted
  semantic-closure compatibility tests passed.
- Provider/network calls were scripted only. Spend: USD 0. Retained Aster access:
  none.

## 2026-08-20 — Slice 3 API review correction

- Added an explicit `aggregate_grant_required` refusal when generic exact
  interactive resume encounters a stored initial wave in
  `AWAITING_SPEND_AUTHORIZATION` without the exact external request/grant pair.
- Placed the refusal before wave preparation, state/snapshot persistence, and native
  result publication; fresh initial preparation remains supported.
- Added a public CLI regression proving byte-identical `run.json` and workspace
  snapshot, no changed/native-result publication artifacts, and zero provider calls.
- Updated focused authority result: 34 passed with four optional schema skips.

## 2026-08-20 — Slice 4 one-wave lineage fence

- Replaced the old “all pass attempts empty” inference with a complete native
  admission check before exact-interactive wave preparation.
- Refused orphaned `authoring_initial` ledger actions, pass attempts, binding/join
  artifacts, provider identities, consumption/reporting, response evidence, and
  ambiguity as typed `initial_wave_lineage_unjoinable` evidence.
- Validated a stored exact wave against its contract, six-member binding bundle,
  unique ledger bindings, complete request inventory and bytes, and matching pass
  attempts before treating it as reusable.
- Added the same orphan-lineage fence before generic interactive dispatch so a
  partially retained run cannot bypass wave preparation and enter ordinary pass
  continuation.
- Prevented the public authority reader from relabeling orphaned prepared initial
  actions as an ordinary action set.
- Preserved a valid stored wave—including six durable provider identities—without
  changing its inventory or creating provider work.
- Converted the Slice 0 unsafe-path characterizations into positive refusal
  regressions with byte-identical state and zero provider creates.
- Full semantic-closure suite: 92 tests passed. Focused lineage/public/execution:
  22 passed; combined lineage/execution/initial-wave/spend compatibility: 52
  passed. Network/provider calls and spend: zero.

## 2026-08-20 — Slice 5 cross-route authority matrix

- Activated lifecycle inspection v0.5 with mutually exclusive, snapshot-bound
  `external_authority_request` and `external_authority_refusal` projections.
- Kept inspection v0.4 readable but explicitly non-authorizing for constrained
  continuation.
- Extended the aggregate initial-wave fence to bounded interactive authoring and
  removed the legacy bounded initial-wave envelope from provider-create authority.
- Preserved bounded crash recovery: recorded create outcomes reconcile without a
  duplicate create; consumed authority without any durable outcome fails closed.
- Prevented exact historical-lineage detection from misclassifying bounded legacy
  and ordinary pass-local continuation.
- Preserved exact/bounded Batch as one paid round, and preserved retries, polish,
  critic, candidates, optional skipping, and providerless denial under their
  established ordinary-action boundaries.
- Published the complete route matrix in
  `results/SLICE 5 - CROSS-ROUTE AUTHORITY AND SAFETY MATRIX.md`.
- Focused lifecycle/bounded/lineage/capacity result: 77 tests passed in 137.205s.
  Provider/network calls and spend: zero. Retained Aster access: none.

## 2026-08-20 — Slice 5 API bounded-fence correction

- Replaced bounded per-member `AUTHORIZED` submission with the exact route's
  constrained safety shape: all six authorizations and `SUBMITTING` transitions,
  plus one capability-bound intent, are durable under the lifecycle writer before
  provider I/O begins.
- Reacquired the lifecycle writer for every returned provider identity or ambiguity
  checkpoint and retained the existing provider atomicity caveat.
- Removed prepared request-map presence as recovery permission. Generic bounded
  resume now refuses stored awaiting, authorized, and submitting waves.
- Added a paused-after-intent two-resumer regression proving the generic resumer
  makes zero provider calls and changes no workspace bytes.
- Added explicit `AUTHORIZED`-with-prepared-requests/no-provider-ID refusal coverage.
- Strengthened public request reading to validate the complete route-specific wave
  join before publishing create-capable authority evidence.
- Combined authority, lifecycle, bounded, lineage, and capacity result: 113 tests
  passed in 182.399s with four optional schema skips. Provider/network calls and
  spend: zero. Retained Aster access: none.

## 2026-08-20 — Slice 6 failure atomicity and observability

- Added injectable boundaries after request/grant validation, immediately before
  the durable intent, after that intent, after provider return/before identity,
  after each identity checkpoint, and after the final wave snapshot.
- Proved pre-intent failures preserve byte-identical state/snapshot and make no
  provider calls.
- Proved a final-snapshot interruption leaves a complete detached checkpoint and
  cannot replay the six provider creates.
- Retained the explicit provider atomicity limit: identity-less acceptance is
  ambiguity, never create authorization.
- Added redacted structured logs for request selection, fence validation, durable
  intent, provider-I/O permission, and bounded refusal reason.
- Retained typed lifecycle branch, provider identity, waiting, reconciliation, and
  checkpoint events as failure-isolated observations rather than authority.
- Detailed matrix:
  `results/SLICE 6 - FAILURE ATOMICITY AND OBSERVABILITY.md`.
- Combined authority, lifecycle, bounded, lineage, capacity, and event gate: 122
  tests passed in 210.972 seconds with four optional schema skips.

## 2026-08-20 — Slice 6 typed authority-event completion

- Added five closed execution-event names for request selection, validated fence,
  committed intent, provider-create permission, and typed refusal.
- Added the exact success-order and stale-refusal regressions, bounded success-order
  coverage, and a deliberately failing sink qualification.
- Proved event delivery failure does not alter the completed native checkpoint or
  six scripted provider creates.
- Used a unique protected sentinel as grant metadata and proved it appears in
  neither captured authority event data nor captured logs.
- Final typed-event/exact/bounded gate: 20 tests passed in 53.456 seconds.
- Closed-vocabulary/schema/catalog gate: 25 tests passed.

## 2026-08-20 — Slice 7 installed-wheel and consumer handoff

- Added public `astrowoof-external-authority-qa`, accepting no credential,
  endpoint, production workspace, input package, or spend authority.
- Added a closed qualification receipt/schema and root-level Python builders,
  readers, and validators.
- Exercised six scripted initial creates, durable fresh-reader restore, retained
  replay without a seventh create, conflicting-lineage refusal, stale request
  refusal, ordinary action grant validation, and reconciliation/create separation.
- Generated four sanitized consumer fixtures, a receipt, and a manifest carrying
  both exact file hashes and canonical contract hashes.
- Published `EXTERNAL AUTHORITY CONSUMER HANDOFF.md` with exact API sequencing,
  authority ownership, compatibility, refusal, Batch/ordinary action, and review
  guidance.
- Source contract/authority/event gate: 72 passed in 45.321 seconds with five
  optional JSON Schema skips.
- Built and installed the first, contract-object-only candidate wheel in a clean
  disposable Python 3.11 venv; console command and root-level Python API both passed
  from outside the repository. This build was superseded by the holistic runtime
  candidate recorded above and is not the Slice 7 consumer-manifest candidate.
- Superseded contract-object-only wheel SHA-256:
  `1e8c405df44ed31ed49c71a765c278100d2e35f8e70cada7fab77aedca26b5ef`.
- Source-tree and installed-wheel receipt bytes matched at SHA-256
  `dee698e4d3663a66b07a0dbcad59f1c11ce43695b5768a4a6260a8d9dd7756a2`.
- Installed `--schema` returned the packaged
  `astrowoof.external_authority_qualification.v1` Draft 2020-12 schema.
- Provider/network calls: 0. Spend: USD 0. Retained Aster access: none.

The authoritative installed-wheel qualification and consumer manifest use the
later holistic candidate SHA-256
`32f6572ae26af19ebd687548a87dbd8bfc4ac8d1a81ee1408c1377440a52057b`.
Both candidates emitted the same stable sanitized receipt bytes, but only the later
candidate exercised the real workspace/lifecycle/fresh-process/reconciliation path.

## 2026-08-21 — Slice 8 release closeout begins

- API and Kevin approved the holistic Slice 7 contract, fixtures, handoff, and
  installed qualification.
- Selected fresh immutable patch version 0.4.14; preserved 0.4.13 unchanged.
- Added candidate release notes, compatibility, known-limitations, and API handoff
  documents.
- Tagging and publication remain behind the explicit final Slice 8 gate.
