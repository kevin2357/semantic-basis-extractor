# Froth/Ganache stalled initial-provider action investigation

## Frozen QA evidence

The QA SBE worker is suspended. This sprint is read-only: no resume, reconciliation, provider access, workspace mutation, R2 write, lease manipulation, database mutation, or retry is authorized.

| Pup | API run | Native run | Frozen state |
| --- | --- | --- | --- |
| Froth Fermat | `aa5a6019-dbc6-4d10-a698-0aee2a70920a` | `ea2267d6328955a1675bd2541d45914876f1427655afc18b25073b26ea892b78` | API running; authoring `retry_wait` attempt 6/64 |
| Ganache Godel | `c1baf1d2-13d7-477f-8e85-d01f58b485f0` | `41e69bfd48b8b8fab0ef9000dfd1b8a58e4a9ee6f98e159e9673b90c84720d1f` | API failed; authoring 64/64, `sbe.dependency.command_failed` |

API custody shows five `reported` and one `provider_created` initial action for **each** run.

## Relevant SBE traces (Denver MDT, 2026-09-03)

- Froth generation 7 checkpoint accepted at 3:12 PM after `provider_reconciliation`; trace reports `provider_local_dependency_count=1`, `local_continuation_required=false`, capacity disposition `release_until_due`, then lease released.
- Ganache repeats a `CalledProcessError` classified as retryable about every minute until attempt 64, ending at 4:11 PM. Each iteration has a fresh 120-second lease acquisition.

## Investigation questions

1. From bounded retained checkpoints/workspace evidence, which exact initial action remains locally pending for each native run and what state does SBE believe it has?
2. Can SBE account for Froth's one remaining local dependency versus API's one provider-created action, without treating logs as transition authority?
3. What exact native command/subprocess failed for Ganache? Was the error semantically retryable, and which public evidence should have made it terminal or quiescent instead?
4. Does this share a cause with the Froth retained-action discrepancy, and what minimal contract/API/SBE work would prevent recurrence?

## Bounded inspection

SBE may use only the exact existing run coordinates above and API-provided immutable checkpoint coordinates when supplied. HEAD/GET of exact objects is acceptable; listing, writes, provider calls, resume, repair, or mutation are not.
