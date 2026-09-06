# Slice 0 — Logging Surface and Field Census

## Disposition

The migration is feasible at one shared formatter boundary, but useful
structured correlation requires more than replacing the format string.
SBE has nine public CLI/configuration call sites using the same application
logger and approximately 169 ordinary logging calls. The high-value diagnostic
helpers already compute bounded dictionaries before flattening them into prose,
so they are the safest first structured-payload adopters.

No runtime format has changed in Slice 0.

## Current transport map

| Surface | Stream/storage | Current representation | Authority |
|---|---|---|---|
| Ordinary application trace | stderr | `✨🐶` pipe-delimited text | diagnostic only |
| Lifecycle/default command result | stdout | one JSON document | public command authority |
| Lifecycle `--stdout-jsonl` | stdout | execution-event envelopes plus command-result envelope | typed public transport |
| v2 `--events-stdout-jsonl` | stdout, with result written to `--output` | execution-event envelopes | diagnostic typed events; output file holds result |
| `--events-jsonl` | caller-selected file outside workspace | execution-event JSONL | diagnostic typed events |
| API worker relay | captured subprocess stderr | currently relayed verbatim | diagnostic only |
| Native result/receipt/checkpoint | workspace files | closed JSON contracts | durable transition evidence |

The JSON application-log migration belongs only in the first and sixth rows.
It must not change or combine the other transports.

## Configuration coverage

The common `add_logging_arguments()` / `configure_logging_from_args()` boundary
is used by:

- semantic closure / ordinary authoring;
- bounded admission and bounded run;
- lifecycle inspection/continuation;
- external-authority v2 execution;
- native transition and result-availability commands;
- repair;
- response diagnostics.

The single shared handler means one formatter can cover normal worker commands.
Direct library callers that never configure logging remain governed by their
host application's handlers, as they should.

## Existing context and availability

| Desired field | Available now? | Current source | Census decision |
|---|---|---|---|
| `host_id` | yes | environment/CLI | producer field |
| `invocation_id` | yes | environment/CLI or native publication | correlation field |
| `native_run_id` | yes | bound from `run.json` | rename current ambiguous `run_id` in JSON |
| `api_run_id` | not generally | not supplied by current SBE CLI contract | nullable; API may pass later, never infer |
| `subject_id` | locally at stage call sites | currently message/helper argument | scoped correlation when exact |
| `action_id` | locally at provider/authority call sites | currently messages and event correlations | scoped correlation when exact |
| `response_id` | locally after durable provider identity | currently messages/summaries | scoped correlation only after known |
| `checkpoint_id` | sometimes | checkpoint metadata/summary | nullable correlation |
| `checkpoint_generation` | sometimes | workspace/checkpoint summary | structured payload |
| `snapshot_sha256` | yes at validation/publication boundaries | computed evidence helpers | structured payload |
| `current_state` | yes | context bound from native state | structured payload |
| `branch` / `outcome` | yes at decision boundaries | lifecycle/result dictionaries | structured payload, not global context |
| `runtime_version` | available to CLI | package `__version__` | required producer field |
| `logger` / `function` | yes | stdlib `LogRecord` | required diagnostic fields |

## High-value payload census

`trace_observability.py` already builds bounded, privacy-reviewed values for:

- workspace fingerprint and snapshot/checkpoint identity;
- native action/provider/custody summary;
- lifecycle/command decision and positive permission;
- stage adoption and acceptance evidence;
- final validation/lint evidence;
- native result/receipt publication evidence;
- CLI exit, authoritative transport, and sanitized exception fingerprint.

Today each helper renders its value into a long `key=value` message. Slice 2
should pass the already-computed dictionary as structured record data and retain
a shorter readable message. It must not parse its own rendered prose back into
fields.

## Questions recent investigations repeatedly asked

The following facts account for most checkpoint downloads and manual trace
reconstruction. They should be queryable when known:

1. Which exact native run, invocation, action, subject, and provider response
   does this observation describe?
2. What checkpoint generation, state revision, snapshot digest, and checkpoint
   basis were inspected or published?
3. Was the workspace valid at entry, and did this command mutate or publish it?
4. Which branch was selected, why, and what positive operation was permitted?
5. What provider custody classes and bounded action inventory remained?
6. Was provider create entered, was an identity durable, or was work only
   retrieved/adopted?
7. Which local operation was advertised or consumed, including its stable key?
8. Was a terminal result actually sealed, with which result/receipt identities
   and custody summary?
9. What did the CLI return, by which authoritative transport, and with what
   exit/failure classification?
10. Which SBE release and producer instance emitted the observation?

These become the Slice 1 field-selection test. Not every record carries every
field; unknown values must remain null/absent.

## Current weaknesses characterized

1. `run_id` currently means native run identity but its name is ambiguous across
   the API relay.
2. Subject, action, response, checkpoint, branch, and outcome values are mostly
   embedded in prose instead of bound context.
3. Runtime version is not present on every ordinary record.
4. The logger name is not rendered, although the function name is.
5. `-` represents several kinds of absence in text.
6. Exception tracebacks can span physical lines, which prevents strict
   one-record-per-line ingestion.
7. The run reporter recognizes events by reparsing the first message token and
   maintains a large prose-field allowlist.
8. JSON execution-event envelopes and pipe application logs can coexist in one
   capture; their distinction is implicit rather than typed at the application
   record level.

## Baseline characterization

Two tests now explicitly freeze that, before migration:

- ordinary application logs go to stderr and leave stdout clean;
- ordinary application logs are not execution-event envelopes.

The existing tests continue to freeze the human marker, timestamp/context
prefix, level filtering, and handler replacement behavior. Execution-event
tests separately freeze JSONL sink behavior.

## Slice 1 recommendations

1. Use `astrowoof.sbe_worker_log.v1` and an explicit
   `record_type=application_log` discriminator.
2. Require timestamp, level, message, logger, function, correlation, payload,
   and producer objects.
3. Use semantically explicit `native_run_id`; add nullable `api_run_id` only as
   caller-supplied context.
4. Keep correlation fields closed and nullable; keep event-specific data in a
   bounded payload.
5. Require `producer.runtime_version` and `producer.service`; retain host identity
   as bounded producer metadata.
6. Preserve `✨🐶` at the start of `message`, not outside the JSON object.
7. Serialize exception information as bounded fields and escaped newline text.
8. Make JSON the eventual default, with any compatibility switch explicitly
   temporary and tested.
9. Extend the reporter to prefer JSON fields and fall back to the historical
   parser without allowing prose to override structured values.

## Gate

Ready for the Slice 1 contract freeze and Voof-paws 1 review. No formatter,
context, call-site, parser, or public-command behavior has changed yet.

