# Slice 0 — Frozen trace timelines and source map

Status: complete; causal review gate before retained-workspace access or runtime
implementation.

## Evidence boundary

The source evidence is the unfiltered SBE `0.4.40` worker export at
`C:\tmp\sbe-worker-last-2-hours-puff-20260903.log`. API custody facts come from
the companion Sprint 71 packet. No retained workspace was read, no provider was
called, and no QA state was mutated.

## Pastiche timeline

Native run:
`e9a72ba7695dddddc977da162388396a854a0813139c5475ce0b290d038c4ffb`.

| UTC | Native evidence | Interpretation |
|---|---|---|
| 13:31:00 | Pass 6 attempt 2 acceptance subprocess exits 2; `theme_group_balance` is logged as an advisory; the attempt is rejected and attempt 3 is prepared. | Advisory evidence and rejection coexist. The concise trace does not expose the complete hard-issue list. |
| 13:37:21 | Completed provider result for attempt 3 is joined back to pass 6 as action `paid_87801f2fe550bbd9c953181c`, provider response `resp_0d0295183f24c431006a9976c3a91c87d08eec73a2595edb98`. | Provider custody/adoption succeeds before QA. |
| 13:37:22 | Acceptance subprocess exits 2; `theme_group_coverage` is logged as an advisory; attempt 3 is rejected. | Again suspicious, but the trace alone does not prove the advisory was the sole rejection cause. |
| 13:37:22–23 | Run transitions to `FAILED_REQUIRES_REVIEW`, commits revision 99, and retires the completed v2 intent at revision 100. | No retained provider custody remains. |
| 13:37:28 | Native v0.2 `review_required` result `nres_6615e36edf7aef434be8098f` and receipt `nreceipt_11c2e26c57da95dbd56df66f` are sealed; CLI exits 2. | Terminal review publication is present and invocation-bound. |

### Source map

- `pass_acceptance.py` moves selected theme-group findings into
  `advisory_reasons`, preserves hard findings in `rejection_reasons`, and exits
  0 only when the report's overall status is `accept`.
- `closure.run_pass_acceptance()` logs only `advisory_issue_codes`; it does not
  log `editorial_issue_codes`. It accepts only when both subprocess exit is 0
  and report status is `accept`.
- `closure.author_one_pass()` records `PASS_QA_REJECTED` whenever that combined
  result is false.

Therefore the logs prove an advisory/rejection coincidence, not yet an
advisory-only rejection. The exact acceptance JSON is required to distinguish:

1. a separate legitimate hard finding;
2. inconsistent report status/exit semantics; or
3. a policy translation defect.

## Puff timeline

Native run:
`84a24f8facd330a80ad42c19986ccc0f5fde2287e307d30ccbf6e3f85f3c30be`.

| UTC | Native evidence | Interpretation |
|---|---|---|
| 13:50:08–09 | Creative retry finishes; run reaches `AUTHORING_COMPLETE`; its completed v2 intent is retired at revision 103. | Retry custody is cleanly retired before polish. |
| 13:50:11–16 | Finalization starts from `FINAL_QA_WARN`; polish action `paid_047fd998009e0e133e0a64a1` is prepared; lifecycle publishes one-action external authority. | Polish enters the supported ordinary-v2 path. |
| 13:51:01 | Polish is provider-bound and the run is `WAITING_FOR_RESPONSE` at revision 110. | Durable provider custody exists. |
| 13:52:10–11 | Reconciliation selects the exact polish action and completes response `resp_09fee2f3adfd1124006a997b439bd487d08fd9a9a95bc44799`. | Retrieval succeeds; no create occurs in reconciliation. |
| 13:52:12–15 | Local continuation becomes ready; finalization runs; reconciliation publishes `progressed_local` with snapshot `d5e368…`. | Completed provider evidence has created deterministic local work, but has not yet proved semantic consumption. |
| 13:53:15–17 | Ordinary resume selects local work; revision advances 113→115; sealing is deferred as `stage_consumer_not_reached`; `finalize_subjects` re-enters polish. | The prior polish operation remains advertised while the consumer is attempted. |
| 13:53:17 | The spend boundary catches `AmbiguousProviderSubmission` (“Provider submission outcome requires reconciliation”), advances to revision 117, and retains one waiting polish action. | Re-entry encounters already-provider-bound evidence instead of adopting/closing it. No new provider-create success is shown. |
| 13:53:19–21 | `commit_local_work_progress` refuses `semantic_work_not_consumed`; v0.2 result `nres_dac25445bfa8c6613d0d0ca0`, receipt `nreceipt_d38140389b21ae33e151f1fe`, cause `local_work_progress_contradiction` are sealed. | The terminal review accurately records the contradiction, but custody remains unresolved. |

### Source map

- Exact resume snapshots v0.7 local work before native execution.
- The first checkpoint boundary intentionally defers optional-stage progress
  sealing until the stage consumer can run.
- `finalize_subjects()` is then called inside a second checkpoint boundary.
- After the boundary, `commit_local_work_progress()` requires native truth to
  prove the prior semantic operation was consumed; otherwise it seals the v0.2
  contradiction result.

The safety fence behaves conservatively. The unresolved question is why the
polish consumer re-entered provider-submission ambiguity after completed
reconciliation rather than adopting the exact completed response and consuming
the local operation. The trace cannot expose the complete stored polish attempt,
operation-key, consumed-key, and v2-intent joins.

## Current causal classifications

| Branch | Confirmed | Not yet proven |
|---|---|---|
| Pastiche | Attempts 2 and 3 had theme-group advisories, exited acceptance with 2, and were rejected; terminal result was published. | Whether any hard issue accompanied either advisory and whether the policy translator is defective. |
| Puff | Polish response was durably retrieved; local progress was not consumed; re-entry hit provider-submission ambiguity; v0.2 review retained custody. | The exact stale/missing native join that prevented adoption and whether current source reproduces it provider-free. |

## Gate recommendation

This remains primarily native work, but retained artifacts are now the shortest
route to both exact answers:

- Pastiche: the attempt-2 and attempt-3
  `authoring-pass-acceptance.json` artifacts.
- Puff: the final checkpoint's polish attempt record, v0.7 local-work inventory
  and cumulative consumed keys, live/retired v2 intent, action record, and sealed
  terminal-review join.

Before any R2 access, API should supply exact immutable checkpoint coordinates
and approve bounded read-only access. No provider call, resume, reconciliation,
repair, or mutation is needed.
