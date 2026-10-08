# Bounded Initial-Wave v2 Execution — Background

## Trigger

The first paid QA bounded run under SBE `0.4.71` reached a valid, durable
initial spend-authority boundary and stopped before any provider operation:

- API run: `bf50cad2-aa78-4543-9e82-dd7c7e654dec`
- Native run:
  `2aece7cba784409c9d9c1aec11b7abf1465cc50af58a192310af5afd276856a5`
- State: six prepared `authoring_initial` actions, `AWAITING_SPEND_AUTHORIZATION`
- Provider custody/spend: zero
- Failure: `SBE v2 external authority request kind is unsupported`

The API evidence and exact handoff are retained in the completed predecessor
sprint's [API to SBE handoff](../20261005-bounded-birth-time-modern-authoring-integration-sprint4/API%20TO%20SBE%20-%200.4.71%20BOUNDED%20INITIAL-WAVE%20V2%20EXECUTION%20GAP.md).

## What is already true

SBE's legacy bounded lifecycle has a bounded-specific initial-wave resume
path. It validates a v1 `initial_wave_admission` request/grant with exactly six
semantically ordered members, persists a constrained intent, and invokes the
bounded initial-wave executor. The v1 authority reader distinguishes that
semantic ordering from the ordinary lexical action-ID ordering.

SBE's current v2 authority family instead deliberately admits only
`ordinary_action_set`. Both its grant validator and its durable dispatch-intent
writer reject `initial_wave_admission`. The generic v2 adapter is therefore
correct to fail closed, but leaves no executable v2 route for the bounded
initial wave.

## Required outcome

Define and implement a new immutable SBE successor context capable of
validating and executing a bounded v2 `initial_wave_admission` exactly once.
It must bind all six prepared members in their semantic order and preserve the
existing sealed run, checkpoint, profile, and spend-policy identity. It must
not create a second reservation, silently reinterpret v1 documents as v2, or
weaken later ordinary-v2 contracts.

The existing 0.4.71 QA witness is terminal. It is evidence, not a migration
target: any attempt to use a successor on its existing v1 grant must fail
closed unless a separately designed, sealed compatibility bridge is approved.

## Scope fences

- No provider-backed execution in this sprint.
- No deployment, profile activation, or QA retry.
- No change to ordinary-v2 lexical ordering or its current dispatch semantics.
- No implicit v1-to-v2 migration from workspace files, logs, or inferred
  identity.
- No new prompt/guidance wording is intended. A successor profile/prompt
  release record may still be required because immutable catalog allowlists
  cannot be amended in place.

## Initial risk assessment

This is a contained but custody-sensitive change. The missing behavior is not
a new authoring algorithm—the bounded initial-wave executor and its six-member
validation already exist—but v2 needs its own precise request/grant/intent
representation and replay properties. A short cross-repository review and
provider-free installed-wheel gate are required before a release candidate.
