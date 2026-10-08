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

## Post-publication corrective track — 0.4.71 bounded paid initialization

The released `0.4.70` bounded command accepts a sealed, eligible four-context
source and reaches the paid native lifecycle, but it has no profile-bound way
to receive API's already-approved native spend policy. It therefore fails
closed before it writes a workspace, ledger, or public state. This is a narrow
missing CLI-to-generation-profile handoff, not a change to bounded selection,
editorial guidance, authority, or provider dispatch semantics.

The correction is a new release line. Do not rewrite the `0.4.70` bounded
profile/prompt identities or treat a newer package descriptor as equivalent.
`0.4.71` will introduce immutable bounded `v2` processing-profile and prompt
release records; the original `v1` records remain available for their
historical package context.

### Slice 3A — Freeze the policy and immutable successor identities

Define the bounded CLI contract using the established exact-route spelling,
`--spend-policy <json-path>`, only for a new OpenAI-bound profile initialization.
The CLI loads and validates the policy before durable state creation and carries
the validated policy unchanged into the native generation profile. A missing,
malformed, or invalid policy refuses before workspace/ledger/provider activity.
Resume/reconciliation must continue to read the sealed existing ledger, not
accept replacement policy input.

Create successor records for the bounded processing profile and bounded prompt
release, both allowlisting only the new `v2` profile. Their package descriptor
must require `astrowoof-natal-authoring==0.4.71`; record canonical component
inventories and catalog/profile/release digests. The `v1` records are immutable.

### Slice 3B — Implement bounded spend-policy handoff

Add the bounded CLI option and its strict applicability/validation boundary.
When a profile-bound new run resolves to OpenAI, merge the validated policy
into `_profile_generation_settings()` so `create_bounded_run()` establishes the
ordinary paid ledger. Do not add defaults, bypass API spend authority, relax
authorization requirements, or alter the provider-free under-floor outcome.

### Slice 3C — Provider-free CLI proof and candidate handoff

Exercise a real eligible four-context bounded CLI invocation with an OpenAI
profile, a valid API-supplied policy, disabled network, and no authorizations.
It must create a durable OpenAI-bound workspace, retain the policy in its
ledger/state, prepare exactly the initial six-member authority wave, and stop
at the authority boundary with zero submissions. Cover missing/malformed
policy refusal, resume-policy rejection, and unchanged under-floor behavior.

Build a retained `0.4.71` candidate wheel and hand API its complete immutable
identity table, the new bounded profile/prompt/catalog digests, and the
provider-free fixture evidence. API must install and qualify that exact wheel
before any tag, publication, context deployment, profile activation, or
provider-backed bounded work.

**Gate C — joint 0.4.71 installed-wheel admission:** API confirms the exact
candidate can create and subsequently resume the normal authority-gated bounded
workspace using its real handoff. A release/tag and any QA deployment remain
separate owner-approved actions.

**Implementation status:** Slices 3A–3B are complete in source. Slice 3C's
provider-free CLI proof is recorded in
[Slice 3 bounded spend-policy handoff](SLICE%203%20-%20BOUNDED%20SPEND%20POLICY%20HANDOFF.md),
and its retained-wheel coordinates are frozen in the
[0.4.71 candidate handoff](GATE%20C%20-%200.4.71%20BOUNDED%20SPEND%20POLICY%20CANDIDATE.md).
The exact candidate now awaits the API portion of Slice 3C and Gate C.

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
