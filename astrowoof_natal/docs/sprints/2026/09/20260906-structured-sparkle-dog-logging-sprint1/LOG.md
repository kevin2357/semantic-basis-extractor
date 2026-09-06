# Log

## 2026-09-06 — Slice 3

- Converted the central bounded trace adapters from prose-only records to
  explicit catalog events while retaining readable messages.
- Added positive-permission diagnostics and explicit exit side-effect fields.
- Structured deterministic finalization failure and not-sealed custody paths.
- Added the narrow validated JSON parser bridge required by the new default;
  deferred the complete dual-format migration matrix to Slice 4.
- Replayed recent investigation-class distinctions using the native structured
  payloads rather than reparsed key/value prose.
- Reached Voof-paws 2 with 52 focused tests passing and two expected
  optional-schema skips.

## 2026-09-06 — Slice 2

- Replaced the SBE handler's pipe formatter with closed one-line JSON output.
- Added nullable correlation context without changing legacy native `run_id=`
  call sites.
- Added caller-only `--api-run-id`/`ASTROWOOF_API_RUN_ID` intake.
- Preserved foreign root handlers, levels, interpolation, stderr destination,
  and explicit context restoration.
- Added bounded secret sanitization, exception projection, and nonrecursive
  serialization fallback tests.
- Confirmed that semantic trace helpers need explicit Slice 3 event extras;
  the formatter does not parse their prose to invent structured fields.

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
