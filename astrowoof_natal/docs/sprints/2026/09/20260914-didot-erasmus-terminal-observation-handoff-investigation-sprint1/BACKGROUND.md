# Didot / Erasmus Terminal Observation Handoff Investigation

## Purpose

Jointly determine why one ordinary accepted delivery and one ordinary terminal
editorial-review closeout completed in QA without producing the exact native
handoff API needs to invoke the best-effort Better Stack observer.

This is an investigation opening only. Do not mutate retained work, resume,
reconcile, recover, replay provider calls, or alter either live run.

## Cohort

| Pup | API run | SBE job | Native run | Outcome |
| --- | --- | --- | --- | --- |
| Didot Danish | `18c59e66-d58c-42c3-b12d-274528f9cee1` | `23045c6a-a0e8-4715-a757-a2c379026981` | `bab4b77f930c02445f484a4c5b3c45e62050fb23c385c0dae5adf96966175d25` | accepted delivery / published |
| Erasmus Eclair | `bf86f7f8-99ea-4362-a50d-ef6c7a23fd62` | `cb5f2ef7-25fa-4458-bd48-7dbfe06e3ab1` | `003189754c73b35a1d117e4d4eb88f33629ed6a14cbef202965f8fada6ae88c2` | terminal editorial review |

## API-side observed route issue

- Didot first returned terminal closed and API attempted publication. Its
  eligibility check rejected that attempt because SBE-accepted delivery
  authority was not yet established; API recorded one retryable
  `terminal.publication.retry` at `2026-09-14T16:00:13Z`.
- Didot then took `delivery_validation`, reached `delivery_accepted`, and API
  published at `16:00:42Z`. API did not log an observer call. Its delivery
  observer branch requires a non-null `sealed_terminal_result_id`.
- Erasmus ended through `sealed_terminal_preflight` and a typed
  `native.terminal.review_required` closeout at `16:12:39Z`. API did not log an
  observer call. Its review observer branch requires an invocation-bound
  `terminal_review_command_result` with an exact result ID rather than generic
  terminal evidence.

SBE should map the exact structured JSONL/native reader output for both routes:
which result/receipt identities exist, which are emitted to API, and which are
intentionally absent. Do not invent an identity merely to satisfy observation.

## Render worker logs

Unfiltered bounded exports from QA SBE worker, outside Git:

- `C:\tmp\astrowoof-qa-sbe-worker-didot-erasmus-20260914-01.json` — 15:30–15:45 UTC
- `C:\tmp\astrowoof-qa-sbe-worker-didot-erasmus-20260914-02.json` — 15:45–16:00 UTC
- `C:\tmp\astrowoof-qa-sbe-worker-didot-erasmus-20260914-03.json` — 16:00–16:20 UTC

## Related work

- API prior observer handoff sprint:
  `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260910-gutenberg-hypatia-editorial-observer-handoff-investigation-sprint89`
- API companion sprint:
  `C:\dev\github\astrowoof-api\docs\sprints\2026\09\20260914-didot-erasmus-terminal-observation-handoff-investigation-sprint96`
