# Authoring Lifecycle and Structured Logging Sprint 1 Plan

```yaml
status: complete
date: 2026-08-13
owner: semantic-basis-extractor
consumer: astrowoof-api
scope: current exact-time authoring lifecycle and structured execution events
```

## Purpose

Give API orchestrators supported, machine-readable ways to deny unspent work,
determine native terminality and quiescence, reconcile outstanding provider
actions, and observe SBE execution without parsing prose, exception text, or log
lines as authority.

This sprint separates those operational contracts from bounded-birth-time graph
ingestion. Its deliverables apply first to SBE's existing exact-time authoring
workflow and may later be reused or extended by bounded authoring.

## Source requests

The sprint incorporates the current-authoring portions of:

- `API Agent Implementation Requests.md` from the bounded-btime ingestion sprint;
- `API Agent Logging Requests.md` from the bounded-btime ingestion sprint; and
- AstroWoof API Milestone 002's terminal-closeout and diagnostics dependencies.

The source request documents remain historical context. This plan defines the
focused implementation boundary.

## Scope

### Included

- a supported negative-authorization operation for prepared, unsubmitted paid
  actions;
- deterministic outstanding-action inventory and ordering;
- machine-readable terminal outcome and quiescence/local-dependency summaries;
- explicit provider-less action release eligibility and disposition;
- idempotent closeout and repeat inspection behavior;
- fail-closed ambiguity reporting for known provider identity or inconsistent
  native state;
- allow-listed `sbe.execution_event.v1` structured execution events for the
  existing authoring workflow;
- correlation identifiers suitable for API run, job, attempt, lease, native run,
  and paid-action joins without exposing secrets;
- deterministic provider-free qualification and installed-release consumer
  handoff; and
- versioned schemas, fixtures, tests, and release documentation.

### Excluded

- bounded canonical/projected graph ingestion;
- bounded claim-deck semantics or bounded-specific event fields;
- API queue, lease, PostgreSQL, R2, workspace-deletion, or global spend policy;
- treating logs or events as execution authority;
- API table mutation by SBE;
- automatic repair of ambiguous native/provider state;
- changes to editorial acceptance policy; and
- a new paid live authoring campaign unless separately approved.

## Governing invariants

- Native state, ledgers, checkpoints, and provider identity remain authoritative;
  emitted events are explanatory evidence only.
- Negative authorization may prevent work that has not reached the provider; it
  may never erase, cancel by implication, or release known provider work.
- Closeout is monotonic and idempotent. Repeating it cannot resubmit work, change
  accepted output, or discard history.
- A provider operation ID, uncertain submission boundary, or inconsistent native
  record closes the provider-less release path and produces an explicit ambiguous
  or review-required result.
- Machine-readable summaries are complete enough that a consumer does not need to
  parse human prose or implementation-private workspace files.
- Correlation fields contain opaque identifiers, not credentials, prompts,
  responses, dog birth data, or other sensitive payloads.
- Exact-time behavior remains backward compatible unless a versioned contract
  explicitly says otherwise.
- Mutating lifecycle operations bind their decision to an exact pre-mutation
  operator revision and validated snapshot, then return the distinct durable
  result artifact, new operator revision, and post-mutation validated snapshot.
- API reservation release and lease validity remain API authority. SBE reports
  native disposition, eligibility, and an uninterpreted bounded external authority
  reference; it never accepts a raw lease token or claims to release API funds.

## Approved contract refinements

- Provider-less denial covers exact `PREPARED` and `AUTHORIZED` actions only when
  no submission, consumption, provider identity, or provider evidence exists.
  `SUBMITTING` without durable identity and every later/ambiguous state fail closed.
- Negative decisions use `DENIED_PROVIDERLESS`, preserve whether authorization had
  previously been recorded, and bind the complete immutable action identity,
  request version, run/action IDs, observed revision/snapshot, closed denial reason,
  and opaque external authority/fencing reference.
- Action inventory separates deterministic presentation order from execution
  dependency and reports necessity, independence/supersession/blocking, eligibility,
  and exact ineligibility reason. Provider ledger state is not editorial acceptance.
- Quiescence is a point-in-time observation bound to revision, snapshot SHA-256,
  logical root, inventory validity, timestamp, and native exclusivity/race facts.
- Local continuation is a typed, versioned dependency inventory rather than only a
  Boolean. Terminal output separately reports deck existence, native QA, assembly/
  lint/validation acceptance, delivery completeness, publishability, policy/review/
  failure terminality, and remaining provider or local continuation.
- Closeout persists a durable native result artifact and complete checkpoint;
  repeat closeout preserves the same semantic disposition and accepted delivery.
- JSONL event files live outside the authoritative workspace. An opt-in stdout
  adapter emits only typed envelopes (including the final result); human diagnostics
  use stderr. Python callers receive normal typed results and may inject a sink.
- Event names and lifecycle reasons are closed, versioned vocabularies. Unknown
  consumer events cannot affect execution. Sink failure cannot affect native state;
  serialization/schema failures surface only as bounded safe warnings/counters.
- Action inventory exposes bounded durable provider identity and explicit native
  identity/evidence/consumption facts. Required empty arrays remove missing-versus-
  empty ambiguity for dependency and review collections.
- Negative-authorization results echo the immutable action binding and represent
  both applied/idempotent outcomes and typed non-mutation refusals. Request
  observation may only be strengthened to native exclusive access; native revision,
  snapshot, logical root, validation facts, and binding cannot change.
- Lifecycle inspection and closeout expose an explicit typed quiescence result with
  closed reasons.

## Slice 1: Contract vocabulary and schemas

### Goals

Define the public lifecycle and event vocabulary before changing execution.

### Scope

- Define versioned schemas for negative authorization requests/results,
  outstanding-action inventory, terminal outcome, quiescence, local dependencies,
  closeout result, and `sbe.execution_event.v1`.
- Define terminal outcome states, action states, ambiguity reasons, and stable
  ordering rules.
- Identify required and optional correlation fields.
- Document which fields are authoritative snapshots and which are observations.

### Testing strategy

- Schema validation for complete examples and rejection of malformed/unknown
  required shapes.
- Stable serialization and ordering tests.
- Redaction tests proving prohibited payloads cannot enter event fields.
- Compatibility tests against retained exact-time run fixtures.

### Gate

Consumer review confirms every API closeout question has a typed answer and no
event is needed to authorize a state transition.

Before closing this slice, remind Kevin to loop in the AstroWoof API agent for a
review of the schemas, vocabularies, sanitized fixtures, and read-only inspection
shape. Record the review outcome in `LOG.md` and `EVIDENCE.md`.

## Slice 2: Read-only lifecycle inspection

### Goals

Expose deterministic native truth about current and terminal runs.

### Scope

- Inventory prepared, submitted, active, reported, accepted, and unresolved
  provider actions from native evidence.
- Report terminal outcome, whether provider work remains, whether local
  continuation remains, and the exact local dependency inventory.
- Report provider-less release eligibility without performing release.
- Support fresh and detached/resumable exact-time runs.

### Testing strategy

- Fixtures covering clean success, policy stop, QA failure, prepared-only work,
  active provider work, reported work, retained continuation, and inconsistent
  state.
- Repeat inspection must be byte-stable apart from explicitly documented volatile
  observation fields.
- Inspection must perform no provider call or workspace mutation.

### Gate

Every fixture is classified completely or fail-closed as ambiguous; none requires
exception-text parsing.

## Slice 3: Negative authorization and provider-less disposition

### Goals

Provide a supported way for the API to deny work before provider submission and
close out the resulting native authorization safely.

### Scope

- Accept an explicit negative authorization for an exact prepared action.
- Verify the action remains provider-less and matches immutable run/profile
  authority.
- Record denial/release disposition durably without deleting history.
- Refuse denial when provider identity exists, submission is uncertain, or the
  action no longer matches.
- Define deterministic handling and ordering when several actions are outstanding.

### Testing strategy

- Sarah-shaped provider-free spend denial fixture.
- Idempotent repeated denial and inspection.
- Race-shaped tests where provider identity appears before disposition.
- Cross-run/action mismatch rejection.
- Proof that no provider client is invoked.

### Gate

Prepared provider-less work can be denied and durably classified, while every
known or ambiguous provider boundary remains protected.

## Slice 4: Idempotent terminal closeout

### Goals

Combine lifecycle inspection and supported dispositions into one consumer-safe
closeout operation.

### Scope

- Reconcile terminal native outcome and outstanding actions.
- Apply externally supplied negative authorizations only to exact eligible actions.
- Return final quiescence, local dependencies, unresolved work, and closeout
  disposition.
- Preserve native evidence and permit safe repeated calls.
- Stop with an explicit review-required result rather than guessing.

### Testing strategy

- Closeout from every interruption boundary represented by retained fixtures.
- Repeat and crash/restart tests around each durable write.
- No duplicate provider action under any replay.
- History and accepted delivery remain unchanged.

### Gate

An API consumer can decide whether its paid-action rows may be released and whether
workspace cleanup evaluation may begin using only supported SBE output.

## Slice 5: Structured execution events

### Goals

Emit useful, bounded, allow-listed observations for operational timing,
diagnostics, metrics, and correlation.

### Scope

- Emit `sbe.execution_event.v1` around native run start/resume/detach, pass/action
  preparation, authorization outcome, provider submission/attachment, provider
  completion, deterministic QA, retry/polish/critic decisions, checkpoint and
  terminal transitions, closeout, and failures.
- Include event ID, event time, event name, severity, component/release identity,
  run/action correlations, attempt counters, duration/cost fields where known, and
  bounded reason codes.
- Define duplicate tolerance, event ordering expectations, and behavior when the
  event sink is unavailable.
- Define stable event-name-specific payload schemas or an equivalent versioned
  payload catalog; free-form outcome or metric dimensions do not pass the slice.
- Keep events on an observational side channel; execution cannot depend on
  successful delivery.

### Testing strategy

- Golden event fixtures for success, provider-free denial, retry, failure,
  detach/resume, and closeout.
- Allow-list/redaction tests.
- Sink failure, duplication, delay, and reordering tests proving native execution
  truth is unchanged.
- Correlation coverage tests across a complete retained run.

### Gate

The API can reconstruct timing and operational behavior from events but reaches the
same lifecycle conclusion when events are missing, duplicated, delayed, or reordered.

## Slice 6: Consumer surface and installed-runtime qualification

### Goals

Ship the lifecycle and logging contracts as supported release-consumer interfaces.

### Scope

- Provide documented CLI and/or Python entrypoints for inspection, denial,
  closeout, and event configuration.
- Package schemas and sanitized fixtures in the wheel.
- Add a self-contained installed-runtime smoke covering provider-free denial,
  terminal summary, quiescence, closeout replay, and representative events.
- Document compatibility, migration expectations, and API integration examples.

### Testing strategy

- Repository test suite.
- Fresh installed-wheel smoke outside the source tree.
- Byte-reproducible wheel builds where supported by the existing release process.
- Consumer-shaped test using only documented installed interfaces.

### Gate

The API agent can implement Milestone 002 Sprint A Slice 4 and Sprint Family B
without importing SBE internals, parsing log prose, or editing native state.

## Sprint-wide testing and acceptance

The sprint passes when:

1. current exact-time runs expose complete machine-readable lifecycle summaries;
2. prepared provider-less work can be negatively authorized and dispositioned
   without provider submission;
3. known or ambiguous provider work always fails closed;
4. closeout is idempotent across replay and interruption boundaries;
5. quiescence and local-dependency output is sufficient for API workspace cleanup
   evaluation but does not grant deletion authority;
6. structured events are versioned, allow-listed, correlated, and non-authoritative;
7. event loss, duplication, delay, and reordering do not affect execution;
8. retained exact-time compatibility tests pass;
9. installed-runtime smoke passes outside the repository; and
10. release-consumer handoff documents exact versions, hashes, interfaces, schemas,
    fixtures, limitations, and examples.

No bounded-birth-time functionality is required for this sprint to pass.

## Evidence policy

`EVIDENCE.md` will record commands, counts, fixture identities, release artifacts,
hashes, and acceptance outcomes as slices complete. `LOG.md` will record chronology,
decisions, deviations, and blockers. Both start empty intentionally.

Every completed-slice handoff will link the full sprint `PLAN.md`, `LOG.md`, and
`EVIDENCE.md` so the complete current record is directly reviewable.
