# Nori / Biscuit terminal-review and reconciliation-loop investigation

## Purpose

Investigate two fresh, current QA runs created from the same two-pup cohort after the QA fleet was reset and deployed with the SBE `0.4.37` release pair. This is read-only diagnosis first: establish why Nori reached a terminal review-required outcome after completing provider reconciliation, and why Biscuit is repeatedly taking ordinary-resume turns without advancing the active SBE checkpoint.

No provider activity, workspace mutation, retained-run recovery, operator action, deployment, or release is authorized by this investigation.

## Environment and cohort

- Environment: `qa`.
- SBE release/profile identity: `0.4.37` / `astrowoof.qa.sbe0437-generic-quarantine.v2`.
- One SBE capacity slot is configured.
- API run ceilings for this already-created cohort: USD 50/run, USD 100/cohort, USD 150 rolling 24h, USD 49/active stage, USD 0 candidate.

| Pup | API run ID | Native SBE run ID | SBE job ID |
| --- | --- | --- | --- |
| Nori Nybble (created as Nori Nonce) | `5741d84d-b053-494f-9644-1cb9e4cb6cbf` | `e0b406dbacf2edf0ce7b421586e7464d8056fe0f893033a03edfdee957f6a9a0` | `329b39f1-3084-4be4-86a0-152cfd68fb43` |
| Biscuit Byte | `25704e4a-059d-49b0-b0e8-c0de5b230e58` | `8a7c25e37385ef75e95d8b72a7efe7bdb1355495df4195cf1bab93f0d821dd84` | `62c77c95-b5a0-4f77-8479-604a4d5364cd` |

## Observed facts

### Nori

- Initial provider reconciliation correctly reduced from six dependencies to one, then to zero.
- At `2026-08-31T15:46:29Z`, SBE executed `local_resume` with `terminal_closed`; it then emitted `sbe.closeout.completed` with `terminal-closed`.
- The API recorded the SBE authoring job as failed with non-retryable reason `native.terminal.review_required`.
- Nori released her lease and completed workspace cleanup. She does not hold capacity, a lease, or a pending authoring job.

This is a stable terminal outcome, but it needs semantic explanation: determine whether `review_required` is expected editorial/quality behavior for the materialized result, or whether the final local-resume/closeout path classified an otherwise valid run incorrectly.

### Biscuit

- Biscuit began only after Nori released the sole slot, so the original provider-pending handoff is not the immediate issue.
- Her initial wave prepared and then reconciled. A later active workspace has held **one** provider-local dependency and `local_continuation_required=true`.
- From approximately `2026-08-31T16:25Z`, repeated ordinary-resume cycles preserve the same active checkpoint generation `13`:
  - each cycle reports `execution_branch=ordinary_resume`, `outcome=quiescent`, and `execution_capacity_disposition=continue_local_cycle`;
  - the API records a new checkpoint acceptance but the checkpoint ID/generation does not advance;
  - readiness remains `local_continuation_required=true`, `provider_local_dependency_count=1`;
  - the job is deferred, then reclaimed about 15 seconds later.
- At the latest observation, the API job had attempt count `46`, remained leased, and held the only active capacity allocation.

This is a material progress/capacity concern: identify the exact retained provider-local dependency, why ordinary resume does not consume or reconcile it, and why the repeat loop preserves generation 13 while retaining local-continuation eligibility.

## Exact protected checkpoint coordinates

These are supplied for narrow read-only recovery and inspection. They are QA data only. Do not list storage, write storage, mutate a retained run, make provider calls, or include credentials/signed URLs in artifacts.

### Biscuit active checkpoint

- API/native run: `25704e4a-059d-49b0-b0e8-c0de5b230e58` / `8a7c25e37385ef75e95d8b72a7efe7bdb1355495df4195cf1bab93f0d821dd84`
- Checkpoint/job/attempt: `9c14e28e-eb1a-470e-b023-a5d5253f6137` / `62c77c95-b5a0-4f77-8479-604a4d5364cd` / `64b7963c-821c-485c-a8f5-8c862823760b`
- Generation/state: `13` / `active`
- Archive: object `9bbb5bbd-abfc-457a-856c-95a7cc1efa09`, bytes `4115956`, SHA-256 `925dfed7c7a6a3b43c29ac963f3aa978c50d6d7a98c26c870c50e4ce3af89d47`
- Inventory SHA-256: `3aa7b1dbb99701d56ec7774cb5df99384340e1fa41400e00ac0a7b1a17b1c7b3`
- Contracts/compatibility: `astrowoof.sbe-workspace-checkpoint.v1` / `astrowoof.qa.sbe0437-generic-quarantine.v2`
- Storage: environment `qa`, namespace `checkpoint`, protection `protected-operator`, provider version `5107c10aff34b46927dc0c346eca2288`
- Restore path: `/work/runs/25704e4a-059d-49b0-b0e8-c0de5b230e58/sbe`
- Persisted native lifecycle status: `bounded-progressed_local`

### Nori terminal checkpoint

- API/native run: `5741d84d-b053-494f-9644-1cb9e4cb6cbf` / `e0b406dbacf2edf0ce7b421586e7464d8056fe0f893033a03edfdee957f6a9a0`
- Checkpoint/job/attempt: `2a9c5936-b64a-4a7d-b81b-d74522713ebc` / `329b39f1-3084-4be4-86a0-152cfd68fb43` / `814f5d0e-208f-42e4-a33f-597cc127f348`
- Generation/state: `15` / `active`
- Archive: object `7482718a-f773-4ae4-929d-3fc043171271`, bytes `5014073`, SHA-256 `721926c6b10c7cc3ee3de5276674a844afbfaef3abdd2d9058c8fd6a928e6e8d`
- Inventory SHA-256: `56514a2f326d85357f452dc4fcf035fdcd0c6697f220b36114ec644ff9cea756`
- Contracts/compatibility: `astrowoof.sbe-workspace-checkpoint.v1` / `astrowoof.qa.sbe0437-generic-quarantine.v2`
- Storage: environment `qa`, namespace `checkpoint`, protection `protected-operator`, provider version `04934a4da3493aa5d2921bd7bf90b1fd`
- Restore path: `/work/runs/5741d84d-b053-494f-9644-1cb9e4cb6cbf/sbe`
- Persisted native lifecycle status: `WAITING_FOR_RESPONSE`

## Available non-authoritative trace evidence

Render service: `srv-da12sktbedkc73btpu00` (`qa-sbe-worker`). Search by API run ID or the native SBE run ID above.

Useful time windows:

- Nori reconciliation/final closeout: `2026-08-31T15:42:00Z` through `15:46:30Z`.
- Biscuit loop: `2026-08-31T16:24:00Z` onward. Representative traces show ordinary resumes preserving checkpoint `9c14e28e-eb1a-470e-b023-a5d5253f6137`, generation `13`, with one provider-local dependency.

The traces are diagnostic-only. PostgreSQL and the storage receipts remain authoritative for custody and any later mutation decision.

## Requested investigation order

1. Recover and inspect Biscuit’s exact active checkpoint read-only; identify the one dependency, its state/lineage, and the selector/transition evidence that chooses ordinary resume.
2. Prove or refute that the repeated result is a valid due-time wait rather than a no-progress loop. In particular, explain why `continue_local_cycle` coexists with a deferred API job and a freshly re-acquired capacity slot.
3. Recover and inspect Nori’s terminal checkpoint read-only; classify `review_required` as expected editorial terminal review versus erroneous native closeout classification.
4. Add provider-free regression coverage for any identified defect. Do not turn a diagnostic guess into a recovery path without an exact public contract and evidence.
5. Stop for API review before proposing a patch/release or any retained-run action.
