# Slice 0 — Incident Reproduction and Causal Findings

Date: 2026-08-27
Status: complete; awaiting owner/API review before Slice 1

## Result

The provider-free production-shaped reproduction confirms the principal
hypothesis for exact interactive Natal.

The retained creative-retry response is not waiting for provider retrieval. Its
native action has a durable provider ID and `provider_reconciliation.last_outcome
= completed`. Lifecycle v0.7 therefore correctly selects exactly one local
`provider_result_fan_in_and_retry_evaluation` operation.

The public semantic-closure resume dispatcher then misroutes that local operation
because it treats the existence of any `initial_authoring_wave` dictionary as an
active initial-wave admission.

## Proven sequence

The sanitized fixture contains:

- a complete, validator-joinable six-member exact initial wave;
- six terminal initial actions with durable provider identities;
- the stored initial wave in `DETACHED` state;
- one creative-retry action with a durable provider ID and completed retrieval;
- one later ordinary creative-retry action in `PREPARED`; and
- a valid complete workspace snapshot.

Against those bytes:

1. `inspect_post_fan_in_lifecycle()` emits lifecycle v0.7 and selects
   `ordinary_resume` with one local fan-in/retry-evaluation operation.
2. The public semantic-closure resume command supplied with an ordinary
   authorization rejects with `aggregate_grant_required` before local fan-in.
3. The refusal performs zero provider I/O, does not change `run.json` or the
   snapshot, and publishes no native result.
4. The same public resume without an ordinary authorization still enters the
   exact initial-wave branch solely because stored `DETACHED` lineage exists. It
   never calls ordinary authoring/fan-in and instead publishes a new native result
   for the unchanged detached wave.
5. An actually active `AWAITING_SPEND_AUTHORIZATION` initial wave continues to
   require its exact aggregate request/grant, which is the safety behavior the
   correction must preserve.

## Exact causal predicates

Two predicates in `closure.main()` are overbroad:

1. Ordinary `--spend-authorization` is rejected whenever
   `initial_authoring_wave` is a dictionary, irrespective of wave state.
2. `exact_initial_wave_mode` is selected whenever `initial_authoring_wave` is a
   dictionary, irrespective of whether the wave is active or historical.

The first predicate explains the incident's visible exception. The second
explains why removing the ordinary authorization would not safely repair the
route: generic resume would still bypass local fan-in and can publish unchanged
initial-wave meaning.

## Route applicability

The bounded-interactive route does not share this exact defect. Its generic
initial-wave refusal is already restricted to the active states
`AWAITING_SPEND_AUTHORIZATION`, `AUTHORIZED`, and `SUBMITTING`; a stored
`DETACHED` bounded wave falls through to ordinary processing. Bounded parity must
still be retained in regression coverage, but Slice 2 should prefer one shared
active-wave predicate only if doing so does not weaken bounded's existing fence.

## Contract conclusion

No new lifecycle state or public schema is presently indicated. Lifecycle v0.7
already selects the correct local operation. The correction belongs at the exact
runtime command-routing boundary:

- completed/detached initial-wave evidence remains immutable lineage;
- active initial admission remains aggregate-grant constrained;
- post-fan-in local work reaches ordinary execution;
- the later prepared retry remains ordinary v2 external-authority work; and
- unchanged local work cannot be republished as progress.

## Safety totals

- Retained QA workspaces accessed: 0
- External network/OpenAI calls: 0
- Provider creates/retrievals: 0
- Spend: USD 0
- Runtime source changes: 0

