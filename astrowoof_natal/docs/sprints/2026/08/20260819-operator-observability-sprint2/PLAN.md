# Practical Application Logging Sprint 2 Plan

Date: 2026-08-19  
Status: implementation complete; awaiting final commit approval  
Starting release: SBE 0.4.10

## Purpose

Add ordinary, useful application logging throughout SBE so a human reading worker
logs can understand what the program is doing, where control is moving, what
important state it sees, and why it failed.

This is conventional Python logging: put a clear log statement next to interesting
or risky code. Do not make every message a versioned public contract and do not
require operators to reconstruct the story from database rows or native artifacts.
Use Python's standard `logging` module so verbosity, formatting, destinations, and
future aggregation can be configured without rewriting application logic.

## Technical direction

- Every production module uses `logger = logging.getLogger(__name__)`.
- Library code emits records but does not install global handlers.
- CLI entry points configure logging once, to stderr, with a useful default format.
- CLI controls provisionally include `--log-level` with `DEBUG`, `INFO`, `WARNING`,
  `ERROR`, and `CRITICAL`.
- Existing JSON/stdout command results and JSONL event streams stay clean; ordinary
  logs always go to stderr unless the embedding application configures otherwise.
- The API/worker may configure handlers, formatters, JSON formatting, aggregation,
  or suppression later using normal Python logging facilities.
- Existing structured execution events and authoritative native artifacts remain
  separate. They are not replaced, and ordinary logs are never execution or
  billing authority.

## Default line format

Use a simple grep-friendly default on stderr:

```text
✨🐶 2026-08-19T10:14:48.123Z | INFO | host-abc | run_123 | inv_456 | reconcile_provider_cycle | WAITING : retrieving due Responses count=4
```

Conceptually:

```text
✨🐶 timestamp | level | host_id | run_id | invocation_id | function | current_state : message
```

- `timestamp`: UTC ISO-8601 with milliseconds.
- `level`: standard Python logging level.
- `host_id`: worker/container/process identity supplied by configuration or a
  documented environment variable; `-` when unavailable.
- `run_id`: native SBE run ID; `-` before a run is known or for run-free tools.
- `invocation_id`: native command/publication invocation when known; `-` otherwise.
- `function`: Python `LogRecord.funcName`, requiring no manually maintained label.
- `current_state`: the most relevant run/pass/action/subject state at that location;
  `-` when no meaningful state exists.
- `message`: ordinary human-readable text with searchable `key=value` context.

The prefix is a useful default, not a frozen public data contract. An embedding
worker remains free to replace the formatter. A small standard logging
filter/adapter may supply safe defaults and scoped `host_id`, `run_id`, and
`current_state`; this should stay thin and must not become a parallel context or
telemetry framework.

## What should be logged

### Exception boundaries

Add a record at every meaningful `except` handler before it handles, translates,
suppresses, retries, detaches, or re-raises the exception.

At minimum record the exception class and safe message, current
route/stage/pass/attempt/action when available, the handler's decision, and useful
local state such as provider ID, state revision, or artifact path.

Use `logger.exception(...)` when handling an unexpected exception where a stack
trace is valuable. Use `logger.warning(..., exc_info=True)` or a concise message
for expected/recoverable failures. Never silently swallow an exception without a
log unless it is demonstrably internal control flow and logging it would be
misleading noise.

### State transitions and decisions

Log every meaningful native state/status transition and the reason for it:

- run creation, resume, detach, and terminalization;
- pass/attempt preparation, waiting, acceptance, rejection, and retry;
- spend authorization waiting, grant, denial, and consumption;
- provider identity durability and reconciliation outcomes;
- validation, lint, final-QA, polish, critic, candidate, and optional-stage skips;
- budget, policy-stop, ambiguity, and review decisions;
- snapshot/checkpoint/native-result publication; and
- delivery and closeout.

Prefer old state, new state, identity, and reason in one message when available.

### External service and subprocess calls

Log immediately before and after every web-service request and important subprocess
call.

Before a request, include safe salient facts such as method and sanitized endpoint,
known provider operation ID, route/stage/pass/attempt, model, service level,
timeout, bounded payload size/count/hash where useful, and transport attempt.

After a request, include elapsed duration, HTTP/provider status, provider request
and operation IDs when available, safe response size/count/usage summary, and the
next application action.

Never log API keys, authorization/cookie headers, prompts, authored output, raw
provider bodies, protected subject parameters, Batch JSONL content, or full request
payloads.

### Control and custody handoffs

Log whenever control or responsibility crosses a meaningful boundary:

- SBE returns awaiting authorization to the API;
- SBE detaches with known provider work and gives the API a resume recommendation;
- a fresh SBE worker resumes/reconciles a retained workspace;
- SBE publishes a native result/receipt for API ingestion;
- SBE reports quiescence/closeout eligibility;
- provider custody or retained consumer authority changes classification; and
- work moves from initial authoring into fan-in, retry, QA, polish, critic,
  candidate, delivery, or closeout.

SBE does not own API worker leases, so it must not claim it granted or released a
lease. It should log the native facts that cause the API to acquire, retain, or
release capacity. If an API-provided lease/job/worker correlation ID is available,
include it as context and log its receipt/return without treating it as native
authority.

### Concurrency and scheduling

Log initial six-pass wave membership, concurrent create start/end, durable-ID
checkpoints, retrieval due/selected/deferred counts, fan-in completion, Batch
round/member cardinality, provider-pending detach, and the reason work is not due,
awaiting authority, locally runnable, retained for review, or terminal. Log
single-writer lock acquisition/contention/release at DEBUG unless exceptional.

## Levels

- `DEBUG`: scheduling, locks, artifact/hash/count details, and internal decisions.
- `INFO`: lifecycle progress, state transitions, web-call start/end, handoffs,
  checkpoints, and successful outcomes.
- `WARNING`: recoverable trouble, transport warnings, optional-stage skips,
  validation warnings, and log sink loss.
- `ERROR`: failed operations, malformed/conflicting provider evidence, invariant
  failures, terminal non-delivery, and exceptions preventing progress.
- `CRITICAL`: only process-wide conditions where safe operation cannot continue.

Default proposal: `INFO` in deployed workers, with `DEBUG` enabled temporarily for
QA/problem runs.

## Safety and usability rules

- Pass log arguments separately (`logger.info("... %s", value)`) rather than
  eagerly formatting strings.
- Apply the bounded sanitizer used by provider diagnostics to exception messages
  and endpoint identities.
- Use searchable keys in messages (`run_id=%s action_id=%s`) without making prose a
  frozen schema.
- Bound messages and collection rendering; log counts and selected IDs, not huge
  objects.
- Logging failure must not alter native execution correctness.
- Avoid duplicate spam: the decision-owning layer logs the decision; lower
  transport layers log request mechanics.
- Tests assert important records with `assertLogs` but do not freeze every sentence.

## Slices

### Slice 0 — Inventory and conventions

- Inventory modules, CLIs, exception handlers, state writes, web/subprocess calls,
  concurrency coordinators, and API/native handoffs.
- Identify silent catches and places where only structured events exist.
- Add a short logging guide covering logger ownership, levels, safe fields,
  sanitization, stdout/stderr, and examples.
- Decide whether a tiny shared helper is useful for CLI setup and safe context; do
  not build a new logging framework.

Gate: review inventory/conventions, then proceed without freezing message prose.

### Slice 1 — Setup and transport boundaries

- Add shared CLI logging configuration, the default line formatter/context filter,
  and `--log-level` consistently to supported production commands.
- Define the supported host-ID input and thread/task-safe scoped run/state context;
  absent context renders as `-` rather than causing formatting failure.
- Instrument OpenAI Responses and Batch HTTP calls before/after/error, including
  durations and safe provider/request metadata.
- Instrument important subprocess calls similarly.
- Prove stdout JSON/JSONL remains uncontaminated.

### Slice 2 — Exceptions and state transitions

- Audit every production `except` handler and log where control is handled,
  translated, suppressed, retried, or re-raised.
- Log meaningful run/pass/action/subject/status transitions with reasons.
- Cover spend authorization, ambiguity, budget/policy stops, QA, optional stages,
  and terminal delivery/review states.

### Slice 3 — Scheduling, concurrency, and handoffs

- Instrument initial-wave fan-out/fan-in, Batch rounds, retrieval waves, retry
  scheduling, single-writer boundaries, detach/resume, and local continuation.
- Log SBE-to-API authorization/result/capacity recommendations and fresh-worker
  resume boundaries using native facts.
- Accept optional API/job/lease correlation if a supported seam already exists;
  otherwise document the consumer addition rather than inventing API lease
  ownership inside SBE.

### Slice 4 — Editorial and delivery flow

- Instrument assembly, validation/lint, retries, polish, critic/candidate,
  packaging, native publication, delivery, closeout, and repair tools.
- Make happy paths and common failures readable at INFO/WARNING/ERROR, with deeper
  mechanics at DEBUG.

### Slice 5 — Practical QA and tuning

- Capture representative scripted exact/bounded and interactive/Batch stderr logs.
- Review them as a human: remove spam, fill gaps, improve context, and verify
  concurrency remains understandable.
- Test exception handlers, secret canaries, bounds, level filtering, stdout purity,
  and logging failure isolation.
- Publish sample INFO/DEBUG logs and a short operator guide.
- Run proportionate affected tests and lightweight CLI checks. A wheel rebuild and
  broad historical matrix are explicitly deferred for this fast logging patch.

## Acceptance criteria

- At INFO, an operator can follow the major lifecycle and see where a run waits,
  progresses, hands off, or fails.
- Default stderr records consistently render UTC timestamp, host ID, native run ID,
  Python function, current state, and message; unknown fields render as `-`.
- At DEBUG, a developer can diagnose scheduling, state, provider transport, and
  artifact-flow problems without adding emergency print statements.
- Meaningful exception handlers retain safe exception and local context.
- Every web-service call has safe before/after/error logging and duration.
- Every meaningful state transition and cross-boundary handoff is visible.
- Concurrent records carry enough run/action/pass/attempt identity to follow.
- Logs contain no credentials, prompts/outputs, raw bodies, or protected subject
  data.
- Logging never changes native results, provider/spend behavior, or API authority.

## Explicit non-goals

- Turning log messages into stable consumer contracts.
- Replacing native transition evidence, snapshots, or API database state.
- Building a custom logger, hosted backend, dashboard, or tracing platform.
- Logging every function call or dumping whole objects.
- Moving API lease ownership or product orchestration into SBE.
