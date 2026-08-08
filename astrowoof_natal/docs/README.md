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

## Current release

The current immutable AstroWoof natal authoring runtime is version `0.1.0`,
published under the annotated tag `astrowoof-natal-authoring-v0.1.0`.

Start with:

- [`../releases/0.1.0/API WORKER INTEGRATION.md`](../releases/0.1.0/API%20WORKER%20INTEGRATION.md)
  for the pinned installation, invocation, polling, terminal-state, and service
  ownership handoff;
- [`../releases/0.1.0/COMPATIBILITY.md`](../releases/0.1.0/COMPATIBILITY.md)
  for supported Python, input, run-state, delivery, and upstream boundaries;
- [`post_extraction_authoring/Semantic Closure Runner.md`](post_extraction_authoring/Semantic%20Closure%20Runner.md)
  for the detailed CLI and operational reference; and
- [`post_extraction_authoring/Maintainer Release Playbook.md`](post_extraction_authoring/Maintainer%20Release%20Playbook.md)
  for qualification, compatibility, and publication work on later releases;
- [`post_extraction_authoring/Provider Spend Enforcement.md`](post_extraction_authoring/Provider%20Spend%20Enforcement.md)
  for the v0.8 per-run paid-action ledger and provider atomicity boundary;
- [`post_extraction_authoring/Spend Authorization Consumer Handoff.md`](post_extraction_authoring/Spend%20Authorization%20Consumer%20Handoff.md)
  for the API prepare/authorize/execute integration contract; and
- [`post_extraction_authoring/Provider Disclosure and Durable Workspace Contract.md`](post_extraction_authoring/Provider%20Disclosure%20and%20Durable%20Workspace%20Contract.md)
  for minimized provider fields and complete stable-path snapshots; and
- [the GitHub release](https://github.com/kevin2357/semantic-basis-extractor/releases/tag/astrowoof-natal-authoring-v0.1.0)
  for the immutable wheel and checksum assets.

The released wheel SHA-256 is
`58f8d93066cce040ebfc07bc89ffb11254895f0768965aa305296a722aa39dfe`.
Release-specific handoff files are authoritative for consuming that immutable
version. Sprint records explain how it was qualified but are not the primary
consumer documentation.
