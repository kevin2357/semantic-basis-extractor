# API Review — Voof-paws 2 Formatter and Decision Adoption

## Verdict

Approved. Slices 2–3 correctly establish the new structured SBE application
log surface without changing any API/SBE authority boundary.

## What is aligned

- The formatter emits exactly one valid `astrowoof.sbe_worker_log.v1` object
  per stderr line, preserves the useful `✨🐶` human message, and neither
  writes to nor changes command stdout, execution-event JSONL, result files,
  checkpoints, or sealed artifacts.
- API-run identity remains caller-supplied only. Existing `run_id=` retains its
  native-run compatibility meaning; it is not silently reinterpreted as API
  identity.
- The decision summaries expose the investigation-critical distinction between
  branch/outcome and `positive_permission`, but are explicitly diagnostic.
  They cannot grant a lifecycle transition, custody action, or provider call.
- The fallback path is single-record, nonrecursive, sanitized, and does not
  turn observability failure into native-work failure. Null correlation values
  remain honestly null rather than being inferred from prose.
- The reporter bridge validates native v1 records and does not use the JSON
  message text to manufacture/override correlations or decision fields.

## Required next gates

Slice 4 should prove mixed historical-pipe and v1-JSON inputs, malformed and
truncated JSON accounting, duplicate/order behavior, and unknown-record
handling. Slice 5 must separately qualify the real process routes: the
reconciliation stderr relay, plus ordinary-resume and v2 routes under both the
configured inherited-stream and suppressed-stream cases. The latter must not
be inferred from this formatter work.

Keep the privacy sentinel checks over both raw emitted lines and the reporter
outputs. No API runtime change, deployment, or live QA activity is implied by
this review.

API review: 2026-09-06
