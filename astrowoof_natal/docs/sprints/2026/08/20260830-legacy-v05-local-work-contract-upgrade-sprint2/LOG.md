# SBE companion log

## 2026-08-30 — created

- Created as the SBE companion to API Sprint 59 from the independently
  reproducible legacy v0.5 representation seam.
- No implementation, provider work, retained-QA access, or release has
  occurred.
- Clarified that the seam is one precise semantic-validation incompatibility,
  not a fully API-valid v0.5 document or a broad contract-error fallback.
- Made v0.7 versus v0.8 selection evidence-driven and removed the implied blind
  upgrade ladder.
- Made reuse of released 0.4.31 evidence the default; a new SBE package/release
  is conditional on proving a public evidence gap.

## 2026-08-30 — Slice 1 contract inventory

- Froze the exact asymmetric predicate: native v0.5 permits completed provider
  evidence to establish ordinary local fan-in while API additionally requires a
  nonempty `local_dependencies` inventory.
- Defined the cross-version same-checkpoint join using native run, observation
  revision, snapshot digest, logical root, route, action/binding inventory, and
  provider identity rather than comparing version-specific basis digests.
- Defined the minimum-evidence rule and made v0.8 the final scheduling surface
  for the Diffie-shaped mixed retry-custody case.
- Inventoried the released 0.4.31 public APIs, schemas, fixtures, CLI, and
  provider-free qualifications. No SBE source, schema, or package gap is
  presently established.
- Ran the focused legacy/v0.7/v0.8 contract and runtime matrix: 26 tests passed.
- Paused for API review before any fixture extension or implementation.

## 2026-08-30 — Slice 2 same-checkpoint witness

- Added one provider-free regression which validates v0.5, v0.7, and v0.8 over
  the same restored mixed-custody checkpoint and compares stable shared
  identities.
- Confirmed the sole additional API rejection relation is the empty dependency
  count despite completed provider evidence.
- Discovered and documented a necessary precedence refinement: consistent,
  completed fan-in may run while unrelated pending custody is not due; due
  custody still selects reconciliation, and no provider create is authorized.
- No runtime behavior, schema, package resource, provider operation, or retained
  QA state changed.
- Focused legacy/v0.7/v0.8 matrix passed: 27 tests.
- Paused for API choice between direct released-reader consumption and an
  additive packaged qualification wrapper.

## 2026-08-30 — Slice 2 API review and lean-patch classification

- API approved the same-checkpoint witness and refined precedence.
- API requested a closed packaged three-version fixture/receipt so its consumer
  does not import SBE test helpers or construct a native workspace.
- Activated Slice 3 as additive qualification/package work only.
- Provisionally classified the eventual release as a lean package-only patch:
  focused contract/resource tests, installed-wheel qualification, reproducible
  receipt, deterministic build, and scope audit; no full runtime suite unless
  scope or evidence changes.
- Made setting the fresh version before release-shaped tests a mandatory gate.

## 2026-08-30 — Slice 3 contract frozen

- Froze static fixture, dynamic complete-public-document bundle, and concise
  reproducible receipt as separate artifacts.
- Kept canonical composition validation delegated to released SBE validators.
- Prevented temporary workspace identity from making installed receipts
  irreproducible while preserving complete documents in the per-run bundle.
- Implementation is in progress; no production runtime source has changed.

## 2026-08-30 — Slice 3 implementation complete

- Added the closed fixture, bundle schema, receipt schema, public Python exports,
  qualification runner/validators, and console entry point.
- Bundle generation uses SBE-owned provider-free materialization and the released
  public v0.5/v0.7/v0.8 validators; no test helper is imported by the package.
- Added strict recomputation of stable identity, selected command, local source,
  and custody projections rather than trusting summary booleans.
- New qualification suite passed: 6 tests with one optional `jsonschema` skip.
- Two fresh qualification runs produced receipt SHA-256 `aaa8792054996520e9eb8d0f145b693c96b7de3f871b277f9e63d3f31bb790ea`.
- Paused for API fixture review before version bump and installed-wheel work.

## 2026-08-30 — Slice 3 API review correction

- Tightened bundle validation to derive the frozen v0.5 seam directly from the
  embedded public inspection: exact `ordinary_resume` branch/capacity posture,
  empty `local_dependencies`, and completed provider evidence in retained
  custody.
- Added recomputed-digest mutation coverage for the seam relation, selected
  local source-action projection, retained/due custody projection, and lineage
  conflict outcome.
- New qualification suite passed: 9 tests with one optional `jsonschema` skip.
- Combined legacy/v0.7/v0.8/qualification matrix passed: 36 tests with one
  optional `jsonschema` skip.
- Receipt bytes remain unchanged because the correction strengthens validation
  rather than changing the qualified evidence.
- Paused for API re-review before the lean installed-wheel release gate.

## 2026-08-30 — Slice 4 lean release candidate

- Received API approval of the corrected Slice 3 package.
- Set fresh candidate version `0.4.32` before release-shaped tests and builds.
- Release-shaped focused matrix passed: 36 tests with one optional-schema skip.
- Built two byte-identical wheels with SHA-256
  `c45cd46ff4d7ffa98024b662c55f840e8f7cbea9682d32e97273f6e451493d6e`.
- Audited the wheel for all three new resources and the console entry point.
- Installed exact SBE `0.4.32` with SPC `0.11.1`; `pip check` passed.
- Installed generic release smoke passed.
- Two clean installed qualification invocations emitted byte-identical receipt
  SHA-256 `2401cba4fbf18c21238b34508d28494ad23067033ecfbd072ed256455a9800b1`.
- Scope audit confirms no production lifecycle/provider/custody/authority/
  snapshot/mutation source changed, so the approved lean package-only gate
  remains applicable and the full runtime suite was not run.
- Paused before commit/tag/publication for final owner/API release review.
