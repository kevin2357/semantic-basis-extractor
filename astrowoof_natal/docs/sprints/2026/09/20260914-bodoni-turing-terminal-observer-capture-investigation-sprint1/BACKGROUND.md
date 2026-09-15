# Bodoni/Turing terminal-observer local-capture investigation

## Purpose

Determine why two otherwise clean QA terminal-review paths selected exact review
authority but produced no Better Stack editorial-review packet or longitudinal
artifact POST. This is an investigation only. It must not mutate retained
workspaces, contact providers, resume/reconcile runs, or repair their terminal
state.

## Frozen QA witnesses

| Pup | API run | Native run | Exact terminal result | Terminal outcome |
| --- | --- | --- | --- | --- |
| Bodoni Brioche | `e64ab155-432a-433a-b3f8-ebfa737db0d7` | `af93c196e0ef923ff617086004d2de0cec503eafb651cd9774068db8510a5ba7` | `nres_2b91727d5ba5b97bf07110ff` | `review_required` / `native.terminal.review_required` |
| Turing Tart | `9cb4d9d8-be9d-4ffb-948c-e47839831f00` | `ddf49bcaf474f3ff5493d8c990541031c8fffce563da24d6faa35fa16ca2e95d` | `nres_433d168be822521a18043c6a` | `review_required` / `final_qa_requires_review` |

Both runs are terminal. API authority confirms that all leases, execution capacity,
provider custody, and active paid actions were released.

## What the deployed traces establish

The SBE worker is running the API worker loop plus the installed SBE wheel. The
call boundary is:

`API SBE worker loop -> astrowoof_natal_authoring.build_editorial_review_runtime_capture -> API envelope/preflight -> Better Stack HTTP POST`.

For both witnesses, the structured SBE worker trace establishes:

1. `editorial.observation.selection` selected the exact terminal-review result
   with `exact_authority_present=true`.
2. The observer wrapper entered and emitted `capture entered`.
3. The wrapper returned with `branch=unavailable` roughly 0.36--0.40 seconds
   later.
4. No `capture completed`, editorial envelope, preflight, HTTP-post, artifact,
   or observer-completed event was emitted.

Consequently, the current evidence places the failure in local capture
construction, before Better Stack request preparation or network I/O. The current
transport catches the local exception and returns `unavailable`; the best-effort
failure-phase reporter did not emit its corresponding failure event, so the
exception class and exact failure reason remain unknown.

## Exported unfiltered SBE worker logs

Render service: `srv-da12sktbedkc73btpu00` (SBE worker). The intended export is
a two-hour UTC window, unfiltered, split into 15-minute files. Empty windows are
retained deliberately. The original file 07 is capped, but its full interval is
now replaced by the three non-capped five-minute exports below. Both Bodoni and
Turing decisive sequences are present in that replacement set.

| UTC window | File |
| --- | --- |
| 2026-09-14 23:11:35Z--23:26:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-01.log` |
| 2026-09-14 23:26:35Z--23:41:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-02.log` |
| 2026-09-14 23:41:35Z--23:56:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-03.log` |
| 2026-09-14 23:56:35Z--2026-09-15 00:11:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-04.log` |
| 2026-09-15 00:11:35Z--00:26:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-05.log` |
| 2026-09-15 00:26:35Z--00:41:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-06.log` |
| 2026-09-15 00:41:35Z--00:56:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-07.log` |
| 2026-09-15 00:56:35Z--01:11:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-08.log` |

The original `-07.log` export reached Render's 1,000-line cap before its
requested end. Its complete evidence replacement is the following unfiltered,
non-capped five-minute set; use these three files for chronology rather than the
capped 15-minute original:

| UTC window | Replacement file | Physical lines |
| --- | --- | ---: |
| 2026-09-15 00:41:35Z--00:46:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-07-01.log` | 513 |
| 2026-09-15 00:46:35Z--00:51:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-07-02.log` | 356 |
| 2026-09-15 00:51:35Z--00:56:35Z | `C:\tmp\sbe-worker-terminal-observer-20260915-07-03.log` | 326 |

## Suggested first slice

Repair and freeze the capped log interval before treating Turing's missing events
as evidence. Then perform provider-free source/public-boundary mapping before any
retained-workspace access. Exact workspace reproduction remains separately gated
on pinned coordinates and owner authorization.

Do not infer an HTTP, Better Stack credential, source-token, ingestion-host, or
payload-size issue without a reached `editorial_post` phase.
