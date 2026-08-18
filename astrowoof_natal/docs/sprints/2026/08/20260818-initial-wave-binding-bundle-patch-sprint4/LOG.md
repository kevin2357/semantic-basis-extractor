# Initial-Wave Binding Bundle Patch Sprint 4 Log

## 2026-08-18 — 0.4.8 tagged, published, and verified

- Created annotated tag `astrowoof-natal-authoring-v0.4.8` at release-lock commit
  `d34bd5810949cf88368f4962968928461d982ac3`.
- Published GitHub release ID `372680192` with the exact wheel and checksum asset.
- Authenticated independent re-download matched 828,375 bytes and SHA-256
  `572a46f310b9ea150a49d32705a45e3d0ced501462d2b2743d989ef5b44fb9e1`.
- Release is neither draft nor prerelease. The immutable tag was not moved.

## 2026-08-18 — Exact 0.4.8 artifact qualified and authorized

- Kevin explicitly authorized a fresh immutable 0.4.8 tag and publication.
- Versioned artifact source commit:
  `4e017dbe16846d57dea0649845c76f9be693b991`.
- Two exact fixed-epoch builds were byte-identical: 828,375 bytes, SHA-256
  `572a46f310b9ea150a49d32705a45e3d0ced501462d2b2743d989ef5b44fb9e1`.
- The exact 0.4.8 wheel passed installed Windows and network-isolated Linux
  `pip check`, lifecycle smoke, release smoke, and exact/bounded joined-reader/CLI
  qualification. Provider operations and spend remained zero.

## 2026-08-18 — Final API review accepted

- API approved the reviewed source boundary for a fresh immutable 0.4.8 release
  without code, schema, or handoff changes.
- Confirmed the public joined-reader sequence supplies every SBE-owned fact API
  needs for atomic six-member reservation and exact-copy authorization creation.
- Release remains gated on Kevin's explicit publication authorization, exact
  0.4.8 rebuild, immutable tag/publication, and independent published-asset hash
  verification.
- Repository-root `.runs/` remains excluded from commits, tags, and wheel input.

## 2026-08-18 — Slice 4 complete; release review pending

- Full source suite completed 469 tests in 338.064 seconds: 449 passed and 20
  expected environment-dependent tests skipped.
- Built twice from `34de4798be76482dbb9f39a9fd59561bea9f81fe` at fixed
  epoch `1787090323`; both non-publishable 0.4.7-labeled candidate wheels were
  byte-identical SHA-256
  `f15d0afc9fd4eaac6c0a48c78af4c0787fef696ecc55a158be5778047e633b1e`.
- Wheel inspection found 118 entries, 71 resources, `py.typed`, all new public
  contracts/fixtures, and no tests or bytecode.
- Installed Windows CPython 3.12.13 and network-isolated Linux CPython 3.11.15
  passed `pip check`, lifecycle smoke, release smoke, and exact/bounded public
  joined-reader/CLI round trips.
- Strict Linux initial-wave contract suite: 36 passed without skips.
- Recommend a fresh immutable 0.4.8 only after final Kevin/API review and explicit
  release authorization. Provider operations and spend: zero.

## 2026-08-18 — Slice 3 complete; awaiting Kevin review

- Added provider-free exact and bounded API-shaped round trips from the joined
  public authority inputs through six ordinary authorizations, the wave envelope,
  all-or-none preflight, and six independently persisted simulated identities.
- Changed exact/bounded route integration tests to source complete bindings from
  the public bundle rather than the private native spend ledger.
- Added reordered, missing, duplicate, unknown, cross-run, profile, revision,
  price-book, model, wrapper, wave, order, and one-field binding mismatch cases.
- Every refusal proves zero create callbacks; existing route integration continues
  to cover zero native authorization consumption on failed preflight.
- Focused route/round-trip gate: 5 passed. Initial-wave public/contract suite:
  36 passed with 10 optional schema-library skips in the base Windows runtime.
- Provider operations and spend: zero.

## 2026-08-18 — Sprint proposed

- API Slice 2 identified that Initial Authoring Wave v1 exposes binding digests but
  lacks a strict supported public artifact carrying the six complete bindings.
- Confirmed `spend-authorization-requests.json` contains the facts but is not an
  adequate wave-bound closed public contract.
- Proposed a narrow additive binding-bundle v1 contract and fresh immutable 0.4.8.
- Awaiting Kevin approval before Slice 0.

## 2026-08-18 — Slice 0 complete; awaiting contract review

- Inventoried exact and bounded preparation: both create and persist complete native
  action bindings before projecting prepared-wave members.
- Froze `astrowoof.initial_authoring_wave_binding_bundle.v1` and root artifact path
  `initial-authoring-wave-binding-bundle.json`.
- Froze canonical digest, six-member ordering, wave/binding cross-validation,
  snapshot-validating run reader, CLI shape, refusal causes, legacy failure, and
  disclosure inventory.
- Confirmed no lifecycle/oracle vocabulary, Batch authority, editorial, or provider
  request changes.
- Proposal/current-wave suite: 18 passed without skips in offline Linux with
  `jsonschema`; the base Windows environment passed 16 with two expected optional
  `jsonschema` skips.
- Provider operations and spend: zero.

## 2026-08-18 — Slice 2 API review accepted

- API approved the joined public reader, wrapper/schema, cross-validation, root
  exports, CLI, consumer handoff, and exact/bounded test evidence without changes.
- Confirmed API Slice 3 can consume the wrapper, persist both documents and digest,
  atomically reserve the six ordered bindings, create six ordinary authorizations,
  build the wave envelope, and resume without reconstructing SBE facts.
- Reconciled the consumer-review manifest to `api_approved`.

## 2026-08-18 — Slice 2 complete; awaiting API review

- Added one snapshot-validating public reader that returns the exact prepared wave
  and binding bundle together in a closed content-bound wrapper.
- Added `--initial-wave-inputs --run-dir` CLI support and rejected output paths
  inside the inspected workspace.
- Packaged strict bundle/pair schemas, exact/bounded fixtures, root exports, catalog
  entries, lifecycle-smoke resources, and updated consumer handoffs.
- Public/contract suite: 61 passed. Strict resolved schema validation: pass.
- Installed candidate and exact/bounded run-specific Python/CLI qualification: pass.
- Candidate SHA-256: `15068ee064654226a7c05a37cddce18cc0e0ecb28c27b54e7824b1e8f46fd78a`;
  qualification-only and not publishable as 0.4.7.
- Provider operations and spend: zero.

## 2026-08-18 — Slice 0 API review accepted

- API accepted the binding-bundle design with one public-reader completion
  condition.
- Added a closed content-bound authority-inputs wrapper returning the exact
  run-specific prepared wave and binding bundle from one snapshot-validating
  operation.
- Froze root reader `read_initial_wave_authority_inputs(run_dir)` and CLI operation
  `--initial-wave-inputs`; validation failure of either document or their join
  returns neither.

## 2026-08-18 — Slice 1 complete

- Added shared binding-bundle construction, strict validation, canonical digest,
  action-identity validation, and prepared-wave cross-validation.
- Exact and bounded fresh interactive preparation now write one root binding bundle
  from the same authoritative complete bindings used for native action preparation.
- The artifact is included in the complete workspace snapshot. Changed bytes fail
  snapshot validation; restored exact bytes validate again.
- Documented the publication protocol without claiming cross-file filesystem
  atomicity. Interrupted pre-snapshot publication exposes no valid checkpoint.
- Combined wave/exact/bounded suite: 139 passed in 289.799 seconds. Final focused
  regression: 5 passed in 4.810 seconds.
- Provider operations and spend: zero.
