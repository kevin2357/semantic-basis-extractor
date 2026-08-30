# Completed retry duplicate-submission investigation

## Status

Investigation-only sprint scaffold. No implementation, retained-run mutation,
provider call, release, or deployment has been authorized by this document.

## Trigger

The fresh QA qualification cohort launched against SBE `0.4.29` completed both
six-member initial authoring waves, then entered ordinary creative-retry work.
The QA SBE worker was deliberately suspended after evidence showed that one
creative-retry authorization was submitted to OpenAI twice.

This is not a request to repair the affected run. The purpose is to establish
the exact native lifecycle failure and a general, contract-safe correction.

## Affected records

| Field | Value |
| --- | --- |
| QA API run | `f84b3524-659a-4b86-83b4-7deb5b7c59a6` |
| Native SBE run | `42407f1f4386eb0fcd387de9feb305a932d6626949dea247750f785bd1851920` |
| Affected native action | `paid_fb28a0c3a7e2a44743d65b8d` |
| Stage | `creative_retry` |
| SBE release | `0.4.29` |
| Environment | QA |

The other cohort run is Scone Ranger, native run
`a587c4fa00f22e57ca9b4177c58783918a2ca991cd16a562769b7a978359f8d0`.
It has one ordinary creative-retry action awaiting normal ingestion and is not
the duplicate-submission case.

## Observed timeline

All times are UTC on 2026-08-30.

1. `04:14:06.617` — SBE prepared `paid_fb28…` as a creative retry.
2. `04:15:05` — API authorized it. SBE consumed it and began provider
   submission.
3. `04:15:07` — SBE recorded provider identity
   `resp_0a83dca212896636006a93ae4a599087d0ae269439ce29c1d8`.
4. `04:17:01` — SBE recorded reported cost; `04:17:01.196` emitted
   `provider.completed` for that identity.
5. `04:17:02.884` — SBE emitted
   `local_work_progress_refused reason=semantic_work_not_consumed` in
   `AUTHORING_COMPLETE`, and the native command exited non-zero.
6. `04:17:22` — the retrying worker again authorized/consumed the exact same
   action and began provider submission.
7. `04:17:23` — SBE recorded a *different* identity for that same action:
   `resp_00ecec3e2a02b87b006a93aed2cb2887d0912ecce39fcef0a4`.
8. `04:19:36` — SBE again recorded completion, then again exited non-zero with
   `semantic_work_not_consumed`.

The API's authoritative `sbe_paid_actions` row for `paid_fb28…` remained
`authorized` with no provider operation ID despite the native events above.
That mismatch is the key cross-boundary fact: neither side may infer a safe
recovery by selecting one provider response or resubmitting again.

## Immediate containment

The owner explicitly authorized pausing **only** `astrowoof-qa-sbe-worker`.
Render reports it as `suspended`. This freezes the existing evidence and
prevents another retry of the same action. Do not resume the worker as part of
this investigation.

## Investigation questions

1. Why does a provider-completed creative retry reach
   `semantic_work_not_consumed` during local work-progress commit?
2. Why is the same authorization eligible for a later native submission after
   SBE has emitted provider identity and completion for it?
3. What durable native record should fence a consumed action before slow
   provider work, and what must be committed after provider completion?
4. Which API/SBE handoff receipt should make the API's authoritative action row
   converge exactly once, including a retry after a post-provider local fault?
5. What typed disposition covers an already-duplicated historical action
   without inventing a one-off recovery path for this QA run?

## Required investigation discipline

Begin with read-only retrieval of the exact retained workspace, native journal,
action ledger, and event output for the listed run. Correlate every conclusion
with the API's authoritative action/authorization records. Do not call OpenAI,
mutate the retained run, list broadly in R2, or modify any workspace artifact.

Any proposed fix must be generalized and exercised with a provider-free
fixture that demonstrates: provider completion, a post-completion local
failure, safe replay/reconciliation, and prevention of a second provider
submission for the same authority.
