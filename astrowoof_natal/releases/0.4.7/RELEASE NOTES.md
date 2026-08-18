# AstroWoof Natal Authoring 0.4.7 Release

Status: final artifact qualified; tag and publication pending

## Summary

SBE 0.4.7 makes the six quality-preserving initial authoring passes concurrently
provider-pending for exact and bounded interactive Natal runs. One SBE run remains
the deck-level unit of custody and recovery; each pass remains independently
prompted, authorized, provider-bound, validated, and provenance-preserved.

The release adds:

- complete six-member authorization preflight before any interactive create;
- concurrent create-only submission with immediate serialized provider-ID durability;
- bounded detach and fresh-worker reconciliation through existing lifecycle states;
- deterministic completion-order-neutral fan-in and pass-local retry;
- unchanged one-paid-round/one-reservation semantics for exact and bounded Batch;
- defensive bounded semantic-equivalence admission and final-QA precedence fixes;
- packaged strict initial-wave schemas, fixtures, builders, validators, and CLI;
- API handoff evidence distinguishing wave evidence from lifecycle authority; and
- provider-free Windows and Linux timing and four-route installed qualification.

The full-response cache-warmer barrier is removed from interactive initial waves.
Retrieval concurrency remains independently capped at four due actions per short
cycle.

## Release gate

Kevin and the AstroWoof API consumer approved Slice 8 and authorized the fresh
0.4.7 build, tag, and publication.

The final wheel is 821,729 bytes with SHA-256
`8fd5268e69a64517e82a3c33eda700ceeaf13bb4465a9e3efe91aafafacc4ad8`.
Two fixed-epoch builds were byte-identical. Exact installed Windows and
network-isolated Linux gates passed without provider calls or paid spend. Final
artifact identity and post-publication verification are recorded in
`release-manifest.json`.
