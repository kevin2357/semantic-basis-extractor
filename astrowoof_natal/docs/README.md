# AstroWoof Natal Documentation

## Documentation authority

This directory is authoritative for the implementation and evidence owned by
the AstroWoof natal Semantic Basis Extractor and Semantic Closure runtime:

- extraction, scoring, selection, and synthesis behavior;
- authoring workspace construction and guidance;
- provider orchestration, retry, resume, and accounting;
- deterministic acceptance, validation, lint, assembly, and cleanup;
- component-level artifact schemas and compatibility behavior;
- authoring experiments, reference decks, sprint logs, and detailed findings.

Cross-system product direction, repository ownership, shared consumer
contracts, architecture decisions, roadmaps, and private-launch policy are now
owned by the
[AstroWoof project control plane](https://github.com/kevin2357/astrowoof-project).

## Relationship between the repositories

Project documents describe what participating components collectively promise.
These SBE documents describe how this component implements and verifies its
part of those promises. Historical sprint records remain here as evidence even
after their decisions are promoted to the project repository.

If the project contract and current implementation disagree, treat the mismatch
as work to reconcile. Do not silently reinterpret either document as stale.

## Primary areas

- `extractor/`: semantic-basis extraction design and contracts.
- `post_extraction_authoring/`: authoring, Semantic Closure, editorial QA, and
  implemented deck behavior.
- `sprints/`: date-scoped plans, logs, results, and experimental evidence.

