# Atomic Providerless-Denial Batch Lifecycle Sprint 1 Plan

```yaml
status: in_progress
date: 2026-08-15
owner: semantic-basis-extractor
consumer: astrowoof-api
scope: atomic batch denial of exact providerless paid actions
implementation_started: true
```

## Purpose

Add a supported public lifecycle operation that lets an API consumer deny a
bounded ordered set of independently eligible providerless actions from one
observed native checkpoint. SBE must validate the complete request under one
single-writer lock, apply every requested denial or none, publish one coherent
post-mutation checkpoint, and support exact replay without provider submission.

This closes the concurrency seam exposed by the API's paid two-slot Sprint 18
qualification: repeated calls to the existing single-action mutation correctly
invalidate the original observation after the first call, but terminal cleanup may
need to disposition several actions against that one observation.

## Source request

The normalized API-agent request is retained in
[`SOURCE REQUEST.md`](SOURCE%20REQUEST.md). It is the input to this plan, not an
already implemented contract.

## Scope

### Included

- a versioned batch request/result contract for one native run and one observed
  lifecycle/snapshot identity;
- an ordered bounded list of exact action denial requests, including immutable
  action bindings and bounded external authority references;
- one-lock, all-actions preflight before any authoritative mutation;
- all-or-none semantic disposition and one coherent post-mutation observation and
  result checkpoint;
- exact idempotent replay of a successfully committed batch;
- fail-closed typed refusal for stale observation, run/binding mismatch, duplicate
  or unknown action IDs, provider identity/evidence/consumption, ambiguous
  submission, ineligibility, invalid snapshots, and exclusivity failure;
- supported denial of eligible unused actions retained after
  `DELIVERY_COMPLETE`;
- public Python and CLI surfaces, packaged schemas/fixtures/catalog entries,
  lifecycle events, installed-wheel smoke, and API handoff documentation;
- failure injection around each durable-write boundary; and
- compatibility preservation for the existing single-action operation.

### Excluded

- API PostgreSQL paid-action ledger mutation, reservation release, capacity
  allocation, lease validation, publication, or recovery of already affected API
  runs;
- submitting, cancelling, polling, or reconciling provider work;
- denial of provider-bound, ambiguous, consumed, reported, or otherwise ineligible
  actions;
- automatically selecting which actions the API should deny;
- changing editorial retry, polish, critic, delivery, or spend policy;
- redesigning closeout into an implicit denial operation;
- claiming filesystem-wide atomicity that the workspace does not provide; and
- a release, tag, or publication unless separately authorized after sprint review.

## Proposed semantic decisions

These decisions are part of the proposed review gate and may be refined before
implementation.

1. **Terminal delivery is supported.** `DELIVERY_COMPLETE` does not itself make a
   prepared or authorized-but-unconsumed action provider-bound. A retained terminal
   workspace may batch-deny such actions if every ordinary providerless eligibility
   rule still passes. This is cleanup of unused authority, not mutation of accepted
   delivery.
2. **Every action must independently qualify.** The batch operation accepts only
   actions that would be `providerless_denial_eligible` at the locked decision
   basis. One ineligible, unknown, duplicate, or mismatched member refuses the
   entire batch with zero semantic mutations.
3. **Request order is preserved but grants no execution authority.** Order is used
   for canonical request identity, per-action result order, and deterministic event
   order. It does not imply action dependency or precedence.
4. **The batch result is authoritative as a whole.** Proposed batch outcomes are
   `applied`, `idempotent_replay`, and `refused`. On success, each member reports
   its exact action ID/binding, denial disposition, prior-authorization fact, and
   release-eligibility evidence. On refusal, each requested member receives a
   closed validation status/reason while the batch reports `applied: false` and no
   result checkpoint. No member may report an applied denial in a refused batch.
5. **Refusal reasons remain machine-distinguishable.** The closed vocabulary will
   distinguish stale observation, provider identity, provider evidence,
   consumption evidence, ambiguous submission, immutable binding mismatch,
   unknown action, duplicate action, ordinary ineligibility, invalid native state,
   and failure to establish exclusivity. Schema/programmer misuse remains an input
   error rather than a normal lifecycle race.
6. **Replay binds exact canonical request identity.** A versioned request digest
   covers schema version, run ID, original observed identity, ordered member list,
   each immutable binding, denial reason, and external authority reference. Exact
   replay returns the durable original semantic result and current verified
   checkpoint without another mutation. A reordered or changed request is not the
   same replay.
7. **The single-action API remains supported unchanged.** It retains its current
   request/result schemas and behavior. Consumers use batch denial when multiple
   actions must share one pre-mutation observation.
8. **No provider client is reachable.** Batch denial can be performed and replayed
   against a restored retained terminal workspace. It cannot submit or resubmit
   provider work.
9. **Atomicity is honestly bounded.** SBE will provide an all-or-none semantic
   protocol under its cross-process lock, using atomic per-file replacement,
   durable intent/result evidence, snapshot validation, and constrained recovery.
   It will not describe several workspace files as one filesystem transaction.

## Contract sketch for Slice 1 review

The proposed Python surface is:

```python
deny_providerless_actions(
    run_dir: Path,
    request: dict[str, Any],
    *,
    decision_at: str | None = None,
    event_emitter: ExecutionEventEmitter | None = None,
) -> dict[str, Any]
```

The proposed CLI surface is:

```text
astrowoof-authoring-lifecycle --run-dir RUN deny-providerless-batch \
  --request BATCH_NEGATIVE_AUTHORIZATION.json
```

The batch limit will be a documented conservative contract constant, not caller-
controlled. Slice 1 will choose the exact value from realistic SBE action bounds
and schema-size/redaction review; changing that value later requires explicit
compatibility consideration.

## Governing invariants

- SBE remains authoritative for native state, immutable action binding, provider
  evidence, snapshot identity, eligibility, denial disposition, and native
  lifecycle mutation.
- The API remains authoritative for leases, reservations, capacity, global policy,
  PostgreSQL state, release of API authority, and publication.
- Preflight and mutation occur under the existing cross-process lifecycle/spend
  single-writer lock.
- Validation observes one locked native state and one complete validated snapshot.
- No authoritative workspace byte changes on a normal refused request.
- Accepted delivery and monotonic evidence cannot be removed or weakened.
- Provider identity, provider evidence, consumption, or submission ambiguity always
  blocks providerless denial.
- Exact replay cannot advance revision, duplicate denial history, duplicate native
  events, or invoke a provider.
- Events remain non-authoritative and sink failure cannot alter the native result.
- Workspace recovery may bless only bytes derived from the exact durable batch
  intent and known write set; arbitrary changed bytes fail closed.

## Slice 0: Baseline and fixture reproduction

### Outcome

Freeze the current contract and reproduce the two-action terminal scenario without
paid work.

### Work

- Record repository/release baseline and confirm a clean starting tree.
- Build a provider-free fixture with `DELIVERY_COMPLETE` plus two independently
  eligible authorized, unconsumed creative-retry actions.
- Demonstrate the current sequential behavior: first single denial succeeds and a
  second call using the original observation returns typed stale refusal.
- Verify the existing single-action replay and terminal delivery bytes.

### Tests

- Focused lifecycle fixture test using no provider client or API key.
- Hash comparison proving delivery artifacts are unchanged.
- Baseline full repository suite and `git diff --check`.

### Gate

The seam is reproducible, no unrelated defect is found, and the fixture reflects
the API report closely enough to drive the new contract.

## Slice 1: Versioned batch contract and consumer review

### Outcome

Freeze strict request/result schemas, closed vocabularies, ordering, replay identity,
and examples before mutation code is written.

### Work

- Add batch request/result schema identifiers and contract catalog entries.
- Specify required observed identity, canonical digest rules, batch bound, exact
  member binding, per-action fields, batch outcome, refusal details, and shared
  checkpoint.
- Publish sanitized applied, replay, stale, and mixed-refusal examples.
- Specify how batch refusal maps provider evidence versus stale observation when
  both changed, following the existing provider-safety precedence.
- Define event names/payloads or document reuse of the single-denial event plus a
  new batch-level result event.

### Tests

- Strict schema acceptance/rejection and unknown-field policy.
- Canonical serialization/digest and ordered-member stability.
- Duplicate action, empty batch, over-limit batch, malformed authority reference,
  and prohibited-payload/redaction tests.
- Packaged resource enumeration tests.

### Gate

Pause for Kevin and AstroWoof API-agent review. The review must confirm that the
typed result supports API reservation release and recovery without parsing prose,
and that terminal `DELIVERY_COMPLETE` cleanup semantics are accepted.

## Slice 2: Locked all-or-none preflight

### Outcome

Implement a mutation-free decision phase that resolves and validates the whole
batch against one locked native checkpoint.

### Work

- Acquire the existing cross-process lock once.
- Load and validate one state/snapshot/inspection decision basis.
- Resolve every requested action and reject unknown/duplicate IDs.
- Verify exact run, observation, immutable binding, denial reason, authority
  reference, state, necessity/eligibility, and absence of all provider evidence.
- Return one deterministic typed refusal with ordered per-action validation when
  any member fails.

### Tests

- Stale observation and logical-root/snapshot/revision mismatches.
- One ineligible action among eligible actions causes zero mutations.
- Unknown, duplicate, cross-run, and binding-mismatched members.
- Provider identity, provider evidence, consumption, and identity-less submission
  races, including precedence over generic staleness.
- Lock contention and invalid snapshot.
- Byte/hash proof that every refusal leaves authoritative workspace unchanged.

### Gate

Every requested failure class is typed and deterministic, and no failed preflight
changes native state or reaches provider code.

## Slice 3: Durable batch mutation, checkpoint, and replay

### Outcome

Apply a successful batch as one semantic transition and replay it exactly.

### Work

- Persist a versioned durable batch intent/result under a dedicated lifecycle path.
- Apply every member denial from the preflighted state, preserving positive
  authorization history and action-local denial evidence.
- Advance native revision once and publish one coherent state/projection/snapshot
  checkpoint.
- Return ordered per-action outcomes and the shared post-mutation observation and
  artifact descriptor.
- Recognize exact replay before ordinary stale-observation refusal and reject
  altered/reordered near-replays.

### Tests

- Two successful denials in one batch with one revision transition.
- Exact replay is byte-stable and reports `idempotent_replay`.
- Reordered, partially overlapping, altered-reason, altered-authority, and altered-
  binding requests are not exact replay.
- Terminal `DELIVERY_COMPLETE` run retains byte-identical accepted delivery.
- Multiple unrelated actions remain unchanged.
- No provider client is constructed or invoked.

### Gate

One accepted request dispositions all requested actions, one rejected request
dispositions none, and exact replay produces no additional mutation.

## Slice 4: Interrupted-write recovery and concurrency qualification

### Outcome

Make the multi-file protocol safely resumable and prove behavior at every state-
persistence boundary.

### Work

- Define the exact known write set and durable intent/result states.
- Add constrained recovery for interruption before/after intent, action/state
  persistence, result artifact, public projection, and snapshot publication.
- Ensure retry under the lock completes or replays the exact batch without partial
  semantic denial or arbitrary snapshot repair.
- Exercise competing batch/single denial and provider-evidence races.

### Tests

- Failure injection at every durable-write boundary followed by restore/resume.
- Concurrent callers: one winner, safe exact replay or typed stale/refusal for the
  other, never split application.
- Single-action versus batch contention.
- Provider identity/evidence appearing before locked preflight refuses all; no test
  fabricates unsafe concurrent provider mutation inside SBE's exclusive section.
- Snapshot incompleteness and unexpected changed bytes fail closed.

### Gate

Every injected interruption has a documented safe recovery result, and tests make
no stronger atomicity or provider-idempotency claim than the underlying boundaries
support.

## Slice 5: Events, CLI, packaging, and consumer handoff

### Outcome

Ship the operation through supported installed interfaces with complete integration
guidance.

### Work

- Export the public Python operation and CLI subcommand.
- Emit deterministic per-action denial observations and a batch-level result event;
  define replay emission policy and keep events non-authoritative.
- Update the payload catalog, contract catalog, schemas, fixtures, lifecycle smoke,
  and package-resource checks.
- Update consumer handoff with exact request/result/refusal/replay examples,
  terminal workspace sequence, migration from the sequential loop, ownership
  boundary, and recovery limitations.
- Explicitly state that the existing single-action operation remains supported.

### Tests

- Event order, correlation, closed payload validation, replay behavior, redaction,
  and sink failure isolation.
- CLI success/refusal/replay tests using typed stdout and optional JSONL events.
- Fresh installed-wheel smoke outside the source tree, including packaged schemas
  and a terminal two-action provider-free batch.
- Consumer-shaped test importing only documented public surfaces.
- Full repository suite and wheel-content inspection.

### Gate

The API agent can replace its sequential denial loop with one documented installed-
wheel call and can deterministically process success, replay, and every refusal
class without native-file edits or provider work.

## Slice 6: Sprint closeout and release recommendation

### Outcome

Lock evidence, answer the source request, and state whether a new pinnable patch
release is warranted. Do not tag or publish without separate authorization.

### Work

- Run final focused, full-suite, installed-wheel, and reproducibility gates.
- Record exact commands, counts, artifact hashes, source commit, compatibility, and
  zero-provider-operation evidence.
- Produce the final API handoff and a concise response to each semantic question.
- Reconcile plan/log/evidence/results status and inspect the complete diff.

### Gate

All acceptance expectations are evidenced, consumer review has no blocking issue,
the worktree contains no temporary qualification tree, and release status is
explicitly `recommended`, `withheld`, or `not required`.

## Sprint-wide testing strategy

The test ladder is intentionally incremental:

1. strict schema, digest, and vocabulary unit tests;
2. provider-free lifecycle fixture tests;
3. mutation/refusal/replay tests with authoritative-byte comparisons;
4. exhaustive durable-boundary failure injection and concurrency tests;
5. event/CLI/consumer tests;
6. the complete repository suite;
7. fresh installed-wheel smoke outside the source tree; and
8. reproducible wheel/content/hash qualification if a release is recommended.

No paid OpenAI request, API key, or network provider operation is required or
authorized by this sprint plan.

## Exit criteria

The sprint is complete only when:

1. two eligible actions can be denied from one observation in one locked batch;
2. exact replay is deterministic and non-mutating;
3. any ineligible or invalid member causes zero semantic mutations;
4. all requested race/refusal classes are machine-distinguishable;
5. terminal delivery remains unchanged and eligible unused authority can be
   dispositioned on a retained workspace;
6. interrupted writes recover only through the exact durable protocol;
7. single-action denial remains backward compatible;
8. events are useful but non-authoritative and failure-isolated;
9. Python, CLI, schemas, fixtures, catalog, smoke, and handoff are packaged;
10. focused, full-suite, installed-wheel, and diff gates pass; and
11. the API agent accepts the consumer contract or all remaining objections are
    explicitly recorded.

## Evidence and review policy

`LOG.md` records chronology and decisions. `EVIDENCE.md` records commands, test
counts, hashes, fixtures, and gates. `results/README.md` indexes durable slice
artifacts. Each slice pauses for review before commit/continuation, and each slice
handoff links the full plan, log, evidence, and relevant result document.

Implementation has not started. Approval of this plan authorizes Slice 0 only;
later slices retain their explicit review gates.
