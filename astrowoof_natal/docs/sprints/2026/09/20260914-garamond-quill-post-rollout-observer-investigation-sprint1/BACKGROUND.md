# Garamond / Quill Post-Rollout Observer Investigation

## Purpose

Provide the initial SBE-side read-only investigation for a fresh QA cohort
whose two accepted-delivery runs completed after the API Sprint 96 terminal
observation repair but have no confirmed Better Stack editorial packet or
longitudinal artifacts. The API worker's expected observer outcome events were
not found in the bounded SBE-worker logs.

This opening is evidence-only. Do not resume, reconcile, replay, mutate,
recover, list R2, or otherwise alter either retained run.

## Cohort

| Pup | API run | SBE job | Native run | Outcome |
| --- | --- | --- | --- | --- |
| Garamond Ganache | `abd73e79-f102-4f91-8fda-fd3a56268d58` | `47fda7a5-9e43-4f42-b436-125ba9f01bf4` | `3b9d7bedd799e2a7118d2c0cddde483d2fc03a0fa3109e60a36d94f3763f1afe` | accepted delivery / API succeeded |
| Quill Biscotti | `02744933-4b93-4390-8696-4993aee87375` | `a9be5e83-585a-44c7-81c4-95f934030aca` | `de6a6649510df3fae4bf850be06db93bc1accf66f305e9a587fe939b454b6ae8` | accepted delivery / API succeeded |

## Frozen evidence

- Garamond native publication logged `DELIVERY_COMPLETE` at
  `2026-09-14T19:05:08Z`, result `nres_8a0f803d144b9430fe945e6c`, receipt
  `nreceipt_bc0a2a6938486fa73bc126f4`, seven reported actions, and an accepted
  polish. API later succeeded at attempt 6/64 after one retryable terminal
  publication boundary.
- Quill logged `delivery-accepted` and publication completion at
  `2026-09-14T19:10:15Z`; API succeeded at attempt 7/64.
- A complete parse of the raw terminal window found
  `editorial.observation.completed` for both jobs. Each used the exact SBE
  delivery result ID but returned `branch=unavailable`,
  `failure_kind=capture_or_preflight`, and zero artifacts. The earlier absence
  was a log-search miss, not a missing invocation.
- Better Stack's direct query capability currently errors on a bad/absent
  ClickHouse cluster mapping. It is not evidence that a source has zero rows.

## Raw SBE worker exports

These unfiltered Render exports are outside Git:

- `C:\tmp\garamond-quill-sbe-worker-logs-20260914T1815-1830Z.json` — empty.
- `C:\tmp\garamond-quill-sbe-worker-logs-20260914T1830-1845Z.json` — empty.
- `C:\tmp\garamond-quill-sbe-worker-logs-20260914T1845-1900Z.json` — launch
  through initial activity.
- `C:\tmp\garamond-quill-sbe-worker-logs-20260914T1900-1915Z.json` —
  reconciliation through terminal closeout.

Each source request was an unfiltered 15-minute `render logs` export with its
own `--limit 1000` ceiling.

## Requested Slice 0

Using only source, the raw log export, and any already-local runtime evidence:

1. Map the exact structured JSONL/native command handoff emitted for each
   accepted delivery.
2. Confirm whether the handoff has the exact result/receipt/invocation identity
   that the API observer expects after the Sprint 96 repair.
3. Identify any SBE-owned reason a valid accepted-delivery handoff could omit
   that identity, without adding a fabricated fallback.
4. Clearly distinguish SBE handoff evidence from API observer invocation,
   Render relay, and Better Stack transport, which remain API-owned unless
   source proof says otherwise.

## Related API sprint

`C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260914-garamond-quill-post-rollout-observer-investigation-sprint97`
