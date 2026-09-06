# Slice 1 — Structured record and privacy contract

## Decision

The ordinary SBE application-log contract is frozen as
`astrowoof.sbe_worker_log.v1`. Runtime emission has not changed yet.

The normative contract is the combination of:

- `sbe-worker-log.v1.schema.json`, which closes the record envelope; and
- `sbe-worker-log-event-catalog.v1.json`, which closes each event payload.

The Python reader/validator enforces both resources plus privacy and physical
line constraints. A generic payload object is not an extension point: an event
must be named in the catalog, and its payload may contain exactly that event's
required/optional fields.

## Exact envelope

Every key is required. Nullable values are JSON `null`, never `"-"`,
`"unknown"`, an inferred identity, or an omitted key.

| Field | Meaning |
|---|---|
| `schema_version` | Exact `astrowoof.sbe_worker_log.v1`. |
| `record_type` | Exact `application_log`; never an execution event or command result. |
| `timestamp` | Log-observation time in UTC RFC 3339 with exactly millisecond precision. |
| `level` | Closed stdlib level vocabulary. |
| `event_name` | Closed catalog event identity supplied by the call site/formatter, never parsed from prose. |
| `message` | Sanitized, bounded human message beginning `✨🐶 `. |
| `logger`, `function` | Bounded source metadata. |
| `current_state` | Native descriptive state if known; nullable and not API disposition authority. |
| `correlation` | Exact always-present identity object. |
| `payload` | Event-catalog-bounded diagnostic facts. |
| `producer` | Service, host, and installed SBE release identity. |
| `exception` | Null or the closed sanitized diagnostic shape. |

## Correlation semantics

The always-present keys are:

- `api_run_id`: caller-supplied API identity only. SBE must never derive this
  from native state, subject identity, paths, or message prose.
- `native_run_id`: SBE native run identity; replaces the ambiguous old
  formatter label `run_id`.
- `subject_id`: exact subject/member identity when the boundary knows it.
- `invocation_id`: API/native command invocation correlation identity.
- `action_id`: exact SBE paid-action identity.
- `provider_operation_id`: durable provider Response/Batch identity; this is
  deliberately not named generic `response_id`.
- `checkpoint_object_id`: exact public checkpoint object identity if supplied
  or known at the boundary.

Missing identities remain null. Correlation values are observations and do not
authorize joins, replay, mutation, provider I/O, or API settlement.

## Event vocabulary

The first catalog covers the fallback `application_message` plus the existing
high-value bounded projections: workspace fingerprint, native state, lifecycle
decision, stage evidence, validation evidence, native publication, and command
exit. Slice 3 may add catalog entries only with explicit bounded fields and
tests; it may not introduce a generic arbitrary payload event.

`native_decision_summary` includes `positive_permission` separately from its
descriptive branch/outcome. `command_exit` separately records mutation,
publication, and provider-I/O status. These names do not themselves grant
authority; they make the diagnostic observation unambiguous.

## Privacy and failure behavior

1. Strings are single-line and bounded; containers have bounded depth, size,
   key length, and item count.
2. Prompt/payload bodies, raw provider responses, credentials, authorization
   secrets, source archives, and workspace paths are prohibited.
3. Exception output is limited to class, optional classified code, a 16-hex
   fingerprint, and the existing sanitized one-line message. Raw traceback and
   raw `exc_info` are excluded from v1.
4. Existing message sanitization remains mandatory. JSON framing is not a
   confidentiality mechanism.
5. Formatter/serialization/sink failure must remain isolated from native work;
   Slice 2 will prove a bounded fallback that cannot recurse.
6. Scope is only records emitted through SBE's configured application handler.
   Foreign/root handlers, stdout, execution-event JSONL, command results, and
   sealed artifacts are unchanged.

## Migration decision

JSON becomes the ordinary SBE-handler default in the release containing this
work. There will not be two indefinite defaults. Historical pipe records remain
supported by the reporter: it first accepts a recognized v1 JSON application
record and otherwise tries the old pipe parser. JSON `message` prose can never
override native JSON fields.

## API relay matrix to qualify in Slice 5

| Invocation | Current stderr behavior | Required qualification |
|---|---|---|
| provider reconciliation | API relays every child stderr line verbatim | One SBE JSON object arrives unprefixed, unwrapped, unescaped, and unsplit. |
| ordinary resume | Inherits stderr only when its event-stream configuration enables it; otherwise may use `DEVNULL` | Qualify both configured behaviors and name suppression explicitly. |
| v2 dispatch | Inherits stderr only when its event-stream configuration enables it; otherwise may use `DEVNULL` | Qualify both configured behaviors and name suppression explicitly. |

No acceptance statement may generalize the reconciliation relay to every API
subprocess route.

## Better Stack query intent

Once API relay qualification is complete, operators should be able to filter
directly by `correlation.api_run_id`, `correlation.native_run_id`,
`correlation.subject_id`, `correlation.action_id`,
`correlation.provider_operation_id`, `event_name`, `payload.outcome`, and
`producer.runtime_version`. Until then, existing pipe logs remain searchable as
text and no sink behavior is assumed.

## Evidence

The contract/resource suite and the pre-existing logging, execution-event, and
run-reporter suites pass together: 29 tests. No runtime formatter or call site
has changed, provider/network activity is zero, and command transports are
untouched.
