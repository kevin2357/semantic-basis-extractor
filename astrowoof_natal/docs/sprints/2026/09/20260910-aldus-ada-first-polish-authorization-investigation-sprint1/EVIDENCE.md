# Evidence Register

## Supplied API-owned facts

- Frozen IDs and terminal/job summaries: `BACKGROUND.md`.
- Current cohort creation one-off: `job-dahauhtbedkc739sqasg` (succeeded).
- QA SBE service: `srv-da12sktbedkc73btpu00`.

## Supplied non-authoritative diagnostics

- `C:\tmp\sbe-pair-aldus-ada-live-check.log`.
- Contiguous Better Stack cohort export:
  `C:\tmp\astrowoof-most-recent-two-runs-20260910\cohort.log`.
- Derived two-run swimlane:
  `C:\tmp\astrowoof-most-recent-two-runs-20260910\report\report.timeline.json`
  and `.html`.

These traces establish event order and API-observed failure details. They do
not establish the complete sealed result/request contents.

No R2 coordinate is authorized by this document.

## Slice 1 immutable reads

Owner authorization was subsequently supplied for exactly one conditional
HEAD and one bounded conditional GET per coordinate. Both objects matched the
frozen ETag, byte size, archive SHA-256, and inventory SHA-256.

- `ada-generation-6-r2-read-receipt.v1.json`
- `aldus-generation-11-r2-read-receipt.v1.json`
- `ada-generation-6-selective-inspection.v1.json`
- `aldus-generation-11-selective-inspection.v1.json`

The operation budget is exhausted: two HEADs, two GETs, zero listings, writes,
deletes, provider operations, workspace executions, recoveries, or mutations.
