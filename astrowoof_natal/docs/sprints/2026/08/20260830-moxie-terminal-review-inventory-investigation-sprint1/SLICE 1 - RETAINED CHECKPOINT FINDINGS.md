# Slice 1 — retained checkpoint findings

## Access and validation

The approved protected access is complete:

- remote operations: one exact `HEAD`, one exact streaming `GET`;
- list/write/delete/copy operations: zero;
- ETag, byte count, archive SHA-256, and frozen object identity: exact match;
- archive members: 765 total, comprising one manifest and 764 regular workspace
  files;
- member paths: unique, relative, contained, and manifest-exact;
- declared workspace bytes: 17,122,490;
- every declared member byte count and SHA-256: exact match;
- inventory SHA-256:
  `88d6e44341ade8d21fccf3c2964f721e03f45e089a510c4859f3ca9f8bc61509`.

No SBE command, provider call, database operation, or retained workspace
mutation was performed. Extraction occurred only in a new local temporary
directory.

## Decisive inventory finding

Generation 11 contains **eight** native paid actions, not seven:

| Ordinal | Native action | Stage/state | Provider/custody |
| ---: | --- | --- | --- |
| 1 | `paid_a015169151774e145f831c33` | initial / `REPORTED` | terminally accounted |
| 2 | `paid_e720b871d1dd3ddc2e05d948` | initial / `REPORTED` | terminally accounted |
| 3 | `paid_0cd6b9243c939ccc09e37169` | initial / `REPORTED` | terminally accounted |
| 4 | `paid_3427805988bab60cfad8553d` | initial / `REPORTED` | terminally accounted |
| 5 | `paid_856d9da5b181ea9a11099bbf` | initial / `REPORTED` | terminally accounted |
| 6 | `paid_a40ffcb021c9f200d352fc2e` | initial / `REPORTED` | terminally accounted |
| 7 | `paid_5769a5e279df0fc506f65a91` | creative retry 2 / `WAITING` | provider reconciliation only; durable `resp_057af…128a1` |
| 8 | `paid_95b6252fedb1610b3be397d9` | creative retry 3 / `PREPARED` | providerless denial only |

This reverses the initial omission hypothesis. Native evidence did not omit the
API-owned creative retry. It retained that retry and additionally prepared a
successor action that API's supplied chronology does not include.

## The rejected result is retained natively

Contrary to the API-side evidence limit, the exact result rejected by API is
recoverable from the protected native checkpoint:

- result: `nres_b68e9150988370d154aa3c06`;
- receipt: `nreceipt_5306a291337a44ce6b26c380`;
- schema/outcome: native result v0.2 / `review_required`;
- cause: `local_work_progress_contradiction`;
- native revision: 69;
- action count: 8;
- custody finality: `mixed_resolution_required`;
- reconciliation inventory: retry-2 action `paid_5769…`;
- providerless-denial inventory: retry-3 action `paid_95b6…`;
- new provider create permitted: false.

The public result validator, receipt validator, bounded journal range, retained
snapshot hash, and checkpoint-basis hash all pass. The original Linux logical
workspace root is preserved as native identity and was not rewritten to the
temporary Windows extraction path.

## Retry lineage at the checkpoint

The sixth initial pass has three attempts:

1. attempt 1: `PASS_QA_REJECTED`, initial action `paid_a40f…`;
2. attempt 2: `AMBIGUOUS_PROVIDER_SUBMISSION` in pass metadata, while its ledger
   row is `WAITING` with a durable provider identity and consumption evidence;
3. attempt 3: `AWAITING_SPEND_AUTHORIZATION`, action `paid_95b6…`, ledger state
   `PREPARED`.

Attempts 2 and 3 have different stable attempt keys and action IDs but the same
canonical request SHA-256. That observation is relevant to causal reconstruction
but does not by itself prove erroneous duplicate lineage: they are numbered
attempts with different native states.

## What is now proven

- The terminal result is complete with respect to its generation-11 native
  ledger: eight ledger rows and eight result rows.
- The API rejection is consistent with API reporting only seven current paid
  actions.
- The mismatching native row is most plausibly the providerless prepared third
  attempt, not the provider-created second attempt.
- SBE's result accurately retained both provider reconciliation custody and the
  providerless successor requiring denial/review.
- Accepting the result as an unchecked seven-row subset would discard real native
  authority evidence and is not safe.

## Remaining proof boundary

The six initial API action IDs and all seven complete API immutable binding
documents have not been supplied. Therefore the exact set difference is not yet
proven from both authorities field by field, although the recovered native IDs,
the API's asserted count/statuses, and the exact historical error make the extra
prepared action the leading explanation.

For Voof-paws 2, API should confirm its ordered seven native action IDs. Complete
bindings are needed only if any shared ID fails the set comparison or if a later
binding/provider join is disputed.

## Likely seam for Slice 2

The working causal model is:

1. retry-2 provider evidence became locally consumable;
2. ordinary local work prepared retry 3 and durably added its native paid action;
3. the same invocation detected `local_work_progress_contradiction` and sealed a
   truthful eight-action terminal-review result before API had admitted/persisted
   the newly prepared action through external-authority inspection;
4. API correctly rejected eight native rows against seven API rows; and
5. the separate lease-loss defect converted that typed refusal into retry churn.

This model must be checked against journal ordering and the external-authority
publication/admission boundary in Slice 2 before it is called causal.
