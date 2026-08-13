# Slice 1 Authoring Lifecycle Contract

Status: consumer-review draft, 2026-08-13

## Published document contracts

The package resource
`contracts/authoring-lifecycle-contracts.schema.json` is the strict Draft 2020-12
schema for six public documents:

| Document | `schema_version` | Authority |
| --- | --- | --- |
| Negative authorization request | `astrowoof.provider_negative_authorization_request.v0.1` | External instruction bound to one exact native observation and action |
| Negative authorization result | `astrowoof.provider_negative_authorization_result.v0.1` | Durable SBE-native disposition and resulting checkpoint |
| Provider action inventory | `astrowoof.provider_action_inventory.v0.1` | Read-only projection of exact native evidence at one observation |
| Lifecycle inspection | `astrowoof.authoring_lifecycle_inspection.v0.1` | Read-only projection of exact native evidence at one observation |
| Closeout result | `astrowoof.authoring_closeout_result.v0.1` | Durable SBE-native closeout disposition and resulting checkpoint |
| Execution event | `sbe.execution_event.v1` | Non-authoritative operational observation |

The catalog exposes each document name and version. Sanitized package fixtures live
under `fixtures/lifecycle/`, including both an applied denial and a typed
non-mutation refusal.

## Mutation boundary

Every mutation request identifies its external `request_observation`: the operator
revision, validated snapshot SHA-256, logical root, inventory validation status,
observation time, and native exclusivity/race conditions that the API authorized
against. Under native exclusive access, SBE records the authoritative pre-mutation
`decision_basis`. Revision, snapshot SHA-256, logical root, snapshot completeness,
and inventory validity must match exactly. SBE may record a later `observed_at` and
may strengthen exclusivity from `declared` to `established`; it may not weaken it or
proceed when a writer race is possible. Any invariant mismatch returns a typed
non-mutation result.

A successful mutation returns a separate `result_checkpoint` with its new revision,
snapshot SHA-256, and durable result-artifact identity. Consumers must never treat
the result checkpoint as the observation on which the decision was authorized.

The external authority reference is an opaque correlation and fencing reference.
It is bounded and returned unchanged. It must not contain a lease token. SBE does
not interpret it, validate the API lease, release a reservation, or claim authority
over account-wide spend.

## Provider-less denial

Only `PREPARED` and `AUTHORIZED` actions can become `DENIED_PROVIDERLESS`, and an
authorized action is eligible only before consumption or submission evidence.
Eligibility is always explicit. `SUBMITTING` without a durable provider identity,
any provider identity/evidence, consumption, an immutable-binding mismatch, an
observation mismatch, or inconsistent native state fails closed.

The result echoes the complete immutable action binding and records whether external
authorization had previously been recorded.
`release_eligible` is SBE evidence for an API decision; it is not a release action.

Negative-authorization results cover applied denial, idempotent replay, stale
observation, binding mismatch, provider identity/evidence/consumption appearing,
ambiguous submission, native inconsistency, failed exclusivity, writer race, and
explicit review-required outcomes. Refused requests set `applied` and
`release_eligible` false and have no result checkpoint. Applied and idempotently
recovered outcomes identify the durable result checkpoint/artifact.

## Inventory and lifecycle semantics

Action array order is deterministic presentation only. It never grants permission
or communicates executable sequence. Each action separately declares necessity,
its independent/superseded/blocking relationship, blocking action identities,
provider-less eligibility, durable provider operation identity, explicit provider
identity/evidence/consumption presence, and exact eligibility or review reasons.
Blocking-action and ambiguity/review collections are always present, including
when empty.

Provider ledger state is distinct from pass, QA, deck, and delivery acceptance.
The terminal summary consequently reports each of these facts independently:

- deck bytes exist;
- native QA passed;
- assembly/lint/validation acceptance completed;
- the delivery package completed;
- delivery is publishable under current native policy;
- provider continuation remains; and
- typed local continuation remains.

Quiescence is a typed `quiescent`, `not_quiescent`, or
`unknown_review_required` result with closed reasons; consumers need not derive it
from several flags. It is never asserted as an eternal property. Inspection records the exact
revision and snapshot observed and whether exclusive access was established,
declared, absent, or unknown, including whether a writer race was possible. API
lease and cleanup authority remain outside SBE.

## Closed vocabularies

The Python constants in `astrowoof_natal_authoring.lifecycle_contracts` and the
JSON Schema define the closed v0.1 vocabularies for action states, denial reasons,
terminal reasons/outcomes, ambiguity and review reasons, local dependency kinds,
provider-less eligibility reasons, action relationships, closeout dispositions,
event names, and event severities. Producers cannot emit an unknown value under
these schema versions.

Future compatible vocabulary additions require an explicitly documented schema
revision/version. Consumers should ignore or quarantine unknown event versions or
names; they must never use events to mutate execution state.

## Event boundary

Events are bounded observational envelopes. Correlation may identify API run/job/
attempt, the opaque external authority reference, native run, action, and pass.
Prompts, provider request/response bodies, protected birth/location fields, raw
lease tokens, API keys, and authorization tokens are prohibited recursively.

Later implementation slices will provide the injected Python sink and opt-in JSONL
adapter. JSONL files must remain outside the authoritative workspace. When stdout
transport is selected, every stdout line—including the final command result—will
be a typed envelope, and human diagnostics will use stderr. Sink delivery failure
cannot affect native execution.

Before Slice 5 closes, each allow-listed event name must receive a stable typed
payload contract (or equivalent versioned payload catalog). The generic bounded
`data` shape is sufficient for the observational transport boundary in Slices 1–4,
but is not the final stable metrics contract.

## Consumer-review questions

The AstroWoof API agent is asked to confirm:

1. The six document boundaries and version names are suitable for persistence.
2. The precondition observation versus result checkpoint split supports fencing.
3. Closed vocabularies cover every currently known API branch without prose parsing.
4. Inventory necessity/dependency fields are sufficient without implying execution order.
5. Terminal facts and typed local dependencies answer cleanup evaluation inputs.
6. The event envelope is useful while remaining non-authoritative and payload-safe.
