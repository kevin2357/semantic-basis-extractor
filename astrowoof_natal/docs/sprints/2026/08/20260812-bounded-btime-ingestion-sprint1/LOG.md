# Bounded Birth-Time Natal Ingestion Sprint 1 Log

This log is append-only once implementation begins. Planning entries document
decisions and evidence but do not represent completed implementation slices.

## 2026-08-12: sprint seed

- Created the sprint directory and retained three API-agent planning inputs.
- `PLAN.md` and `LOG.md` intentionally remained empty while upstream AGF and SPC
  bounded contracts were still evolving.

## 2026-08-14: upstream review and product-policy discussion

- Reviewed the four most recent relevant AGF sprints: runtime decoupling,
  coordinate-derived bounded Natal, terrestrial/time-frame bounded Natal, and
  bounded evidence-schema reconciliation.
- Reviewed SPC's completed bounded projection sprint, released schemas, profile and
  context contracts, consumer handoff, and SBE acceptance finding in detail.
- Validated the supplied AGF 0.8.1/SPC 0.11.0 four-context archive against SPC's
  official bounded schema and specialized parallel-context validator. Validation
  passed for 106 object and 1,520 relationship correspondences with common
  epistemic and structural-semantic hashes.
- Added `Ingesting Bounded Birth-Time Natal Projection Artifacts.md` as the durable
  pre-planning assessment.
- Product owner confirmed a separate bounded semantic pipeline, invariant-only
  authorship, exactly fifty initial claims, configurable foundational policy with
  strong preference by default, family-aware derived-material handling, an
  explicitly editorial scoring policy, invariant configuration synthesis, a
  separate disposition report, SPC release pinning, and separate bounded schemas.
- Product owner approved factoring exact Natal behind a policy seam and adding an
  opt-in experimental axis-aware angle policy while preserving legacy exact behavior
  as default.
- Reconciled historical API implementation/logging requests against published SBE
  0.3.0. Common lifecycle work is satisfied; bounded semantic events, privacy, and
  provider-free integration qualification remain.
- Wrote the proposed sprint plan. No implementation, test fixture, package
  dependency, schema, version, tag, or release was changed during planning.

## 2026-08-14: Slice 0 - baseline, contract freeze, and fixture strategy

- Committed and pushed the approved sprint plan together with the previously
  accepted `py.typed` packaging follow-up as `8ba9613`.
- Named the released exact-Natal behavior `legacy_atomic.v1` and froze a fresh Bre
  replay at 103 candidates, 50 selected claims, 53 rejected claims, passing QA,
  and stable candidate, selection, packet, and QA hashes.
- Passed the source release smoke through `DELIVERY_COMPLETE` with 50 cards, four
  summaries, matching delivery hashes, and the frozen resource-set identity.
- Adopted SPC 0.11.0's 7.6 KB sanitized bounded source fixture and generated all
  four official projected contexts through SPC's public CLI. Official schema and
  parallel-family validation passed with two object and one relationship
  correspondences.
- Retained only the supplied full-scale archive's hash, compact metrics, and
  semantic validation identities; its expanded protected artifacts remain outside
  Git and release packaging.
- Reserved distinct v1 names for bounded admission, candidate policy, editorial
  utility, claim deck, disposition report, authoring packet, and final cards.
- Recorded that the AGF 0.8.1 archive passes SPC 0.11.0 runtime validation while
  SPC's prose compatibility table still names AGF 0.8.0, a documentation
  qualification that must remain explicit.
- Added a regression test that dynamically replays and verifies the exact Bre
  semantic baseline plus bounded inventory/contract-name checks.
- Passed three focused baseline tests, all 218 repository tests, source release
  smoke, and an isolated offline-installed wheel smoke with `--require-installed`.
  `git diff --check` also passed apart from expected Windows line-ending notices.
- Gate 0 is awaiting review. No production refactor has begun.

## 2026-08-14: Slice 1 - shared engine seam and exact legacy policy

- Gate 0 was approved, committed, and pushed as `f4270dc`.
- Added a named `ExactNatalPolicy` seam and made `legacy_atomic.v1` the explicit
  default for exact candidate semantics, scoring, weights, budget expectations,
  and packet compilation identities.
- Kept graph indexing, dependency closure, portfolio mechanics, evidence and
  provenance assembly, and artifact orchestration in the shared engine.
- Added `--exact-natal-policy`; unknown versions and policies for another route fail
  closed before input processing.
- Recorded the resolved identity in candidate-pool, selection-audit, subject-run,
  and batch-run audit surfaces without changing the legacy selected packet.
- Proved omitted versus explicit `legacy_atomic.v1` replay equality and retained
  every Slice 0 Bre semantic hash.
- Passed eight focused policy/baseline tests, Python compilation, and all 223
  repository tests in 114.923 seconds.
- Built and offline-installed a fresh wheel in an isolated environment. Its public
  lifecycle smoke and complete release smoke both passed from site-packages; the
  latter reached `DELIVERY_COMPLETE` with the unchanged 50-card/four-summary and
  resource-set identities.
- `git diff --check` passed with only expected Windows line-ending notices.
- Gate 1 is ready for review. Slice 2 has not begun.

## 2026-08-14: Slice 2 - experimental exact axis-aware policy

- Gate 1 was approved, committed, and pushed as `4fafab8`.
- Added opt-in `axis_aware.v1` while retaining `legacy_atomic.v1` as every public
  and installed default.
- Generated complete ASC–DSC and MC–IC planet/point configurations with both
  component edges, source references, context evidence, and transformation lineage
  preserved.
- Classified six Bre frame edges as `structurally_inevitable` and twelve component
  edges as `represented_by_axis_configuration`; all remain inspectable and none can
  re-enter selection through dependency closure.
- Verified incomplete axes do not synthesize or suppress the surviving atomic edge.
- Added a deterministic comparison artifact covering selected-ID drift, topology,
  source coverage, closure cost, and policy dispositions.
- Wired the policy through the extraction CLI and closure generation profile; the
  API can opt in without forking orchestration.
- Passed 13 focused policy/baseline tests, Python compilation, and all 228
  repository tests in 127.692 seconds.
- Built and offline-installed a fresh wheel. Installed lifecycle and complete
  default release smokes passed.
- Ran the installed closure end to end with the fake provider and explicit
  `axis_aware.v1`; it reached `DELIVERY_COMPLETE`, preserved the policy in the
  authoring profile, and emitted the expected six-configuration comparison.
- `git diff --check` passed with only expected Windows line-ending notices.
- Gate 2 is ready for review. Slice 3 has not begun.

## 2026-08-14: Slice 3 - strict bounded packet admission

- Gate 2 was approved, committed, and pushed as `21022d0`.
- Pinned `semantic-projection-core==0.11.0` and added the separate installed
  `astrowoof-admit-bounded-natal` command.
- Required official per-artifact schema validation plus SPC's specialized
  four-context certainty/structure validator and exact supported release, profile,
  context, upstream-contract, runtime-resource, capability, limitation, registry,
  evidence, and correspondence boundaries.
- Added machine-classified invalid, unsupported, and mixed failures and a minimized
  provider-free admission event with protected identity and birth fields excluded.
- Hardened the legacy exact loader to reject bounded artifacts explicitly.
- Passed sanitized and full-scale official families and rejected injected source,
  registry, runtime-resource, correspondence, capability, and evidence drift.
- Passed 234 repository tests, installed default release smoke, and the packaged
  bounded CLI inside the qualified Linux SPC 0.11 image.
- Corrected the trailing blank line reported when Slice 2 was committed.
- Gate 3 is ready for review. Slice 4 has not begun.

## 2026-08-14: Slice 3 - strict bounded packet admission

- Gate 2 was approved, committed, and pushed as `21022d0`.
- Pinned `semantic-projection-core==0.11.0` and added the separate installed
  `astrowoof-admit-bounded-natal` command.
- Required official per-artifact schema validation plus SPC's specialized
  four-context certainty/structure validator and exact supported release, profile,
  context, upstream-contract, runtime-resource, capability, limitation, registry,
  evidence, and correspondence boundaries.
- Added machine-classified invalid, unsupported, and mixed failures and a minimized
  provider-free admission event with protected identity and birth fields excluded.
- Hardened the legacy exact loader to reject bounded artifacts explicitly.
- Passed sanitized and full-scale official families and rejected injected source,
  registry, runtime-resource, correspondence, capability, and evidence drift.
- Passed 234 repository tests, installed default release smoke, and the packaged
  bounded CLI inside the qualified Linux SPC 0.11 image.
- Corrected the trailing blank line reported when Slice 2 was committed.
- Gate 3 is ready for review. Slice 4 has not begun.

## 2026-08-14: Slice 4 - bounded normalization, candidates, and family topology

- Gate 3 was approved, committed, and pushed as `5328def`.
- Added a distinct invariant-only bounded candidate builder and private disposition
  report under the reserved v1 contract identities.
- Normalized all projected rows by correspondence identity while preserving all
  four context records, source and projected-term references, proof scope, direct
  and opaque prerequisite lineage, root owners, evidence families, independence
  groups, and record-independence groups.
- Collapsed derived sibling rows into family candidates, retained transform
  ownership as dependency-only topology, and built initial configurations from
  independent relationship-family units between canonical root owners.
- Added explicit family accounting that prevents raw multiplicity from becoming
  support or weight and implemented the three approved foundational policies with
  `strong_preference` as default.
- Added a complete disposition report for projected rows, source evidence,
  outside-scope material, and upstream feature dispositions.
- Excluded ranges, orbs, structural strength, confidence, and representative state
  from candidate authority. No score or selection policy was introduced.
- Passed 15 focused bounded tests, all 240 repository tests in 160.311 seconds,
  fresh-wheel import, and official SPC admission plus candidate construction over
  both sanitized and full-scale families in Linux.
- The full family produced 586 candidates and disposition coverage for 1,626
  projected rows, 1,544 evidence records, and two outside-scope objects. Local
  construction took 1.650 seconds with 35.64 MiB peak traced allocation.
- Gate 4 is ready for review. Slice 5 has not begun.

## 2026-08-14: Slice 5 - bounded editorial utility and exactly-fifty portfolio

- Gate 4 was approved, committed, and pushed as `3a821aa`.
- Added the versioned bounded editorial-utility profile and deterministic
  exactly-fifty optimizer without changing exact-Natal selection.
- Kept epistemic invariance as a binary authority boundary and labeled every
  numeric component and tier as editorial rather than confidence or strength.
- Conserved SPC target relevance at the evidence-family allocation unit, added
  root-owner derived-family diminishing returns, and charged configurations for
  their complete dependency closure so raw or bundled multiplicity cannot create
  advantage.
- Implemented all three foundational policies, exact dependency closure, fixed
  editorial tiers, complete decision audits, and selection-aware disposition
  updates.
- Added machine-readable failures for insufficient invariant basis, unsupported
  size, non-invariant candidates, duplicate IDs, missing/cyclic dependencies, and
  unsafe relevance accounting.
- The full default portfolio selected 12 foundations, 28 individualized
  relationships, 9 derived-family candidates, and one configuration, covering all
  12 root owners, 41 terms, and 48 evidence families.
- Passed 21 focused/combined bounded tests, all 246 repository tests in 174.817
  seconds, full-scale reorder replay, all three policies under Linux SPC 0.11.0,
  and a fresh non-editable wheel import.
- No provider operation occurred. Gate 5 is ready for review; Slice 6 has not begun.

## 2026-08-14: Slice 6 - bounded claim deck, authoring, and final cards

- Gate 5 was approved, committed, and pushed as `f55a3e3`.
- Added separate bounded claim-deck, provider authoring-packet, disposition, final
  cards, provider-disclosure, and delivery-provenance contract identities.
- Packaged four JSON Schemas, added the contracts to the catalog, and shipped a
  bounded-specific authoring brief and field-level provider disclosure inventory.
- Locked invariant authority, dependencies, private evidence digests, source and
  family lineage, selected projected terms, and separate card/summary evidence
  scopes through claim compilation and final QA.
- Built the provider packet from an allow-list. Protected birth/interval/location
  fields, full graphs, raw evidence, strength/range data, private references,
  unselected material, and disposition/selection internals do not enter it.
- Added deterministic provider-free bounded authoring and final QA, including
  locked-field, registry, evidence-scope, placeholder, editorial-shape, and
  normalized-duplication validation.
- The full Linux path passed with 50 cards, four summaries, 41 selected terms, and
  seeded protected values absent. No provider operation occurred.
- Passed 29 combined bounded tests, all 254 repository tests in 171.428 seconds,
  JSON/schema/catalog parsing, and fresh non-editable wheel resource/import smoke.
- Gate 6 is ready for review. Slice 7 has not begun.

## 2026-08-14: Slice 7 - shared lifecycle, spend, snapshots, and recovery

- Gate 6 was approved, committed, and pushed as `d0dc880`.
- Added a bounded route sequencer over the released common run-state, spend-ledger,
  single-writer authorization, workspace snapshot, lifecycle inspection, closeout,
  and non-authoritative event implementations; no second integrity or spend system
  was introduced.
- Materialized claim deck, provider packet, disposition, durable provider results,
  final cards/reports, critic result, and delivery record inside the authoritative
  snapshot boundary under distinct bounded contracts.
- Added deterministic provider-free execution for initial authoring, separate
  creative retry, polish, critic, qualitative candidate, and delivery. Optional
  stages are enabled or disabled by the frozen generation profile and can skip
  under their frozen spend ceilings.
- Reused exact request-bound prepare/authorize/execute, conservative commitment,
  single-writer consumption, provider-ID persistence, reported-cost accounting,
  and machine-distinct authorization/budget/ambiguity states.
- Persisted provider results before settling paid actions. A restart with a durable
  provider ID polls that operation; it never creates another paid request. A
  submission interrupted before durable identity remains ambiguous and fail-closed.
- Added five minimized bounded lifecycle events and updated the packaged event
  schema and payload catalog. Event loss and sink failure remain observational and
  cannot affect execution.
- Passed the focused bounded lifecycle suite, persistence-boundary fault matrix,
  paid authorization/identity/reconciliation and providerless-denial cases,
  optional-budget skip, snapshot mutation/stable-path rejection, shared
  inspection/closeout/replay, and event sink-loss tests.
- Passed all 263 repository tests in 169.368 seconds and verified the bounded
  lifecycle module, updated event contracts, and `py.typed` in a fresh offline
  wheel (`f694f7558b483dec1d5f13d6970a3f6bba0cd3e3d2f56fd31b0fd7f61fb063b5`).
- Gate 7 is ready for review. Slice 8 has not begun.

## 2026-08-14: Slice 8 - deterministic, scale, privacy, and product QA

- Gate 7 was approved, committed, and pushed as `dcaadf5`.
- Added a compact bounded product-qualification contract and provider-free harness
  covering selection, claim compilation, provider minimization, fake authoring,
  final QA, semantic hashes, topology counts, and observed time/memory evidence.
- Qualified SPC's released 1-hour/61-evaluation, 24-hour/1,441-evaluation, and
  48-hour/2,881-evaluation route-equivalence evidence without turning interval
  width or evaluation count into SBE semantic authority, confidence, or strength.
- Recorded the fixture boundary honestly: the sprint has one official full-scale
  four-context archive for a four-hour interval. The 1/24/48-hour upstream cases
  prove SPC route behavior; SBE proves the same admitted invariant graph yields the
  same exact-fifty product independent of non-authoritative interval labels.
- Exercised terrestrial-frame inconclusive and optional-object unavailable
  dispositions; neither creates a claim or enters the provider packet.
- Exercised a 300-member single-family stress case. It remains one support unit,
  cannot inflate selection, and passes loose observed regression guards of ten
  seconds and 256 MiB without claiming a product SLA.
- Seeded handler identity, dates and interval endpoints, timezone, coordinates,
  location evidence, raw evidence text, filesystem path, API key, and authorization
  header values. None entered initial authoring, polish, critic, candidate, or
  event payloads. The explicitly allow-listed dog display name remains editorially
  visible as documented.
- The official four-hour Linux artifact passed with 586 candidates, exactly 50
  invariant claims/cards, four summaries, 54 evidence families, 41 selected terms,
  12 root owners, and zero provider operations. Reversed contexts, rows, and term
  serialization produced identical semantic product hashes.
- Passed all 270 repository tests in 196.432 seconds, including both exact angle
  policies and all released exact lifecycle/spend/snapshot/authoring regressions.
- Gate 8 is ready for review. Slice 9 has not begun.

## 2026-08-14: Slice 9 - installed cross-repository acceptance and handoff

- Gate 8 was approved, committed, and pushed as `fcdedce`.
- Added the installed `astrowoof-run-bounded-natal` create/resume command and a
  bounded OpenAI Responses adapter over SBE's released spend and resumable-provider
  implementation. Real bounded Batch submission is explicitly rejected rather
  than mislabeled for Batch pricing.
- Restricted provider structured output to editorial fields and correlation IDs.
  SBE deterministically reattaches invariant authority, evidence scopes, subject,
  selected terms, and registry bytes, rejecting missing, duplicate, or unknown
  claim/summary identities.
- Added packaged bounded delivery and critic schemas/catalog entries, 0.4.0 release
  candidate documentation, compatibility/limitations guidance, API/frontend
  handoff, sanitized delivery example, and exact upstream pin/hash instructions.
- Passed all 274 repository tests in 149.848 seconds. The final 0.4.0 wheel built
  twice byte-identically at 711,052 bytes with SHA-256
  `4fb7a114ae4866475778d36b677d170499a5558e0f1a854aeb88616b9c6c8c84`;
  it contains 78 entries, 38 resources, `py.typed`, and no cache entries.
- The predecessor candidate passed the complete installed Linux gate in the exact
  AGF 0.8.1/SPC 0.11.0 image. The final candidate's rerun could not execute because
  the desktop approval service reported its usage limit; this remains a required
  unexecuted gate, not a test failure. Windows final-candidate E2E is also pending
  due unavailable dependency-install authorization.
- No provider operation occurred and spend remained `$0`. API-agent review and the
  final Linux installed rerun are required before Gate 9 approval or release
  recommendation. No tag or publication was created.

## 2026-08-14: Gate 9 approval and final installed Linux acceptance

- Product-owner Gate 9 approval was received and Slice 9 was committed and pushed
  as `946f6fd`.
- Reinstalled the exact final wheel
  (`4fb7a114ae4866475778d36b677d170499a5558e0f1a854aeb88616b9c6c8c84`)
  without source-tree imports in the qualified Linux image with AGF 0.8.1 and SPC
  0.11.0.
- `pip check`, installed lifecycle smoke, and installed release smoke passed. The
  full four-context bounded CLI run reached `DELIVERY_COMPLETE`.
- Native inspection found a complete, valid snapshot inventory, terminal accepted
  delivery, quiescence, no provider/local continuation, and no unresolved actions.
  Closeout returned `closed` and persisted its result checkpoint.
- No provider operation occurred and spend remained `$0`. API-agent consumer
  review remains the sole release-recommendation checkpoint; Windows bounded E2E
  remains a documented non-blocking qualification limitation.
