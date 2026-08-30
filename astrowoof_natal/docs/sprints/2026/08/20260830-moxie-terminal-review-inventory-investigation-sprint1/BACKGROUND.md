# Background — Moxie terminal-review inventory investigation

## Purpose

Perform a narrow, provider-free investigation of why the retained QA Moxie
native workspace selected terminal-review / `terminal_closed` after a completed
creative-retry path, while API retained one additional provider-created action
and rejected the result with:

```text
SbeProviderContractError: SBE terminal review API action inventory changed
```

This is evidence gathering for the API companion sprint:

`C:\dev\github\astrowoof-api\docs\sprints\2026\08\20260830-terminal-review-action-inventory-coherence-sprint62`

It is not an authorization to repair, reconcile, resume, submit provider work,
mutate the retained run, or release/terminalize anything.

## Exact retained target

| Field | Value |
| --- | --- |
| API run | `b39c8b14-d0c7-440a-b5b8-bd4bb0d85205` |
| SBE job | `5f2757db-feb6-457e-8f76-e56f45e7eadf` |
| native run | `53bacbe893fa722a50a251111d9263a7c703da28c088b30fcdc9ff3798a8dea4` |
| active checkpoint | `95a0bfa6-c067-45a2-817c-83d0aa57117d` |
| checkpoint generation | `11` |
| checkpoint state | `active` |
| native checkpoint status | `AWAITING_SPEND_AUTHORIZATION` |
| contract | `astrowoof.sbe-workspace-checkpoint.v1` |
| compatibility identity | `astrowoof.qa.sbe0432-semantic-decision-consumer-hardening.v1` |
| storage environment/namespace | `qa` / `checkpoint` |
| R2 storage object ID | `429d43b2-6dc0-4ad9-ac31-ee68c9d32878` |
| Exact R2 object key | `v1/checkpoint/429d43b26dc04ad9ac31ee68c9d32878` |
| archive SHA-256 | `aa6b472e3b865242f93c388a8664828a292ff05953e835211f90a70567132920` |
| archive bytes | `3,924,276` |
| inventory SHA-256 | `88d6e44341ade8d21fccf3c2964f721e03f45e089a510c4859f3ca9f8bc61509` |
| logical restore path | `/work/runs/b39c8b14-d0c7-440a-b5b8-bd4bb0d85205/sbe` |
| provider version/ETag | `"43ecac806938556e1bf16e6b63952130"` |

No credentials, signed URLs, or protected payload bytes are included here.

The key is not inferred from a bucket listing or an undocumented naming
convention. It is the closed API storage-contract rendering of the supplied
`qa`/`checkpoint` object reference: `v1/{namespace}/{object_id.hex}`.

## API-authoritative chronology

Moxie has seven API paid actions: six `reported` initial actions and one
`provider_created` creative retry:

`paid_5769a5e279df0fc506f65a91` →
`resp_057af41fd08baade006a947ae12fd087d0b3f03d5d45c128a1`

The API has persisted these SBE lifecycle inspections:

| observed | revision | capacity disposition | reason | provider custody |
| --- | ---: | --- | --- | --- |
| 18:44:33Z | 12 | `continue_local_cycle` | `provider_reconciliation_due` | `known_operations_pending` |
| 18:44:53Z | 13 | `release_until_due` | `known_provider_work_pending` | `known_operations_pending` |
| 18:46:41Z | 34 | `continue_local_cycle` | `provider_reconciliation_due` | `known_operations_pending` |
| 18:47:08Z | 47 | `release_until_due` | `known_provider_work_pending` | `known_operations_pending` |
| 18:47:55Z | 55 | `await_external_authority` | `spend_authorization_required` | `none` |
| 18:49:04Z | 59 | `release_until_due` | `known_provider_work_pending` | `known_operations_pending` |
| 18:51:11Z | 65 | `continue_local_cycle` | `local_work_ready` | `completed_evidence_pending_local_work` |

After that final inspection, the SBE worker's non-authoritative trace reported
`local_resume` and `terminal_closed`. API rejected the terminal-review
result before receipt persistence because the result's action-disposition IDs
did not equal API's current complete seven-action inventory. The raw rejected
result is not retained; do not claim an exact historical ID difference without
recovering it from the protected checkpoint or other immutable native evidence.

## Requested investigation

1. Restore/read the exact active checkpoint using the established protected,
   provider-free checkpoint procedure. Verify all supplied identifiers/digests
   before interpreting content.
2. Inspect its lifecycle, journal range, result/receipt inventory, and
   action/lineage records without provider access or native mutation.
3. Determine whether a terminal-review result produced from this snapshot is
   supposed to enumerate:
   - the full native action inventory;
   - a snapshot-scoped inventory; or
   - an otherwise bounded subset with a public scope/provenance field.
4. If it is snapshot-scoped, identify the exact public evidence that safely
   distinguishes in-scope versus later action lineage. If it is full-run scoped,
   identify how/why the creative retry was omitted or diverged.
5. State whether SBE's current public contracts already express the required
   scope. If not, propose the smallest versioned artifact/field needed; do not
   tell API to reconstruct private `run.json` semantics.

## Guardrails

- Exactly one checkpoint target; no R2 listing, writes, or delete.
- No OpenAI/provider calls or credentials.
- No native commands that mutate workspace state.
- No retained-QA database mutation, lease/capacity action, result publication,
  reconciliation, terminalization, or release.
- Record findings in this sprint directory and leave them uncommitted for API
  review before any implementation/release work.
