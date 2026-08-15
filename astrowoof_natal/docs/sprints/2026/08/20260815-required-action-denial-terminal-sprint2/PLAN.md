# Required-Action Denial Terminalization Sprint 2 Plan

```yaml
status: in_progress
date: 2026-08-15
owner: semantic-basis-extractor
consumer: astrowoof-api
scope: native terminalization after providerless denial of required actions
implementation_started: true
release_status: not_authorized
```

## Purpose

Close the lifecycle gap in which a required paid action is validly denied by
API-owned global authority, SBE persists `DENIED_PROVIDERLESS`, but the parent run
retains an active authoring status and therefore synthesizes a false local
continuation dependency. The supported native denial operation must durably
resolve both the exact action and the run-level consequence so inspection,
closeout, restoration, and replay agree that no legal continuation remains.

The source handoff is retained in [`SOURCE REQUEST.md`](SOURCE%20REQUEST.md).

## Preliminary diagnosis

Current action projection correctly treats `DENIED_PROVIDERLESS` as no longer
necessary. The contradictory closeout arises because `_local_dependencies()` maps
the unchanged run status `AUTHORING` directly to blocking
`retry_preparation / authoring_continuation`. This plan therefore tests and fixes
the authoritative state transition at denial time rather than adding a closeout-
only exception that would leave runner, public state, inspection, and closeout in
disagreement.

## Scope

### Included

- exact reproduction of a required creative-retry denial followed by inspection
  and closeout;
- a reviewed run-level terminal state/outcome for externally denied required work;
- a reason × necessity × stage × single/batch decision matrix;
- atomic persistence of action denial and any required run terminalization under
  the existing one-lock denial protocols;
- consistent private state, public state, lifecycle inspection, quiescence,
  closeout, CLI, events, snapshots, replay, and restore behavior;
- mixed batch behavior where required and independently optional actions are
  denied together;
- preservation of monotonic accepted evidence, prior authorization, delivery
  bytes, provider-safety rules, and exact API authority references;
- exact and bounded-route regression coverage where the shared lifecycle applies;
- installed-wheel smoke, consumer handoff, recovery guidance, and a release
  recommendation.

### Excluded

- changing API-owned quotas, reservations, circuit breakers, entitlements,
  leases, billing reconciliation, publication policy, or PostgreSQL state;
- submitting, polling, cancelling, or reconciling provider work;
- weakening providerless-denial eligibility or permitting denial after provider,
  consumption, report, or ambiguous-submission evidence exists;
- treating optional-stage skipping as required-action terminalization;
- redefining SBE's per-run dollar ceiling or fifty-claim semantic budget;
- reopening accepted delivery or inventing substitute editorial output;
- arbitrary repair of retained workspace bytes;
- product-policy redesign of retries, polish, critic, Quick/Complete, unknown-time
  handling, or bounded selection; and
- release, tag, or publication without separate authorization after closeout.

## Proposed semantic direction for review

1. **Terminalization belongs to native denial mutation.** If an action is required
   at the locked decision basis and an accepted providerless denial makes its work
   impossible, SBE should atomically persist a run-level terminal consequence in
   the same semantic transition. Closeout should report that authority, not infer
   a different outcome later.
2. **Use budget exhaustion as the leading status proposal, but retain exact cause.**
   The consumer recommends `BUDGET_EXHAUSTED` as the clearest current terminal
   status for denial by external spend authority. The leading design is therefore
   `BUDGET_EXHAUSTED` plus a closed machine-readable reason such as
   `external_spend_authority_denied`, so API global refusal is distinguishable from
   SBE's own per-run ceiling. Slice 1 will compare that with a distinct native
   policy-stop status and freeze the simpler unambiguous contract after API review.
3. **Action disposition remains exact.** The action remains
   `DENIED_PROVIDERLESS`, retaining positive authorization history, exact binding,
   denial reason, authority reference, and single/batch evidence. Run
   terminalization supplements rather than replaces action provenance.
4. **Requiredness is evaluated under the locked decision basis.** The API does not
   declare an action required. SBE uses its native `necessary`/relationship
   semantics immediately before mutation. A stale request still fails closed.
5. **Optional denial does not automatically fail the run.** Independently optional
   work follows its existing skip/continuation policy. The decision matrix must
   prove that optional cleanup cannot spuriously terminalize a deliverable run.
6. **A batch has one coherent run consequence.** If all members pass and at least
   one required member implies terminalization, all requested denials and the
   single run transition commit together. A refused batch changes neither actions
   nor run status. Exact replay performs no second transition.
7. **The resulting terminal state is non-publishable unless delivery was already
   accepted.** For pre-delivery required denial, inspection should be terminal and
   quiescent, closeout should be closed with a machine-distinct terminal reason,
   and delivery flags should remain false. For cleanup after accepted
   `DELIVERY_COMPLETE`, denial must preserve delivery authority and must not
   downgrade the successful run merely because an unused action was historically
   marked required; Slice 1 will define this precedence explicitly.
8. **No continuation-by-fiat.** Neither runner nor closeout may prepare a
   replacement action, submit provider work, or report blocking local continuation
   after native terminalization.

## Contract questions to settle in Slice 1

- Whether to use `BUDGET_EXHAUSTED` with a distinct terminal reason (leading
  proposal) or a separate policy-stop status, plus the exact private status,
  public outcome, closeout disposition, and event vocabulary.
- Whether all accepted `external_authority_denied` denials of a required action
  terminalize, whether `reservation_unavailable` is equivalent or retryable, and
  whether any other existing denial reason has terminal meaning.
- Precedence among accepted delivery, native budget exhaustion, ambiguity/review,
  and external-authority denial.
- Whether the single/batch result should directly return a `run_transition` block
  so the API need not infer terminalization from a later inspection.
- The bounded provenance fields needed to distinguish global-policy refusal from
  SBE per-run budget exhaustion without exposing API policy detail.
- Supported recovery procedure for already-retained 0.4.1 workspaces exhibiting
  the contradictory state.

## Governing invariants

- SBE owns native requiredness, action state, run status, snapshots, lifecycle
  projection, closeout, and native recovery.
- The API owns the decision and audit authority behind
  `external_authority_denied`, plus all cross-run/global policy.
- Denial and terminalization use the existing lifecycle/spend single-writer lock
  and publish one coherent revision/snapshot.
- Provider evidence and submission ambiguity always prevent providerless denial.
- Accepted evidence and authorization history are monotonic.
- Exact replay cannot advance revision, duplicate events, alter terminal reason,
  or reach provider code.
- Public state, inspection, closeout, and runner behavior must derive from the same
  durable native state and cannot contradict one another.
- Events remain non-authoritative, redacted, and failure-isolated.

## Slice 0: Baseline and exact reproduction

### Outcome

Freeze the 0.4.1 behavior and reproduce the retained-run contradiction without
provider work.

### Work

- Record clean repository/release baseline.
- Construct a provider-free fixture with a genuinely required authorized creative
  retry and the smallest realistic parent authoring state.
- Apply single and two-action batch `external_authority_denied` requests.
- Capture action state, run status, public state, inspection, closeout, snapshot,
  and replay evidence.
- Verify whether the same contradiction is shared by exact and bounded routes.

### Tests

- Focused denial and closeout regression tests.
- Hash proof that denial changes only its documented write set and never accepted
  editorial/delivery evidence.
- Baseline full repository suite and `git diff --check`.

### Gate

The report is reproduced precisely, requiredness is proven from native state, and
no separate defect or fixture artifact explains the false continuation.

## Slice 1: Terminal contract and API review

### Outcome

Freeze the state machine and consumer-visible vocabulary before mutation changes.

### Work

- Publish the reason/necessity/stage/status decision table.
- Specify the new status/outcome/reason, closeout disposition, delivery flags,
  quiescence, local dependencies, result transition evidence, and event payload.
- Specify accepted-delivery and existing terminal-state precedence.
- Define migration/recovery behavior for retained 0.4.1 workspaces.
- Update strict schemas/fixtures/catalog drafts as needed.

### Tests

- Strict vocabulary/schema acceptance and rejection.
- Truth-table tests for required versus optional, single versus batch, supported
  denial reasons, pre-delivery versus delivery-complete, and competing terminal
  states.
- Contract resource and redaction checks.

### Gate

Pause for Kevin and AstroWoof API-agent review. The API must be able to map the
terminal result, release its matching authority, and decide workspace retention
without parsing prose or confusing global denial with SBE budget exhaustion.

## Slice 2: Atomic native terminalization

### Outcome

Persist required-action denial and its run-level consequence as one coherent
semantic transition in both single and batch operations.

### Work

- Derive terminalization from locked native requiredness and reviewed precedence.
- Update private and public state inside the existing denial write protocols.
- Return typed run-transition evidence if approved in Slice 1.
- Preserve batch all-or-none behavior and single-action compatibility.
- Prevent runner continuation or new action preparation from the terminal state.

### Tests

- Single required denial terminalizes once.
- Batch with required members terminalizes once; mixed eligible batch remains
  atomic.
- Optional denial does not spuriously terminalize.
- Refusal changes no action or run state.
- Exact replay is byte-stable and provider unreachable.
- Accepted authorization/evidence and unrelated actions remain monotonic.

### Gate

Every successful required denial produces one coherent terminal checkpoint; every
refusal produces none; no legal execution path can submit replacement work.

## Slice 3: Inspection, closeout, and recovery coherence

### Outcome

Make every lifecycle projection agree with the new durable terminal authority and
support safe recovery of affected retained workspaces.

### Work

- Update local dependency, terminal, quiescence, and closeout derivation.
- Ensure closeout returns no unresolved action IDs or false local continuation.
- Add constrained interrupted-write recovery at every changed persistence boundary.
- Implement a supported migration/recovery command or exact automatic migration
  only if the reviewed 0.4.1 evidence can be recognized without blessing arbitrary
  bytes.
- Document fail-closed cases that require retaining the workspace for review.

### Tests

- Inspect and closeout the exact regression state.
- Failure injection before/after action, run/public state, terminal evidence, batch
  artifact, and snapshot persistence.
- Restore/rebase-at-stable-logical-path and exact replay tests.
- Missing, changed, contradictory, provider-bound, ambiguous, and unrelated bytes
  fail closed.
- Closeout artifact replay remains stable.

### Gate

Private/public state, inspection, quiescence, and closeout are mutually consistent,
and retained-run recovery is provenance-preserving and narrowly bounded.

## Slice 4: CLI, events, installed interfaces, and consumer handoff

### Outcome

Ship the behavior through supported consumer surfaces and make API adoption
unambiguous.

### Work

- Extend supported schemas, fixtures, catalog, CLI results, structured events,
  lifecycle smoke, and installed resource enumeration.
- Document the API sequence for global denial, SBE mutation, API authority release,
  fresh inspection, closeout, publication decision, and scratch cleanup.
- Document exact mapping differences among external denial, budget exhaustion,
  ambiguity, review, successful delivery, and optional-stage skipping.
- Preserve existing single/batch command compatibility.

### Tests

- Consumer-shaped Python and CLI tests using documented surfaces only.
- Event correlation, ordering, replay, redaction, and sink-failure isolation.
- Exact and bounded lifecycle smoke.
- Fresh installed-wheel smoke outside the source tree on Windows and Linux if a
  release is recommended.

### Gate

The API can recover the retained scenario and handle future global denials using
typed installed interfaces, with no native-file edits or provider work.

## Slice 5: Closeout and release recommendation

### Outcome

Lock evidence, answer the source handoff, and state whether another pinnable patch
release is warranted.

### Work

- Run final focused, full-suite, failure-injection, installed-wheel, reproducible-
  build, content, and diff gates proportionate to the final change.
- Record exact commands, counts, source commit, artifact hashes, compatibility,
  consumer review, recovery result, and zero-provider evidence.
- Reconcile plan/log/evidence/results and publish a concise API response.
- Recommend or withhold release; do not tag or publish without separate approval.

### Gate

All lifecycle projections agree, the retained-run path is safely addressed, API
review has no blocker, qualification trees are removed, and release status is
explicit.

## Sprint-wide testing strategy

1. Provider-free exact reproduction and authoritative-byte inventories.
2. Closed state-machine truth table and strict schema tests.
3. Single/batch atomic mutation and exact replay tests.
4. Runner, inspection, public-state, closeout, and quiescence coherence tests.
5. Failure injection and constrained retained-workspace recovery tests.
6. Exact and bounded regression tests plus the complete repository suite.
7. Consumer-shaped Python/CLI/event tests.
8. Reproducible wheel and Windows/Linux exact-wheel smoke if release is recommended.

No API key, paid request, provider submission, cancellation, or polling is needed
or authorized for this sprint.

## Exit criteria

The sprint is complete only when:

1. a required providerless denial produces explicit durable native terminal
   authority under single and batch operations;
2. optional denial and accepted-delivery cleanup retain their reviewed semantics;
3. external/global denial remains machine-distinguishable from SBE per-run budget
   exhaustion even if both use the `BUDGET_EXHAUSTED` status;
4. runner, public state, inspection, quiescence, and closeout agree;
5. no provider or local continuation is reported or attempted after terminalization;
6. exact replay is non-mutating and failure recovery is narrowly provenance-bound;
7. accepted evidence, authorization history, and delivery bytes remain monotonic;
8. the retained 0.4.1 case has a supported recovery path or an explicit safe
   refusal procedure;
9. exact and bounded shared-lifecycle regressions pass;
10. supported Python, CLI, schemas, fixtures, events, smoke, and handoff are complete;
11. full qualification passes with zero provider work; and
12. Kevin/API review accepts the contract or all objections are explicitly retained.

## Evidence and review policy

`LOG.md` records chronology and decisions. `EVIDENCE.md` records exact commands,
counts, hashes, mutations, recovery outcomes, and provider/spend evidence.
`results/README.md` indexes slice reports. At every slice gate, inspect the diff,
run proportionate tests and `git diff --check`, update all three records, link them
in the handoff, and pause for approval before committing.

Implementation began after plan approval. Later slices retain explicit review
gates. Release/tag/publication requires a separate authorization after sprint
closeout.

Slices 0 through 2 are committed. Slice 3 is implementation-complete and paused
at its review gate; CLI/event/installed-interface and consumer-handoff work remains
assigned to Slice 4. Release, tag, and publication remain unauthorized.
