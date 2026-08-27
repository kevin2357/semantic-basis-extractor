# Background — Executable Lifecycle Adversarial Simulation

Date: 2026-08-25
Status: planning; no implementation authorized
Companion API sprint: `20260825-executable-lifecycle-adversarial-simulation-sprint52`

## Why this sprint exists

AstroWoof's lifecycle contracts have become intentionally sophisticated. They
separate native execution truth, provider custody, local capacity, spend authority,
temporal eligibility, external authorization, review, ambiguity, terminality, and
publication. Focused failure-injection tests have protected many individual seams,
but recent QA cohorts have continued to discover valid components composed through
an incorrect cross-boundary route.

Muffin is the clearest recent example. SBE produced a typed non-local lifecycle
result. The API worker then reduced the full result to the negation of
`release_until_due`, incorrectly reconstructing local continuation and creating a
capacity-retaining loop. Every component-level contract test could pass while the
composed system still behaved incorrectly.

Finding these paths one dog at a time is expensive and incomplete. We need a
provider-free executable model that deliberately explores combinations and checks
the real SBE and API boundaries against durable safety, progress, and fairness
invariants.

## Existing foundation

API Sprint 20 already delivered a pure transition oracle, a deterministic native/
provider stub, replayable traces, and four fixed-seed campaigns. Sprint 21 exercised
provider-free multi-run qualification. SBE also has extensive scripted-provider,
failure-injection, installed-wheel, snapshot, replay, and route-parity fixtures.

Those assets should be extended rather than replaced. The missing layer is broader
composition:

- real installed SBE commands and readers rather than helper-only mutation;
- the real API worker result translation rather than an idealized adapter;
- multiple runs competing for bounded capacity;
- generated event orderings beyond repeated not-due observations;
- explicit progress and starvation properties; and
- automatic shrinking and durable replay of discovered counterexamples.

## Proposed architecture

The campaign has five layers:

1. A pure reference model defines legal states, commands, transitions, refusals,
   progress, and fairness.
2. A deterministic fault language scripts provider, time, persistence, process-loss,
   authority, and lease events.
3. A real SBE adapter drives supported installed-wheel commands against disposable
   workspaces with scripted transports and clocks.
4. A real API adapter passes SBE's public artifacts through production worker
   translation, persistence, lease, capacity, and scheduling code.
5. A generated campaign compares observed durable state with the oracle, shrinks a
   failure, and emits a sanitized replayable trace.

Random provider failures are part of this, but blind fuzzing is not the design.
Generated actions must be state-aware so that they reach meaningful boundaries and
produce minimal explanations rather than mostly-invalid noise.

## SBE ownership

SBE owns:

- disposable native workspaces and validated snapshots;
- provider-free scripted Response and Batch transports;
- exact and bounded route semantics;
- public lifecycle, temporal, authority, transition, and qualification artifacts;
- native command selection and bounded due subsets;
- native failure injection and restart behavior; and
- proof that advertised work progresses, changes disposition, or fails closed.

SBE does not model API-global reservations, capacity allocation, leases, queue
fairness, database transactionality, or product state as native facts.

## API ownership

The API owns its transition oracle, worker translation, PostgreSQL state, leases,
capacity, reservations, queue ordering, public state, and cross-run fairness. It
must consume SBE's supported artifacts without inspecting private workspaces or
reconstructing native meaning.

## Safety boundary

All campaign execution is provider-free. No OpenAI credentials, external network,
paid work, retained QA workspace, or production database may be accepted. Fixtures
must use generated identities and protected-data sentinels. A failing trace is test
evidence, never authority to mutate a real run.

## Core properties

- A known provider operation is never created twice.
- Retrieval-only custody never reaches a create path.
- Capacity release never implies provider-custody or spend-authority release.
- A typed review, terminal, unsupported, or no-action result is never reconstructed
  as local continuation.
- The same checkpoint and semantic command cannot loop indefinitely without a typed
  no-progress/refusal outcome.
- Every advertised local operation is consumed, replaced, or explicitly refused.
- A due runnable run cannot starve indefinitely behind a non-runnable run.
- Replays and stale observations are nonmutating.
- Unknown cost, usage, and timing remain distinct from zero.
- A provider-entered identity-less call remains ambiguous and never replayable.

## Expected outcome

The useful artifact is not merely more tests. It is a permanent adversarial
qualification system: deterministic in CI, broader under nightly/local seeds, able
to replay and minimize failures, and required whenever either repository changes a
lifecycle command, result, wrapper translation, or scheduler rule.
