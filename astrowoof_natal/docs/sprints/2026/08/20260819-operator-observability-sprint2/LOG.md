# Operator Observability Sprint 2 Log

## 2026-08-19 — Sparkle-dog operator signature

- Kevin requested that every default SBE log line begin with `✨🐶`.
- This is implemented once in the shared formatter; embedding applications remain
  free to replace the default formatter.

## 2026-08-19 — Implementation and lean qualification complete

- Added direct human-readable logging across the principal exact/bounded,
  interactive/Batch, spend, reconciliation, lifecycle, snapshot/publication,
  editorial, delivery, closeout, and repair paths.
- Corrected two findings during trace review: repeated in-process CLI setup now
  replaces its own prior handler instead of duplicating every line, and explicit
  context is carried into create/retrieval thread pools.
- Kept stdout machine results separate from stderr logs and retained the existing
  native/public authority contracts unchanged.
- Focused checks passed: 70 test cases plus source compilation and diff hygiene.
- No provider work or network activity occurred.
- Work is paused for Kevin's final commit review as requested.

## 2026-08-19 — Implementation underway

- Added a thin stdlib logging configuration/context module with UTC rendering,
  stderr output, level selection, host/run/invocation/state context, and safe
  missing-field behavior.
- Added package `NullHandler` behavior so unconfigured library consumers remain
  quiet.
- Instrumented Responses and Batch HTTP transport, subprocesses, snapshots,
  persistence, spend decisions, initial-wave concurrency, reconciliation,
  lifecycle inspection/closeout, bounded lifecycle, native transition publication,
  authoring/Batch rounds, QA, polish, qualitative review, and delivery.
- Kept request/response bodies, prompts, authored prose, protected subject data,
  and credentials out of messages.
- Kevin requested deliberately lean patch qualification rather than the full
  historical release matrix.

## 2026-08-19 — Default human-readable line shape selected

- Kevin selected the intentionally simple default:
  `timestamp | host_id | run_id | function | current_state : message`.
- Fields use UTC milliseconds, native SBE run identity, built-in Python function
  identity, and the locally meaningful current state; unavailable values are `-`.
- Message text remains ordinary and evolvable. The worker may replace the formatter
  later through normal Python logging configuration.

## 2026-08-19 — Direction corrected to conventional application logging

- Kevin clarified that the goal is ordinary developer/operator statements at the
  code locations where interesting work occurs, using Python stdlib `logging`.
- Replaced the event-contract/timeline-centered plan with direct instrumentation of
  exception handlers, state transitions, web/subprocess calls, concurrency,
  scheduling, and control/custody handoffs.
- Existing typed JSONL events and native evidence remain separate and do not
  constrain ordinary log-message evolution.
- SBE will log native capacity/handoff facts and API-provided lease correlation when
  available, but will not claim ownership of API worker leases.

## 2026-08-19 — Sprint opened

- Kevin requested richer operator/reviewer visibility into application state and
  flow than the API's normal database records provide.
- Sprint is explicitly exploratory and may revise slices as representative traces
  expose the useful semantic level.
- Initial inventory confirms SBE uses a custom typed JSONL execution-event layer,
  not Python stdlib logging, for important operational telemetry.
- No implementation or contract change has begun.
