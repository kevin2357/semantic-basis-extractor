# AstroWoof Natal Authoring v0.1 Release-Engineering Sprint

```yaml
status: complete
started: 2026-08-05
owner: semantic-basis-extractor
project_initiative: astrowoof-project/planning/now/Release Engineering - Semantic Closure v0.1.md
target_distribution: astrowoof-natal-authoring
target_release: astrowoof-natal-authoring-v0.1.0
```

## Outcome

Produce a versioned, self-contained, smoke-tested AstroWoof natal authoring
runtime that a future API worker can consume as an immutable dependency. The
canonical release artifact is a Python wheel; a thin worker container may be
derived from it later.

The release begins from four completed SPC projected-chart artifacts and
subject parameters. It does not bundle or execute AGF or SPC. It validates and
records the upstream provenance available in those inputs, then performs SBE,
six-pass LLM authorship, pass QA, retry/resume, assembly, final QA, bounded
polish, accounting, cleanup, and delivery.

## Release names

- Distribution: `astrowoof-natal-authoring`
- Import package: `astrowoof_natal_authoring`
- Primary CLI: `astrowoof-semantic-closure`
- Extraction CLI: `astrowoof-build-natal-basis`
- Release tag: `astrowoof-natal-authoring-v0.1.0`

Existing source-tree scripts remain compatibility shims during v0.1.

## Slices

### Slice 1 — Package and dependency audit

- Inventory runtime modules, imports, subprocess boundaries, static resources,
  fixtures, repository-relative paths, and generated material.
- Define package inclusion/exclusion policy and proposed installed layout.
- Record supported Python and dependency assumptions.
- Make no runtime behavior changes.

### Slice 2 — Installable package boundary

- Add `pyproject.toml` and the `astrowoof_natal_authoring` package.
- Convert sibling imports to package imports.
- expose console entry points;
- replace repository-relative runtime assets with packaged resources;
- preserve source-tree script compatibility;
- build and import the wheel in a clean environment.

### Slice 3 — Stable runtime contracts

- Version projected-input bundle normalization.
- Define subject parameters, public/operator run state, delivery manifest, and
  authoring-profile contracts.
- Preserve legacy directory discovery by normalizing it into the same internal
  manifest.

### Slice 4 — Provenance implementation

- Record runtime, contract, resource, authoring-profile, model/routing, and QA
  provenance.
- Harvest available AGF/SPC source, engine, profile, context, registry, and
  artifact provenance without inventing absent fields.
- Hash inputs and delivery artifacts.

### Slice 5 — Packaged-runtime QA

- Install the wheel outside the repository.
- Run deterministic extraction and fake-provider end-to-end tests.
- Test retry, resume, assembly, validation, cleanup, resource completeness,
  and delivery integrity without source-tree access.

### Slice 6 — Controlled live release candidate

- Run Ella from the installed wheel through the actual OpenAI service.
- Use the approved cost-optimized release profile and normal polish policy.
- Compare result class, cost, and provenance with the last known-good run.

### Slice 7 — Release and consumer handoff

- Build the final wheel and checksums.
- Produce release, resource, compatibility, smoke, and live-QA reports.
- Document pinned API-worker installation and invocation.
- Commit and create the annotated v0.1 tag after approval.

## Controls

- Do not redesign extraction or editorial behavior during packaging.
- Preserve the current source-tree CLI until compatibility tests pass.
- Use an explicit package allowlist; never package directories by repository
  proximity.
- Do not include historical sprint workspaces or bulk reference-deck history.
- Do not claim AGF/SPC provenance that source artifacts do not carry.
- Keep operator provenance primarily in run/delivery manifests rather than
  swelling the reader-facing deck.
- No live API call before deterministic installed-wheel QA passes.
- Tag only after the controlled live run and explicit approval.

## Exit criteria

- clean installation outside the source tree;
- both primary CLIs work from the installed wheel;
- required resources are present and hashed;
- deterministic fake-provider workflow passes without repository access;
- retry/resume/cleanup and final artifact integrity pass;
- one installed-wheel Ella live run succeeds;
- final artifacts identify runtime, profile, contracts, inputs, and hashes;
- a release manifest and compatibility declaration exist;
- the API can pin the immutable wheel by version and SHA-256;
- the annotated release tag is created only after approval.
