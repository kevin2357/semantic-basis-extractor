# Provider-Pending Capacity Release Sprint 3 Plan

```yaml
status: complete
date: 2026-08-15
owner: semantic-basis-extractor
consumer: astrowoof-api
scope: provider-pending custody, local-capacity release, and bounded reconciliation scheduling
implementation_started: true
release_status: 0.4.3_tagged_and_published
```

## Purpose

Stop treating durable remote-provider waiting as continuous consumption of scarce
local SBE execution capacity. Preserve one native closure run, its exact provider
action identities, snapshots, spend evidence, and resume semantics while exposing
a supported machine-readable boundary that lets the API release a short-lived
local capacity allocation and later claim a bounded reconciliation cycle.

The source handoff is retained in
[`API AGENT PROCESS ORCHESTRATION BRIEF.md`](API%20AGENT%20PROCESS%20ORCHESTRATION%20BRIEF.md).

This is an incremental lifecycle improvement, not a general workflow-engine or
queue redesign.

## Preliminary assessment

SBE 0.4.2 already provides most of the safety foundation:

- provider identities, action states, authorization/consumption/report evidence,
  attempts, and snapshots are durable;
- polling a known provider operation does not create a new spend commitment;
- exact restoration at the stable logical absolute path and fresh-process resume
  are supported;
- worker threads unwind before the main coordinator publishes the final snapshot;
- no authoritative provider/run state is intentionally held only in process memory;
- lifecycle inspection exposes provider and local continuation booleans plus the
  native action inventory; and
- API-owned spend reservations can remain live independently of a worker lease.

The current public projection is not sufficient for capacity release, however:

1. `WAITING_FOR_RESPONSE` creates a blocking local dependency named
   `provider_result_reconciliation` while the corresponding action also creates
   provider continuation. Inspection therefore reports both provider and local
   continuation and calls the workspace `not_quiescent`, even after the process has
   safely checkpointed and exited.
2. The cohort's `native.quiescent` execution observation is not equivalent to
   public lifecycle `quiescence.state == quiescent`. The former can mean the local
   process is safely unwound; the latter currently means no provider or local
   continuation remains. Conflating them would create another authority mismatch.
3. SBE exposes provider timestamps and polling metadata internally but no durable,
   supported per-run reconciliation recommendation such as `resume_not_before`.
4. Interactive Responses resume can poll for another complete local timeout
   window. A capacity model based on short worker claims therefore needs a
   supported poll-once/bounded-detach mode, not merely a smaller API-configured
   timeout.
5. The action inventory shows native state and provider identity, but does not yet
   give the API a closed scheduling/custody classification identifying which
   actions require consumer reservation retention while releasing only local
   execution capacity.

## Recommended contract direction

Do not redefine existing `terminal`, `quiescence`, or continuation fields. Add an
orthogonal scheduling/custody projection to lifecycle inspection. Exact names and
versions freeze in Slice 1 after API review, but the leading shape is:

```json
{
  "execution_capacity": {
    "disposition": "release_until_due",
    "local_work_ready_now": false,
    "checkpoint_safe_for_worker_release": true,
    "resume_not_before": "2026-08-15T23:00:00Z",
    "reason_code": "known_provider_work_pending"
  },
  "provider_custody": {
    "state": "known_operations_pending",
    "provider_action_count": 3,
    "reservation_retention_action_count": 3
  }
}
```

Candidate closed capacity dispositions:

- `continue_local_cycle`: native local work can proceed now;
- `release_until_due`: only known durable provider work prevents progress;
- `await_external_authority`: prepared work awaits API authorization rather than
  provider completion;
- `retain_for_review`: ambiguity, invalid snapshot, or contradictory evidence;
- `terminal`: no further native execution is legal; and
- possibly `release_no_schedule`: safely unwound but no reliable due time can be
  stated. Slice 1 must justify whether this is necessary.

`resume_not_before` is SBE's durable lower-bound recommendation. The API may resume
later. An earlier bounded attempt returns a typed `not_due` detach result and does
not poll early. The projection is SBE evidence/advice, not API scheduling
authority. The API owns
queue timing, leases, capacity allocation, admission, and whether to claim a due
cycle. SBE owns whether native work is locally runnable, whether provider custody
is known, and whether its checkpoint is safe to resume elsewhere.

SBE does not claim literal API spend exposure. It identifies exact native actions
whose known provider-bound custody requires the consumer to retain its separately
owned reservation/financial authority. The API remains the sole authority for
whether a reservation exists, its amount, account-wide exposure, and its release.

## Proposed reconciliation timing

- Freeze a bounded reconciliation policy/version in native run state or derive it
  from an already frozen profile; do not depend on an ephemeral process default.
- Record each known provider action's last reconciliation attempt and next native
  recommended due time at the same durable boundary as its waiting state.
- Derive the run-level `resume_not_before` deterministically from the earliest
  relevant provider action.
- Treat the recommendation as a lower-bound/backoff signal, not a provider SLA or
  promise of completion.
- Preserve the original provider ID and action identity. Reconciliation of a known
  operation performs no new paid commitment and must never fall through to a new
  submission.
- Use bounded backoff with explicit minimum/maximum and optional deterministic
  jitter only if its inputs and version are persisted. Random process-local jitter
  is not acceptable native authority.
- API may schedule later than SBE recommends. Earlier bounded resume returns a
  typed `not_due` result, performs no provider retrieval, publishes no unnecessary
  new checkpoint, and releases the short claim. There is no ordinary consumer
  override in the leading contract.

## Supported bounded polling mode

Add a supported mode for provider reconciliation cycles that:

- polls each already-known due provider operation at most once, or within one
  tightly bounded native cycle;
- freezes an explicit small per-cycle wall-clock ceiling, including the provider
  retrieval HTTP timeout; "one poll" alone is not considered bounded;
- never submits a replacement for a known operation;
- persists every completed response and state transition normally;
- continues immediately into local assembly/QA if the required provider barrier
  clears;
- otherwise publishes one complete checkpoint, updates due advice, and exits;
- waits for all local worker threads to unwind before claiming the checkpoint is
  safe for capacity release; and
- fully supports the exact interactive natal route across initial authoring,
  creative retries, polish, critic, and qualitative candidates when enabled; and
- classifies Batch and bounded-Natal explicitly as parity-supported or
  fail-closed/deferred rather than letting them inherit unproven semantics.

The existing blocking mode remains supported. The API can adopt bounded mode for
short reconciliation claims without changing editorial semantics.

## Scope

### Included

- exact reproduction of the two-slot provider-wait capacity problem;
- a closed additive execution-capacity/provider-custody lifecycle contract;
- durable per-action and run-level reconciliation timing evidence;
- supported interactive poll-once/bounded-detach behavior;
- full exact-interactive support across every enabled provider stage;
- explicit parity-supported or fail-closed/deferred classification for Batch and
  bounded-Natal lifecycle behavior;
- exact fresh-worker restore/resume after provider-pending checkpoints;
- multiple parallel outstanding provider actions and run-level fan-in behavior;
- preservation of provider IDs, spend authority, accepted evidence, and snapshots;
- typed CLI/Python/schema/fixture/event/installed-wheel surfaces;
- API consumer handoff listing every additive or changed contract field;
- Windows/Linux installed smoke and a parallel multi-run qualification harness; and
- patch-release recommendation after closeout.

### Excluded

- changing API PostgreSQL queue, reservation, capacity, lease, admission, HTTP
  status, publication, or billing-reconciliation implementation;
- implementing a general scheduler, DAG engine, or external workflow platform;
- one durable API queue task per provider action;
- changing OpenAI provider semantics, cancelling known work, or claiming provider
  idempotency stronger than the provider supports;
- releasing spend reservations merely because local execution capacity is released;
- changing editorial prompts, claim selection, QA, polish, critic, or product policy;
- changing SBE's fifty-claim semantic budget or frozen per-run dollar ceiling;
- weakening stable-path restoration or complete-snapshot requirements; and
- release, tagging, or publication without separate authorization.

## Governing invariants

- A known durable provider identity is reconciled, never resubmitted.
- Identity-less interrupted submission remains ambiguous and retains capacity for
  review rather than being classified as ordinary provider-pending custody.
- Local capacity release does not release authorization, reservation, or spend
  exposure.
- The checkpoint is advertised as releasable only after all SBE writers/threads
  have unwound and a complete exact snapshot is valid.
- Fresh-worker resume uses the same stable logical absolute path contract and
  exact native workspace bytes.
- SBE scheduling advice is not API queue authority and events are not authority.
- API scheduling delay cannot invalidate provider identity or native state.
- Multiple outstanding provider actions produce one coherent run-level resume
  recommendation; the API does not need one queue message per action.
- Completed responses and accepted editorial evidence remain monotonic across
  bounded cycles.
- No new paid operation is initiated merely to inspect, poll, detach, or classify
  provider-pending state.

## Explicit API contract additions or changes

The following are proposed and must freeze during Slice 1:

1. A new lifecycle inspection version, or a separately versioned nested projection,
   carrying execution-capacity and provider-custody evidence. Existing v0.1 readers
   must either remain valid or fail deterministically; silent semantic change is
   not acceptable.
2. Closed vocabularies for capacity disposition, custody state, timing reason, and
   checkpoint-release safety.
3. A durable RFC 3339 `resume_not_before`, with exact nullability and clock semantics.
4. Per-action custody-retention/due fields sufficient to explain the run-level
   projection without claiming literal API spend exposure or exposing prompts,
   provider payloads, or API-owned reservation detail.
5. A supported CLI/Python flag or command for bounded provider reconciliation.
6. A typed result/exit behavior distinguishing:
   - provider still pending and capacity releasable;
   - one or more responses completed and local work continued;
   - external authorization required;
   - terminal outcome;
   - ambiguity/review; and
   - invalid/stale checkpoint.
7. Additive structured-event fields or one new event only if useful for observation;
   authoritative decisions continue to use the persisted inspection/result.
8. A consumer rule identifying action states whose provider custody requires the
   API to retain its separately owned reservation/financial authority after local
   lease release.

The API companion sprint is expected to decouple local capacity allocation from
provider custody, preserve reservations, schedule one delayed reconciliation per
run, and map API status honestly. Those are not SBE mutations.

## Contract questions for Slice 1 review

- Should the scheduling projection be part of lifecycle inspection v0.2 or a new
  independently versioned contract referenced by inspection?
- Freeze `resume_not_before` as durable native lower-bound advice. Confirm the
  exact typed `not_due` result and prove early bounded resume performs no poll.
- Does one bounded cycle poll every due known action once, only the earliest action,
  or a fixed maximum number? Leading proposal: every due known action once, with a
  documented fixed upper bound and deterministic presentation order that is not
  execution authority.
- When some provider actions complete but another remains pending, should SBE run
  all newly unblocked local work before detaching? Leading proposal: yes.
- Which optional provider stages can remain pending without blocking delivery, and
  must native policy skip/cancel them before capacity release?
- How should Batch `next_due_at` and interactive Responses timing share vocabulary
  while preserving their different provider mechanics?
- For Batch and bounded-Natal, which behaviors are low-risk parity support and
  which must be explicitly fail-closed/deferred for this release?
- What small frozen per-cycle wall-clock ceiling covers both orchestration and the
  provider retrieval transport timeout, and how is timeout reported?
- What exact evidence proves all local writers have unwound: snapshot validity plus
  lifecycle exclusive access, a new persisted checkpoint kind, or both?

## Slice 0: Baseline and authority inventory

### Outcome

Reproduce the reported capacity condition and map every current state to durable or
process-local authority before changing contracts.

### Work

- Reproduce a run with several known interactive provider operations pending.
- Capture run/public state, action inventory, provider metadata, snapshot,
  lifecycle inspection, execution events, and process exit behavior.
- Contrast public `quiescence` with execution-level `native.quiescent` terminology.
- Trace interactive, Batch, bounded, polish, critic, and candidate wait/resume paths.
- Prove whether any authoritative state or live writer survives process exit.
- Inventory exactly which API capacity/spend decisions can and cannot already be
  made from 0.4.2.

### Tests

- Provider-free or scripted-provider fixtures with multiple pending IDs.
- Snapshot and fresh-process restore tests.
- Thread/process unwinding assertions.
- Baseline full repository suite and `git diff --check`.

### Gate

The observed bottleneck is reproduced without paid work, the terminology collision
is explicit, and no hidden process authority or separate correctness defect remains.

## Slice 1: Scheduling and custody contract

### Outcome

Freeze the additive public state machine and API mapping before orchestration changes.

### Work

- Publish the complete state/action × capacity × custody × due-time decision table.
- Choose inspection/version composition and compatibility behavior.
- Freeze closed vocabularies, nullability, timestamp rules, bounded-cycle result,
  exit behavior, events, and consumer sequence.
- Define exposure classification for authorized/provider-bound/reported/ambiguous
  actions as native custody-retention advice, distinguish it from local-capacity
  ownership, and disclaim API reservation/dollar authority.
- Freeze `resume_not_before` as a durable lower bound, typed early `not_due`
  behavior, and the small end-to-end reconciliation-cycle wall-clock ceiling.
- Define early-resume, mixed completed/pending, optional-stage, terminal, review,
  and invalid-snapshot precedence.

### Tests

- Strict schema and fixture validation/rejection.
- Exhaustive truth-table tests over action state, provider identity, local work,
  terminal/review state, snapshot validity, and due time.
- Compatibility tests for existing v0.1 consumers.
- Event redaction and catalog consistency.

### Gate

Pause for Kevin and AstroWoof API-agent review. The API must be able to implement
capacity release and delayed reclaim without parsing internal state or guessing at
native timing semantics.

## Slice 2: Durable reconciliation policy and checkpoint projection

### Outcome

Persist deterministic provider reconciliation timing and derive one coherent
run-level scheduling/custody projection.

### Work

- Freeze/persist reconciliation policy identity and parameters.
- Record last attempt, outcome, and next recommended due time at native boundaries.
- Derive earliest run due time across multiple relevant actions.
- Add checkpoint-release safety evidence only after complete snapshot publication.
- Preserve provider custody and reservation-retention advice independently of
  local capacity disposition.

### Tests

- Deterministic clock/backoff tests, including minimum/maximum behavior.
- Multiple-action earliest-due/fan-in tests.
- Restart and stable-path restoration tests.
- Failure injection before/after action state, public state, timing evidence, and
  snapshot persistence.
- Monotonic provider ID, authorization, consumption, report, and accepted-evidence
  assertions.

### Gate

The same exact native bytes always yield the same custody/capacity projection, and
no checkpoint is declared releasable before its writers and snapshot are complete.

## Slice 3: Interactive bounded reconciliation

### Outcome

Add a supported short reconciliation cycle for known interactive Responses work.

### Work

- Poll each due known provider operation once or within the reviewed fixed bound.
- Persist completed results and run all newly unblocked local work.
- If a provider barrier remains, update timing, publish a checkpoint, and detach.
- Prevent every known-ID path from entering provider submission.
- Retain existing blocking mode unchanged.
- Handle mixed completion, transport failure, provider failure, and API early resume.

### Tests

- One pending response; several parallel pending responses; mixed completed/pending.
- No duplicate POST/submission under normal, crash, restore, or concurrent resume.
- Transport retry remains bounded and distinct from provider reconciliation delay.
- Poll-only cycles add zero commitment and preserve reservations/exposure.
- Crash injection around provider retrieval, response persistence, local fan-in,
  detach state, and snapshot publication.

### Gate

Every bounded cycle either advances durable native work or exits quickly with an
exact releasable checkpoint; no known provider operation can be resubmitted.

## Slice 4: Exact-stage completeness and secondary-route classification

### Outcome

Complete the production exact-interactive path without allowing secondary routes
to delay the core fix or accidentally inherit unsupported capacity semantics.

### Work

- Require full bounded-reconciliation support for exact interactive initial
  authoring, creative retries, and every enabled optional provider stage: polish,
  critic, and qualitative candidate generation.
- Classify existing Batch detach as parity-supported where low risk or explicitly
  fail-closed/deferred where it cannot meet the contract this sprint.
- Classify bounded-Natal interactive waiting the same way; do not require full
  orchestration parity merely to release the exact-interactive fix.
- Ensure a fail-closed/deferred route never advertises `release_until_due` and
  returns a closed unsupported/retain-capacity reason.
- Resolve optional-stage and accepted-delivery precedence.
- Ensure one run-level due reconciliation represents multiple child actions.

### Tests

- Exact interactive initial/retry/polish/critic/candidate matrices.
- Interactive versus Batch classification tests.
- Exact versus bounded classification tests.
- Required versus optional stage matrices, including disabled stages.
- Delivery-complete cleanup and terminal/review precedence.
- No provider work for pure inspection/classification.

### Gate

The entire exact interactive production route is supported. Every secondary route
has an explicit tested parity or fail-closed/deferred classification; unsupported
combinations cannot advertise capacity release.

## Slice 5: Public interfaces, events, and consumer handoff

### Outcome

Ship the scheduling/custody boundary through supported installed interfaces.

### Work

- Update Python, CLI, strict schemas, fixtures, catalog, public state as approved,
  execution events, lifecycle smoke, and resource enumeration.
- Document API capacity-release/reclaim sequence, authority ownership, timing
  semantics, exposure retention, and cleanup restrictions.
- Provide exact examples for waiting, due, early, mixed-progress, authority pause,
  ambiguity, review, terminal, and delivery outcomes.
- State explicitly that HTTP status reads API-persisted authority and events/logs
  are never scheduling authority.

### Tests

- Consumer-shaped Python/CLI tests using installed public surfaces only.
- JSONL result/event ordering, replay, redaction, and sink-failure isolation.
- Fresh-worker restore and bounded resume through installed commands.
- Existing 0.4.2 consumer compatibility.

### Gate

The API can implement its companion sprint without reading `run.json`, parsing
logs, shrinking undocumented timeouts, or retaining local capacity during safe
provider waits.

## Slice 6: Native cross-platform and parallel cohort qualification

### Outcome

Prove SBE's fresh-worker, provider-pending, bounded-resume semantics and native
capacity classifications before a release recommendation. The real API capacity
allocation result belongs to the API companion sprint.

### Work

- Run multiple provider-pending native workspaces through short fresh-worker
  cycles and prove each publishes `release_until_due` without a resident process.
- Run a third independent native workspace to prove SBE has no hidden cross-run
  process dependency; do not claim this test mutates API capacity allocation.
- Reclaim due cycles through fresh short-lived workers.
- Preserve API-shaped spend exposure fixtures throughout lease release/reclaim.
- Run exact installed-wheel smoke on Windows and Linux Python 3.11.
- Compare bounded versus blocking mode outputs after eventual completion.

### Tests

- Parallel scripted-provider cohort with deterministic clocks.
- Concurrent claim/single-writer contention and stale checkpoint tests.
- Crash/restore during multiple pending actions.
- Full repository suite, reproducible wheel build, content inspection, and diff
  hygiene.

### Gate

SBE proves provider-pending work can safely release its process, resume on fresh
workers, and coexist with unrelated native work while provider IDs,
custody-retention evidence, snapshots, accepted evidence, and exactly-once native
reconciliation remain correct. The API companion gate separately proves two
provider-pending API runs release capacity and a third reading proceeds.

## Slice 7: Closeout and release recommendation

### Outcome

Lock evidence, answer the API brief, and recommend or withhold a pinnable patch.

### Work

- Record exact commands, counts, hashes, source commit, compatibility, zero-provider
  evidence, and residual limitations.
- Publish the final API response and companion adoption checklist.
- Reconcile plan, log, evidence, results, consumer handoff, and release guidance.
- Remove qualification trees and verify a clean repository boundary.

### Gate

Every exit criterion passes, API review has no blocker, and release status is
explicit. Version bump, tag, and publication still require separate authorization.

## Sprint-wide testing strategy

1. Scripted provider operations with durable fake IDs and deterministic clocks;
   no paid provider request is required or authorized.
2. Closed contract truth tables for capacity, custody, exposure, due timing,
   terminal/review, and snapshot validity.
3. Multiple pending actions, mixed completion, fan-in, and local work continuation.
4. Failure injection across submission identity, retrieval, timing, state/public
   files, snapshot, detach, and fresh-process resume boundaries.
5. Exact, Batch, and bounded-Natal route/stage regression matrices.
6. Consumer-shaped Python/CLI/event tests and installed resource validation.
7. Parallel native multi-run qualification showing no hidden resident-process or
   cross-run dependency; the API companion sprint owns the actual capacity-slot
   admission proof.
8. Complete repository suite plus reproducible Windows/Linux wheel smoke.

No API key, paid request, provider submission, provider cancellation, or account
mutation is needed or authorized for this sprint. Real-provider qualification, if
later desired, requires separate explicit spend authorization.

## Exit criteria

The sprint is complete only when:

1. SBE distinguishes local execution capacity from provider-pending custody and
   consumer reservation-retention advice without redefining existing quiescence
   semantics or claiming API financial authority;
2. every releasable checkpoint is complete, writer-free, snapshot-valid, and safe
   for exact fresh-worker resume;
3. a supported bounded cycle polls known provider work without any new submission;
4. run-level due advice is deterministic, durable, bounded, and explainable from
   action evidence;
5. multiple provider actions use one coherent run-level reconciliation schedule;
6. newly unblocked local work runs before detach, while remaining provider barriers
   release capacity promptly;
7. ambiguity, provider-ID conflict, invalid snapshot, and writer races fail closed;
8. native custody-retention action evidence survives local lease release, while
   API qualification separately proves its reservations/dollar exposure survive;
9. exact, Batch, bounded, optional, delivery, terminal, and review behaviors are
   explicit and tested;
10. the API can consume only supported installed contracts and persist its own
    authoritative queue/status mapping;
11. a parallel cohort proves unrelated local work proceeds while prior runs wait;
12. full Windows/Linux qualification passes with zero provider operations; and
13. Kevin/API review accepts the final contract or all objections are retained.

## Effort and sequencing assessment

This is one medium-large SBE sprint, comparable to the recent lifecycle-hardening
sprints and somewhat larger than a schema-only change because interactive polling
behavior must change safely. It is not several SBE implementation sprints.

The API should run one separate companion sprint to adopt capacity release,
provider custody, delayed reconciliation, status mapping, and staging recovery.
The shared acceptance boundary is split deliberately: SBE proves native
fresh-worker/bounded-resume semantics, and the API companion proves actual capacity
release and third-reading admission. A future general
scheduler/orchestrator remains a separate multi-sprint program and is not required
for this incremental improvement.

## Evidence and review policy

`LOG.md` records chronology and decisions. `EVIDENCE.md` records exact commands,
counts, state projections, timing, mutations, provider-operation evidence, and
artifact hashes. `results/README.md` indexes slice reports.

At every slice gate, inspect the diff, run proportionate tests and
`git diff --check`, update all sprint records, link the full plan/log/evidence and
slice result, and pause for approval before committing. Slice 1 requires explicit
AstroWoof API-agent review before runtime orchestration changes begin.

Kevin approved the plan with the API agent's four Slice 1 refinements incorporated.
All SBE-native slices and API review are complete. Kevin authorized 0.4.3, which
was reproducibly built, tagged, published, downloaded, and hash-verified. Provider
operations and paid spend remained zero.
