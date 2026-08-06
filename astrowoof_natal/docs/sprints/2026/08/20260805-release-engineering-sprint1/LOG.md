# Release-Engineering Sprint Log

## 2026-08-05 — Sprint start

- Reviewed the reconciled `astrowoof-project` documentation after frontend,
  SPC, and AGF contributions.
- Confirmed that release provenance must describe the complete upstream basis
  without bundling AGF or SPC into the Semantic Closure wheel.
- Approved a seven-slice sprint ending in an installed-wheel live Ella run and
  an AstroWoof-scoped v0.1 tag.

## 2026-08-05 — Slice 1 package and dependency audit

- Confirmed the repository has no existing Python packaging metadata.
- Confirmed the seven runtime modules use only the Python standard library.
- Current verified interpreter is Python 3.12.13. Syntax requires at least
  Python 3.10; v0.1 will support Python 3.11 and newer unless installed-wheel
  matrix tests reveal a narrower boundary.
- Found flat sibling imports and extensive `Path(__file__)` source-tree
  assumptions.
- Found subprocess boundaries for SBE invocation, bundled pass acceptance,
  final validation, and final lint.
- Identified authoring documents, schemas, gold references, and executable
  source copied into generated workspaces.
- Found approximately 49 MB of tracked generated material under
  `astrowoof_natal/src` and approximately 252 MB of tracked repository content.
  Package discovery must therefore use a strict allowlist.
- Chose an installed package beneath `astrowoof_natal/src/` so setuptools can
  discover only `astrowoof_natal_authoring` while legacy flat scripts remain
  wrappers beside it.
- Chose `importlib.resources` for static authoring assets and explicit package
  module references for standalone scripts embedded into workspaces.
- Preserved full Kevin and Bre reference inputs for behavioral parity in v0.1;
  later releases may replace them with validated compact extractions.

## 2026-08-05 — Slice 2 installable package boundary

- Added PEP 517/setuptools packaging for distribution
  `astrowoof-natal-authoring` version `0.1.0`, requiring Python 3.11 or newer
  and no third-party runtime dependencies.
- Moved the seven runtime modules beneath the import package
  `astrowoof_natal_authoring`; retained every historical source entry point as
  a thin compatibility wrapper.
- Added the `astrowoof-semantic-closure` and
  `astrowoof-build-natal-basis` console commands.
- Replaced source-tree asset discovery with `importlib.resources` and copied
  only the explicitly approved authoring guidance, schema, and reference
  inputs into the wheel.
- Changed the closure runner's default extractor subprocess to package-module
  invocation, eliminating reliance on a repository script path.
- Built and clean-installed the wheel outside the repository. Both console
  commands loaded from `site-packages` and returned help successfully.
- Ran a complete six-pass Bre workflow from the clean-installed wheel with the
  fake provider and repository examples supplied only as external input. It
  reached `DELIVERY_COMPLETE`, produced 50 cards, four summaries, both dynamic
  theme registries, and an integrity-tested delivery ZIP.
- Re-ran all 105 repository tests after the final invocation change; all
  passed.
- Latest Slice 2 candidate wheel SHA-256:
  `1b97caf2b24f52bf939b266e7d2880104f8240e1019add8e7306fcda20e6b2c5`.

## 2026-08-05 — Slice 3 stable runtime contracts

- Added a versioned projected-input contract and explicit
  `astrowoof-input-manifest.json` format. Existing direct and
  one-directory-per-subject layouts normalize to the same contract and remain
  supported.
- Added a versioned subject-parameters contract. Historical unversioned
  `params.json` files normalize to v0.1; unsupported explicit versions and
  fields are rejected.
- Advanced durable operator state to
  `astrowoof.semantic_closure_run.v0.7`; v0.2 through v0.6 remain resumable.
- Added an authoring-profile snapshot that records behavior-affecting
  extraction, routing, caching, QA, polish, and qualitative-review settings.
- Added atomic `public-run.json` generation as a path-free API polling view.
- Added a versioned delivery manifest to every subject delivery ZIP.
- Preserved source-tree compatibility by selecting the historical extractor
  shim when it exists and installed module invocation otherwise.
- Added six focused contract tests covering legacy normalization, explicit
  manifests, path containment, parameter normalization, public-state
  redaction, and delivery contents.
- Completed a token-free six-pass Bre run through the source compatibility
  entry point. The run reached `DELIVERY_COMPLETE`, exposed all new contract
  versions, and produced a five-file delivery ZIP containing its manifest.

## 2026-08-05 — Slice 4 provenance implementation

- Added versioned authoring provenance covering runtime identity, Python
  runtime class, packaged resources, normalized inputs, declared upstream
  metadata, authoring profile, observed models, attempts, QA reports, and
  delivery artifacts.
- Added deterministic SHA-256 and byte-size descriptors for all four projected
  inputs, optional params, packaged resources, final deck/report artifacts,
  and the completed delivery ZIP.
- Added an aggregate resource-set digest based on ordered resource paths and
  individual content hashes. Generated bytecode remains excluded.
- Harvested only allowlisted AGF/SPC declarations present in projected graphs:
  projection engine/profile/context/registry identities, canonical graph
  type/version/hash, source chart identity, target ontology, and audit hashes.
- Added an explicit unavailable marker for creation-time input provenance when
  migrating old run state; no hashes or upstream versions are reconstructed by
  inference.
- Embedded compact runtime, resource-set, and subject-input provenance into
  each delivery manifest while retaining the complete record in operator state.
- Added four focused provenance tests. The complete suite now contains 115
  passing tests.
- Completed a token-free six-pass Bre run. It verified SPC engine `0.10.0`,
  AGF graph `1.3.0`, four 64-character input digests, 15 packaged resources,
  two final QA report records, a delivery digest, and exact agreement between
  all delivery-manifest hashes and files on disk.

## 2026-08-05 — Slice 5 packaged-runtime QA

- Added `astrowoof-release-smoke`, a self-contained deterministic smoke command
  shipped by the wheel.
- Added four packaged Bre projected-context fixtures. The fixture input is
  materialized from installed resources, not read from the checkout.
- The smoke test creates a run and stops at the pre-authoring `AUTHORING`
  checkpoint, then starts a separate installed-module process with `--resume`.
- Injected one deterministic rejection into pass 1 and verified rejection,
  persisted feedback, retry, and acceptance before the remaining delivery flow.
- Verified extraction, six-pass completion, assembly, 50 cards, four summaries,
  final validation/lint, five-member delivery integrity, delivery-manifest
  hashes, public polling state, input/resource/delivery provenance, cleanup dry
  run, real cleanup, and retained final/operator artifacts.
- Built a clean 612,568-byte candidate wheel with 39 entries, four fixture
  resources, zero bytecode caches, and SHA-256
  `11a1fa255720e9d73c1b1e42bafe937773ec1db544dd62aec786fe89a986e1b7`.
- Installed the wheel in a fresh virtual environment and ran the smoke command
  twice. The second run used `C:\tmp` as its working directory, proving no
  checkout or source-tree import dependency.
- Cleanup identified 20 reconstructable targets and reclaimed 4,627,864 bytes
  while retaining run state, public state, accepted evidence, QA, and delivery.
- Added one fixture-completeness unit test. The complete suite now contains 116
  passing tests.

## 2026-08-05 — Slice 6 controlled live release candidate

- Started the installed-wheel Ella live run only after Slice 5 deterministic
  packaged-runtime QA passed.
- Found and corrected a historical input-fixture naming mismatch before the
  first billable submission: embedded SPC context metadata, rather than legacy
  filenames, established the authoritative general and handler identities.
- The first live candidate safely stopped at `FAILED_REQUIRES_REVIEW`: pass 6
  alternated between theme-group balance and registry failures while passes
  1–5 remained accepted. The run spent an estimated `$0.65478326` and exposed
  that creative retries received only the latest rejection constraint.
- Changed retry feedback to accumulate all distinct issue codes and affected
  claim IDs from earlier rejected attempts. Added focused regression coverage;
  the complete deterministic suite now contains 117 passing tests.
- Built replacement wheel SHA-256
  `8f1f2a700c1cee99b2f5cbd44fa2c89673168b210ec32c2444836b19bb497a97`
  and installed it into a second clean virtual environment.
- The replacement installed-wheel Ella run reached `DELIVERY_COMPLETE` in
  9m 37.6s. All six passes cleared attempt 1, one sparse polish edited two of
  nine eligible fields, final validation passed, and final lint had zero
  warnings.
- Successful-run estimated cost was `$0.43773973`: `$0.42353573` authoring and
  `$0.01420400` polish. The five-member delivery ZIP passed integrity testing
  with SHA-256
  `5217324951edd9d70ed1f144e80a81f4b879161559791d594b921b60f497d12a`.
- Preserved the exact deck, selected packet, delivery manifest, and QA reports
  as the 20260805 Ella release-candidate reference.

## 2026-08-05 — Slice 7 release and consumer handoff

- Committed Slice 6 as `38d21b6` before constructing the final artifact.
- Built the final wheel twice with `SOURCE_DATE_EPOCH=1785928100`; both builds
  were byte-identical at 612,752 bytes with SHA-256
  `58f8d93066cce040ebfc07bc89ffb11254895f0768965aa305296a722aa39dfe`.
- Installed the final wheel in a fresh virtual environment outside the source
  tree. Both production CLIs and the packaged smoke CLI resolved from the
  installation.
- Re-ran the complete installed deterministic smoke: forced rejection and
  cumulative retry, resume, 50-card/four-summary assembly, final QA, five-file
  delivery, manifest hashes, resource identity, and cleanup all passed.
- Added the v0.1 release manifest, checksum, compatibility declaration, release
  notes, and hash-pinned API-worker installation/invocation guide.
- Preserved the final installed-smoke report and Slice 7 release report.
- Left annotated tag `astrowoof-natal-authoring-v0.1.0` intentionally uncreated
  pending explicit final approval.
- Added a release-handoff consistency test tying together artifact filename,
  digest, checksum file, hash-pinned worker requirement, installed smoke, and
  packaged resource identity. The complete suite now contains 118 tests.

## 2026-08-05 — Publication

- Created annotated tag `astrowoof-natal-authoring-v0.1.0` at release commit
  `8fdad164b151c87f77dfc416f6efb754cf00fd7b` and pushed `main` plus the tag.
- Published non-draft, non-prerelease GitHub release ID `365479789` at
  `2026-08-05T11:33:40Z`.
- Uploaded wheel asset ID `502545315` and checksum asset ID `502545321`.
- Downloaded both assets back through the authenticated private-release API.
  The wheel remained 612,752 bytes with SHA-256
  `58f8d93066cce040ebfc07bc89ffb11254895f0768965aa305296a722aa39dfe`,
  and the published checksum matched.
- Documented that private API-worker builds must authenticate to GitHub using
  an ephemeral build secret; no token belongs in the pinned requirement,
  source tree, image layer, or runtime configuration.

## 2026-08-05 — Post-sprint documentation and decision audit

- Reconciled the editorial-quality, cleanup, and release-engineering logs with
  durable component and project documentation.
- Added a maintainer release playbook and promoted installed-runtime,
  reproducibility, retry, metadata-authority, resource-identity, publication,
  and cleanup lessons out of the sprint log.
- Confirmed that project ADR-0002, ADR-0003, and ADR-0005 already cover the
  architectural decisions implicated by this work; remaining surprises are
  component invariants or operational policy rather than missing ADRs.
- Identified and documented a new compatibility boundary: authoring v0.1
  requires `source_chart_id == natal:<subject_id>`, while AGF 0.6 supports an
  arbitrary caller-owned opaque chart ID. No runtime behavior was changed; a
  future versioned authoring-input contract must resolve the distinction before
  that exact production compatibility set is claimed.
- Full regression verification passed: 118 tests.
