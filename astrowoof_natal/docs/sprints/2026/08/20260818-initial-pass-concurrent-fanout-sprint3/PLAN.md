# Initial Authoring Pass Concurrent Fan-Out Sprint 3 Plan

Date: 2026-08-18
Status: complete; 0.4.7 release authorized
Starting release: SBE 0.4.6

## Purpose

Reduce one-deck initial-authoring latency by making all six quality-preserving
initial passes provider-pending at approximately the same time, without changing
claim assignment, prompts, editorial independence, pass QA, retry policy, assembly,
optional stages, or deck-level custody.

The governing distinction is:

> One SBE run owns one deck and six independent editorial passes. Interactive
> transport creates those six provider operations concurrently; Batch transport
> carries the same six logical members in one paid Batch round. The run detaches
> after durable provider identities exist and later cycles reconcile the fan-in.

The success criterion is not merely six threads. For interactive initial authoring,
all six provider operation IDs must normally become durable within one short
bounded submission cycle. SBE must not wait for pass 1 to complete before creating
pass 2, and it must not retain a worker lease merely to poll six known operations.

## Four route/transport pipelines

| Semantic route | Interactive Responses | Batch |
|---|---|---|
| Exact Natal | Six separately authorized initial actions, concurrently created and independently reconciled | One paid round/reservation containing six logical pass members |
| Bounded Natal | Six separately authorized initial actions, concurrently created and independently reconciled | One paid round/reservation containing six logical pass members |

“All four pipelines” means all four cells must preserve the same six-pass editorial
topology and compose with the provider-pending lifecycle. It does not mean Batch
creates six global reservations or six Batch jobs. Exact and bounded Batch already
have a natural member fan-out; this sprint proves and hardens their compatibility
while changing the interactive submission topology.

## Frozen product and editorial invariants

- Initial authoring remains five ten-card story passes plus one summary/theme pass.
- Each pass is separately prompted, provider-visible, validated, accepted, and
  provenance-bound. Concurrent execution must never combine model context.
- Frozen assignment membership and request bytes are independent of completion
  order and transport scheduling.
- Exact and bounded retain separate semantic adapters, schemas, authority
  reattachment, and delivery contracts.
- Creative retries remain pass-local. This sprint does not require concurrent
  retries; only the six initial passes are the required concurrent wave.
- Polish, critic, and qualitative-candidate topology and product policy do not
  change.
- Canonical fan-in and final QA remain deterministic and completion-order neutral.
- The fifty-claim semantic budget is unrelated to provider concurrency or dollars.

## Ownership boundary

SBE owns the six-pass assignment, exact per-action binding, native per-run spend
ceiling, provider submission and ID durability, reconciliation, pass QA, fan-in,
snapshot/journal/result publication, and route-specific semantic authority.

The AstroWoof API owns transactional cross-run reservations, global ceilings,
quotas, circuit breakers, entitlements, rate-pressure policy, worker leases,
PostgreSQL/R2 authority, billing reconciliation, and public product state.

For interactive mode, the API must be able to authorize the exact bounded set of
six prepared actions before SBE creates them. Authorization remains bound to each
action's exact request digest, route/pass/attempt, run/profile/state identity,
model, maximum output, commitment, and price book. SBE does not infer aggregate
API permission merely because its own immutable run ceiling permits all six.

The all-or-none boundary has two deliberately separate owners:

- the API transactionally reserves or refuses the complete six-action wave in its
  own authority; it must not expose a partially reserved set as executable; and
- SBE validates one complete wave authorization envelope and all six exact member
  authorizations before the first provider create. Missing, denied, stale,
  duplicate, mismatched, or mixed member authority causes zero creates.

The wave envelope is evidence that the API authorized one exact complete set; it
does not transfer reservation transactionality or global spend authority into SBE.
After the first create begins, partial provider outcomes are legitimate and remain
individually durable rather than being rolled back or disguised as atomic provider
submission.

For Batch mode, one Batch round remains one paid SBE action and one API global
reservation. Member-level evidence settles beneath the round and must not multiply
global reservation authority.

## Safety model

- A provider ID is persisted immediately after each successful create, before that
  action can be polled or any further semantic mutation depends on it.
- Concurrent provider I/O never implies concurrent unsynchronized mutation of
  `run.json`, the spend ledger, journal, public state, or snapshot.
- One native single-writer coordinator serializes action consumption and provider-ID
  commits in deterministic action order or through an equivalently reviewed
  conflict-free protocol.
- A known provider ID is reconciled, never resubmitted.
- A create that may have succeeded but whose ID is not durable remains ambiguous
  and fail-closed. Local deterministic keys are not provider idempotency proof.
- If only a subset of creates succeeds, known IDs remain durable, untouched
  authorized/unstarted actions remain distinguishable, and ambiguous members block
  unsafe resubmission without discarding safe evidence.
- The full snapshot must validate before any checkpoint is advertised as safe for
  capacity release or fresh-worker restoration.
- Polling/reconciling known work incurs no new commitment.
- Interactive fan-out has a frozen maximum of six initial creates per run. No
  caller-controlled unbounded concurrency is introduced.
- Slice 1 must freeze numeric per-create I/O and complete submission-cycle bounds,
  informed by Slice 0 measurements. “Concurrent” without a tested wall-clock
  ceiling is not an accepted contract. Qualification must show that six durable IDs
  normally take approximately the slowest create plus bounded coordination and
  persistence overhead, never the sum of six create durations.
- Submission concurrency and retrieval concurrency are separate controls. Six
  initial creates may overlap, while released reconciliation remains capped at four
  due Response retrievals per cycle unless independent evidence and contract review
  justify a later change. A six-member wave may therefore reconcile in two short
  retrieval subwaves without weakening correctness or initial latency.

## Scope

- Provider-free baseline of current submission timing in all four pipelines.
- A versioned initial-wave prepare/authorize/execute/reconcile contract.
- Exact and bounded interactive concurrent create with immediate ID durability.
- Detach after submission into the existing provider-pending capacity contract.
- Fresh-worker bounded reconciliation and deterministic six-pass fan-in.
- Batch parity/non-regression for exact and bounded six-member rounds.
- Failure injection at every authorization, create, ID-persistence, state,
  journal, snapshot, detach, reconciliation, and fan-in boundary.
- Strict Python/CLI/schema/fixture/event and API consumer handoff updates.
- Transition-oracle extensions using existing public lifecycle vocabulary unless
  contract review proves a new state is unavoidable.
- Correct bounded final-QA state precedence and add defensive pre-provider
  equivalence detection for selected bounded claims that would predictably produce
  duplicate cards across isolated passes.
- Windows and Linux Python 3.11 installed-wheel qualification.

## Non-goals

- Decomposing one deck into six API jobs, worker leases, or native workspaces.
- A general scheduler, queue, DAG engine, or provider rate limiter.
- Concurrent creative retries or optional stages.
- Changing assignment, prompts, model, reasoning, output limits, selection,
  scoring, unknown-time policy, Mean/True Node projection policy, or final QA.
- Weakening authorization binding, snapshot integrity, stable-path restoration,
  ambiguity handling, or API ownership of global spend authority.
- Claiming OpenAI create idempotency beyond documented provider guarantees.
- Paid qualification without separate explicit API-key and dollar authorization.
- Tagging or publishing a release without separate approval.

## Slice 0 — Four-pipeline baseline and seam inventory

### Work

- Instrument scripted providers to record prepare, authorization, create, ID commit,
  poll, result, and detach timing for exact interactive, exact Batch, bounded
  interactive, and bounded Batch.
- Prove which pipelines currently serialize initial pass completion, which create
  operations concurrently, and which already use a single six-member Batch round.
- Trace exact and bounded paid-action cardinality, active-action assumptions,
  single-writer locks, provider adapters, lifecycle inspection v0.3, cycle result
  v0.2, native journal/result/receipt publication, and API-facing fixtures.
- Identify whether exact interactive's older `max_workers` path creates all six
  operations promptly or merely overlaps blocking execution without supporting
  clean detach.

### Tests and evidence

- Zero-provider scripted timeline for every cell.
- Existing route-parity and transition-oracle suites.
- Baseline repository suite and `git diff --check`.

### Gate

Pause for review of the measured topology and the smallest safe shared seam. No
contract or runtime behavior changes in this slice.

## Slice 1 — Initial-wave contract and API review

### Work

- Freeze a versioned initial-wave identity containing the ordered six actions,
  assignment identity, route family, transport, pass IDs, attempts, request
  digests, commitments, and aggregate maximum commitment.
- Define one prepare result that exposes all six exact interactive authorization
  requests before any submission, while retaining per-action authorization and
  consumption evidence.
- Define a digest-bound wave authorization envelope covering the exact ordered
  member set and its aggregate maximum commitment. SBE requires the complete valid
  envelope plus all six member authorizations before any provider create; the API
  owns the transaction that acquires or declines the corresponding reservation set.
- Define exact replay, stale observation/revision behavior, partial authorization,
  mixed applicability, and all-or-none preflight rules. Leading proposal: no create
  begins until all six initial actions have valid exact authorization; an API may
  delay or deny individual authority without creating a partial editorial wave.
- Freeze actual numeric concurrent-create count, per-create transport timeout, and
  total submission-cycle wall-clock bound, plus deterministic presentation and
  detach behavior. The values must be justified by Slice 0 evidence and become
  versioned contract constants rather than caller-selected production tuning.
- Freeze the exact interactive cache-warming decision. The reviewed leading policy
  is to eliminate full-response cache-warmer serialization for initial waves and
  accept measured cache economics. A create-only warm-up may be retained only if it
  does not delay the other five creates and evidence shows useful behavior. Waiting
  for one complete Response before beginning the remaining five is prohibited as an
  implicit optimization.
- Preserve the released retrieval maximum of four per short cycle as an independent
  rate-pressure control; do not raise it to six merely to match create cardinality.
- Define partial-create outcomes: provider-bound, untouched authorized/unstarted,
  ambiguous, refused, and safe replay/reconciliation.
- Confirm that existing inspection v0.3, cycle-result v0.2, public states, capacity
  dispositions, custody projections, and terminal vocabulary can express the wave;
  version explicitly if strict consumers require new fields.
- Freeze Batch compatibility: one round action/reservation, six member identities,
  no new reservation cardinality.

### Tests

- Strict schemas, closed vocabularies, unknown-field rejection, and digest replay.
- Authorization binding, duplicate/missing action, stale state, route/pass mismatch,
  and mixed-authority truth tables.
- Complete wave-envelope success; partial API/member authority; envelope/member
  digest conflict; aggregate-commitment mismatch; and proof that every refused
  preflight performs zero provider creates and zero authorization consumption.
- Deterministic timing tests proving the frozen submission-cycle bound covers six
  overlapping creates and serialized immediate ID commits.
- Cache-policy comparison proving the chosen initial-wave behavior has no hidden
  full-response warm-up barrier, plus explicit cost/cache evidence classification.
- Six pending members reconciled safely through the existing maximum-four retrieval
  subwaves with monotonic member evidence and deterministic fan-in.
- Existing-state composition and transition-oracle proposal.

### Gate

Pause for Kevin and AstroWoof API-agent approval before runtime implementation.
This is the cross-repository authority and schema freeze.

## Slice 2 — Transport-neutral wave coordinator

### Work

- Add the smallest shared coordinator for a six-action initial wave while retaining
  exact and bounded packet/result adapters.
- Separate prepare, submit, retrieve, validate, and assemble phases so interactive
  create does not block waiting for completion.
- Serialize native mutations through one writer while permitting bounded provider
  create I/O concurrently.
- Persist wave/member state and derive run-level custody/capacity projections.
- Add a bounded selection/packet admission check for equivalent provider-visible
  editorial semantics. It must report both claim IDs and their source/evidence
  basis and fail before paid preparation; it must never silently select, merge, or
  rewrite upstream evidence. SPC retains ownership of Mean/True Node projection
  policy.

### Tests

- Deterministic wave construction for exact and bounded.
- Request-byte and assignment non-regression.
- Completion-order independence and conflicting-writer refusal.
- No provider calls during preparation, inspection, or replay-only paths.
- Equivalent Mean/True Node fixture rejection before any paid action is prepared,
  plus nearby non-equivalent Node fixtures proving the check is not name-based.

### Gate

Both routes can express the same orchestration phases without sharing or weakening
their semantic authority.

## Slice 3 — Exact interactive concurrent submission

### Work

- Prepare and authorize six exact initial paid actions as one bounded wave.
- Create up to six Responses concurrently with separate prompts and output schemas.
- Commit each Response ID immediately and detach after the submission cycle rather
  than polling the wave to completion.
- Reconcile completed members through short provider-pending cycles, validate each
  independently, and fan in only after all required initial members close.

### Tests

- Six creates overlap and all IDs become durable within the frozen cycle bound.
- Fresh-worker restore, not-due, mixed pending/completed, and final fan-in.
- Failure injection before/after every create and ID commit, including partial
  success and identity-less ambiguity.
- No duplicate POST under resume, contention, crash, or reordered completion.

### Gate

Exact interactive achieves bounded concurrent creation and safe detach with no
editorial or delivery drift.

## Slice 4 — Bounded interactive concurrent submission

### Work

- Apply the reviewed wave coordinator to bounded initial passes.
- Preserve bounded provider minimization, invariant-only authority, locked local
  hydration, pass validation, and separate bounded schemas.
- Reconcile and assemble independently of completion order.
- Preserve final-QA failure as `FINAL_QA_REQUIRES_REVIEW`; generic pass-derived
  persistence must not overwrite it or permit optional submissions.

### Tests

- Six bounded creates overlap with independent route/pass/action bindings.
- Protected subject/provenance canaries across every concurrent request.
- Mixed pending/completed, crash/restore, ambiguity, and deterministic fan-in.
- Regression using the retained Kevin bounded finding: duplicate cross-pass output
  blocks optional stages and the machine-readable QA state remains authoritative
  through native persistence, public state, snapshot, lifecycle inspection, native
  result, and receipt publication.

### Gate

Bounded interactive reaches the same safe concurrent provider-pending shape as
exact without weakening its semantic or final-QA boundary.

## Slice 5 — Exact and bounded Batch compatibility

### Work

- Prove exact and bounded Batch retain one round action/reservation with six logical
  members and do not inherit the interactive six-reservation model.
- Reuse the initial-wave member identity where compatible without changing Batch
  request bytes or settlement semantics.
- Preserve partial-member failure, unavailable-usage, retry-round, retrieval
  custody, consumer-authority, and billing-pending behavior.

### Tests

- Six-member request inventory and one paid round authority for both routes.
- Member reorder, partial output/error, missing usage, terminal provider failure,
  pass-local retry, detach/not-due/reclaim, and final assembly.
- Interactive/Batch logical request parity for each route after documented envelope
  normalization.

### Gate

Both Batch pipelines remain production-compatible and cannot accidentally multiply
API reservations or regress cost disposition.

## Slice 6 — Failure atomicity, lifecycle, and transition oracle

### Work

- Exercise every irreducible create/persistence crash window and document the
  provider atomicity gap explicitly.
- Extend lifecycle inspection, cycle results, journal, immutable result/receipt,
  events, and route-parity oracle only as frozen in Slice 1.
- Prove a detached wave releases local capacity while retaining per-action provider
  custody and API consumer authority.
- Prove newly completed members are monotonic and safe local work is exhausted
  before the next detach.

### Tests

- Exhaustive partial-wave state matrix from zero through six known IDs.
- Concurrent resume/single-writer contention and stale observation tests.
- Snapshot publication and orphan-repair injection.
- Existing API transition oracle plus route-specific four-pipeline traces.

### Gate

Every partial wave is either safely resumable/reconcilable or explicitly ambiguous;
no state can duplicate paid work or falsely release custody/authority.

## Slice 7 — Public interfaces and consumer handoff

### Work

- Package supported Python, CLI, schemas, catalog entries, fixtures, event examples,
  and worker integration guidance.
- Publish exact examples for prepare/authorize, six-ID detach, partial completion,
  not-due, ambiguity, Batch round, fan-in, retry, final QA, and delivery.
- Document API adoption order and the distinction between interactive per-action
  reservations and Batch round-level reservation.

### Tests

- Consumer-shaped installed-wheel Python/CLI validation without internal imports.
- Strict fixture/schema/catalog validation and unsupported-version rejection.
- Provider-visible disclosure and event redaction.

### Gate

Pause for API review before joint qualification. The API must be able to adopt the
wave without parsing `run.json`, logs, or private workspace files.

## Slice 8 — Cross-platform qualification and closeout

### Work

- Run provider-free Windows and Linux Python 3.11 installed-wheel qualification for
  all four pipelines.
- Measure scripted serial versus concurrent initial-wave elapsed time and verify
  concurrent time approaches the slowest member plus bounded overhead rather than
  the sum of six members.
- Qualify fresh-worker detach/reclaim, partial completion, pass-local retry, final
  fan-in, optional continuation, and delivery.
- Record hashes, commands, counts, compatibility identities, residual limitations,
  and release recommendation.

### Tests

- Full repository suite, reproducible wheel build/content inspection, `pip check`,
  installed smoke, and clean-tree/diff hygiene.
- Optional paid live qualification only after separate explicit authorization and
  an approved ceiling.

### Gate

Pause for final Kevin/API review. Version bump, tag, and publication require
separate authorization.

## Sprint-wide test strategy

1. Deterministic scripted providers with barriers and clocks prove actual create
   overlap rather than relying on wall-clock luck.
2. Per-action authorization, commitment, provider ID, usage, and reconciliation
   evidence remain exact under a six-member wave.
3. Failure injection covers every member and every write boundary, including
   partial success and the irreducible identity-less provider ambiguity window.
4. Single-writer contention tests prove concurrent I/O cannot corrupt native state.
5. Exact/bounded request, authority, minimization, hydration, QA, and assembly
   regressions prevent semantic-route leakage.
6. Batch tests preserve one round reservation and complete/unavailable usage rules.
7. Lifecycle/oracle traces prove no new public state is smuggled into strict API
   consumers and capacity release never implies authority release.
8. Installed-wheel tests exercise only packaged public interfaces on Windows and
   Linux Python 3.11.
9. No paid provider operation is authorized by this plan.

## Exit criteria

The sprint is complete only when:

1. exact and bounded interactive initial waves create six independent provider
   operations concurrently within a documented bound;
2. every provider ID becomes durable immediately and known work is never
   resubmitted;
3. partial creation has deterministic provider-bound, untouched, or ambiguous
   evidence with no unsafe automatic retry;
4. the run detaches after submission and later fresh workers reconcile without a
   long-lived six-call worker;
5. pass membership, prompts, QA, retries, assembly, and delivery are unchanged by
   execution order;
6. exact and bounded Batch remain one paid round/reservation with six members;
7. local capacity, provider custody, native spend, and API consumer authority remain
   independently represented;
8. bounded final-QA review state cannot be overwritten by accepted-pass status or
   proceed into optional paid work;
9. strict public contracts, fixtures, transition traces, and handoff documentation
   are accepted by the API consumer;
10. all cross-platform source and installed-wheel gates pass; and
11. release status and any remaining provider atomicity gap are explicit.

## Effort assessment

This is one large SBE sprint, comparable to the recent provider-pending and native
transition-journal sprints. The difficult portion is not concurrency itself; it is
turning six interactive actions into one safely authorized, partially durable,
detachable wave without weakening ambiguity or single-writer guarantees. The
Batch cells should be compatibility work rather than parallel reimplementation.
