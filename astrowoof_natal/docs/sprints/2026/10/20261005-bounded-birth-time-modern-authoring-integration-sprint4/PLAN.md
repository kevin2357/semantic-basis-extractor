# Bounded Birth-Time Modern Authoring Integration Sprint 4 Plan

## Status

**Gate A and API Gate B accepted; Slices 1–2 are complete.**
API Sprint 128's Gate A freezes the birth-data and generation-family boundary.
API's representative AGF-originated four-context packet and eligibility-result
receiver are qualified. No profile activation, provider work, wheel
publication, or worker deployment is authorized by that approval.

## Slice 0 — Contract mapping and bounded profile design

Map the historical bounded route to current processing-profile, prompt-release,
runtime-config, package descriptor, terminal-result, receipt, and observability
contracts. Design a new immutable `bounded_natal` profile/prompt family rather
than mutating current exact profiles. Preserve the current three rendered
audiences—handler, direct-to-dog, and hybrid—and the 50-card eligibility rule.

**Complete:** [modern bounded integration map](SLICE%200%20-%20MODERN%20BOUNDED%20INTEGRATION%20MAP.md)
finds the bounded semantic/privacy core reusable, but identifies two required
adapters beyond catalog records: installed profile-bound invocation and current
command-result/receipt terminal handoff.

**Gate A — API contract alignment: accepted.** API Sprint 128 completed its
birth-data, family-selection, migration, and public fixture qualification. The
next SBE work can define the profile-bound bounded command contract; it must
not infer that an arbitrary legacy bounded workspace is API-admissible.

## Slice 1 — Installed-profile-bound bounded lifecycle

Implement an integrated bounded command/lifecycle behind the new installed
profile. Consume only the sealed four-context projection family; validate
source/config/profile and closed disposition vocabulary before selector/provider
work. Derive behavior-affecting values from the installed profile rather than
legacy free-form command flags. Carry stable-facts-only provenance through
planning, authoring, editorial review, terminal result, receipt, and
replay/successor exports.

Provider packets must exclude raw interval/location/source evidence and must
not invent exact/variable placements. Retain sufficient internal provenance for
API's immutable ingress and economics/reconciliation behavior.

Retain the established three rendered audiences in bounded artifacts and
validation, and emit a typed non-provider bounded-eligibility result when a
valid sealed source is below the 50-card floor.

**Complete:** the profile-bound handoff, durable binding/resume equality,
workspace guidance inventory, release-owned provider prompts, exact
terminal-delivery command envelope, and jointly typed under-50 eligibility
result are implemented provider-free. The eligibility path emits no workspace,
receipt, authorization, or provider operation; API validates the source and
profile identities against its immutable authority before admitting it.

## Slice 2 — Provider-free fixture and installed-wheel qualification

Create near-full, sparse, and full-local-day bounded fixture families; assert
the 50-card floor, all three rendered audiences, invariant-only selection,
sealed identity refusal, wrong/missing artifact refusal, and receipt/replay
behavior.
Build and qualify a candidate wheel through the real installed executable.

For a valid sealed source family below the floor, emit a distinct deterministic
bounded eligibility result—not a provider/editorial retry—so API can surface a
non-retryable correction path without conflating it with operational failure.
That command contract and API receiver are implemented. **Complete:** the
installed-wheel real four-context family selects 50 invariant candidates,
reaches a sealed `DELIVERY_COMPLETE` terminal result/receipt, and proves the
exact terminal-command join. Missing-context, incompatible-contract, and
altered-receipt variants refuse fail-closed. The initial under-floor wheel is
superseded by the later retained candidate recorded in
[Slice 2 installed fixture evidence](SLICE%202%20-%20INSTALLED%20REAL%20FOUR-CONTEXT%20TERMINAL%20FIXTURE.md).

**Gate B — candidate handoff to API:** SBE has produced the versioned
candidate identity, real bounded terminal-result/receipt fixture, and mismatch
fixtures. API Sprint 128 now owns receipt-ingress idempotency proof and the
separately authorized public-delivery/admission path.

**Current dependency: satisfied.** API Sprint 128 Gate B has supplied its
representative AGF-originated four-context artifact family. SBE must consume
that sealed evidence for the eligible fixture; no QA deployment or provider
operation is part of this slice.

### Slice 2B — under-floor attempt-identity alignment

Correct the candidate-only under-floor result so its API-issued idempotency
identity is `command_attempt_id`, not `native_invocation_id`. The latter is
reserved for SBE's receipt-backed sealed-publication boundary and does not
exist before a workspace/result/receipt. Advance the closed eligibility schema
to v2, rebuild the candidate, and require API's receiver fixture to validate
the matching attempt ID. **Complete provider-free; candidate rebuild follows.**

## Slice 3 — Joint provider-free and QA qualification

Participate in API Gate C installed-wheel proof. Once API delivery fixtures are
available, confirm bounded payloads remain presentation-compatible. Only after
all joint proof passes may a bounded profile be released/registered for a
separately approved QA cohort.

## Completion criteria

The current SBE architecture—not the historical parallel command alone—can
author and export a sealed bounded 50-card result with immutable prompt/profile
provenance, and API can consume it without special-case translation.

## Deferred follow-up — general projection/product decision

The bounded SPC source includes a `general` projection, as does the broader
semantic contract, but current rendered WoofMap products expose only handler,
direct-to-dog, and hybrid audiences. This sprint must neither add a fourth
rendered audience nor silently discard source evidence needed for a future
product decision. A later cross-repo investigation can decide whether the
general projection should be rendered, used internally, or explicitly omitted
from every route under one product contract.
