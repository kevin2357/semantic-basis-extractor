# Frisbee / Triumph terminal-delivery outcome investigation

## Purpose

Perform a bounded, evidence-led native-side investigation for the latest QA cohort.
The API persisted both runs as `failed`, but the SBE traces show materially
different terminal outcomes. Establish whether either native result is malformed,
misclassified, or correctly produced and subsequently mishandled by API.

## Immutable identifiers

| Pup | API run | Native run |
| --- | --- | --- |
| Frisbee Fandango `4a05f776` | `e2d7f0ce-8c2a-4209-b79f-eb2187a58b15` | `cfdd79f1f50bbe940ba40d2c42743bf8b009cc02eef0f44895f0697b0d46be98` |
| Triumph Tiramisu `e946535b` | `9686b45d-f27b-473a-b167-8893bb4b18c2` | `45eb2039befdf81a3fa09f86a79ef08598dd09085191e98ee5de1bdaa361c468` |

## Current cross-boundary evidence

- Frisbee: six initial and two polish actions; SBE reached
  `FINAL_QA_REQUIRES_REVIEW`, all eight actions `REPORTED`, one accepted polish,
  one rejected polish, and `subject_states=FINAL_QA_WARN:1`.
- Triumph: six initial and one polish action; SBE reached `DELIVERY_COMPLETE`,
  terminal closeout, no local provider dependencies, and lease release. API
  nevertheless persisted `failed`, while the outer worker emitted a non-retryable
  `worker.job.failed` event labeled `native.terminal.delivery_complete`.
- No active QA capacity slot, worker lease, job, or provider operation remains.

## Requested Render log export

The original noon-to-2 PM request was corrected to **midnight through 2:00 AM Denver
time** on 2026-09-05. Denver was MDT (UTC-06), so the exact queried UTC window is
06:00–08:00Z. The previous eight empty afternoon files were deleted. The replacement
unfiltered half-hour exports are:

- `C:\tmp\sbe-worker-20260905-0000-0030-denver.json` (415,868 bytes)
- `C:\tmp\sbe-worker-20260905-0030-0100-denver.json` (1,282,900 bytes)
- `C:\tmp\sbe-worker-20260905-0100-0130-denver.json` (empty; no Render entries)
- `C:\tmp\sbe-worker-20260905-0130-0200-denver.json` (empty; no Render entries)

The cohort executed around 00:25–00:43 MDT (06:25–06:43Z), within the first two
exports.

## Boundaries

No listing, writes, provider access, reconciliation, resume, recovery, API mutation,
or retained-workspace mutation is authorized. If retained evidence is necessary,
request exact checkpoint/object coordinates and explicit bounded HEAD/GET authority.
