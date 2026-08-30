# Slice 0 — Diffie and Hellman sanitized timelines

## Executive finding

The retained evidence changes the leading interpretation.

Hellman did not merely stop at a missing v2 dispatch handoff. Before the repeated
generic refusals, SBE sealed a complete native-result v0.2
`review_required / local_work_progress_contradiction` decision against the exact
active snapshot. It explicitly prohibited new provider creation and separated the
remaining actions into:

- one provider-bound retry requiring reconciliation; and
- one providerless retry eligible only for providerless denial.

API should have ingested that immutable terminal-review handoff before consulting
the still-nonterminal lifecycle projection. The later generic refusal loop is a
downstream symptom of missed terminal-result ingestion, not evidence that SBE
needed to dispatch the prepared retry.

Diffie's retained checkpoint is earlier and does not contain its later failure.
It proves a coherent two-action provider-pending/not-due state, not an
ordinary-resume contradiction. Its exact rejected lifecycle document remains
necessary to identify which consumer predicate failed.

## Access and validation

The owner and API review authorized exactly one `HEAD` and one `GET` for each
coordinate-packet object. The inspection performed exactly:

- 2 R2 `HEAD` operations;
- 2 R2 `GET` operations;
- 0 list/prefix operations;
- 0 R2 writes;
- 0 provider operations; and
- 0 retained-workspace mutations.

Both sizes, ETags and archive SHA-256 values matched. The official checkpoint
archive contract was validated, all 1,484 declared archive member hashes matched,
and both complete workspace snapshot path/hash inventories matched their restored
bytes. Windows relocation changes mixed-case path collation order, but no relative
path, size or hash.

The coordinate packet's `logical_restore_path` values are API-facing run paths and
do not match the native stable roots embedded identically in `run.json` and the
workspace snapshots. Those packet values were not treated as native truth.

## Diffie

Generation 8 was sealed at `08:54:58.326988Z`, state revision 61. It contains:

- six reported initial actions;
- two creative retries in native `WAITING` state;
- two distinct durable provider identities;
- native reconciliation outcome `pending` for both;
- common `resume_not_before = 08:55:24Z`; and
- no reported retry result.

The latest sealed result is
`nres_218114a64a7d0f1221c948f1`, published at `08:54:54Z`, with
`provider_pending / provider_operation_pending`.

At the API-recorded lifecycle observation time (`08:55:01Z`), the validated
checkpoint selects provider reconciliation as not due and is safe for worker
release. It has no local operation, external-authority request, or review reason.

The API failure at `08:56:52Z` is later than this checkpoint and is not represented
inside it. Therefore:

- dashboard completion cannot be projected into generation 8;
- generation 8 does not reproduce the strict ordinary-resume failure; and
- the rejected lifecycle document or later scratch/checkpoint evidence is required
  for a causal Diffie conclusion.

## Hellman

Generation 11 was sealed at `08:59:24.141461Z`, state revision 67. It contains:

- six reported initial actions;
- retry attempt 2 in ledger `WAITING` with a durable provider identity,
  reconciliation outcome `completed`, consumption present and no report;
- the corresponding pass attempt still marked `AMBIGUOUS_PROVIDER_SUBMISSION`;
- retry attempt 3 in `PREPARED / AWAITING_SPEND_AUTHORIZATION` with no provider,
  consumption or report; and
- no v2 dispatch intent for attempt 3—the stored intent belongs solely to attempt
  2 and its already-durable provider operation.

At `08:58:46.712710Z`, before checkpoint publication, SBE sealed:

- result `nres_1087eba75d3c29aba23193d5`;
- receipt `nreceipt_f367d82b9a92c868399d9d17`;
- outcome `review_required`;
- cause `local_work_progress_contradiction`;
- `new_provider_create_permitted = false`;
- `custody_finality = mixed_resolution_required`;
- reconciliation inventory `[paid_886d1daeeb7012b40a6fcae3]`; and
- providerless-denial inventory `[paid_bfce7b3ea385abe55a5045d1]`.

The result/receipt canonical hashes and joins validate. Its journal range 82–85
validates against the complete immutable journal and records:

1. preparation of attempt 3;
2. invocation start;
3. native transition to review-required due to local-work contradiction; and
4. invocation close with the same outcome/cause.

The receipt's snapshot SHA-256 exactly equals generation 11's active snapshot.
This is conclusive native evidence available before the later API lifecycle record
and repeated generic refusals.

The same native state still projects an `ordinary_resume` lifecycle because the
review decision is an immutable command-result handoff rather than a rewrite of the
underlying nonterminal status. This is precisely why the established integration
rule is **terminal/result ingestion first, lifecycle scheduling second**.

## Causal classification

### Hellman: API ingestion/routing defect established

The earliest proven public seam failure is failure to adopt the sealed terminal-
review result. After that miss, API continued scheduling from lifecycle state and
attached authority to generic resume; SBE then correctly refused provider creation.

The correct API behavior is not to mint a new grant for attempt 3. It is to ingest
the review result, retain/reconcile attempt 2 custody, deny attempt 3 through the
supported providerless-denial path, and keep the run in stable review according to
the released terminal-review handoff contract.

### Diffie: insufficient later native evidence

Generation 8 is healthy provider-pending evidence and predates the failure. No SBE
runtime correction can responsibly be inferred from it. API should supply the
exact rejected inspection/branch fields or explicitly record that the offending
document was not retained.

## Consequence for this sprint

No new SBE v2 dispatch schema or runtime create path is justified by the retained
evidence. The already released SBE contracts did three correct things:

1. sealed Hellman's contradiction as review-required;
2. prohibited new provider creation; and
3. later refused unsafe generic dispatch without I/O.

The companion API sprint should focus on terminal-result-first ingestion,
v0.7/v0.8 local-work consumption where no terminal result exists, and typed
generic-refusal mapping that cannot hold capacity in a no-op loop.

Retained-run recovery remains separately authorized and must follow the sealed
Hellman result rather than attempting a fresh v2 dispatch.
