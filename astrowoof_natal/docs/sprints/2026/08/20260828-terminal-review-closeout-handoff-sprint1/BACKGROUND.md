# Terminal review-required closeout handoff

## Status

Planning-only incident record. No implementation, provider work, retained-run
mutation, deployment, or release is authorized by this document.

## Incident

The fresh QA cohort created on 2026-08-28 reached normal initial fan-out,
provider-pending release, and post-fan-in retry handling, then both runs were
marked failed by the SBE worker with `native.review.requires_review`.

The specific review-required editorial disposition may be valid. The broken
behavior is the terminal handoff: SBE did not publish an ingestible terminal
native result before reporting the job failure. The API therefore recorded a
non-retryable worker failure while retaining provider and spend custody that it
could not safely infer away.

## Cohort identities

| Pup | API run ID | Native run ID |
| --- | --- | --- |
| Pippin von Waffle | `fbe8ada6-511d-469f-a9b6-31fe15835138` | `8fcce2334d4e717595cafe5af18bb6ee5d097270da362a6783a5fab2f5a8bb79` |
| Duchess Crumpet | `40783a32-e326-4605-8503-de8838152fc0` | `d436f2a008656d16bb8f1efbdb11342278ed808ad88acba3fdafef087d230268` |

All timestamps below are UTC. The worker was release `0.4.27` on Render QA
service `srv-da12sktbedkc73btpu00`.

## Authoritative API/PostgreSQL evidence

Both `generation_runs` and their SBE authoring jobs are `failed`, with the
final execution attempts carrying `failure_reason_code`
`native.review.requires_review`:

- Pippin attempt 11 failed at `06:20:03.339568Z`.
- Duchess attempt 12 failed at `06:24:28.914022Z`.

For each run, the ledger nevertheless contains:

1. six fully reported initial actions;
2. one reported creative retry;
3. one `provider_created` creative retry with a durable OpenAI response ID and
   only an `identity_recorded` provider observation; and
4. one later `authorized` creative retry with no provider operation.

The two `provider_created` actions retain active reservations of USD
`1.602240` (Pippin) and USD `1.602230` (Duchess). The two unused authorized
actions retain active reservations of USD `1.602713` and USD `1.602550`.
Thus the failed cohort retains approximately USD `6.409733` of active global
reservation. The API cannot simply release the provider-created entries: an
external request was submitted and may have completed, but its result has not
been reconciled into the authoritative ledger.

No terminal native-execution receipt exists for either run. The final retained
receipts are `provider_reconciliation` / `provider_pending`, not a terminal
`review_required` result.

## Non-authoritative SBE trace evidence

The trace establishes the missing handoff boundary, not a provider wait:

- Pippin at `06:19:06Z` and Duchess at `06:23:30Z` selected
  `ordinary_resume` with one local operation.
- Both subsequently reported `local_continuation_required=true` and
  `provider_local_dependency_count=0`, then deferred quiescently.
- At `06:20:03Z` / `06:24:28Z`, respectively, each changed readiness to
  `local_continuation_required=false`, still with provider dependency count
  zero, and emitted `worker.job.failed` with
  `reason_code=native.review.requires_review`.
- There is no corresponding `native_publication_start`,
  `native.result_published`, or `native_publication_complete` event for those
  terminal transitions. The prior publication for each run still announced
  `outcome=provider_pending`.

The current closure main path appears intended to publish a native result before
raising `SystemExit(2)` for review-required statuses. The observed trace says
that intention is not realized by this execution route. This sprint must find
the exact route and make the public terminal-result publication and the worker
failure classification agree.

## Required contract outcome

For a terminal `review_required` authoring result:

1. SBE must first produce one exact, public, snapshot-bound terminal execution
   result/receipt that the API can ingest.
2. The result must distinguish completed/reported, provider-submitted-but-not-
   yet-reconciled, and never-submitted authorized actions.
3. The API must be able to close or refuse only the authority proved unused,
   while retaining submitted provider custody for reconciliation according to a
   typed public disposition.
4. Only after publication may the worker expose its nonzero terminal process
   outcome. A bare worker exit must never be the only terminal signal.
5. Replays must be idempotent and cannot create a second provider request,
   second terminal transition, or cross-run resource effect.

## Non-goals

- Do not decide whether Pippin's or Duchess's editorial result deserved review;
  that is the separate retry/review investigation.
- Do not invent an API-only release of provider-created authority.
- Do not recover, terminalize, or otherwise mutate these retained runs in this
  planning sprint.
