# Evidence

## Slice 3 — high-value decision-point adoption

- Existing bounded workspace, state, lifecycle decision, optional-stage,
  validation, publication, finalization, and CLI-exit adapters now emit explicit
  event names and closed payloads.
- Lifecycle decision records distinguish `positive_permission` from branch,
  outcome, and capacity labels.
- Missing identities remain null; record-level correlation can augment bound
  context but is never recovered from message prose.
- The reporter has a minimal validated v1 bridge so default JSON output does not
  break the existing end-to-end trace regression; full migration hardening
  remains Slice 4.
- Focused trace/qualification/formatter/contract/event/reporter matrix:
  52 passed, 2 expected optional-schema skips.
- No API-relay visibility claim is made before Slice 5's route matrix.

## Slice 2 — formatter and context implementation

- The configured SBE application handler now emits one closed JSON object per
  stderr line; stdout and execution-event transports remain separate.
- Context now distinguishes caller-supplied API run, native run, subject,
  invocation, paid action, provider operation, and checkpoint object IDs.
- Existing `run_id=` bindings remain a compatibility alias for native run ID;
  no API identity is inferred.
- Sanitized messages retain `✨🐶`; exceptions exclude raw traceback and use
  the bounded sanitized representation.
- Invalid event extras produce one valid nonrecursive fallback record and do
  not raise through the logging call.
- Focused formatter/contract/event/reporter tests: 33 passed.
- High-value helpers intentionally remain `application_message` until Slice 3
  supplies their cataloged payloads explicitly.

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
