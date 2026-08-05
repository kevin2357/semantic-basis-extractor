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

