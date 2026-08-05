# Slice 1 — Packaging and Dependency Audit

## Result

Slice 1 is complete. The current runtime is straightforward to distribute but
not currently installable. It has no third-party runtime dependencies; every
identified obstacle is package layout, resource discovery, subprocess
invocation, or release-contract work.

No runtime behavior changed in this slice.

## Runtime module inventory

| Current module | Release role | Proposed package module |
|---|---|---|
| `author_semantic_closure.py` | orchestration, providers, resume, accounting, polish, cleanup | `astrowoof_natal_authoring.closure` |
| `build_projected_semantic_basis.py` | extraction, selection, synthesis, compact chart, workspace generation | `astrowoof_natal_authoring.extractor` |
| `assemble_authoring_workspace.py` | parse authored fields and assemble deck | `astrowoof_natal_authoring.assembly` |
| `validate_astrowoof_editorial.py` | final structural validation | `astrowoof_natal_authoring.validation` |
| `lint_astrowoof_editorial.py` | whole-deck editorial lint | `astrowoof_natal_authoring.editorial_lint` |
| `lint_authoring_pass.py` | opaque per-pass acceptance | `astrowoof_natal_authoring.pass_acceptance` |
| `merge_projected_term_registries.py` | projected registry merge | `astrowoof_natal_authoring.registries` |

Existing filenames remain thin wrappers in v0.1. This avoids breaking local
commands and gives tests a deliberate migration path instead of maintaining two
behavioral implementations.

## Dependency inventory

All runtime imports are from the Python standard library. No OpenAI SDK is used;
provider transport uses `urllib`. The wheel therefore requires no third-party
runtime dependency.

Build/test tooling may use `setuptools`, `build`, and `wheel`, but those are not
runtime requirements.

The code uses union type syntax and other modern annotations requiring Python
3.10 or later. The release target is Python 3.11+ because 3.11 is a stable
deployment floor and 3.12 is the currently verified environment. Slice 5 will
test the actual available interpreter matrix before the metadata is frozen.

## Source-tree coupling

### Imports

Runtime modules currently import flat siblings by filename. Installed package
modules require relative/package imports. Tests currently prepend
`astrowoof_natal/src` to `sys.path` and patch flat module names.

### Subprocesses

Closure currently launches:

1. SBE by Python executable plus a filesystem script path;
2. each pass's standalone bundled acceptance checker;
3. final validation by Python executable plus a sibling script path; and
4. final lint by Python executable plus a sibling script path.

The pass checker remains a legitimate standalone subprocess because it is part
of the authored workspace contract. SBE, validation, and lint should use package
APIs or module entry points so installed execution does not depend on sibling
files. Subprocess evidence remains captured in run state where operationally
useful.

### Static resources

SBE currently derives a repository root from `__file__` and reads authoring
guidance, schemas, and references from `docs/` and `qa/`. These become package
resources accessed through `importlib.resources`.

The opaque checker currently reads the three checker/assembly source modules
from the repository `src/` directory, compresses them, and embeds them in a
portable launcher. In the package it should read the installed package module
source explicitly. Wheels install `.py` source, but a packaged-resource snapshot
or integrity test must prevent source/checker drift.

## Required runtime resources

### Authoring-workspace release path

- `AstroWoof Story Workspace Authoring Brief.md`
- `AstroWoof Authoring Guiding Lights.md`
- Kevin six-pass final deck, used only to render the four-Summary craft reference
- source for assembly, editorial lint, and pass acceptance
- final validator and linter standalone source copied into handoff bundles

### Supported secondary SBE profiles

The secondary extraction CLI currently exposes rigorous and compact handoffs in
addition to the Closure authoring workspace. Preserving those public modes
requires:

- Semantic Basis Extractor Pipeline and Scoring Metrics
- Proposed LLM Handoff Prompt
- LLM Editing Permissions and QA Checklist
- LLM Card-by-Card Authoring Execution Protocol
- AstroWoof Independent Card Writing Brief
- AstroWoof Projected Natal Card Authoring Manual
- AstroWoof Compact Single-Subject Authoring Brief
- Compact LLM Handoff Prompt
- Multi-Subject LLM Handoff README
- AstroWoof Authoring Packet Schema
- AstroWoof Bre Editorial Gold Reference

These files will be copied into a package-owned `resources/` hierarchy. The
release will not read them from project documentation paths at runtime.

## Inclusion policy

The wheel includes only:

- `astrowoof_natal_authoring/**/*.py`;
- explicitly enumerated authoring documents;
- explicitly enumerated JSON schemas;
- the Bre editorial reference;
- the Kevin Summary craft source;
- one minimal deterministic projected-input smoke fixture;
- package metadata and release-profile resources.

The wheel excludes:

- `docs/sprints/**`;
- `docs/**/orig/**`;
- bulk `qa/reference_decks/**` history;
- generated SBE outputs and LLM handoff bundles;
- `.tmp-*` workspaces;
- OpenAI request/response evidence;
- `.idea`, caches, logs, and local environments;
- personal input archives and absolute-path material;
- the AGF and SPC runtimes.

The two required gold sources are copied into package resources; their original
directories are not package roots.

## Proposed installed layout

```text
pyproject.toml
astrowoof_natal/
  src/
    astrowoof_natal_authoring/
      __init__.py
      closure.py
      extractor.py
      assembly.py
      validation.py
      editorial_lint.py
      pass_acceptance.py
      registries.py
      cli/
        __init__.py
        closure.py
        extract.py
      resources/
        authoring/
        schemas/
        references/
        fixtures/
        release-profile.json
    author_semantic_closure.py        # compatibility wrapper
    build_projected_semantic_basis.py # compatibility wrapper
    ...                               # remaining compatibility wrappers
```

Setuptools package discovery will include only
`astrowoof_natal_authoring*`. It will not scan arbitrary files or directories
already present under `astrowoof_natal/src`.

## Size and repository hygiene finding

Tracked generated material beneath `astrowoof_natal/src` is approximately
49 MB; the repository contains approximately 252 MB of tracked content. This
does not prevent a small wheel when package discovery is allowlisted, but it is
a repository-hygiene issue and a credible accidental-packaging hazard.

This sprint will protect the release artifact through strict inclusion tests.
Removing or relocating historical tracked material is a separate, potentially
destructive cleanup decision and is not silently folded into packaging.

## Slice 2 adjustments

1. Establish the package before changing behavior.
2. Keep compatibility wrappers so the current test suite can migrate in steps.
3. Add a resource API rather than scattering `importlib.resources` calls.
4. Preserve rigorous/compact secondary CLI behavior in v0.1 even though Closure
   uses the authoring-workspace profile.
5. Include the current full Bre and Kevin reference sources for exact behavioral
   parity; optimize them only after installed-wheel comparison tests exist.
6. Make installed CLI input explicit rather than silently defaulting to a
   repository examples directory.

## Slice 1 acceptance

- Audit covers all seven runtime modules.
- Runtime imports are standard-library-only.
- Every identified subprocess and repository-relative resource boundary is
  recorded.
- Inclusion/exclusion policy is explicit.
- Package/CLI names and layout are explicit.
- No runtime code changed.

