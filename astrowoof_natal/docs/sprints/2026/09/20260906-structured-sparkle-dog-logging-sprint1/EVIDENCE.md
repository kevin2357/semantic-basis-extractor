# Evidence

## Slice 1 — structured record/privacy contract

- Added packaged closed envelope schema
  `sbe-worker-log.v1.schema.json`.
- Added packaged closed payload vocabulary
  `sbe-worker-log-event-catalog.v1.json`.
- Added a reader/validator enforcing exact keys, event-specific payload fields,
  bounded JSON values, nullable correlation, sanitized exception shape, and
  privacy sentinels.
- Recorded the invocation-specific API stderr relay matrix; reconciliation is
  verbatim, while ordinary resume/v2 visibility depends on event-stream
  configuration.
- Focused contract + existing logging/event/reporter tests: 29 passed.
- Runtime formatter, stdout, execution-event JSONL, provider I/O, and native
  state remain unchanged.

## Current gate

Slice 0 is complete. The logging surface and desired-field census are ready for
Slice 1 contract work. No runtime format change has begun.

## Source findings

- One shared application formatter emits the pipe-delimited stderr records.
- Nine public CLI/configuration paths use the shared logging arguments.
- Approximately 169 ordinary logging calls exist in the authoring package.
- Four context variables currently bind host, native run, invocation, and native
  state.
- Typed execution events already use JSON envelopes and isolated sinks.
- Seven bounded observability helpers compute structured values before
  flattening them into messages.
- The run reporter currently reparses pipe messages with a boundary-event set
  and safe-field allowlist.

## Safety characterization

- Ordinary application logs use stderr and do not contaminate command stdout.
- Ordinary application records are distinct from execution-event envelopes.
- No provider, R2, QA, API database, deployment, or retained workspace was
  accessed or mutated.
