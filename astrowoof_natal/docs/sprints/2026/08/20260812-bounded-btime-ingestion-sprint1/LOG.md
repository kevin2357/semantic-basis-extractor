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
