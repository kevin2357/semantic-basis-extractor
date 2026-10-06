# Bounded Birth-Time Modern Authoring Integration Sprint 4 Plan

## Status

**Not started.** No prompt release, provider work, wheel publication, or worker
deployment is authorized by planning alone.

## Slice 0 — Contract mapping and bounded profile design

Map the historical bounded route to current processing-profile, prompt-release,
runtime-config, package descriptor, terminal-result, receipt, and observability
contracts. Design a new immutable `bounded_natal` profile/prompt family rather
than mutating current exact profiles. Specify the current public general voice
alongside handler/direct/hybrid outputs and the 50-card eligibility rule.

**Gate A — API contract alignment:** wait for API Sprint 128 Gate A. Record the
accepted sealed handoff, artifact/disposition vocabulary, profile identity,
receipt fields, and strict mismatch behavior jointly with API.

## Slice 1 — Installed-profile-bound bounded lifecycle

Implement the bounded CLI/lifecycle behind the new installed profile. Consume
only the sealed four-context projection family; validate source/config/profile
and closed disposition vocabulary before selector/provider work. Carry stable
facts-only provenance through planning, authoring, editorial review, terminal
result, receipt, and replay/successor exports.

Provider packets must exclude raw interval/location/source evidence and must
not invent exact/variable placements. Retain sufficient internal provenance for
API's immutable ingress and economics/reconciliation behavior.

## Slice 2 — Provider-free fixture and installed-wheel qualification

Create near-full, sparse, and full-local-day bounded fixture families; assert
the 50-card floor, all four public voices, invariant-only selection, sealed
identity refusal, wrong/missing artifact refusal, and receipt/replay behavior.
Build and qualify a candidate wheel through the real installed executable.

For a valid sealed source family below the floor, emit a distinct deterministic
bounded eligibility result—not a provider/editorial retry—so API can surface a
non-retryable correction path without conflating it with operational failure.

**Gate B — candidate handoff to API:** publish a versioned candidate identity,
real bounded terminal-result/receipt fixture, and mismatch fixtures for API
Sprint 128 Slices 2–3. API then owns receipt-ingress idempotency proof.

## Slice 3 — Joint provider-free and QA qualification

Participate in API Gate C installed-wheel proof. Once API delivery fixtures are
available, confirm bounded payloads remain presentation-compatible. Only after
all joint proof passes may a bounded profile be released/registered for a
separately approved QA cohort.

## Completion criteria

The current SBE architecture—not the historical parallel command alone—can
author and export a sealed bounded 50-card result with immutable prompt/profile
provenance, and API can consume it without special-case translation.
