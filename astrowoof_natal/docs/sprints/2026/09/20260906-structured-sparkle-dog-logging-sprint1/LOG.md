# Log

## 2026-09-06 — Slice 1

- Read and incorporated `API REVIEW - PLAN AND SLICE 0.md` in full.
- Froze the v1 record as a closed envelope plus closed event payload catalog.
- Distinguished caller-supplied API run identity from native run identity and
  provider operation identity from paid-action identity.
- Excluded raw tracebacks and required sanitized, bounded exception evidence.
- Chose one JSON default at runtime migration while retaining historical pipe
  input support in the reporter.
- Preserved the Voof-paws 1 stop before formatter/runtime mutation.

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
