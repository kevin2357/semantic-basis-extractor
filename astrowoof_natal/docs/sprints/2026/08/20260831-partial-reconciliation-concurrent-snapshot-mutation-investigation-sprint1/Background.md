# Partial reconciliation concurrent snapshot-mutation investigation

## Purpose

Investigate the QA failure of **Kardamom Kaboom** in which an otherwise normal
initial six-member authoring wave entered provider reconciliation, discovered a
mixed completed/pending subset, and then failed while launching local work for
the completed members. This is an investigation-only starting point: no
provider calls, retained-run mutation, repair, release, or deployment is
authorized by this document.

The immediate question is whether the native reconciliation path incorrectly
allows concurrent local authoring continuations to mutate a workspace while
`validate_workspace_snapshot` requires that same workspace to remain an exact,
sealed snapshot. The trace strongly suggests that it does.

## Environment and frozen cohort

- Environment: QA
- SBE wheel/image: `0.4.35` / `ghcr.io/kevin2357/astrowoof-sbe-worker@sha256:d3628bff6db50e0cfcdf9b5332d340d16a52360f187ffc6804fd1f748d7867e2`
- SBE service: `srv-da12sktbedkc73btpu00` (`astrowoof-qa-sbe-worker`)
- The worker was suspended at `2026-08-31T12:02:29Z` after the loop was
  confirmed. It must remain paused during investigation.
- Cost policy was explicitly approved at USD 50/run, USD 100/cohort, USD 150
  rolling 24-hour, USD 49 active stage, USD 0 candidate. The cohort is now
  frozen: no additional spend or work is authorized.

### Reads/runs

| Pup | Reading ID | API run ID | Current relevance |
| --- | --- | --- | --- |
| Kardamom Kaboom | `66b3b699-0514-4066-84d5-39ee49c0b1e2` | `1e7564dd-ebd1-497e-ba8e-c2663f9b118f` | Active failure-loop subject |
| Saffron Sparkler | `8cf812ab-129a-427c-8295-0213882ecf32` | `9b441810-f50c-43d8-a441-463e93a17350` | Deterministic work succeeded; SBE job has not begun because Kardamom held the sole SBE slot |

### Kardamom coordinates

- Native run ID: `a120a14edaf523856444d3fb895b15340874efe258fe818b8bbb5d943b6e518f`
- API SBE job: `259fadb2-d972-4bdb-8940-21fed595b1c8`
- Active workspace ID: `29460172-ef84-42df-be6e-f4bb5ec979d9`
- Workspace path in worker: `/work/runs/workspace-29460172-ef84-42df-be6e-f4bb5ec979d9/sbe`
- At the last authoritative audit (`2026-08-31T11:55:35Z`): six paid actions
  existed, all `provider_created`; reported and reconciled cost were both USD
  0; workspace was registered with `local_continuation_required=true` and
  `provider_local_dependency_count=6`.
- The SBE job had already failed attempts 4–6 as retryable
  `sbe.dependency.command_failed` / `CalledProcessError` after three earlier
  successful attempts. The lease from attempt 6 was active before suspension.

## Observed trace, in timestamp order

The exact trace is retained in the unfiltered Render export below. Key events:

1. `11:54:00Z`: lifecycle inspection reported `WAITING_FOR_RESPONSE`, six
   provider actions, no local dependencies, branch
   `provider_reconciliation_cycle`, and `branch_action_count=4`.
2. `11:54:02Z`: reconciliation fetched four due provider actions concurrently.
   Two returned `completed` and two `in_progress`.
3. `11:54:03.486Z`: follow-up inspection remained
   `WAITING_FOR_RESPONSE`, selected `ordinary_resume`, and reported
   `local_continuation_required` work.
4. `11:54:03.488Z`: `author_pending_passes` started **two** selected local
   passes concurrently (`max_workers=2`, pass numbers 3 and 5).
5. `11:54:04.386Z`: snapshot validation failed with `expected_members=390,
   actual_members=390`; soon after it failed again with
   `expected_members=390, actual_members=420`.
6. One local authoring attempt then raised:
   `ValueError: Run snapshot is incomplete or changed; restore the complete exact snapshot before resuming`.
   The provider-reconciliation command exited status 1, and the API wrapper
   converted its empty stdout / nonzero return into retryable
   `sbe.dependency.command_failed`.
7. Subsequent leases reran the same reconciliation path and produced the same
   `CalledProcessError` loop. No conclusion should be drawn from database state
   alone; the trace establishes the concrete native failure.

## Evidence export

An unfiltered last-hour Render log export was saved locally at:

`C:\tmp\sbe_worker_logs.txt`

It is JSON emitted by `render logs` for the whole QA SBE worker, not filtered by
run, severity, or text. It includes the relevant sparkle traces and traceback.
Do not treat it as authority for mutation; use it to reproduce and diagnose the
native behavior together with the retained workspace/checkpoint evidence.

## Initial hypotheses to prove or reject

1. The reconciliation path is allowed to start multiple local authors against
   one snapshot-bound workspace, and their state/save operations race the
   snapshot validator.
2. `validate_workspace_snapshot` may be correctly enforcing the sealed
   snapshot contract, while the caller is applying that check at a point where
   approved local output/checkpoint files legitimately exist. If so, the fix
   must distinguish immutable input inventory from legal output evolution;
   weakening validation globally would be unsafe.
3. The wrong boundary may instead be temporary/concurrent workspace material
   created before publication. The `390 -> 420` member transition is a useful
   lead, but the paths and provenance of the additional members must be
   identified before proposing a fix.

## Desired investigation outputs

- Reproduce provider-free from a faithful copy/fixture of this state where
  possible.
- Identify each added/removed member and its writer.
- State whether a single-pass local continuation succeeds while two concurrent
  continuations fail.
- Specify the narrowest invariant-preserving correction and regression matrix
  for partial reconciliation: mixed completed/pending initial-wave members,
  one and multiple selected local continuations, ordinary resume, and later
  retry/polish paths.
- Preserve the distinction between trace evidence and authoritative custody;
  do not use the result to resume these runs without separate owner approval.
