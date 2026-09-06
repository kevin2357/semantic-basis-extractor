# Slice 3 — Fairness Contract and Ownership

## Status

Proposed for joint Voof-paws 3 review. No runtime mutation is authorized by this
document.

## Causal classification

The provider-free replay rejects a binary historical-regression explanation.
Sprint 58 did not change healthy provider-pending scheduling, and `8c389b3`
changed only retry-ceiling terminal cleanup.

The reproduced cause is:

> **Legitimate actionable native topology plus unbounded incumbent allocation
> retention under the current API one-slot policy.**

Both native permissions are truthful and distinct:

- due provider retrieval returns
  `continue_local_cycle / provider_reconciliation_due`; and
- completed provider evidence returns
  `continue_local_cycle / local_work_ready`.

API currently maps both to the same behavior: defer the incumbent job while
retaining its run-owned allocation. When the one-slot pool is full, claim
selection restricts eligibility to allocation owners, so the incumbent is
selected again and a ready never-run peer is excluded. This can repeat for an
arbitrary number of successful native commands.

The issue is therefore progressive peer latency/starvation risk, not false
native quiescence and not mishandling of `release_until_due`.

## Selected correction direction

Use an **API-owned cooperative scheduler turn at an existing durable command
boundary**. Do not add or overload an SBE lifecycle disposition.

The safe boundary exists only when all of the following are proven:

1. one claimed SBE command has returned normally;
2. its final result was parsed and validated through the installed public SBE
   consumer path;
3. API has accepted the exact successor checkpoint and persisted checkpoint-
   backed readiness;
4. the successor checkpoint generation is newer than the generation on the
   claim, proving a completed native turn rather than a no-op reinspection;
5. the final capacity disposition is `continue_local_cycle` and API has
   persisted the exact validated lifecycle decision bound to that successor:
   - `SbeLocalWorkLifecycleDecision` with reason `local_work_ready` for
     `ordinary_resume`; or
   - the exact provider-pending lifecycle decision proving due reconciliation
     for `provider_reconciliation_cycle`;
6. no subprocess/native workspace writer remains active;
7. at least one other compatible, ready API run is waiting without an active
   capacity allocation; and
8. the current lease still authorizes the atomic API queue/capacity transition.

The branch name, dependency count, native status, trace message, or elapsed time
cannot substitute for that exact persisted decision.

At that boundary API may atomically in one database transaction:

- defer the incumbent job using the ordinary configured defer;
- release only the incumbent's API execution-capacity allocation; and
- allow normal queue selection to admit the ready peer.

It must retain the incumbent's workspace, provider custody, action/grant/
authorization identities, spend reservation, checkpoint, and native readiness.
Rotation grants no provider or native execution authority by itself.

## First-release applicability

The initial policy should be closed to the two characterized exact-interactive
branches:

| Final branch | Native positive permission | Cooperative rotation eligible? |
|---|---|---|
| `provider_reconciliation_cycle` plus exact persisted due-reconciliation decision | Retrieve the exact ordered due subset | yes, after one durable completed cycle |
| `ordinary_resume` plus exact persisted `local_work_ready` decision | Consume the exact advertised deterministic local operation | yes, after one durable completed cycle |
| `release_until_due` | No work before exact due time | existing release path; not this policy |
| `await_external_authority` | Await a compatible API grant | existing authority-release path |
| terminal/review/ambiguity/unsupported | Typed disposition-specific handling | no |
| initial provider creation before its first durable result | Create under exact authority | no mid-command rotation |
| Batch or uncharacterized bounded/optional route | route-specific | no until separately qualified |

The policy is evaluated after the command, never between members of an SBE
operation or while a provider call may be entered.

## Fairness bound

With a compatible peer already ready, one run may receive at most **one
successful actionable native command turn** before its API allocation rotates.
This is the mechanical `N=1` bound.

The first release must not claim a strict wall-clock `T` bound. API currently
has no demonstrated hard deadline on the duration of every native command, so
one peer turn is bounded structurally but not by elapsed time. Qualification
must measure command duration, queue handoff latency, and provider due-time
lateness separately. A future wall-clock SLA requires a separately proven safe
command timeout/cancellation boundary.

## Due-work protection

- Rotation does not change an incumbent's native due time.
- After the peer completes one command boundary, the same `N=1` rule makes the
  prior incumbent eligible for the next rotation when ready.
- Claim selection must record both waiting runs and why the chosen run won.
- Qualification must prove the incumbent's due work is delayed by no more than
  one intervening successful peer command plus queue handoff overhead.
- The controlled fixture must prove B actually claims before A's ordinary defer
  matures; releasing A's allocation without a peer claim is not fairness proof.
- Provider identities and retrieval attempts remain exact; no create or
  retrieval is replayed because of allocation rotation.

## Fail-closed cases

Do not rotate through this policy when:

- the final SBE result is absent, malformed, contradictory, or from an unknown
  installed contract version;
- no newer accepted checkpoint exists;
- checkpoint/readiness persistence failed;
- the persisted lifecycle decision is absent, stale, wrong-reason,
  checkpoint-mismatched, or inconsistent with the returned branch;
- the command crashed, timed out, lost its lease, or left ambiguity;
- the result is terminal, review-required, unsupported, or authority-waiting;
- no compatible ready peer exists;
- the peer is blocked by its own admission/compatibility contract;
- the branch/route is outside the closed first-release matrix; or
- the API cannot perform defer plus allocation release atomically.

Existing typed handling remains authoritative in every excluded case.

## Ownership

### SBE

- Publish truthful final lifecycle/result evidence.
- Preserve exact checkpoint, action, provider, custody, and local-work joins.
- Keep `release_until_due` reserved for real no-work-before-due semantics.
- Make no change for the first-release policy described here.

### API

- Determine peer readiness and compatibility from durable API state.
- Count completed scheduler turns.
- Atomically defer and release the API execution allocation.
- Preserve all non-capacity custody and authority.
- Record allocation owner, eligible set, selected run, reason, defer boundary,
  prior/successor checkpoint generation, and due-time lateness.

## Rejected alternatives

1. **Return false `release_until_due`:** corrupts native meaning while due or
   local work is immediately actionable.
2. **Drain more reconciliation members per command:** may shorten total cycles
   but increases incumbent monopoly and does not create fairness.
3. **Immediate same-run continuation:** improves incumbent throughput but makes
   peer latency worse.
4. **Increase global slot count:** changes resource topology and can hide rather
   than correct starvation.
5. **New SBE cooperative-yield schema:** unnecessary because API already has a
   durable post-command checkpoint boundary and owns cross-run allocation.
6. **Rotate on elapsed time or trace output:** lacks transition authority and
   risks interrupting a writer or provider call.

## Required API implementation tests

- due-retrieval A rotates to ready B after one durable turn;
- local-work-ready A rotates to ready B after one durable turn;
- `ordinary_resume` with absent, wrong-reason, stale, or checkpoint-mismatched
  local-work decision does not rotate;
- provider reconciliation with absent, stale, or checkpoint-mismatched due-work
  decision does not rotate;
- no peer means A retains/reclaims without needless allocation churn;
- B incompatible/ineligible means no rotation;
- checkpoint generation unchanged means fail closed/no cooperative release;
- crash, lease loss, ambiguity, and malformed result do not rotate;
- terminal and external-authority precedence remain unchanged;
- A and B alternate under repeated actionable cycles without duplicate work;
- provider due-time lateness is one peer command plus handoff overhead;
- B claims before A's configured ordinary defer matures;
- defer and capacity release roll back together on injected failure;
- no concurrent writer and no duplicate create/retrieve/adopt.

## Gate — Voof-paws 3

API and SBE must approve the existing-boundary/API-only ownership decision,
the `N=1` structural bound, the lack of a false wall-clock promise, and the
closed first-release route matrix before API runtime implementation begins.
