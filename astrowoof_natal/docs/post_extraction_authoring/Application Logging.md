# Application Logging

SBE uses Python's standard `logging` package for human-facing operational logs.
Logs explain execution; they are never native-state, spend, billing, delivery, or
API authority.

Supported CLIs write their normal machine-readable result to stdout and operational
logs to stderr. The default level is `INFO`; use `--log-level DEBUG` for a focused
QA or incident run and `--log-level WARNING` when only trouble is useful. Embedding
applications may install their own handlers and formatters.

The default line is:

```text
✨🐶 timestamp | level | host_id | run_id | invocation_id | function | current_state : message
```

`host_id` comes from `--host-id`, `ASTROWOOF_HOST_ID`, `HOSTNAME`, or
`COMPUTERNAME`, in that order. Unknown context is rendered as `-`. Context is
scoped safely across concurrent work; each member message also names its action,
pass, attempt, round, or provider identity where relevant.

Messages include state transitions, external-authority handoffs, concurrent wave
progress, provider request start/end/error, subprocess boundaries, validation and
editorial decisions, checkpoint publication, and delivery. DEBUG adds mechanics
such as hashes, counts, and scheduling decisions.

Logs must never contain credentials, authorization headers, prompts, authored
content, Batch JSONL bodies, raw provider bodies, protected birth parameters, or
complete subject records. Provider endpoints omit query strings and user-info;
errors pass through the bounded provider-diagnostic sanitizer. Prefer counts,
identities, statuses, durations, and digests.

Library imports install no global logging configuration. A package `NullHandler`
prevents surprise output for unconfigured library consumers; CLI entry points
explicitly configure stderr. Logging failure must never change native execution.

When adding code near a meaningful exception, state transition, provider/subprocess
call, scheduling choice, or custody handoff, add a nearby log at the level a human
would expect. Do not freeze prose as a consumer contract or duplicate entire JSON
artifacts into a log line.
