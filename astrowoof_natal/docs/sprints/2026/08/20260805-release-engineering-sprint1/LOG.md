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
