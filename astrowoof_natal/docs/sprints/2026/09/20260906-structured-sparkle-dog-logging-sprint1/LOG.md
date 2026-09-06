# Log

## 2026-09-06 — Slice 0

- Mapped ordinary stderr logs, public command stdout, typed execution-event
  JSONL, API stderr relay, and durable native artifacts as separate surfaces.
- Enumerated shared logging configuration and approximately 169 call sites.
- Recorded current versus desired correlation-field availability.
- Identified the seven existing bounded summary helpers as the safest first
  structured-payload integration points.
- Converted recurring workspace-download questions into a concrete field
  selection checklist.
- Added baseline tests proving stderr/stdout separation and the current
  application-log/execution-event distinction.
- Paused before formatter or runtime mutation for Slice 1 contract review.

