# API Request — Slice 4B Public Happy-Path Witnesses

## Purpose

Sprint 54 in the API repository now separates broad generated lifecycle
simulation from installed-SBE engine qualification. The existing Slice 4A bundle
is an excellent real-engine witness for one post-fan-in creative retry, including
not-due reconciliation, retrieval, local fan-in, ordinary v2 authority, one
dispatch, and exact replay.

It deliberately does not prove every normal continuation shape. API can simulate
those shapes, but must not claim SBE produces them unless SBE exports a public
provider-free witness. We request a narrow Slice 4B rather than a fixture for
every permutation.

## Requested public witnesses

Add two representative, provider-free, installed-wheel qualification artifacts:

1. **Two ordinary retries with out-of-order provider completion.**
   - Two distinct prepared ordinary actions and provider identities.
   - One provider result becomes available before the other despite opposite
     submission/order position.
   - Reconciliation and local fan-in retain exact action/operation identity.
   - Each successor requires its own distinct exact ordinary-v2 action binding,
     authorization document, and ordered grant member; no initial-wave v1
     authority is revived. When both successors become co-ready after retained
     provider custody has cleared, one sealed ordinary-v2 action-set
     request/grant may authorize their complete ordered set. The fixture must
     not require artificial separate temporal request envelopes.
   - Replay causes no duplicate retrieval, local consumption, grant consumption,
     or create.

2. **A retry followed by a supported downstream ordinary stage.**
   - One completed retry is locally consumed exactly once.
   - The next ordinary stage is selected through the supported native route and
     exposes a distinct exact v2 authority request.
   - Explicitly end at the next truthful public non-local/provider-pending or
     delivery-ready disposition; do not claim API reader delivery.
   - Replay is nonduplicating.

## Required public boundary

Follow the Slice 4A pattern where appropriate:

- closed versioned schemas and packaged fixtures;
- supported public Python reader/runner/validator and provider-free CLI;
- exact ordered projection phases, semantic/outer digests, and canonical receipt
  binding;
- public route/mechanism/command/capacity/reason/eligibility, provider custody
  inventory, local operation keys and consumption, and external-authority action
  inventory;
- strict privacy: no raw workspace state, paths, prompts, provider payloads or
  IDs, credentials, protected provenance, or retained-QA data; and
- installed-wheel reproducibility, mutation, and replay tests with zero provider
  network calls and zero spend.

The artifact must remain observational evidence only. It must not grant API
permission to choose a native command, create provider work, reconstruct omitted
private checkpoint state, or manufacture authority documents.

## API consumption and acceptance

API will pin the resulting wheel by SHA-256, run the public artifacts from an
isolated installation, validate the receipt/bundle joins, and use a narrow public
adapter to exercise real API persistence, queue, lease, capacity, reservation,
and stale-replay effects. It will not use private SBE workspace state.

The generated API simulator remains the broad combinatorial layer; these two
fixtures are representative real-engine witnesses, not a demand for exhaustive
fixture enumeration.
