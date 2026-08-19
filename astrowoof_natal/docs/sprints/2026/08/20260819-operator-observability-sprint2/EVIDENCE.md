# Operator Observability Sprint 2 Evidence

Status: implementation qualification complete; awaiting commit.

## Existing mechanisms

- `ExecutionEventEmitter`: typed `sbe.execution_event.v1` envelope generation,
  validation, correlation, severity, release identity, timestamp, and delivery
  statistics.
- `JsonlEventSink`: locked append-only JSONL file outside native workspaces.
- `StdoutJsonlSink`: locked line-delimited stdout suitable for platform capture.
- `sbe.execution_event_payload_catalog.v1`: packaged required-field catalog.
- Event sink/serialization failures: non-authoritative, counted, and isolated from
  native execution.
- Native transition journal/result/receipt: separate authoritative publication
  protocol, not a log substitute.
- Response-retrieval diagnostics: separate snapshot-covered operational artifacts
  added in SBE 0.4.10.

## Revised gap hypothesis

The typed event transport does not replace conventional developer logs. The main
gap is the absence of stdlib logging statements beside exception handlers, state
transitions, HTTP/subprocess calls, scheduling/concurrency logic, and native/API
handoffs. Operators need those direct observations with adjustable verbosity and
ordinary stderr/platform-log behavior.

## Selected default rendering

```text
✨🐶 timestamp | level | host_id | run_id | invocation_id | function | current_state : message
```

The format is a configurable stdlib logging default, not a consumer contract.
Missing contextual values render as `-`.

## Provider activity

- Provider calls/submissions/spend: 0 / 0 / USD 0.

## Focused checks completed

- Python compilation passed for the new logging module and initially instrumented
  core modules.
- `test_application_logging`, `test_initial_wave`, and `test_execution_events`:
  19 tests passed.
- Final logging/diagnostic/wave/event group: 27 tests passed.
- Representative exact interactive, exact Batch, bounded interactive, bounded
  Batch, final-QA precedence, provider retry, and final packaging paths: 7 tests
  passed. (One separately mistyped test selector produced a loader error and was
  replaced by the valid native-transition check below; it was not a product-test
  failure.)
- Native transition plus lifecycle inspection/closeout: 18 tests passed.
- Spend enforcement: 18 tests passed.
- `compileall` over `astrowoof_natal/src`: passed.
- `git diff --check`: passed; only the repository's expected Windows line-ending
  notices were emitted.

Total final focused product tests: 70 passed.

## Trace-review findings

- Repeated direct CLI invocation in one Python test process initially accumulated
  SBE handlers and duplicated messages. Configuration now replaces only the prior
  SBE-owned handler and preserves embedding-application handlers.
- Python context variables do not automatically propagate through
  `ThreadPoolExecutor`. Initial create and provider retrieval coordinators now
  capture and explicitly bind host/run/invocation/state context in worker threads.
- Malformed provider responses remain diagnostics rather than becoming logging
  exceptions; logging checks response shape before reading status/identity.
- Library-only callers remain silent until their application configures logging.

## Scope statement

This fast patch changes observability only. It does not add lifecycle states,
change provider/spend decisions, alter public artifact schemas, or make logs
authoritative. Broad wheel/release qualification was intentionally not run.
