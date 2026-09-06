# Structured Sparkle-Dog Logging Sprint 1 Plan

## Status

Planned. Slice 0 may begin after owner review. Runtime mutation pauses at
Voof-paws 1 after the current surface and v1 shape are frozen.

## Objective

Replace SBE's pipe-delimited ordinary worker trace lines with one-object-per-line
structured JSON while preserving readable `✨🐶` messages, privacy, non-authority,
failure isolation, historical-log readability, and current command transports.

The operational success condition is that Better Stack or another JSON-aware
sink can query exact correlation and decision fields without extracting them
from prose, while existing investigations can still read old retained logs.

## Frozen safety principles

1. Logs are diagnostic observations, never transition authority.
2. Public command results and sealed/checkpointed evidence outrank logs.
3. Application stderr and typed execution-event JSONL remain distinct streams.
4. Authoritative stdout formats do not change.
5. Missing identity is null/absent, never inferred or replaced with another ID.
6. A logging serialization or sink failure cannot fail native work.
7. No prompt, provider response body, authorization secret, credential, or
   protected workspace content may enter the structured record.
8. One physical line contains exactly one complete JSON record.

## Proposed v1 record direction

The exact closed shape is frozen in Slice 1, but the starting design is:

```json
{
  "schema_version": "astrowoof.sbe_worker_log.v1",
  "timestamp": "2026-09-06T12:34:56.789Z",
  "level": "INFO",
  "message": "✨🐶 lifecycle selected: provider reconciliation remains due",
  "logger": "astrowoof_natal_authoring.lifecycle",
  "function": "inspect_lifecycle",
  "correlation": {
    "api_run_id": null,
    "native_run_id": "run_...",
    "subject_id": null,
    "invocation_id": "inv_...",
    "action_id": null,
    "response_id": null,
    "checkpoint_id": null
  },
  "payload": {
    "current_state": "WAITING_FOR_RESPONSE",
    "checkpoint_generation": 11,
    "branch": "provider_reconciliation",
    "outcome": "continue_local_cycle"
  },
  "producer": {
    "service": "sbe-worker",
    "host_id": "...",
    "runtime_version": "0.4.x"
  }
}
```

The implementation must not obtain structured fields by reparsing `message`.
Call sites or bound logging context supply them explicitly.

## Slice 0 — Current-path characterization and field census

### Goal

Map every production logging transport and determine which correlation/decision
fields are actually available at each important boundary.

### Work

1. Trace logging configuration for all public CLIs and coordinator entrypoints.
2. Separate stderr application logs, stdout command results, stdout execution
   events, file JSONL events, and API-relayed stderr.
3. Inventory all logging-context bindings and high-value lifecycle/provider/
   checkpoint/terminal call sites.
4. Produce a field availability matrix for API run, native run, subject,
   invocation, action, response, checkpoint, branch, outcome, generation, and
   runtime version.
5. Characterize exception/multiline behavior and Render's raw-line envelope.
6. Freeze the existing run reporter assumptions and compatibility surface.
7. Write provider-free baseline tests for current pipe output and transport
   separation before changing format.

### Deliverables

- `SLICE 0 - LOGGING SURFACE AND FIELD CENSUS.md`
- `EVIDENCE.md`
- `LOG.md`

## Slice 1 — Structured record and privacy contract

### Goal

Freeze one bounded v1 application-log shape and its migration behavior.

### Work

1. Choose exact required, nullable, and optional keys.
2. Define field semantics, especially API versus native run identities and
   provider response versus action identities.
3. Define producer/version identity and timestamp semantics.
4. Define bounded payload value types and prohibited names/content.
5. Define exception serialization without multiline framing breakage.
6. Decide whether JSON becomes the immediate default or is introduced behind a
   short-lived explicit format switch; do not maintain two defaults indefinitely.
7. Define API relay expectations and Better Stack example queries.
8. Define parser auto-detection for old pipe records and new JSON records.

### Gate — Voof-paws 1

Review the field census, schema shape, privacy rules, default/migration choice,
and API relay compatibility before runtime implementation.

## Slice 2 — Formatter and context implementation

### Goal

Implement isolated, deterministic JSON stderr emission.

### Work

1. Add a JSON `logging.Formatter` using stable serialization and UTC timestamps.
2. Extend context binding only with approved, semantically distinct fields.
3. Preserve stdlib logging argument interpolation and levels.
4. Normalize absent fields to JSON null or exact contract omission.
5. Encode exception type/message/traceback safely as JSON values on one line.
6. Preserve foreign root handlers and current reconfiguration behavior.
7. Prove serialization fallback is bounded, visible, and cannot recurse or fail
   the command.

### Tests

- exact top-level and nested key shape;
- Unicode `✨🐶` preservation;
- null/unknown context;
- scoped context restoration and thread/task isolation;
- exception and newline handling;
- non-JSON extra/prohibited content rejection or safe omission;
- logging failure isolation;
- stdout remains untouched.

## Slice 3 — High-value decision-point adoption

### Goal

Make the fields that repeatedly required workspace downloads directly queryable
at the decisive boundaries.

### Priority call sites

1. Workspace restore/initial fingerprint.
2. Lifecycle branch selection and final returned disposition.
3. Provider create entry, durable identity, retrieval observation, and adoption.
4. Checkpoint mutation/publication generation and snapshot digest.
5. External-authority request/grant/intent/refusal identities.
6. Terminal/review result publication and custody summary.
7. CLI exit and whether mutation/publication/provider I/O occurred.

### Rules

- Prefer explicit structured `extra`/helper data over message parsing.
- Keep payloads bounded to counts, enums, identifiers, timestamps, and digests.
- Do not duplicate complete public documents into logs.
- Log both selected decision and positive permission where ambiguity would
  otherwise remain.

### Gate — Voof-paws 2

Review the emitted field coverage against recent investigation questions and
privacy sentinels before parser migration.

## Slice 4 — Reporter/parser dual-format migration

### Goal

Preserve old-log analysis while making JSON the preferred input.

### Work

1. Auto-detect valid structured records before trying the historical regex.
2. Map both formats into one internal observation model.
3. Prefer native JSON fields; never parse the JSON `message` to override them.
4. Retain unknown-event and malformed-line accounting.
5. Add mixed-file, chronological-ordering, duplicate-line, truncated-JSON, and
   pipe-regression fixtures.
6. Update the run-reporter playbook with Better Stack export/query examples.

## Slice 5 — Production-boundary and sink qualification

### Goal

Prove the format works through public commands and the API-style stderr relay.

### Work

1. Exercise representative lifecycle, reconciliation, v2 dispatch, refusal,
   terminal, and failure paths through public CLIs.
2. Capture stderr exactly as a process supervisor/API relay would.
3. Parse every structured line and verify correlation continuity.
4. Verify command stdout/result files and execution-event JSONL are unchanged.
5. Verify privacy sentinels across raw logs, parsed reports, and fixtures.
6. Produce a sanitized Better Stack-ready example bundle and query cookbook.

### Gate — Voof-paws 3

Cross-repository review of relay compatibility and installed qualification.

## Slice 6 — Regression, documentation, and release preparation

1. Run focused logging, execution-event, reporter, lifecycle, reconciliation,
   and v2 CLI suites.
2. Use the broad suite because the formatter is shared across public commands;
   escalate to the full suite if implementation changes command wiring beyond
   logging/context injection.
3. Run `git diff --check` and privacy scans.
4. Update operator/run-reporter documentation and migration notes.
5. Follow the release playbook, including version alignment before expensive
   tests and deterministic wheel builds from the release-lock commit.
6. Obtain separate explicit owner approval before tag/publication/deployment.

## Acceptance criteria

1. Every ordinary SBE worker trace is valid one-line JSON.
2. The readable `✨🐶` marker and useful human message remain.
3. Known identities are queryable as native fields; unknown ones are not
   inferred.
4. Critical lifecycle decisions expose bounded structured outcomes and positive
   permissions.
5. No sensitive payload/content enters the logs.
6. Logging failures cannot alter execution.
7. Command results and typed execution events retain their existing transports
   and authority.
8. The run reporter accepts historical pipe, new JSON, and mixed inputs.
9. Public-command/relay qualification proves fields survive the real boundary.
10. Documentation includes Better Stack query examples and migration guidance.

## Review points

| Point | Question |
|---|---|
| Voof-paws 1 | Is the v1 shape semantically exact, private, and relay-compatible? |
| Voof-paws 2 | Do the chosen decision points answer recurring investigations without workspace download? |
| Voof-paws 3 | Does public-command and API-style relay qualification preserve authority and framing? |
| Final | Is regression evidence proportionate and the immutable release ready? |

