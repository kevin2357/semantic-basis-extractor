# Slice 2 — Installable Package Boundary

## Result

Slice 2 passed. AstroWoof natal authoring is now an installable Python
distribution with explicit runtime modules and resources, stable console
entry points, and compatibility wrappers for the historical source scripts.

## Installed layout

- Distribution: `astrowoof-natal-authoring==0.1.0`
- Import package: `astrowoof_natal_authoring`
- Supported Python: `>=3.11`
- Third-party runtime dependencies: none
- Primary command: `astrowoof-semantic-closure`
- Extraction command: `astrowoof-build-natal-basis`

The package contains the closure runner, extractor, assembly, validation,
editorial lint, pass acceptance, and projected-term-registry modules. Runtime
guidance, schema, and approved references are accessed through
`importlib.resources`; generated workspaces and historical sprint material are
excluded.

## Compatibility

All seven former flat source modules remain at their previous paths as thin
wrappers. Existing repository commands therefore continue to work while new
consumers can use the installed console commands or package modules. The
installed extractor no longer assumes that repository examples exist: an
input package or input directory is required.

## Verification

The candidate wheel was built and installed into a fresh virtual environment
under `C:\tmp`, outside the source repository. Verification established that:

1. package imports resolve from `site-packages`;
2. both console commands expose their command-line help;
3. approved package resources are present;
4. generated and historical directories are absent from the wheel;
5. a complete six-pass fake-provider run can start from external projected
   inputs and finish without source-tree runtime access;
6. the result contains 50 cards, four summaries, Interdogpendence and
   Takeaways theme registries, and a delivery ZIP; and
7. the complete repository suite passes: 105 tests, zero failures.

The tested candidate wheel was:

`astrowoof_natal_authoring-0.1.0-py3-none-any.whl`

SHA-256:

`1b97caf2b24f52bf939b266e7d2880104f8240e1019add8e7306fcda20e6b2c5`

This is a Slice 2 candidate, not yet the final release artifact. Later slices
may change the wheel while adding contracts and provenance, so the final
release checksum will be generated during Slice 7.

## Deferred to later slices

- versioned public and operator contracts;
- complete provenance harvesting and artifact hashes;
- packaged regression fixtures and automated installed-wheel smoke tests;
- controlled live Ella verification;
- final release manifest, compatibility declaration, wheel, and tag.
