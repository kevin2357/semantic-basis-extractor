# Background

## Investigation subjects

This sprint covers two contemporaneous exact-Natal QA failures from the same
unfiltered SBE `0.4.40` worker export. They are separate causal branches unless
the evidence later proves a shared implementation seam.

### Pastiche-shaped editorial failure

- Native run: `e9a72ba7695dddddc977da162388396a854a0813139c5475ce0b290d038c4ffb`.
- Pass 6 attempt 2 completed provider work, and acceptance logged
  `theme_group_balance` as an advisory, but `author_one_pass` then recorded the
  attempt as rejected and prepared attempt 3.
- Pass 6 attempt 3 completed provider work, and acceptance logged
  `theme_group_coverage` as an advisory, but the attempt was again rejected and
  the run transitioned to `FAILED_REQUIRES_REVIEW`.
- The final native result was sealed as `review_required` with result
  `nres_6615e36edf7aef434be8098f` and receipt
  `nreceipt_11c2e26c57da95dbd56df66f`.

This is suspicious because the public/logged policy classification says the
theme-group findings are advisory while the enclosing authoring control flow
still treats the acceptance subprocess's nonzero return as rejection. The
investigation must establish whether advisory reports are being translated
incorrectly at the subprocess boundary or whether a separate hard failure was
present but omitted from the concise log.

Retained evidence later proved separate hard `theme_group_assignment` findings
on attempts 2 and 3, so the released policy behaved as implemented. The product
owner has since made a broader policy decision: theme-group filtering is not a
delivered feature, its present vocabulary/prompt are not a frozen future
contract, and theme-group QA has imposed disproportionate operational cost.
All theme-group-specific QA evaluation is therefore to become dormant while
the artifact fields remain readable compatibility data. See
`PRODUCT DECISION - THEME GROUP QA DORMANT.md`.

### Perseverance Puff retained-custody failure

## Exact run coordinates

- QA reading: `785ad2a1-6a98-4fb4-89fc-e022ebf93676` (Perseverance Puff)
- API run: `181ae153-1496-4e80-acd3-c7f18a4c9607`
- Native run: `84a24f8facd330a80ad42c19986ccc0f5fde2287e307d30ccbf6e3f85f3c30be`
- Job: `b1bf8c7f-0c9a-46b5-b84a-4c2c4aa5dde9`
- Terminal attempt: `20c0822e-40a8-46f7-8847-15b2524fb173`
- Last lease (released): `9596aba1-34cf-4745-a14c-ac9cc7411ada`

## Frozen evidence

- Latest persisted native receipt: `ordinary_authoring`, `review_required`, `local_work_progress_contradiction`, recorded `2026-09-03T13:53:56.647801Z`.
- Last native trace state: revision 117, 9 actions (6 `authoring_initial`, 2 `creative_retry`, 1 `polish`), `REPORTED:8, WAITING:1`, custody count 1, and v2 intent `PROVIDER_PENDING`.
- Exact v2 action in the trace: `paid_047fd998009e0e133e0a64a1`.
- Native result published at `2026-09-03T13:53:21.071482Z`: `review_required`, receipt `nreceipt_d38140389b21ae33e151f1fe`, result `nres_dac25445bfa8c6613d0d0ca0`.
- API closeout subsequently classified it `review-retained-provider-reconciliation`; worker failure was nonretryable `native.review.provider_reconciliation_required`.
- API shows terminal failed with capacity released and no active lease, but one `provider_created` paid action remains.

## Unfiltered worker-log export

`C:\\tmp\\sbe-worker-last-2-hours-puff-20260903.log` — unfiltered QA SBE service `srv-da12sktbedkc73btpu00` export, explicitly queried in twelve ten-minute windows for `2026-09-03T12:01:03Z` through `14:01:03Z`. It includes both Pastiche and Puff activity. Do not treat it as authority for mutation.

The trace shows Puff's polish provider action completing retrieval and
reconciliation returning `progressed_local`. Subsequent ordinary
resume cycles repeatedly reached `finalize_subjects`, while local-work sealing
reported `stage_consumer_not_reached`; the final attempt refused progress as
`semantic_work_not_consumed` and published the v0.2 review result described
above. The retained workspace is still required to prove which durable polish
consumer fact, operation key, or custody join failed to advance. Bounded
checkpoint inspection later proved that the completed response never joined the
stored `SUBMITTED` polish attempt; see the Slice 1 findings.

## Companion API sprint

`C:\\dev\\github\\astrowoof-api\\docs\\sprints\\2026\\09\\20260903-puff-retained-provider-terminal-review-api-investigation-sprint71`.

## Safety boundary

No workspace mutation, provider request/retrieval, R2 listing/write, run reconciliation, terminalization, deployment, or release is authorized.
