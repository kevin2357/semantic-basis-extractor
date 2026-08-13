# Slice 5 Structured Execution Events

Status: complete, 2026-08-13

SBE exposes `sbe.execution_event.v1` as a bounded, non-authoritative observation
envelope. Native run state, spend ledgers, provider identities, snapshots, lifecycle
results, and closeout artifacts remain the only execution authority.

## Typed payload catalog

Every allow-listed event name has required stable fields in the packaged
`contracts/execution-event-payload-catalog.v1.json`. The catalog exactly matches the
Python producer table. Missing typed dimensions, unknown event names, unsupported
severity, non-serializable data, and recursively prohibited fields are dropped with
bounded in-memory warning counters; they cannot alter native execution.

The allow list covers run start/resume/detach, pass/action preparation,
authorization, provider submission/identity/wait/completion, QA, retry, polish,
critic, checkpoint, terminal, closeout, failure, and event-sink warning observations.

## Transports

Python callers inject an optional event sink callback and receive normal typed
results. Sink exceptions are caught and counted; they never escape into execution.

`--events-jsonl <path>` appends typed JSONL outside the authoritative run workspace.
The CLI rejects event files under the run root so events cannot disturb snapshot
integrity.

`--events-stdout-jsonl` emits only single-line typed envelopes on stdout. The final
command result is `sbe.command_result.v1` with `envelope_type: command_result` rather
than unframed JSON. Human diagnostics remain on stderr. The two JSONL transports are
mutually exclusive.

## Correlation and provider lifecycle

Envelopes support bounded API run/job/attempt and opaque external authority
correlations plus exact native run, action, and pass IDs. Provider spend wiring emits
one action-correlated sequence for authorization, submission start, durable provider
identity, waiting, and reported completion. Events contain provider operation IDs
where operationally necessary but never prompts, request/response bodies, raw lease
tokens, credentials, or protected birth/location fields.

Provider-less denial and closeout emit typed outcome observations. Losing those
events does not alter or obscure their authoritative native artifacts/results.

## Delivery semantics

Event IDs are unique producer observations; consumers tolerate duplication, delay,
loss, and reordering. No event grants authorization, releases funds, proves lease
authority, changes lifecycle state, or substitutes for inspection/closeout. A
consumer reconstructing operational timing from events must reach lifecycle truth
from native contracts when events disagree or are absent.
