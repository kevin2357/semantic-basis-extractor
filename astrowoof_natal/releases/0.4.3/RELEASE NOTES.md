# AstroWoof Natal Authoring 0.4.3

Status: qualified for immutable annotated tag; publication pending.

This patch separates short-lived local execution capacity from durable
provider-pending custody. Exact interactive runs can checkpoint and detach while
known OpenAI Responses work remains pending, then resume in one bounded GET-only
cycle without creating another provider submission or spend commitment.

## Added

- lifecycle inspection v0.2 execution-capacity and provider-custody projections;
- durable versioned `resume_not_before` timing and bounded backoff;
- a one-wave, four-action, 15-second-per-GET, 20-second reconciliation cycle;
- exact interactive coverage for initial authoring, creative retries, polish,
  qualitative critic, and qualitative candidate stages;
- strict nonmutating `not_due` and typed progress/wait/review/terminal outcomes;
- installed CLI and public Python bounded-reconciliation interfaces;
- redacted detach/checkpoint observations and strict local-continuation evidence;
- explicit Batch and bounded-Natal fail-closed classification; and
- API consumer mapping and companion capacity-adoption checklist.

Local capacity release never releases API reservations or financial authority.
Known provider IDs are retrieved, never resubmitted. Identity-less interrupted
submission remains ambiguous and fail-closed.

Provider operations and provider spend during implementation and qualification:
zero / `$0`.

## Qualification

- complete repository suite: 339 passed;
- three-workspace native parallel cohort passed;
- fresh installed lifecycle smoke passed on Windows and Linux CPython 3.11;
- two fixed-epoch candidate builds were byte-identical;
- wheel SHA-256:
  `429bf43b39033f931ebab42e41d14bfa078c1585a32896564ddc11f51cca4c61`;
- wheel bytes/entries/resources/cache entries: 740271 / 88 / 47 / 0;
- exact AGF 0.8.1 and SPC 0.11.0 compatibility remains pinned; and
- artifact source commit:
  `101328fdaf3da38458b1474888b8b9ad989e7168`.

Publication remains pending the immutable release-record tag.
