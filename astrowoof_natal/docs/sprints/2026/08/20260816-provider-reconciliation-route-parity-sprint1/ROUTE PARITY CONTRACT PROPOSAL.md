# Provider Reconciliation Route Parity Contract Proposal

Date: 2026-08-16  
Status: proposed for Kevin and AstroWoof API review  
Runtime/schema implementation: not started

## Decision summary

1. Publish lifecycle inspection v0.3. It adds strict validated native-route,
   provider-mechanism/round, and consumer-authority evidence instead of asking the
   API to infer route identity from its job record or unvalidated native payloads.
2. Publish a new reconciliation policy v0.2 and cycle-result v0.2. The new result
   adds exact route/mechanism operation summaries and permits a Batch-specific
   provider-I/O bound; v0.1 remains the exact-interactive historical contract.
3. Add one public route-aware reconciliation operation. It validates native route,
   service level, stage, provider kind, snapshot, and timing before selecting an
   adapter. Consumers never inspect `run.json` to select an adapter.
4. Treat one exact Batch round as one SBE paid action and one API authorization.
   The round contains an ordered bounded set of `custom_id` request members; those
   members are not independently reservable actions.
5. Support exact Batch only for initial authoring and creative retry. Exact polish,
   critic, and candidate work remains interactive Responses work even when initial
   authoring used Batch.
6. Support bounded Natal only with interactive Responses, across initial authoring,
   creative retry, polish, critic, and candidate stages.
7. Keep bounded Batch rejected at construction, inspection, dispatch, and CLI.
8. Fail closed for timing-free exact Batch workspaces created by 0.4.3. Do not
   silently invent an identity-recorded timestamp. Existing workspaces may finish
   through the prior blocking/detach command; newly created work receives timing
   when its Batch ID is durably recorded.
9. Accept existing bounded 0.4.3 timing only after the new dispatcher validates the
   real bounded `route_contract`. This corrects the accidental exact-route
   inheritance found in Slice 0.
10. Distinguish provider-retrieval custody from consumer-authority retention. A
    terminal Batch can require no further polling while still requiring the API to
    retain financial authority pending billing reconciliation.
11. Preserve SBE-native action evidence and append-only reconciliation references
    while the API remains sole authority for reservations and financial exposure.

## Route identity

Route support is determined from the complete native identity, not from the shared
run schema alone.

| Public route family | Native identity | Supported provider mechanism |
|---|---|---|
| `exact_natal` | shared run schema with no bounded `route_contract` | `response` interactive or `batch` Batch |
| `bounded_natal` | `route_contract = astrowoof.bounded_natal.authoring_run.v1` and `route = bounded_natal.v1` | `response` interactive only |

Unknown, contradictory, missing-required, or bounded-Batch identities return
`unsupported`; they never reach a provider adapter.

## Lifecycle inspection v0.3

Inspection v0.3 retains v0.2 terminal, quiescence, dependency, inventory,
capacity, checkpoint, and review meanings. It adds strict native route identity
and extends every custody action with provider mechanism and native operation
binding:

```json
{
  "schema_version": "astrowoof.authoring_lifecycle_inspection.v0.3",
  "native_route": {
    "route_family": "exact_natal",
    "route_contract": "astrowoof.semantic_closure_run.v0.9"
  },
  "provider_custody": {
    "actions": [
      {
        "action_id": "paid_0123456789abcdef01234567",
        "route_family": "exact_natal",
        "provider_operation_kind": "batch",
        "provider_operation_id": "batch_abc123",
        "native_operation_ref": "batch-round-001",
        "stage": "authoring_initial",
        "service_level": "batch",
        "custody_classification": "retain_consumer_authority",
        "resume_not_before": "2026-08-16T12:01:00Z",
        "reason_code": "known_provider_operation_pending"
      }
    ]
  }
}
```

Closed `route_family` values are `exact_natal` and `bounded_natal`. Closed provider
operation kinds are `response` and `batch`. `native_operation_ref` is the frozen
action binding route and is validated against the corresponding native attempt or
Batch round. A Batch custody action must bind one exact round whose Batch ID
matches `provider_operation_id`; a Response action must bind one exact route/stage
attempt whose Response ID matches.

Inspection v0.3 also adds `consumer_authority`, separate from provider custody:

```json
{
  "consumer_authority": {
    "state": "retain",
    "action_count": 1,
    "action_ids": ["paid_0123456789abcdef01234567"],
    "actions": [
      {
        "action_id": "paid_0123456789abcdef01234567",
        "retention_reason": "billing_reconciliation_pending",
        "cost_disposition": "provider_usage_unavailable_billing_reconciliation_pending"
      }
    ]
  }
}
```

Closed retention reasons are `provider_operation_pending`,
`provider_output_integrity_review`, `provider_submission_ambiguous`, and
`billing_reconciliation_pending`. Closed states are `none` and `retain`.

The API may release a worker based on execution capacity while retaining every
action in `consumer_authority`. It must not derive financial release from an empty
provider-custody list. Inspection v0.2 remains a historical contract and is
insufficient for new route-parity capacity release.

## Stage and transport matrix

| Route family | Stage | Service level | Provider operation | Support |
|---|---|---|---|---|
| Exact | initial | interactive | Response | Existing |
| Exact | creative retry | interactive | Response | Existing |
| Exact | polish/critic/candidate | interactive | Response | Existing |
| Exact | initial | batch | Batch | New |
| Exact | creative retry | batch | Batch | New |
| Exact | polish/critic/candidate after Batch authoring | interactive | Response | Existing mechanism, route-aware dispatch |
| Bounded | initial/retry/polish/critic/candidate | interactive | Response | New |
| Bounded | any | batch | none | Rejected/deferred |

Frozen profile enablement remains authoritative. A disabled optional stage is not
eligible for provider reconciliation. Optional budget skipping remains distinct
from provider custody and terminal failure.

Bounded delivery is constructed only after its enabled optional stages complete or
skip. Unlike the exact route's supported nonblocking critic case, the current
bounded pipeline has no delivery-complete/pending-critic state. This sprint will
not invent one.

## Batch authority and membership

The SBE paid action binds:

- stage (`authoring_initial` or `creative_retry`);
- route (`batch-round-NNN`);
- model and Batch service level;
- aggregate maximum output tokens and commitment;
- exact request digest and price book; and
- one provider Batch ID after submission.

The matching `batch_service.rounds[]` record binds that action to:

- round number and model;
- exact input JSONL hash and input File ID;
- ordered request members;
- each member's `custom_id`, pass ID, attempt number, prompt hash, and layout;
- Batch ID/status and request counts; and
- terminal output/error File identities and downloaded artifacts.

There is one reservation/custody action ID for the round. `custom_id` members are
ingestion authority and audit evidence, not separate API reservation keys.

Before mutation on terminal completion, SBE must validate the entire Batch object,
declared files, and exact member set. Missing, duplicate, or unknown `custom_id`,
Batch-ID mismatch, changed round membership, malformed JSONL, or missing declared
output produces review with zero member ingestion and no action settlement.

## Submitted versus uploaded Batch state

Only a durable Batch ID creates retrieval-only provider custody.

- `PREPARED`, before paid submission consumption: local work or external spend
  authorization may remain.
- Input File uploaded but no paid action consumed: still local work. Re-upload may
  create an unused duplicate File but cannot duplicate paid generation.
- Paid action `SUBMITTING` with no Batch ID: ambiguous and review-required. SBE
  cannot prove whether Batch creation reached the provider.
- `PROVIDER_ID_RECORDED`/`WAITING` with an exact Batch ID: safe retrieval-only
  custody once timing and snapshot evidence validate.

No deterministic local key is claimed as provider idempotency.

## Timing and bounded work

Policy v0.2 contains mechanism-specific frozen limits:

### Interactive Responses

- delays: `15, 30, 60, 120, 240, 300` seconds, then 300-second cap;
- maximum four due actions in one parallel retrieval wave;
- maximum four parallel GETs;
- 15-second timeout per GET; and
- 20-second provider-retrieval-phase wall-clock bound.

### Exact Batch

- delays: `60, 120, 300, 600, 900, 1800` seconds, then 1800-second cap;
- maximum one due Batch action/round per cycle;
- one 15-second Batch-status GET;
- after terminal completion, at most two declared File downloads in one parallel
  wave, each with a 15-second timeout; and
- 40-second provider-I/O-phase wall-clock bound.

`resume_not_before` is always SBE's durable lower-bound recommendation. The API may
run later. An earlier call is exactly nonmutating: no provider call, event,
checkpoint, attempt increment, or changed advice.

The wall-clock limit covers provider I/O, not deterministic local validation,
artifact writes, QA, or delivery construction. Newly unblocked local work remains
on the claimed worker until it reaches another durable boundary. The cycle result
reports both provider-I/O evidence and whether local work was exhausted before
detach; it does not pretend arbitrary local processing fits inside 20 or 40
seconds.

Excess due interactive actions are deferred by the existing bounded ordering.
Only one exact Batch round can be active/resumable in the current native runner;
if future state presents several due rounds, the dispatcher fails closed rather
than guessing execution order.

## Cycle-result v0.2

Top-level outcomes remain closed and unchanged:

```text
not_due
detached_provider_pending
progressed_local
awaiting_external_authority
terminal
review_required
unsupported
```

The existing decision basis, cycle action-ID sets, post-cycle inspection, optional
local-continuation record, and exact result checkpoint remain. Version v0.2 adds:

```json
{
  "provider_operations": [
    {
      "action_id": "paid_0123456789abcdef01234567",
      "route_family": "exact_natal",
      "provider_operation_kind": "batch",
      "provider_operation_id": "batch_abc123",
      "retrieval_outcome": "completed",
      "cost_disposition": "provider_usage_reported",
      "member_count": 6,
      "ingested_member_count": 6,
      "failed_member_count": 0
    }
  ]
}
```

Closed `retrieval_outcome` values:

```text
not_due
pending
completed
provider_failed
transport_warning
identity_conflict
output_invalid
```

For Responses, all member counts are `null`. For Batch, they are nonnegative
integers and must satisfy `ingested + failed <= member_count`. `completed` does not
mean delivery; it means the known provider operation has terminal evidence and
its accepted members were ingested. The post-cycle inspection remains authority
for capacity, custody, and consumer-authority state. Every operation summary has
one of the closed cost dispositions defined below.

An early `not_due` result includes an empty `provider_operations` array and no
result checkpoint. Refused/unsupported results include a sanitized operation
summary only when native identity is safe to disclose.

## Batch terminal outcomes

| Provider status | Native treatment |
|---|---|
| `in_progress`, `validating`, `finalizing` or other reviewed pending status | Update timing and detach |
| `completed` with exact valid files/membership | Atomically ingest members, settle aggregate action, continue locally |
| `failed`, `expired`, `cancelled` with provider usage | Persist terminal evidence and reported usage/cost basis, end retrieval custody, mark member attempts errored, continue to retry authorization or native review without submitting |
| `failed`, `expired`, `cancelled` without provider usage | Persist terminal evidence with billing-reconciliation-pending disposition, end retrieval custody but retain consumer financial authority, mark member attempts errored, continue without submitting |
| Unknown status | Transport/protocol warning, retain custody, back off |
| Identity conflict or unresolved provider File retrieval | Review-required; retain provider retrieval custody and consumer authority; no partial ingestion |
| Output/member integrity conflict after all terminal provider files are durable | Review-required; provider retrieval custody may end, but retain consumer authority for review; no partial ingestion |

Unavailable usage is never recorded as a real zero estimate. SBE records one of
these closed cost dispositions:

```text
provider_usage_reported
provider_usage_unavailable_billing_reconciliation_pending
no_provider_work_consumed
not_applicable_provider_pending
```

`provider_usage_reported` includes actual provider usage evidence and SBE's
versioned-price-book estimate.
`provider_usage_unavailable_billing_reconciliation_pending` contains no fabricated
usage or amount and keeps the action in `consumer_authority` after retrieval
custody ends. `no_provider_work_consumed` is permitted only when native evidence
proves no provider operation was created or consumed; it is invalid for a terminal
Batch ID. The API reconciles account-wide billing through append-only references
and decides when its financial authority may be released.

Review does not itself imply continuing provider polling. Provider custody remains
only while a known provider operation or declared provider File still requires
retrieval. Once all terminal provider bytes are durable, an output/member integrity
failure retains `consumer_authority` for review without advertising a due provider
operation or forcing a worker into indefinite polling.

## Bounded interactive continuation

The bounded adapter:

1. retrieves only the durable Response ID;
2. persists raw completed Response evidence under the lifecycle reconciliation
   area before parsing;
3. validates response ID, frozen action binding, bounded route/stage, provider-
   minimized payload identity, and expected output shape;
4. invokes bounded orchestration using cached evidence only;
5. deterministically reattaches immutable claim authority and provenance;
6. runs validation and prepares retry/optional-stage authorization when needed;
7. exhausts enabled local work through the next provider/authority/review/terminal
   boundary; and
8. publishes one complete snapshot before advertising release.

Invalid editorial content follows ordinary bounded QA/retry policy. Provider-ID or
immutable-authority conflicts require review. Reconciliation never calls
`execute()` or any POST path.

## Public surface

Proposed Python operation:

```python
reconcile_authoring_provider_cycle(
    run_dir,
    *,
    observed_at,
    provider_adapters,
    event_emitter=None,
)
```

`provider_adapters` supplies configured retrieval/download implementations; the
native dispatcher chooses only after validating route and mechanism. The public
function returns cycle-result v0.2.

Proposed CLI mode on the supported authoring commands:

```text
--provider-reconciliation-cycle --observed-at <UTC instant>
```

The existing exact-only `--bounded-provider-reconciliation` spelling remains a
deprecated compatibility alias for exact interactive work during the patch
series. It does not mean bounded Natal. New API integration should use the neutral
name. Bounded Natal gains the neutral mode on `astrowoof-run-bounded-natal`.

CLI validation rejects new-run inputs, simultaneous spend-authority mutation,
fake providers, unsupported service levels, and bounded Batch. Exit code 3 remains
the general detached/nonterminal signal; consumers distinguish outcomes from the
machine-readable result.

## Events

First execution emits, in order where applicable:

1. sanitized provider retrieval observation;
2. provider evidence committed;
3. local continuation observations already owned by the route;
4. `run.detached`; and
5. `checkpoint.committed`.

Exact replay does not duplicate transition events. Early `not_due` emits none.
Events contain action ID, route family, provider-operation kind, result category,
counts, state revision, and snapshot hash; they omit prompts, output content,
authorization references, API reservations, and provider-visible subject data.
Events are non-authoritative and sink-failure-isolated.

## Compatibility

- Inspection v0.2 remains valid historical evidence but is insufficient for new
  route-parity worker release. New parity emits inspection v0.3.
- Cycle-result v0.1 remains valid for 0.4.3 exact-interactive consumers.
- The new public dispatcher returns v0.2 for all supported mechanisms.
- Exact interactive behavior and timing stay unchanged under policy v0.2.
- Timing-free retained exact Batch runs fail closed and use the legacy command to
  finish; there is no automatic repair.
- Existing bounded 0.4.3 workspaces with valid timing may use the new bounded
  adapter after complete route/binding/snapshot validation.
- Bounded Batch remains a deterministic unsupported error.

## API mapping

The API may release local worker capacity only when:

- post-cycle inspection disposition is `release_until_due`;
- inspection is v0.3 and its native route, per-action provider mechanism, and
  native operation binding validate;
- `checkpoint_safe_for_worker_release` is true;
- the exact checkpoint is durably ingested; and
- API policy independently permits release.

The API retains its reservation/authority for every action listed by
`consumer_authority`. For a Batch round that means one action ID, regardless of
request-member count. Provider custody ending does not release authority when the
cost disposition is billing-reconciliation-pending. The API releases authority
only after SBE evidence plus API-owned transactional/reconciliation policy permits
it.

## Questions for API review

1. Is inspection v0.3 with strict native route, per-action mechanism/operation
   binding, and separate consumer-authority projection sufficient?
2. Is one API reservation per exact Batch round—the actual SBE paid action—with
   member counts retained as audit evidence the expected mapping?
3. Are the proposed Batch delays and 40-second provider-I/O bound acceptable for a
   short worker claim?
4. Is fail-closed legacy handling acceptable for timing-free 0.4.3 Batch runs?
5. Is the neutral CLI spelling plus temporary exact-only alias acceptable?
6. Are `provider_failed` and `output_invalid` sufficiently distinct for API retry,
   review, reservation, and operator mapping?
7. Are the four closed cost dispositions and the rule that unavailable terminal
   usage retains consumer authority sufficient for API financial mapping?

No runtime or packaged schema change should begin until these decisions are
approved.
