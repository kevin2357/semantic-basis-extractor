# SBE Agent Pre-Sprint Huddle

Date: 2026-08-21
Status: reconnaissance complete; implementation not started

## Why we paused before planning

The retained QA recovery failed API lifecycle validation with:

```text
SbeProviderContractError: SBE external authority branch evidence is incomplete
```

That message identifies a contract family, but it combines several independently
validated predicates. The initial background reasonably identified an empty action
inventory as the leading hypothesis, but the rejected raw lifecycle inspection is
not currently available in this sprint evidence. We must not promote that
hypothesis to a proven root cause.

The retained workspace remains evidence only. This reconnaissance did not inspect,
restore, mutate, resume, authorize, reconcile, or submit from it.

## Code findings

The released SBE 0.4.14 source already has several relevant defenses:

1. `validate_external_authority_request()` requires an ordered inventory of 1–32
   unique actions. An empty request is invalid.
2. `read_external_authority_request()` refuses when it cannot resolve an admissible
   prepared action set. Initial-wave admission additionally requires exactly six
   providerless, unconsumed, binding-identical `PREPARED` actions.
3. `inspect_lifecycle()` catches a typed request-building failure and converts it
   into an external-authority refusal/native-review branch rather than publishing
   an authorization command.
4. Lifecycle inspection v0.5 requires an embedded request whenever
   `execution_branch.command == "await_external_authority"`.
5. The lifecycle/request join requires exact outer run/observation identity and
   exact equality between branch action IDs and request ordered action IDs.

Consequently, the ordinary 0.4.14 builder/validator path should not emit a valid
`await_external_authority` request with zero actions. A bypass, differing predicate,
run-specific state shape, or evidence-capture gap remains possible and needs a
targeted reproducer.

## What the API error actually means

The API currently raises the same message when any of these is true:

- branch `eligible_now` is true;
- branch reason is not `spend_authorization_required`;
- capacity disposition is not `await_external_authority`;
- branch `action_ids` is empty; or
- branch `not_before` is non-null.

The message therefore does not prove which predicate failed. The API validates the
inspection with SBE's v0.5 validator first, then applies these additional scheduling
guards. Predicate-level, privacy-safe diagnostics are needed on both sides of this
boundary.

## Test findings

Provider-free focused command:

```powershell
python -m unittest `
  astrowoof_natal.tests.test_external_authority_public `
  astrowoof_natal.tests.test_external_authority_contract_proposal `
  astrowoof_natal.tests.test_initial_wave_lineage_fence `
  astrowoof_natal.tests.test_lifecycle_contracts
```

Result: **59 passed, 4 skipped** in 22.660 seconds. The skips are existing
environment-dependent JSON Schema checks on the lean host interpreter.

This is useful baseline evidence, not a reproduction of the retained QA failure.

## Confirmed hardening opportunity

The lifecycle join validator currently derives the nonempty branch guarantee
indirectly from validation of the embedded request. It checks branch/request ID
equality but does not independently state:

```text
await_external_authority => execution_branch.action_ids is nonempty
```

Adding that explicit semantic and schema invariant is worthwhile defense in depth.
It also makes the contract understandable without requiring consumers to reason
through transitive validation. It should not be described as the root-cause fix
until the incident shape is reproduced.

## Recommended investigation order

1. Reproduce or recover the exact predicate-level rejected shape without touching
   the retained workspace.
2. Construct production-shaped provider-free fixtures for every candidate
   contradictory branch.
3. Add safe branch-classification diagnostics that name the failed predicate and
   include only run/action IDs, counts, closed reason values, and digests.
4. Add the explicit nonempty branch invariant to schema and semantic validation.
5. Prove through the real inspection entry point that:
   - a valid prepared inventory publishes an exact nonempty request;
   - empty or inadmissible inventory publishes a typed refusal/review outcome;
   - contradictory lifecycle fields fail native validation; and
   - no path submits, retrieves, authorizes, or mutates provider work.
6. Determine from provider-free evidence whether the retained state class should
   produce a valid external request or a typed refusal.

## Planning posture

Revise the working diagnosis from “SBE emitted an empty action inventory” to:

> The API rejected one SBE lifecycle inspection because at least one required
> external-authority branch predicate was inconsistent. Empty inventory is the
> leading hypothesis, pending exact inspection evidence or reproduction.

The broader safety posture remains unchanged: API validation stays fail closed;
logs do not reconstruct authority; retained state is not manually blessed; and no
provider work is resubmitted during contract investigation.

