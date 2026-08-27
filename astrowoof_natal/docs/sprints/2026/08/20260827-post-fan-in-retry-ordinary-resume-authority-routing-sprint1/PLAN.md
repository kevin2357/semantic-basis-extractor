# Post-Fan-In Retry Ordinary-Resume Authority Routing — SBE Sprint 1

Date: 2026-08-27
Status: planning complete; implementation awaits owner/API review
Companion: AstroWoof API operational incident and follow-on sprint to be identified

## Objective

Correct the native selector/command boundary that routes a post-fan-in creative
retry through an incompatible initial-wave aggregate-grant guard. Preserve initial
wave create safety, ordinary v2 authority, provider reconciliation, idempotent local
fan-in, and API ownership while preventing a non-executable local cycle from
retaining capacity and starving another run.

## Required outcomes

1. A provider-bound post-fan-in retry is reconciliation-only until provider evidence
   is durably retrieved.
2. Retrieved completion evidence may advertise exactly one concrete local
   `provider_result_fan_in_and_retry_evaluation` operation.
3. Consuming that operation advances native truth and selects the exact next
   disposition: fresh ordinary authority, another local operation, review, or
   terminal/delivery work.
4. Initial-wave aggregate authority applies only to an actual active initial-wave
   admission, never merely because immutable initial-wave lineage remains stored.
5. Ordinary prepared actions use the supported v2 request/grant/authorization path;
   no generic resume invents or reuses authority.
6. A selected `ordinary_resume` either consumes its advertised semantic operation or
   produces a different typed disposition. It cannot return quiescent against the
   same basis while retaining local capacity.
7. Exact and bounded interactive routes have an explicit parity/refusal decision.
8. No duplicate provider create/retrieve, spend commitment, authorization
   consumption, accepted-evidence demotion, or cross-run release occurs.

## Invariants

- Retained provider custody outranks new authority and local preparation.
- Provider identity, call-entry, consumption, reported usage, and ambiguity remain
  monotonic safety evidence.
- Initial-wave v1 and ordinary-action v2 authority are never inferred from one
  another.
- Stored initial-wave history is lineage, not proof that initial admission is
  currently executable.
- SBE selects native commands and operation inventory; API invokes supported
  run-level commands and never selects private members.
- SBE does not assert API lease, capacity, reservation, or queue facts.
- API does not reconstruct SBE retry policy or mutate native state.
- Provider-free qualification reports zero network/provider/spend and does not
  access the retained QA cohort.

## Non-goals

- Repairing or resuming Strudel or Princess.
- Submitting or retrieving their provider operations.
- Changing creative retry count, prompts, authoring packets, or editorial policy.
- Changing initial-wave six-member fan-out or Batch topology.
- Redesigning API scheduling/capacity.
- Adding a generic force-resume, rehash, grant synthesis, or lineage deletion path.
- Broad lifecycle schema redesign unless Slice 1 proves current public evidence is
  insufficient.

## Slice 0 — Provider-free incident reproduction and causal characterization

Build a sanitized exact-interactive workspace through supported runtime code with:

- a completed and retained six-member initial-wave record;
- accepted initial pass evidence;
- one post-fan-in creative-retry action with production-shaped provider lineage;
- the exact native/API-relevant authorization and provider states from the incident;
- any later prepared/authorized retry represented separately; and
- a complete valid snapshot at a stable logical root.

Drive the actual public lifecycle inspection and semantic-closure resume/dispatch
entry points using the incident-shaped CLI arguments and a scripted no-network
transport. Capture:

- v0.5/v0.6/v0.7 command and capacity disposition;
- action inventory and complete public bindings;
- provider custody and reconciliation state;
- local-work operation kind/key/source actions;
- initial-wave state and lineage;
- selected command and guard reached;
- state/snapshot/result bytes before and after refusal; and
- redacted branch-selection events/logs.

Characterize at least these nearby controls:

1. provider ID pending/not due;
2. provider ID due but not retrieved;
3. retrieved completion awaiting local fan-in;
4. fan-in consumed and next retry `PREPARED`;
5. ordinary action authorized but providerless;
6. initial wave genuinely awaiting its aggregate grant; and
7. completed initial-wave lineage with no current initial admission.

Assess bounded interactive through the same characterization helper if possible;
do not change it yet.

Gate:

- reproduce the public command failure and no-progress successor without provider
  access or retained QA;
- identify whether the defect is selector classification, command plumbing, guard
  scope, API invocation arguments, or a combination;
- distinguish durable native provider identity from API-only projection; and
- freeze exact authoritative bytes/facts needed for Slice 1.

**Voof-paws 1:** API/owner review of the reproduction and causal boundary before
contract decisions.

## Slice 1 — Operation/authority routing contract and decision matrix

Freeze one closed matrix across route, wave state, ordinary action state, provider
evidence, reconciliation status, and local-work inventory.

At minimum specify:

| Native facts | Required command | Authority/side-effect rule |
| --- | --- | --- |
| fresh initial six-member wave awaiting authority | existing initial-wave constrained boundary | exact v1 request + aggregate grant + six documents |
| provider ID pending/not due | provider reconciliation cycle/not-due | retrieval-only; no create or local work |
| provider ID due | provider reconciliation cycle | SBE selects bounded due subset |
| retrieved completed evidence | ordinary resume | exact concrete local fan-in operation |
| next ordinary action prepared | await external authority | exact v2 request; no mutation/create without grant |
| ordinary action authorized/intent fenced | constrained v2 dispatch or review | generic resume cannot create |
| call entered without durable identity | ambiguity/review | never retry create |
| completed initial-wave lineage only | classify current ordinary/provider facts | must not reactivate initial admission |
| active initial-wave state with wrong command/documents | typed refusal | zero provider I/O and no partial authority |
| no executable operation | non-local typed disposition | no quiescent local-capacity loop |

Decide and document:

- the exact closed set of active initial-wave states;
- whether a helper/predicate is shared by exact and bounded routes;
- whether v0.7 already expresses every corrected branch;
- refusal precedence when stale, provider, ambiguity, and wrong-authority evidence
  coexist;
- which command consumes local-work progress and when;
- replay identities and required publication evidence; and
- legacy workspace posture.

Add schema/semantic fixtures and mutation tests only if the public shape changes.
Otherwise explicitly record that the patch tightens invalid routing in place.

Gate: SBE and API agree that no consumer must infer initial versus ordinary
authority from private state or command failure text.

**Voof-paws 2:** API contract review before runtime correction.

## Slice 2 — Selector and initial-wave guard correction

Implement the smallest route-aware correction under the native writer boundary.
Likely seams include:

- one canonical predicate for an active initial-wave admission rather than
  `isinstance(initial_authoring_wave, dict)`;
- command selection that prioritizes provider custody/reconciliation;
- scoping aggregate-grant refusal to actual initial-wave member documents/state;
- ensuring completed wave lineage proceeds through ordinary v2/local-work paths;
  and
- explicit typed refusal for incompatible mixed evidence.

Do not weaken the existing initial-wave fence. A generic resume against
`AWAITING_SPEND_AUTHORIZATION`, `AUTHORIZED`, or `SUBMITTING` initial-wave work must
still refuse unless it is the exact constrained continuation or a strictly proven
retrieval-only reconciliation path.

Tests:

- exact active initial wave remains fenced;
- exact completed initial wave no longer captures ordinary retry authority;
- ordinary authorization documents cannot authorize initial-wave members;
- initial-wave aggregate documents cannot authorize ordinary actions;
- stale observation, binding mismatch, provider evidence, and ambiguity precedence;
- refusal is nonmutating and publishes no misleading native result; and
- event-sink failure cannot affect native behavior.

Gate: targeted selector/authority suites pass with no provider calls.

## Slice 3 — Real post-fan-in continuation and reconciliation path

Drive the corrected exact runtime through the actual supported commands:

1. known retry provider ID and not-due release;
2. due reconciliation with scripted completed result;
3. durable provider-result evidence;
4. one advertised local fan-in/retry-evaluation operation;
5. ordinary resume consuming that exact operation;
6. next ordinary v2 authority request;
7. constrained grant/dispatch or passive no-grant result as applicable; and
8. replay with no duplicate create/retrieve or operation consumption.

Require each advertised `ordinary_resume` to produce a new checkpoint basis and
cumulative consumed-operation evidence or a different typed disposition. Prove the
previous operation cannot reappear after one or several successors.

Exercise bounded interactive through the same matrix. If it shares the defect,
apply the same route-parameterized helper. If its existing path is already safe,
lock that behavior with parity/non-regression tests rather than changing it.

Gate:

- exact incident-shaped path reaches provider reconciliation, fan-in, and fresh
  ordinary authority without initial-wave refusal;
- bounded route has an explicit supported/refused result;
- all provider identities and reported evidence remain monotonic; and
- no seventh initial-wave create or duplicate retry create occurs.

**Voof-paws 3:** runtime/failure-boundary review before composed fairness work.

## Slice 4 — Adversarial regression and two-run/one-slot handoff

Promote the minimized incident to the adversarial lifecycle corpus following the
[Adversarial Lifecycle Simulation Playbook](../../../../post_extraction_authoring/Adversarial%20Lifecycle%20Simulation%20Playbook.md).

Add:

- a named deterministic historical incident trace;
- corrected production-shaped successor trace;
- semantic stutter/cycle detection despite revision churn;
- command/guard incompatibility as contradiction or typed refusal where relevant;
- exact fixture and adapter-result digests; and
- privacy sentinel coverage.

Publish a sanitized SBE fixture/public qualification component for API. The API
companion must drive it through real lifecycle translation, persistence, lease,
capacity, and scheduler services with two runs and one slot. Prove:

- the non-executable/awaiting run does not retain capacity indefinitely;
- another eligible run progresses;
- releasing capacity does not release provider custody or spend authority;
- stale worker replay cannot duplicate closeout/release or disturb the successor;
  and
- logs are diagnostic only.

Gate: closed SBE and joint receipts bind the exact incident and corrected path.

**Voof-paws 4:** API fixture-by-fixture and fairness review.

## Slice 5 — Installed-wheel and compatibility qualification

From one committed source identity:

- run focused selector, authority, lifecycle, post-fan-in, reconciliation,
  adversarial, and privacy suites;
- run the broad relevant source suite;
- build twice with fixed `SOURCE_DATE_EPOCH` and require byte identity;
- inspect wheel resources, schemas, fixtures, entry points, and `py.typed`;
- install outside the checkout with exact SPC 0.11.1;
- run generic release smoke and installed adversarial qualification;
- run the API joined campaign against that exact candidate; and
- record Windows/Linux status appropriate to the changed runtime path.

All tests are provider-free. Provider/network calls, spend, and retained-QA access
must remain zero.

Gate: API confirms the candidate supplies the evidence needed for a separately
authorized retained-cohort recovery assessment.

## Slice 6 — Consumer handoff, recovery posture, and release decision

Publish:

- exact command/authority routing matrix;
- API invocation and capacity mapping;
- replay/ambiguity/refusal behavior;
- supported route/mechanism table;
- installed fixture and receipt identities;
- compatibility and known limitations; and
- a retained-cohort assessment that states whether Strudel/Princess can be resumed
  through supported commands after deployment.

Do not mutate the retained cohort during release preparation. Any recovery requires
separate owner/API authorization, a pinned released wheel and deployed compatibility
profile, current snapshot validation, exact provider identity reconciliation, and
proof that no new provider create is permitted.

After final owner/API review, use a fresh immutable patch version. Rebuild from the
committed artifact source, rerun installed qualification, tag the release-lock
commit, publish the exact wheel/checksum, download and verify assets, and record
post-publication evidence without moving the tag.

## Test strategy summary

### Deterministic unit/contract

- active/completed initial-wave predicate matrix;
- ordinary versus initial authority document joins;
- provider custody precedence;
- local-work operation construction and consumption;
- schema/semantic mutations if public artifacts change;
- exact replay and stale observation.

### Failure injection

- before/after provider-result persistence;
- before/after local fan-in native mutation;
- before/after local-work consumption checkpoint;
- before/after next ordinary authority request publication;
- concurrent/generic resume during constrained state;
- event/log sink failure; and
- snapshot/result publication interruption.

### Route/mechanism

- exact interactive: required incident path;
- bounded interactive: parity assessment and applicable regression;
- exact/bounded Batch: explicit non-regression or fail-closed deferral; no topology
  expansion.

### Composed API

- real translator and queue/capacity persistence;
- two runs, one slot, bounded progress witness;
- retained provider/spend authority across capacity release;
- stale/lost lease fencing; and
- deterministic replay receipt.

### Release

- source-focused and broad suites;
- deterministic dual build;
- installed Windows/Linux smoke appropriate to the path;
- installed adversarial/joint qualification;
- zero provider/network/spend/retained-QA totals; and
- independent published-asset digest verification.

## Review pauses

1. Before Slice 0: owner approval of this plan.
2. After Slice 0: causal reproduction review.
3. After Slice 1: contract/authority matrix freeze.
4. After Slice 3: runtime and failure-boundary review.
5. After Slice 4: API joint/fairness review.
6. After Slice 5: installed candidate review.
7. Before version bump/tag/publication.
8. Before any retained-cohort recovery or paid QA.

## Acceptance

- The incident-shaped public path no longer reaches an incompatible initial-wave
  guard.
- Provider-bound retry work remains reconciliation-only and duplicate-create safe.
- Completed provider evidence fans in exactly once.
- Next ordinary authority is fresh, exact, and v2-bound.
- Active initial-wave admission retains its existing aggregate-grant fence.
- No `ordinary_resume` can stutter/quiesce indefinitely while retaining capacity.
- Another eligible run progresses under the one-slot joint scenario.
- Existing native/API authority boundaries remain intact.
- Installed qualification is provider-free and reproducible.
- Retained QA remains untouched until separately authorized.
