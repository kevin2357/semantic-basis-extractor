# SBE Agent Pre-Sprint Huddle — Muffin Local-Resume Loop

Date: 2026-08-25
Status: superseded by API wrapper diagnosis; no SBE implementation required

## Post-review correction

API review identified the exact reduction that produced the observed loop. After
the ordinary-resume attempt, the worker correctly reads SBE's lifecycle result but
computes:

```python
local_continuation_required = not inspection.release_until_due
```

That boolean reduction is not equivalent to SBE's closed lifecycle vocabulary. In
particular, `retain_for_review` and `unsupported_retain_capacity` are non-local
dispositions, but neither is `release_until_due`. The wrapper therefore turns a
typed non-local result into another local continuation, retains capacity, and
reclaims the run indefinitely.

This finding supersedes the leading SBE-executor hypothesis below. The earlier
analysis remains in this document as an honest record of the pre-review reasoning;
it is not the accepted diagnosis.

The correction belongs to the API worker translation layer:

- preserve SBE's typed `terminal`, `retain_for_review`, and
  `unsupported_retain_capacity` dispositions;
- route them through the existing non-local result path;
- never infer local continuation from the negation of one unrelated disposition;
- add a regression proving a typed review/no-action result releases the worker
  claim instead of re-entering `local_resume`; and
- keep the expired-lease reaper/reset-precondition work API-owned and separately
  audited.

SBE 0.4.25 requires no patch on the evidence currently available.

## Current assessment

The retained evidence is most consistent with a real SBE 0.4.25 production-path
gap, not merely a missing API validator or a mislabeled queue state.

Lifecycle v0.7 appears to be doing the first half of its job: it can describe
completed provider evidence as one concrete local operation. The API validates
that nonempty inventory and invokes the supported run-level ordinary-resume
command. The native command then appears to make no durable progress, reports a
quiescent result, and leaves the same semantic operation available for another
cycle.

Conceptually:

```text
completed provider response is durable
  -> v0.7 advertises provider-result fan-in / retry evaluation
  -> API invokes ordinary resume
  -> real SBE runtime does not consume the durable response into pass state
  -> no new truthful disposition is reached
  -> same local operation remains current
  -> API defers and reclaims the run
  -> repeat
```

This would explain Muffin's repeated checkpoint generations, short lease release,
long-lived capacity retention, and the starvation of Biscotti's otherwise valid
provider-reconciliation retry.

## Why the provider/API records are not inherently contradictory

The API's `provider_created` row is durable historical custody/accounting lineage.
SBE's `provider_local_dependency_count=0` describes presently outstanding provider
retrieval work. Both can be true after the provider response was retrieved:

- provider identity/history still exists;
- no additional provider GET is currently required;
- deterministic local ingestion/fan-in is still required.

The second API `authorized` retry similarly establishes historical API authority,
but does not by itself prove which native command is currently safe. SBE must
project the exact native disposition from its validated workspace.

## The 0.4.25 qualification limitation

The 0.4.25 v2 qualification is useful but overstates production-path coverage.

It proves:

- provider-free initial six-create/detach behavior;
- bounded 4+2 retrieval;
- v0.7 public inspection in fresh Python processes;
- writer-fenced cumulative operation consumption;
- retry-2 external-authority selection after a native mutation; and
- replay refusal after consumption.

It does **not** prove that the real ordinary-resume implementation performs that
native mutation. The qualification directly changes the completed retry action to
`REPORTED` before invoking `commit_local_work_progress()`. The public runtime
regression similarly mocks `author_pending_passes()` with a function that performs
the expected mutation.

The tests therefore prove the contract around a successful operation, but not the
production executor that is supposed to carry out the operation. A release-quality
replacement must fail unless the real reconciliation artifact, pass attempt,
authoring continuation, retry evaluation, and checkpoint path are exercised.

## Leading implementation hypothesis

The likely gap is between durable reconciliation output and normal authoring-pass
continuation:

1. reconciliation retrieves and stores a completed creative-retry response;
2. lifecycle correctly sees completed provider evidence and advertises local fan-in;
3. ordinary resume enters the normal authoring continuation;
4. the pass/attempt code still sees a waiting/provider-bound attempt or otherwise
   does not load the reconciled response artifact;
5. it performs no ingestion, acceptance, rejection, or retry preparation;
6. the surrounding command returns quiescent without consuming the advertised
   semantic operation.

This is a hypothesis to prove in Slice 0. The fix must follow the observed native
boundary rather than assume this exact missing join.

## Ownership boundary

SBE owns:

- native action/pass/attempt state;
- provider-response artifact joins;
- local operation selection and execution;
- semantic operation consumption;
- snapshot/checkpoint identity;
- retry evaluation and next native disposition; and
- typed terminal/review/authority/reconciliation outcomes.

API owns:

- job scheduling and leases;
- long-lived capacity allocations;
- global spend admission and reservations;
- PostgreSQL/R2 transactionality;
- deployment/profile selection; and
- fleet-level starvation protection.

API should add a defensive contradiction fence so a no-progress native result does
not retain capacity forever. That companion hardening cannot substitute for SBE
truthfully executing—or refusing—the work it advertises.

## Safety posture

- Muffin and Biscotti remain frozen.
- No real provider request, retrieval, grant, spend, or retained-workspace mutation
  is authorized by this sprint plan.
- A status string or API ledger row must not be used to synthesize native progress.
- Provider identity and ambiguity precedence remain unchanged.
- The single-writer boundary remains authoritative for native mutation.
- A local operation may be marked consumed only after the underlying native truth
  changes durably.

## Proposed release invariant

For an exact inspected checkpoint:

```text
ordinary_resume(operation_key = K)
```

must produce exactly one of:

1. a successor checkpoint whose cumulative consumption history contains `K` and
   whose native facts prove the operation completed;
2. a different truthful typed disposition, such as provider reconciliation,
   external authority, terminal, ambiguity, or review/refusal; or
3. a typed `local_work_no_progress` contract failure that is not externally
   schedulable as another ordinary resume and does not retain capacity indefinitely.

It must never return generic quiescence while re-advertising `K` as executable.

## Recommended first gate

Slice 0 should recreate the Muffin topology entirely provider-free through the real
production reconciliation and ordinary-resume entry points, with no mocked local
mutation. The review pause should occur only after we can name:

- the exact persisted provider-response evidence;
- the exact advertised operation;
- the production function that is expected to consume it;
- the first native field/artifact that fails to advance; and
- whether exact and bounded routes share the same defect.
