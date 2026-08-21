# Slice 3 — Structured Observability

Date: 2026-08-21
Status: complete; awaiting review

## Outcome

Lifecycle external-authority classification now emits bounded, redacted,
failure-isolated diagnostics for successful request selection, truthful native
refusal, successful branch selection, and internally contradictory constructed
documents.

Events and logs remain non-authoritative. They cannot change lifecycle bytes,
snapshots, native state, authority, or provider behavior.

## Typed events

No event name or schema version was added.

- `external_authority.request_selected` records request digest, kind, action count,
  and selected command.
- `external_authority.refused` records the closed reason/category, refusal digest,
  evidence-category count, zero action count, and request-construction phase.
- `lifecycle.branch_selected` retains its existing data and adds action count,
  request/refusal presence, request digest or refusal reason, and zero failed
  predicates.
- `execution.failed` records a lifecycle contract validation failure with sorted
  closed predicate names, count, selected command, action count, and request/refusal
  presence.

Exact action IDs remain in the authoritative lifecycle/request document, not typed
event payloads.

## Deterministic predicate diagnostics

`external_authority_branch_predicate_failures()` projects only the approved closed
predicate vocabulary and returns sorted unique values. The same function feeds the
semantic validator, structured failure event, and text log, preventing diagnostic
names from drifting away from actual validator predicates.

## Text logs

The lifecycle completion log now includes command, branch/capacity classification,
action count, request/refusal presence, request digest or refusal reason, and sorted
failed predicates. Constructed-document failure emits a separate error before the
validation exception escapes. The shared formatter supplies the established
`✨🐶` prefix and contextual run/function/state fields in configured runtimes.

No prompt, binding, authorization document, provider body, subject data, or secret
is logged.

## Failure isolation and privacy tests

Provider-free tests prove:

- success emits request-selected then branch-selected in order;
- truthful construction refusal emits refused then branch-selected;
- two injected contradictory fields emit one sorted two-predicate failure event;
- the same predicate names appear in captured text logging;
- a sink that raises on every event does not prevent a valid inspection;
- failed sinks do not alter run or snapshot bytes;
- a unique protected sentinel in native state appears in neither inspection bytes
  nor captured logs; and
- all cases make zero provider calls.

## Verification

- Observability/investigation/events/lineage group: 34 passed.
- Contract/lifecycle consumer/closeout group: 55 passed, 5 skipped.
- Provider-pending capacity group: 29 passed.
- Total focused: 118 passed, 5 environment-dependent schema checks skipped.
- Python compilation: passed.
- `git diff --check`: passed.
- Provider calls/spend/retained workspace access: 0 / USD 0 / none.

## Gate

PASS. Diagnostics explain branch selection and exact validator predicates without
becoming authority or creating a new failure mode.

