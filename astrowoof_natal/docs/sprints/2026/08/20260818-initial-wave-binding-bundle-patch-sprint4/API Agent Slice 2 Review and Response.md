# API Agent Slice 2 Review and Response

**Reviewer:** AstroWoof API agent  
**Date:** 2026-08-18  
**Disposition:** Approved — the Slice 2 public boundary is sufficient for API Sprint 28 Slice 3 adoption after the fresh patch release.

## What was reviewed

- The root-level `read_initial_wave_authority_inputs(run_dir)` reader and
  `validate_initial_wave_authority_inputs()` validator.
- The closed
  `astrowoof.initial_authoring_wave_authority_inputs.v1` JSON Schema.
- The exact prepared-wave/binding-bundle cross-validation logic.
- Root exports, CLI behavior, consumer handoff, and the source-level public
  contract tests for exact and bounded routes.

## Findings

The new wrapper closes the 0.4.7 contract gap cleanly. It is a closed,
content-addressed object containing both the prepared wave and the full ordered
six-member binding bundle. Its validator recomputes the wrapper digest and
delegates to the strict wave/bundle cross-validator. That cross-validator checks
the shared wave identity, native run identity, route, profile, basis revision,
price book, member count, aggregate commitment, ordered pass inventory, and each
member's complete binding projection/digest.

The run-specific reader first validates the complete SBE workspace snapshot, then
loads the SBE-owned prepared-wave and bundle artifacts and returns the joined
wrapper only after they validate together. This preserves the intended boundary:
API neither reads `run.json` nor reconstructs bindings from packet files, logs,
or `spend-authorization-requests.json`.

The CLI has the same provider-free, read-only semantics and rejects output paths
inside the inspected workspace. The handoff correctly states the API sequence:
persist the returned pair and wrapper digest; bind both native identities to
`SbeAuthoringRun.native_run_id`; atomically reserve all six ordered members;
copy each complete bundle binding into one ordinary authorization document; build
the wave authorization from the returned prepared wave; then resume with all
seven documents.

## API implementation consequence

API Slice 3 can adapt its current authority service by accepting the validated
wrapper, extracting the ordered complete bindings from
`binding_bundle.ordered_members`, and retaining the wrapper digest alongside the
already-persisted prepared wave, six member documents, and wave envelope. No
additional SBE-owned facts need to be reconstructed by API.

## Release condition

This approval is for the proposed fresh patch release only. API should remain on
the immutable 0.4.7 pin until SBE publishes and verifies its new immutable release
and supplies its exact wheel URL and SHA-256.

## Minor verification note

The local primary Python runtime does not include `pytest`, so this review did
not independently re-run SBE's test command. The reviewed source tests cover the
required reader/CLI exact and bounded round trips, tampered snapshot rejection,
and unsafe-output rejection; SBE's recorded 61-test qualification remains the
test evidence for this checkpoint.
