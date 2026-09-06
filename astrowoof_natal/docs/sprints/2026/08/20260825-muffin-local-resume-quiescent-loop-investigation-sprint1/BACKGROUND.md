# Background — Muffin Local-Resume Quiescent-Loop Investigation

## Purpose

A fresh, clean-QA qualification cohort launched on 2026-08-26 exposed a
post-fan-in execution loop in the Muffin run. This document preserves the
evidence and the question to investigate. It does not authorize a recovery,
provider request, retained-run mutation, deployment, or release.

The issue must be treated as a general lifecycle/contract problem, not as a
Muffin-specific exception.

## Cohort and runtime context

- Environment: AstroWoof QA, reset before this cohort.
- SBE release: `0.4.25`.
- Expected profile: `astrowoof.qa.sbe0425-local-work-v07.v2`.
- Muffin reading: `d29d397c-0e47-4df1-8b53-2ae6afaffc89`.
- Muffin run: `a183217c-63e2-4cdb-bd5c-960ae03034b1`.
- Biscotti companion run: `7051f5cd-18a4-4169-bf67-62447cc7a341`.
- Authorized cohort ceilings: USD 50 per run, USD 100 cohort, USD 150
  rolling 24-hour, USD 49 per active stage, and USD 0 candidate.

## What authoritative API/PostgreSQL evidence establishes

For Muffin:

1. Six `initial` actions reached `reported` state.
2. One `creative_retry` action reached `provider_created` at
   `2026-08-26T04:24:32.433494Z`.
3. A second `creative_retry` action was `authorized` at
   `2026-08-26T04:26:41.668599Z`.
4. No reconciled cost was recorded for those actions at the latest observation.
5. The run remained `running`; no terminal result or final reconciliation was
   recorded.

Those records establish retained provider/authorization lineage. They do not
by themselves say which native continuation SBE selected, whether a provider
result was still due, or what local work was supposed to occur.

## What SBE trace evidence establishes

SBE trace logs show the initial fan-out, external-authority wait, provider
identity recording, and initial fan-in. They then show an apparent repeated
local quiescence loop.

At least the following cycles occurred:

| UTC time | Checkpoint generation | Selected work/result |
| --- | ---: | --- |
| 04:31:21 | 16 | `local_resume` -> `native.quiescent` -> deferred |
| 04:32:20 | 17 | `local_resume` -> `native.quiescent` -> deferred |
| 04:33:19 | 18 | `local_resume` -> `native.quiescent` -> deferred |
| 04:34:19 | 19 | `local_resume` -> `native.quiescent` -> deferred |
| 04:35:18 | 20 | `local_resume` -> `native.quiescent` -> deferred |
| 04:36:18 | 21 | `local_resume` -> `native.quiescent` -> deferred |

Each trace cycle reported:

```text
local_continuation_required=true
provider_local_dependency_count=0
lease released after native.quiescent
```

The worker subsequently reclaimed the run and repeated the same pattern.
Consequently, this is not evidence of a currently held lease or exhausted
capacity. It is evidence of a scheduler-visible no-progress loop.

## The apparent contradiction requiring contract-level explanation

At observation time, the API action ledger still contained one
`creative_retry` `provider_created` action and one `creative_retry`
`authorized` action, while the SBE local-resume trace reported zero
provider-local dependencies.

That may be a legitimate distinction in timing or vocabulary, but it must be
made explicit. A public consumer must be able to distinguish at least:

1. retained provider work that is due for retrieval/reconciliation;
2. external authority that is ready and requires a create-capable continuation;
3. concrete local work that can be safely performed by `ordinary_resume`; and
4. a quiescent state with no actionable work, which must not self-schedule
   indefinitely.

State-name parsing is not an adequate substitute for this evidence.

## Biscotti contrast: provider reconciliation ready, but capacity-starved

The companion Biscotti run provides a distinct, now-established contrast:

- Run: `7051f5cd-18a4-4169-bf67-62447cc7a341`.
- Six initial actions reached `reported`.
- One `creative_retry` reached `provider_created` at
  `2026-08-26T04:26:14.882935Z`.
- Its last SBE cycle selected `provider_reconciliation`, produced a quiescent
  `release_until_due` result, and explicitly reported
  `local_continuation_required=false` and
  `provider_local_dependency_count=1`.
- The API correctly placed its `sbe-authoring` job into `retry_wait`, with
  `available_at=2026-08-26T04:26:38Z`, `attempt_count=8`, and
  `max_attempts=64`.

At `2026-08-26T04:44:01Z`, that retry was overdue but had not been reclaimed.
The capacity records explain why:

```text
Muffin   slot 1  active    allocated 04:18:41Z, no release
Biscotti slot 1  released  allocated 04:20:19Z, released 04:26:15Z
```

Muffin's repeated short job leases are released, but its long-lived capacity
allocation remains active. With a one-slot QA fleet, Biscotti cannot re-enter
the provider-reconciliation branch even though its next retry is eligible.

This is therefore not evidence that Biscotti has selected the same bad local
loop. It establishes a coupled scheduler/capacity concern: a quiescent
local-resume loop must not retain capacity indefinitely and starve an eligible
provider-reconciliation continuation in another run.

## Investigation questions

1. Under what exact native condition did SBE select `local_resume` after the
   first creative retry had a provider identity and a second retry had been
   authorized?
2. What does `provider_local_dependency_count=0` exclude, and why can that be
   true while the public/API ledger still shows `provider_created` and
   `authorized` creative-retry actions?
3. What concrete local-work inventory, if any, made
   `local_continuation_required=true` true in every quiescent cycle?
4. Is the loop caused by an unrepresented post-fan-in retry matrix case, a
   selector/fence bug, a reconciliation-time eligibility defect, or an
   API/SBE vocabulary mismatch?
5. Which public lifecycle receipt/inspection fields must change so that API
   scheduling can reject a no-progress `ordinary_resume` disposition before
   repeatedly enqueuing it?
6. What provider-free qualification fixture proves the corrected behavior,
   including both genuinely actionable local work and the no-action terminal
   or typed-review alternative?
7. What exact release rule ensures a quiescent local-resume loop cannot retain
   a capacity allocation and starve a due provider-reconciliation job?

## Desired outcome

Produce a closed, provider-free contract and qualification path in which a
local-resume disposition is externally actionable only when it carries a
non-empty, validated local-work inventory. A no-action state must instead
yield a typed terminal, review/refusal, reconciliation, or external-authority
disposition as appropriate—never an unbounded `local_resume` quiescent loop.

## Non-goals

- Do not make a Muffin-specific recovery path.
- Do not infer provider completion from dashboard appearance or log timing.
- Do not mutate Muffin, Biscotti, provider state, custody, leases, or spend as
  part of this investigation.
- Do not weaken the single-writer/native-authority boundary to break the loop.
