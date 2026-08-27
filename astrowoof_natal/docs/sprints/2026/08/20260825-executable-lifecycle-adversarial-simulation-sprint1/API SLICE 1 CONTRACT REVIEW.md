# API Slice 1 Contract Review

Date: 2026-08-27
Reviewer: AstroWoof API agent
Scope: public provider-free trace contract only; no implementation, provider, retained
QA, deployment, or release activity by API.

## Assessment

The overall shape is strong and is the right public bridge for the joint campaign:
closed schema and Python validation; separate materialized native/API/provider facts;
explicit construction, time, route, actor, and side-effect vocabularies; packaged,
canonical fixtures; and a clear prohibition on treating a trace as runtime authority.

The review/no-action, released not-due, and synthetic contradiction fixtures are the
right minimal corpus. The installed-root reader/validator and provider-free guards
also give API the surface it needs for the eventual composed vertical slice.

I recommend correcting the following three items before the joint schema/authority
freeze. They are contract precision issues, not a request to broaden the sprint.

## Required corrections

### 1. Make the semantic fingerprint match its stated semantics

`semantic_fingerprint()` presently hashes the entire `native` object, including
`snapshot_sha256` and `state_revision`. The handoff says that a rewritten wrapper
document, revision, or raw digest is not semantic progress by itself, while the
current implementation makes either value a semantic change unconditionally.

That would let harmless revision/snapshot churn evade the exact stutter/cycle
property this contract is meant to prove.

Please define a narrow explicit semantic projection. It should exclude raw evidence,
observational revisions, and non-fencing rewrites; retain a digest only when it fences
a future command, stale observation, authority/grant/replay, or publication; and make
that fencing role visible in public data (for example, a closed ordered
`semantic_fences` inventory of kind/digest pairs). The original snapshot and revision
may remain materialized/exact-replay facts. The API will mirror the same projection,
not infer it from private state.

### 2. Bind event admissibility to `refused`

The validator currently permits a `refused` classification with `event.enabled=true`
and no refusal reason, or a disabled event with a non-refusal classification. This
makes a typed refusal non-falsifiable.

Please require:

- `classification == refused` iff `event.enabled == false` and
  `event.refusal_reason` is a nonempty closed reason; and
- every other classification has `enabled == true` and `refusal_reason == null`.

`contradictory_evidence` remains distinct: it may arise from an enabled inspection of
a deliberately synthetic-invalid materialized state, exactly as the current fixture
does. Its declared contradiction set remains the fail-closed explanation, not a
normal event refusal.

### 3. Give `cycle` a replayable recurrence witness

The historical review/no-action fixture labels a single equal before/after semantic
fingerprint as `cycle`. With only this transition, that is also a stutter; no field
proves a prior recurrence. Conversely, without a distinction a meaningful
one-supported idempotent replay cannot be modeled sharply.

Please add a small closed progress witness (or equivalent) that records the relevant
prior semantic fingerprint and earlier logical step for `cycle`; require it only for
cycle. A one-step identical successor without that prior recurrence is `stutter`.
The Muffin corpus can then retain its minimal historical transition as stutter, or
encode the shortest two/three-step recurrence as a genuine cycle, with the starvation
witness remaining a separate multi-run witness.

## Alignment notes for API adoption

- SBE uses `completed_local_work`; the API's preliminary internal spelling is
  `completed_evidence_pending_local_work`. API will map to the released SBE value,
  but the value must be treated as an SBE-owned closed public vocabulary rather than
  normalized by implication.
- `native_run_ref`, `api.run_ref`, and `reason_code` are currently only nonempty
  strings. Before the fixture corpus becomes a broadly consumable public surface,
  constrain them to opaque simulation-safe values (or add strict privacy validation)
  so a producer cannot rely on self-reported `privacy=false` while embedding a real
  run/provider/subject identifier.
- The current route matrix, provider-free capability guards, whole-second canonical
  time, and exact fixture-drift checks are approved as-is.

## API decision

Approve the direction and the existing contract corpus, conditional on the three
corrections above and focused regressions for each. After that, API can freeze its
own trace adapter against the released v1 surface and begin the real worker
translation vertical slice without examining SBE private workspace state.
