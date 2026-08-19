# Provider Reconciliation Route Parity Handoff

Status: consumer contract for the next pinnable SBE release  
Current source baseline: post-0.4.3

## Supported routes

| Native route | Provider mechanism | Reconciliation support |
|---|---|---|
| Exact Natal | Responses | supported, unchanged timing |
| Exact Natal | Batch | supported, one Batch round per cycle |
| Bounded Natal | Responses | supported across every bounded stage |
| Bounded Natal | Batch | rejected; no adapter exists |

The native lifecycle inspection v0.4 is authoritative for route family, provider
mechanism, provider operation ID, and native operation/round binding. Consumers
must not infer these from their product job record.

Inspection v0.4 also publishes the closed `execution_branch`. The API invokes the
run-level command it names; the API does not select the bounded action subset.

## Public Python operation

```python
from pathlib import Path
from astrowoof_natal_authoring import (
    ProviderReconciliationAdapters,
    reconcile_authoring_provider_cycle,
)

result = reconcile_authoring_provider_cycle(
    Path("/stable/workspaces/native-run"),
    observed_at="2026-08-17T18:00:00Z",
    provider_adapters=ProviderReconciliationAdapters(
        exact_interactive_provider=responses_provider,
        exact_batch_provider=responses_provider,
        exact_batch_transport=batch_transport,
        bounded_interactive_provider=bounded_provider,
        max_attempts=3,
        python_executable=Path("/usr/local/bin/python"),
        polish_provider=polish_provider,
        critic_provider=critic_provider,
        qualitative_editor_provider=editor_provider,
    ),
)
```

The dispatcher validates the complete workspace snapshot and native identity before
selecting an adapter. Missing adapters, mixed mechanisms, contradictory identity,
or bounded Batch fail closed before provider activity.

`observed_at` is part of the scheduling decision. Calling before
`resume_not_before` returns nonmutating `not_due` with no checkpoint and no provider
request. The API may schedule later, never earlier.

## CLI operations

Exact Natal, including exact Batch:

```text
astrowoof-semantic-closure \
  --run-dir /stable/workspaces/native-run \
  --resume --provider openai \
  --service-level interactive \
  --provider-reconciliation-cycle \
  --observed-at 2026-08-17T18:00:00Z
```

Bounded Natal:

```text
astrowoof-run-bounded-natal \
  --run-dir /stable/workspaces/native-run \
  --resume --provider openai \
  --service-level interactive \
  --provider-reconciliation-cycle \
  --observed-at 2026-08-17T18:00:00Z
```

The old exact-only `--bounded-provider-reconciliation` spelling remains a
deprecated compatibility alias on `astrowoof-semantic-closure`. Despite its name,
it does not select bounded Natal and supports exact interactive work only. New
integrations must use `--provider-reconciliation-cycle`. For compatibility, the
alias keeps its old implicit current-time decision; the neutral spelling requires
an explicit `--observed-at`.

Both commands reject new-run inputs, fake providers, simultaneous spend
authorization/reconciliation mutations, unsupported service levels, and bounded
Batch. Exit code 3 means the cycle is nonterminal; the API must use the JSON
`outcome` and inspection rather than the exit code alone.

## Scheduling and custody

- Responses: at most four due operations, four parallel retrievals, 15-second
  retrieval timeout, and a 20-second provider-I/O cycle target.
- Batch: exactly one due round, one retrieval, 40-second provider-I/O bound.
- Local work is exhausted after durable evidence and before detach.
- Reconciliation can prepare a new action but cannot submit it. External authority
  is then requested through the existing authorization contract.
- Provider custody says whether known provider work still requires retrieval.
- `consumer_authority` separately says which action IDs still require API-owned
  reservation, billing, ambiguity, or integrity-review authority.
- A terminal Batch or Response with unavailable usage never settles as `$0`.

## Outcome mapping

| Cycle outcome | Consumer action |
|---|---|
| `not_due` | Do not mutate API checkpoint; schedule at or after native due time. |
| `detached_provider_pending` | Persist checkpoint; release worker capacity if API policy permits; retain listed authority. |
| `awaiting_external_authority` | Persist prepared action and acquire API-owned authority. |
| `progressed_local` | Persist checkpoint and immediately reevaluate native inspection. |
| `review_required` | Retain workspace and all listed consumer authority for review. |
| `unsupported` | Retain capacity/workspace; do not improvise a provider call. |
| `terminal` | Follow closeout and publication policy; terminal does not itself imply publishable delivery. |

## Batch integrity and replay

One Batch round is one paid action. `custom_id` members are audit members, not
independent reservations. Output and error files are durable and preflighted for
exact, disjoint, unique membership before any response is ingested. A conflict
retains consumer authority for review but does not schedule endless polling once
terminal provider bytes are durable.

Exact replay uses the same durable provider evidence and does not upload a File,
create a Batch, submit a Response, or duplicate provider-transition events.

## Events

`provider.reconciliation_observed` is a redacted, non-authoritative observation
containing only action ID, native route family, provider mechanism, outcome, and
optional Batch member count. Retrieved operations emit it before `run.detached`
and `checkpoint.committed`. Early `not_due` and local-only replay emit no retrieval
event. Sink failures remain isolated from native execution.

## Workspace cleanup

Do not delete worker scratch merely because local capacity was released. The API
must first ingest the exact checkpoint, restore/validate it at the stable logical
absolute path when resuming, reach native terminal/closeout evidence, and satisfy
its own reservation and billing policy. HTTP status endpoints read API-owned
persisted state, never the live workspace.

## API adoption checklist

1. Require inspection v0.3 for worker release.
2. Validate `native_route`, every custody action, and the strict v0.2 cycle result.
3. Persist the exact decision basis, checkpoint, operation summaries, and
   `consumer_authority` projection.
4. Schedule no earlier than `resume_not_before`.
5. Retain API authority for every listed action ID until API-owned policy releases
   it transactionally.
6. Treat provider failure, output invalidity, identity conflict, and ambiguity as
   distinct from retry permission.
7. Reject bounded Batch.
8. Exercise the packaged
   `fixtures/lifecycle/route-parity-transition-oracle.v1.json` scenarios through
   the API transition oracle before promotion.

SBE does not own cross-run reservations, quotas, circuit breakers, entitlements,
global capacity, authoritative billing, reconciliation, or publication policy.
