# Structured Sparkle-Dog Logging — Background

## Why this sprint exists

SBE worker investigations currently rely heavily on human-readable stderr lines
with a stable marker and pipe-delimited context:

```text
✨🐶 <timestamp> | <level> | <host> | <run> | <invocation> | <function> | <state> : <message>
```

Those lines are useful for humans and searchable by identifier, but a log
platform must parse prose and delimiters before it can index run, action,
provider-response, checkpoint, lifecycle, or outcome fields. That makes joined
queries, dashboards, no-progress detection, and cross-service correlation more
fragile than necessary.

The owner has connected Render logs to Better Stack and approved replacing the
ordinary SBE worker trace representation with genuine structured JSON. The
human-friendly `✨🐶` message should remain visible inside each record.

## Existing boundaries

SBE currently has two related but distinct observability surfaces:

1. `application_logging.py` configures ordinary stdlib application logs on
   stderr. These are the familiar pipe-delimited `✨🐶` lines.
2. `execution_events.py` builds typed, bounded
   `sbe.execution_event.v1` envelopes. CLI options can write those envelopes to
   JSONL files or stdout where the command's output-file mode keeps result
   authority unambiguous.

The structured application-log change must not merge these authorities:

- stderr traces remain diagnostic and non-authoritative;
- command results and public lifecycle artifacts remain transition authority;
- typed execution events retain their existing schema and sink-isolation rules;
- ordinary command stdout remains machine-readable and unchanged.

## Desired outcome

Each SBE worker trace line is one valid JSON object with:

- a readable message beginning with `✨🐶`;
- timestamp, severity, logger/function, producer, and runtime version;
- bounded correlation fields for the identities actually known at that point;
- bounded structured decision/evidence fields where a call site supplies them;
- explicit null/absence rather than overloaded `-` values in JSON;
- no prompt, response body, credentials, private payload, or protected content.

Better Stack should be able to filter and group without parsing message prose,
while a human reading raw Render logs still sees useful descriptions.

## Primary correlation inventory

The first-release inventory should assess and, where genuinely available,
standardize:

- API run identity;
- native run identity;
- subject identity;
- invocation identity;
- paid/native action identity;
- provider response/operation identity;
- checkpoint identity and generation;
- lifecycle state, selected branch, and outcome;
- installed SBE version and producer service/host.

An absent identity must remain absent. The formatter must never infer one from a
message, path, subject name, or another identifier.

## Compatibility requirements

- The run reporter/parser must accept both historical pipe-delimited logs and
  new JSON records.
- JSON logging must be deterministic in field naming and serialization shape;
  timestamps and inherently runtime-specific values remain variable.
- Multi-line exception data must not break one-record-per-line JSON framing.
- Logging and downstream sink failures must never change native execution.
- Migration must be coordinated with the API stderr relay, but should not
  require API to reinterpret trace data as authority.

## Non-goals

- Replacing public lifecycle, result, receipt, checkpoint, or execution-event
  contracts.
- Logging full prompts, model output, provider payloads, credentials, or private
  workspace material.
- Parsing arbitrary prose back into trusted fields.
- Requiring Better Stack availability for worker correctness.
- Redesigning API logging in this SBE sprint.

