# Provider-Pending Capacity Fairness Sprint 1 Plan

## Status

Pre-sprint huddle complete. Plan prepared for reciprocal API review. No runtime
change is approved. Begin Slice 0 only after both repositories agree on this
investigation boundary.

## Objective

Explain why earlier paired QA runs overlapped their provider-bound lifetimes,
while recent pairs appear effectively serialized behind one SBE capacity owner,
and then implement the smallest evidence-backed correction in the repository
that owns the divergent behavior.

The practical success condition is not simultaneous provider-create calls. It
is bounded peer access: run B can submit its initial wave while run A still has
durable provider custody, without delaying run A past its lawful due boundary,
creating concurrent writers for one workspace, or duplicating paid work.

## Current evidence

### Established

- Earlier retained traces show provider-lifetime overlap:
  - 2026-09-02: B began fan-out while A continued through approximately 06:51
    America/Denver.
  - 2026-09-03 morning: B began fan-out while A remained active until
    approximately 07:37.
  - 2026-09-03 afternoon: B began fan-out while A still reconciled after 15:12.
- The observed six-create bursts themselves did not overlap. The overlap began
  after the first run detached with durable provider identities.
- The recent Podium/Laurel witness is effectively serial: Podium began fan-out
  at 03:28:32, reached its terminal command result at 03:36:54, and Laurel did
  not begin fan-out until 03:37:40 America/Denver.
- SBE still publishes `release_until_due` when retained provider work is not due
  and no deterministic local work is ready.
- SBE truthfully publishes `continue_local_cycle` when due retrieval or local
  fan-in remains immediately actionable.
- With six due actions and a reconciliation cap of four, one cycle may process
  four while two remain due. That state is not provider quiescence.
- API honors an exact final `release_until_due` result.
- API preserves allocation on ordinary `continue_local_cycle` handling, defers
  the incumbent, and uses allocation-aware selection that can favor the current
  owner over a peer that has never received a slot.

### Sprint 58 boundary hypothesis

Owner recollection places the behavioral change shortly after API Sprint 58,
the terminal-result-first lifecycle handoff.

History anchors:

| Boundary | Commit | America/Denver |
|---|---|---|
| Sprint 58 plan | `31237f6e369fb411732769bb9675a03b599897e3` | 2026-08-30 04:07:55 MDT |
| Sprint 58 closeout | `bc5873f590a0de0154754c0a74f52dcb7a04f045` | 2026-08-30 06:07:59 MDT |

The exact SBE companion is
`20260830-retry-external-authority-v2-dispatch-handoff-sprint1`. Its shipped SBE
change was an additive terminal-result availability reader, not an apparent
provider-pending capacity-policy change. The strongest history lead therefore
remains API-side terminal preflight, result ingress, defer, allocation retention,
and claim selection.

This is a falsifiable hypothesis, not a causal conclusion.

### Historical evidence ceiling

The current QA database was reset and no longer contains the immediate
pre-Sprint-58 population. Render's Hobby retention also no longer provides the
needed exact pre-boundary logs. A paced export confirmed that the relevant clean
windows are empty rather than merely hidden by request throttling.

Later same-day traces and current logs are contextual evidence only. We will not
invent the missing eight-run before/after table or infer identities from subject
names and trace order.

Because direct archaeology is exhausted, deterministic code-history replay
across the Sprint 58 boundary is the primary causal experiment.

## Frozen semantics

1. `release_until_due` means no native/provider operation is actionable before
   an exact due time. It is not a fairness hint.
2. `continue_local_cycle` means native work can advance now. It does not by
   itself mean API must grant the same run unlimited consecutive scheduler
   turns.
3. A trace-visible intermediate inspection is diagnostic only. The final
   returned, schema-validated result is scheduling evidence.
4. Provider custody, execution capacity, API admission, and workspace-writer
   exclusion are distinct authorities.
5. Releasing or rotating API capacity does not release provider custody,
   authorization, or spend reservation unless a separate closed contract says
   so.
6. A scheduler turn may end only at a durable boundary where the workspace has
   no active writer and replay retains exact action/request/grant identities.
7. No solution may make a false native quiescence claim merely to improve
   fairness.

## Scope

### In scope

- Source/history mapping around API Sprint 58 and its SBE companion.
- Provider-free reproduction using the real API worker/scheduler boundary and
  real public SBE lifecycle results where practical.
- Two-run/one-slot deterministic scheduling tests.
- Initial-wave detachment, bounded Response reconciliation, completed-evidence
  fan-in, and relevant external-authority handoffs.
- API allocation, lease, defer, availability, and claim ordering.
- A narrowly scoped API correction if existing SBE facts are sufficient.
- A new public SBE fact only if the experiment proves API cannot distinguish a
  safe yield boundary using existing closed evidence.

### Out of scope

- Live provider calls, paid QA work, retained-run recovery, or R2 mutation.
- Reconstructing unrecoverable historical rows.
- Simultaneous provider-create bursts as a product requirement.
- Increasing global capacity as a substitute for fairness.
- Weakening single-writer, custody, replay, or external-authority rules.
- Assuming Batch, bounded, critic, candidate, polish, and initial-wave routes
  share one safe scheduling boundary.
- Deploying or releasing either repository before joint qualification.

## Metrics and definitions

- **Peer time-to-first-submit:** peer eligibility to first durable provider
  identity.
- **Allocation hold duration:** time the incumbent owns scarce API execution
  capacity.
- **Useful native execution:** command time that advances native truth.
- **Retained-owner idle duration:** time an owner retains allocation while no
  command is executing.
- **Due-time wakeup lateness:** claim time minus the earliest lawful resume time.
- **Provider-lifetime overlap:** interval during which both runs retain unresolved
  provider-bound work.
- **Consecutive scheduler turns:** safe command boundaries awarded to the same
  owner while an eligible peer waits.
- **Starvation witness:** an eligible peer remains unselected beyond a closed
  deterministic bound while another run repeatedly progresses or sleeps.

## Slice 0 — Provenance freeze and production source map

### Goal

Freeze the strongest evidence we actually possess and map the complete decision
path without asserting a causal fix.

### Work

1. Create an evidence manifest for:
   - the three older overlap witnesses;
   - the recent Podium/Laurel serial witness;
   - API Sprint 58 history anchors;
   - relevant API image/commit and SBE wheel identities where recoverable;
   - timezone and source-file provenance.
2. Correct or explicitly isolate the Podium/Goldie versus Podium/Laurel naming
   discrepancy. Names are never join keys.
3. Trace current SBE paths for:
   - initial-wave detach;
   - not-due provider custody;
   - due actions above the four-member cap;
   - completed-evidence fan-in;
   - external-authority wait;
   - terminal/review closeout.
4. Trace current API paths for:
   - final result ingestion;
   - `release_until_due` capacity release;
   - `continue_local_cycle` allocation retention;
   - defer/`available_at` calculation;
   - allocation-aware claim ordering;
   - lease release/reclaim.
5. Separate command duration, configured defer, and post-availability claim
   latency in every timeline.
6. Record the historical evidence ceiling as final unless a new immutable source
   is specifically identified.

### Deliverables

- `SLICE 0 - EVIDENCE MANIFEST AND SOURCE MAP.md`
- `EVIDENCE.md`
- `LOG.md`
- A candidate list of exact pre/post commits for replay.

### Internal checkpoint

Proceed directly into Slice 1. The first joint review occurs after the source
map and semantic diff are both complete, so each repository can finish its own
investigation before the shared huddle.

## Slice 1 — Sprint 58 before/after semantic diff

### Goal

Determine exactly which scheduling-relevant predicates or state mutations
changed across Sprint 58 and adjacent deployment commits.

### Work

1. Compare the last relevant pre-boundary API implementation with:
   - Sprint 58's first terminal-ingress commit;
   - Sprint 58's final commit;
   - the first deployed post-boundary revision.
2. Inventory changes to:
   - terminal-result lookup and precedence;
   - exact invocation-result transport;
   - capacity release/retention;
   - job disposition and defer timing;
   - `available_at` computation;
   - allocation-owner preference;
   - claim eligibility/order;
   - cleanup and successor scheduling.
3. Compare the SBE companion commits and prove whether they changed the final
   provider-pending capacity tuple or merely added result availability.
4. Produce a semantic diff table: old predicate, new predicate, owning
   repository, intended effect, possible fairness effect, and testability.
5. Do not treat code proximity or timestamp correlation as proof.

### Deliverables

- `SLICE 1 - SPRINT 58 SEMANTIC DIFF.md`
- A minimal set of candidate predicates to exercise in replay.

### Gate — Voof-paws 1

API and SBE agree that the evidence/source map, exact revisions, semantic diff,
and replay assertions are accurate. No runtime implementation begins here.

## Slice 2 — Deterministic production-path replay harness

### Goal

Build the smallest provider-free harness capable of executing the same
two-run/one-slot state sequence through pre- and post-boundary behavior.

### Required model

- Deterministic clock.
- One API capacity slot.
- Two independent native workspaces.
- Real allocation, lease, defer, claim, and result-mapping code where feasible.
- Real public SBE lifecycle documents or strict fixture equivalents validated by
  packaged readers.
- Scripted provider adapter with durable create identities and controlled
  pending/completed observations.
- No private-native-state reconstruction by API.

### Scenario

1. Run A obtains the slot, submits six initial actions exactly once, and detaches.
2. Its first reconciliation turn observes a configured mix that leaves truthful
   immediate work after a bounded unit.
3. Run B is eligible and has never held an allocation.
4. Advance the deterministic scheduler through claim/defer/release boundaries.
5. Observe whether B receives a turn before A becomes terminal.
6. Repeat under the pre-boundary and post-boundary revisions/configurations.

### Failure injection

- final `release_until_due`;
- final `continue_local_cycle / provider_reconciliation_due`;
- final `continue_local_cycle / local_work_ready`;
- command crash after durable provider identity;
- lease expiry/reclaim;
- exact result replay;
- stale or contradictory result;
- peer already eligible versus becoming eligible during A's command.

### Assertions

- identical scripted provider topology produces comparable native truth;
- create/retrieval/adoption counts remain exact;
- no same-workspace concurrent writer;
- every final disposition is consumed through its public validator;
- scheduler decisions and their positive permissions are recorded;
- pre/post behavior differs only where the semantic diff predicts, or the Sprint
  58 hypothesis is rejected.

### Deliverables

- Provider-free characterization tests.
- `SLICE 2 - BEFORE AFTER REPLAY RESULT.md`
- Machine-readable timeline/receipt if existing test infrastructure supports it.

### Gate — Voof-paws 2

Joint causal classification:

- confirmed Sprint 58 regression;
- adjacent API/configuration regression;
- legitimate topology plus incumbent-policy starvation;
- no reproducible divergence;
- or multiple contributing causes.

No repair proceeds without this classification.

## Slice 3 — Fairness invariant and ownership freeze

### Goal

Define the smallest safe behavior correction from the reproduced cause.

### Decision order

1. Prefer an API scheduler-turn rule at an already durable command boundary if
   existing SBE evidence is sufficient.
2. Consider changing defer/claim behavior if retained-owner sleeping is the
   proven cause.
3. Consider a new SBE cooperative-yield contract only if API cannot identify a
   safe turn boundary without guessing from native state.
4. Do not change reconciliation batch size merely to conceal scheduling
   starvation.

### Invariant candidates

- An eligible never-run peer receives a turn within `N` safe boundaries or `T`
  deterministic time while an incumbent retains provider custody.
- A due incumbent resumes no later than its lawful due boundary plus a bounded
  scheduling tolerance.
- Fairness rotation does not imply native quiescence.
- Allocation rotation never creates simultaneous writers for one workspace.
- Rotation preserves exact API admission and native provider custody.

The exact `N`, `T`, priority rule, and eligible-set definition must be frozen in
this slice, not hidden in timing-sensitive tests.

### Deliverables

- `SLICE 3 - FAIRNESS CONTRACT AND OWNERSHIP.md`
- Closed state/decision matrix.
- Explicit API and SBE responsibilities.
- Negative cases for ineligible, due, ambiguous, terminal, and authority-waiting
  runs.

### Gate — Voof-paws 3

Contract approval before runtime mutation.

## Slice 4 — Owning-repository implementation

### Expected default

Implement in API only if the replay confirms that existing SBE lifecycle facts
fully describe safe native progress and the defect lies in allocation/defer/claim
policy.

### API implementation requirements

- Apply fairness only at the frozen safe boundary.
- Preserve current final-result validation and precedence.
- Do not convert actionable work to `release_until_due`.
- Do not release provider/spend custody merely by rotating execution capacity.
- Persist enough decision evidence to explain why incumbent or peer won.
- Use deterministic clock and ordering in tests.

### Conditional SBE work

Only if Slice 3 proves a contract gap:

- introduce a new closed/versioned disposition or turn token;
- bind it to exact checkpoint, inventory, and resume evidence;
- distinguish it from provider quiescence;
- fail closed for old consumers;
- keep route applicability explicit.

### Tests

- incumbent with due retrieval;
- incumbent with completed-evidence fan-in;
- incumbent not due;
- peer never run;
- peer ineligible;
- exact tie ordering;
- repeated cycles cannot starve peer;
- due-time protection for incumbent;
- crash/reclaim and replay;
- no duplicate create/retrieve/adopt;
- no concurrent workspace writer.

### Gate — Voof-paws 4

Cross-repository implementation review before joined qualification.

## Slice 5 — Joint two-run/one-slot qualification

### Required positive trace

1. A submits six initial actions exactly once and detaches.
2. B receives a bounded turn and submits six initial actions exactly once while A
   remains provider-bound.
3. A resumes within its lawful due bound.
4. Due retrieval and local fan-in advance without false quiescence.
5. Both runs eventually reach their scripted native outcomes.

### Required safety trace

- zero external provider/network I/O;
- no duplicate create, retrieval, fan-in, request, grant, or consumption;
- no simultaneous writer for either workspace;
- no authority inferred from trace logs;
- crash/reclaim produces the same bounded fairness result;
- terminal/review/ambiguity paths retain their existing precedence;
- neither run can starve under the deterministic clock.

### Evidence

- Closed qualification receipt.
- Ordered scheduler/native event trace.
- Counts and timing metrics from this plan.
- Exact repository commits and installed SBE/API artifact identities.

### Gate — Voof-paws 5

Joint campaign review. Decide whether the correction is ready for repository-
specific release preparation.

## Slice 6 — Conditional release and deployment preparation

This slice exists only for repositories with runtime or public-contract changes.

- Follow each repository's release playbook.
- Select focused, broad, or full regression scope according to actual change
  surface; record any omissions honestly.
- Build deterministic artifacts where applicable.
- Repeat the installed two-run/one-slot qualification against final immutable
  candidates.
- Obtain separate explicit owner authorization before commit/tag/publication or
  QA mutation.
- Do not begin paid QA merely because source tests pass.

If the outcome is API-only and introduces no SBE change, close the SBE sprint as
an investigation/contract contribution with no SBE release.

## Acceptance criteria

1. The historical evidence ceiling is explicit and no missing run identity is
   inferred.
2. A deterministic pre/post replay accepts or rejects the Sprint 58 hypothesis.
3. The first divergent scheduling predicate is identified and owned.
4. `release_until_due` retains its native quiescence meaning.
5. One eligible peer receives bounded access while another run remains provider-
   bound.
6. Due provider work resumes within a documented bound.
7. Single-writer, custody, authority, and replay invariants remain intact.
8. Provider I/O counts are exact and no operation is duplicated.
9. The joined provider-free qualification is reproducible.
10. Only repositories whose runtime/contracts changed are released.

## Review points

| Point | Review question |
|---|---|
| Voof-paws 1 | Are the evidence/source map, history boundary, semantic diff, and replay assertions correct? |
| Voof-paws 2 | What caused the behavioral divergence? |
| Voof-paws 3 | Is the fairness contract safe, bounded, and correctly owned? |
| Voof-paws 4 | Does implementation preserve native/API authority boundaries? |
| Voof-paws 5 | Does the joined one-slot campaign prove fairness without duplication? |
| Final | Does either repository need release/deployment, and under what gate? |
