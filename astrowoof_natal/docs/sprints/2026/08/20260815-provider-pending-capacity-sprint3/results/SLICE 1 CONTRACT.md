# Slice 1: Scheduling and Provider-Custody Contract

## Status

API-approved and schema-complete; pending Kevin's Slice 1 gate review. The accepted
names, values, and closed vocabularies are now strict packaged contracts with
sanitized fixtures. No runtime polling behavior or timing persistence has changed;
those remain Slice 2 work.

## Contract composition

The contract introduces:

1. `astrowoof.authoring_lifecycle_inspection.v0.2`, which preserves every v0.1
   field and adds required `execution_capacity` and `provider_custody` projections;
2. `astrowoof.provider_reconciliation_cycle_result.v0.1`, returned by a future
   bounded provider reconciliation command/Python operation; and
3. `astrowoof.provider_reconciliation_policy.v0.1`, a frozen native per-run policy
   controlling lower-bound due advice and the complete cycle/transport wall-clock
   limit.

Existing inspection v0.1 remains a readable historical contract. Consumers that
require capacity-release evidence must require v0.2; absence of v0.2 is never
interpreted as releasable. Existing terminal, quiescence, local-dependency, action-
inventory, closeout, denial, and event meanings do not change.

## Inspection v0.2 proposal

```json
{
  "schema_version": "astrowoof.authoring_lifecycle_inspection.v0.2",
  "run_id": "native-run-id",
  "observation": {},
  "terminal": {},
  "quiescence": {},
  "local_dependencies": [],
  "action_inventory": {},
  "review_reasons": [],
  "execution_capacity": {
    "disposition": "release_until_due",
    "local_work_ready_now": false,
    "checkpoint_safe_for_worker_release": true,
    "resume_not_before": "2026-08-15T23:00:00Z",
    "reason_code": "known_provider_work_pending",
    "policy_version": "astrowoof.provider_reconciliation_policy.v0.1"
  },
  "provider_custody": {
    "state": "known_operations_pending",
    "provider_action_count": 3,
    "reservation_retention_action_count": 3,
    "action_ids": ["paid_..."],
    "next_due_action_ids": ["paid_..."],
    "earliest_resume_not_before": "2026-08-15T23:00:00Z",
    "actions": [
      {
        "action_id": "paid_...",
        "stage": "authoring_initial",
        "provider_operation_id": "resp_...",
        "custody_classification": "retain_consumer_authority",
        "resume_not_before": "2026-08-15T23:00:00Z",
        "reason_code": "known_provider_operation_pending"
      }
    ]
  }
}
```

Provider payloads, prompts, complete authorization records, API reservation IDs,
reservation amounts, account exposure, and billing detail are prohibited from this
projection.

## Closed vocabularies

### Execution-capacity disposition

| Value | Meaning | API local-capacity implication |
|---|---|---|
| `continue_local_cycle` | Native local work is runnable now | Retain/claim a short execution slot |
| `release_until_due` | Only known durable provider work blocks progress | Release local slot; retain provider custody and API authority |
| `await_external_authority` | Prepared native work awaits API authorization | Release local slot; API decides whether/when to authorize |
| `retain_for_review` | Ambiguity, invalid integrity evidence, or provider conflict | Retain workspace and review; do not schedule ordinary polling |
| `terminal` | No further native execution is legal | Release capacity subject to API terminal/cleanup policy |
| `unsupported_retain_capacity` | Route/stage cannot safely use bounded mode | Do not infer release; use supported blocking path or retain |

There is no generic `release_no_schedule` in v0.1. Provider-pending release must
carry a non-null lower bound. Authorization waiting is event/authority driven and
uses `await_external_authority`, not a fabricated provider due time.

### Execution reason code

- `local_work_ready`;
- `known_provider_work_pending`;
- `provider_reconciliation_not_due`;
- `spend_authorization_required`;
- `terminal_native_outcome`;
- `snapshot_invalid`;
- `writer_or_lease_not_exclusive`;
- `provider_submission_ambiguous`;
- `provider_identity_conflict`;
- `native_review_required`; and
- `route_or_stage_not_supported`.

### Provider custody state

- `none`;
- `known_operations_pending`;
- `completed_evidence_pending_local_work`;
- `ambiguous_or_conflicting`;
- `unsupported`; and
- `terminal_no_custody`.

### Action custody classification

- `retain_consumer_authority`: known provider-bound work remains unresolved;
- `completed_provider_evidence`: provider work is durably complete and awaits or
  has entered local processing;
- `no_provider_custody`: no known unresolved provider operation exists;
- `ambiguous_review`: submission/provider identity is uncertain; and
- `unsupported`: no capacity inference is allowed for this action/route.

Every custody action projection includes immutable `stage` copied from its paid
action binding. The action ID remains the authority-bearing key; stage is bounded
operator/API mapping context and cannot be used alone to mutate authority.

The phrase `retain_consumer_authority` is deliberate. It does not state that an API
reservation exists or quantify dollar exposure. It tells the API that releasing
its matching financial/custody authority would be unsafe based on native evidence.

## Checkpoint release safety

`checkpoint_safe_for_worker_release` is true only when all are true:

- the complete workspace snapshot validates at the stable logical absolute path;
- the inspecting consumer declares or establishes native exclusive access;
- no writer race is possible;
- the persisted checkpoint kind is one approved for detach/resume;
- all local authoring futures and state writers have unwound; and
- no ambiguity/review condition requires retaining the current worker for a
  bounded native repair transition.

Snapshot validity alone is necessary but not sufficient. A new persisted
checkpoint classification in Slice 2 will distinguish a coordinator-published
detach boundary from an arbitrary valid intermediate snapshot.

The API may release local capacity only when both:

```text
execution_capacity.disposition in {release_until_due, await_external_authority,
                                   terminal}
checkpoint_safe_for_worker_release == true
```

For `terminal`, cleanup still requires existing closeout and API policy; this field
does not authorize deletion or publication.

## Reconciliation timing policy

Leading frozen defaults for review:

```json
{
  "schema_version": "astrowoof.provider_reconciliation_policy.v0.1",
  "initial_delay_seconds": 15,
  "backoff_multiplier": 2,
  "maximum_delay_seconds": 300,
  "maximum_cycle_wall_clock_seconds": 20,
  "provider_retrieval_timeout_seconds": 15,
  "maximum_due_actions_per_cycle": 4,
  "maximum_parallel_retrievals": 4,
  "jitter": "none"
}
```

These values are API-reviewed defaults. The important invariants are:

- the policy/version is frozen in the native run;
- `resume_not_before` is an RFC 3339 UTC instant and durable lower-bound advice;
- API may resume later;
- an earlier bounded resume returns typed `not_due` without a provider call or
  state revision advance;
- the provider HTTP timeout is less than the complete cycle wall-clock ceiling;
- the cycle checks its wall-clock budget before starting another retrieval;
- no more than four due actions enter one cycle, matching the four retrieval
  workers so the cycle requires at most one 15-second retrieval wave;
- additional already-due actions are persisted as
  `deferred_by_cycle_limit`, retain their provider-attempt count, and receive a
  non-immediate next cycle eligibility of `cycle_finished_at + 15 seconds`;
- no random process-local jitter exists; and
- run-level due time is the minimum due time among relevant known operations.

Provider rate-limit or transport evidence may increase the next delay within the
frozen maximum. It cannot erase provider identity or turn retrieval into submission.

## Bounded reconciliation cycle result

Proposed schema identity:
`astrowoof.provider_reconciliation_cycle_result.v0.1`.

Required top-level fields:

```json
{
  "schema_version": "astrowoof.provider_reconciliation_cycle_result.v0.1",
  "run_id": "native-run-id",
  "outcome": "detached_provider_pending",
  "decision_basis": {},
  "cycle": {
    "started_at": "...",
    "finished_at": "...",
    "wall_clock_limit_seconds": 20,
    "provider_retrieval_count": 3,
    "retrieved_action_ids": ["paid_..."],
    "completed_action_ids": [],
    "still_pending_action_ids": ["paid_..."],
    "transport_warning_action_ids": []
  },
  "inspection": {},
  "result_checkpoint": {}
}
```

Closed outcomes:

| Outcome | Meaning |
|---|---|
| `not_due` | Called before durable lower bound; no provider retrieval or mutation |
| `detached_provider_pending` | Bounded retrieval occurred; known work remains; releasable checkpoint published |
| `progressed_local` | Provider completion unblocked local work and native execution advanced |
| `awaiting_external_authority` | Next native boundary requires API authorization |
| `terminal` | Native run reached terminal/delivery outcome |
| `review_required` | Ambiguity, conflict, invalid snapshot, or provider failure requires review |
| `unsupported` | Route/stage is explicitly not supported by bounded mode |

`not_due` has no new result checkpoint because it does not mutate state. It returns
the current valid observation and inspection. Every mutating outcome returns one
coherent post-cycle checkpoint. `progressed_local` may still end with
`release_until_due` if some provider actions remain after all currently runnable
local work is exhausted; the returned inspection, not the outcome name alone,
controls capacity release.

## State/action decision table

| Native evidence | Capacity disposition | Custody | Due time | Poll? |
|---|---|---|---|---|
| Terminal/delivery, valid checkpoint | `terminal` | terminal/known custody as exact evidence requires | null | No |
| Delivery publishable plus nonblocking critic/candidate custody pending | `release_until_due` | known pending | non-null future | Bounded retrieval; delivery remains publishable |
| Snapshot invalid or writer race | `retain_for_review` | exact or ambiguous | null | No |
| `SUBMITTING` without durable provider ID | `retain_for_review` | ambiguous | null | No |
| Provider-ID conflict | `retain_for_review` | ambiguous | null | No |
| `PREPARED`, authorization absent | `await_external_authority` | none | null | No |
| `AUTHORIZED`, provider absent, local submit legal | `continue_local_cycle` | none | null | Submission may occur only in ordinary authorized execution, never poll-only fallback |
| Known provider ID, not due, no local work | `release_until_due` | known pending | non-null future | No; early result `not_due` |
| Known provider ID, due, no local work | `continue_local_cycle` during claim | known pending | due/current | Bounded retrieval |
| Mixed known pending plus independent local work | `continue_local_cycle` | known pending | earliest provider due | Run local work, then bounded retrieval only if due/budget remains |
| Provider completed, local assembly/QA ready | `continue_local_cycle` | completed evidence | null/other action minimum | No new submission |
| Supported exact stage still pending after bounded cycle | `release_until_due` | known pending | next non-null due | Detach |
| More than four actions due | Handle first four; remaining actions become durably `deferred_by_cycle_limit` | known pending | cycle finish + 15s for deferred members | No tight follow-up spin |
| Secondary route explicitly deferred | `unsupported_retain_capacity` | unsupported/exact evidence | null | No bounded inference |

## Exact interactive release requirement

The release path must support the same contract across:

- initial authoring;
- creative retry;
- polish when enabled;
- qualitative critic when enabled; and
- qualitative candidate generation when enabled.

A stage cannot claim parity solely because it uses an OpenAI client. It must prove
durable provider identity, bounded retrieval, local fan-in, snapshot publication,
fresh-worker resume, and no resubmission.

Batch and bounded-Natal are secondary classifications for this sprint. Each must
be marked either:

- `parity_supported`, with the same public capacity/custody guarantees; or
- `fail_closed_deferred`, producing `unsupported_retain_capacity` and never
  advertising `release_until_due`.

## Events

Leading proposal: add one non-authoritative `provider.reconciliation_cycle`
observation requiring only:

- `outcome`;
- `provider_retrieval_count`;
- `completed_action_count`;
- `pending_action_count`; and
- `reason_code`.

No provider operation IDs, bindings, prompts, reservation references, due action
IDs, or timestamps beyond the standard event envelope are required in event data.
The event may be dropped, duplicated, delayed, or reordered. Capacity decisions use
the persisted v0.2 inspection/result only.

## Compatibility

- Existing lifecycle inspection v0.1 remains readable and unchanged.
- Existing blocking closure commands remain supported.
- The bounded cycle is opt-in through a new explicit CLI/Python surface.
- Legacy 0.4.2 workspaces lack frozen reconciliation timing evidence and fail
  closed for capacity release unless Slice 2 defines a narrow deterministic
  migration. No implicit process defaults may authorize release.
- Existing action, spend, snapshot, denial, closeout, delivery, and event contracts
  retain their authority.

## API ownership and sequence

1. API restores the exact workspace and holds its fenced native lease.
2. API obtains inspection v0.2 and persists its mapped API state.
3. API releases local capacity only from an allowed disposition plus
   `checkpoint_safe_for_worker_release=true`.
4. API retains every separately owned reservation/custody record corresponding to
   SBE `retain_consumer_authority` actions.
5. API schedules at or after `resume_not_before`; one run gets one delayed task.
6. A fresh worker restores the exact workspace, claims short capacity, and invokes
   the bounded cycle.
7. API ingests the typed result and new inspection, then releases, retains, or
   closes capacity according to its own transaction and product policy.
8. HTTP status reads API-owned persisted state only. Events/logs are diagnostics.

## Questions requiring API review

1. Are the six capacity dispositions sufficient for API allocation mapping?
2. Is `retain_consumer_authority` the right non-financial wording, and does the API
   need action IDs only or also stage/route in the custody projection?
3. Confirmed: 15-second initial delay, 300-second maximum delay, 20-second cycle,
   15-second retrieval timeout, 4-action cycle bound, and 4 retrieval workers.
4. Should `not_due` be strictly nonmutating and omit a result checkpoint as
   proposed, or should it write an audit checkpoint despite performing no poll?
5. For mixed local/provider work, does the API agree SBE should exhaust immediately
   runnable local work before detaching?
6. Is requiring inspection v0.2 for capacity release acceptable, with v0.1 always
   treated as retain/unknown?
7. Does the API need a distinct disposition for external authorization waiting, or
   is `await_external_authority` sufficient?
8. Is the secondary-route rule acceptable: exact interactive all-stage support is
   mandatory; Batch/bounded-Natal must be explicit parity or fail-closed deferred?

## API review disposition

The API agent conditionally approved the proposal and supplied the following
binding clarifications, all incorporated above:

- use one four-action/four-worker retrieval wave within the 20-second cycle;
- defer excess due actions durably by at least 15 seconds without incrementing
  their provider-attempt count;
- include immutable `stage` in custody action projections;
- freeze backoff at `15 -> 30 -> 60 -> 120 -> 240 -> 300` seconds;
- keep `not_due` strictly nonmutating with no checkpoint;
- exhaust runnable local work before detach;
- require v0.2 for capacity release and treat v0.1 as retain/unknown;
- retain `await_external_authority` as the authorization disposition;
- require exact-interactive all-stage parity and explicit secondary-route parity or
  fail-closed classification; and
- allow reader delivery to remain publishable while a nonblocking critic/candidate
  retains provider custody and consumer authority through bounded reconciliation.

## Gate recommendation

The contract is approved for strict schema/fixture implementation. Runtime polling
and timing persistence remain prohibited until the completed Slice 1 resources are
reviewed and committed.
