# Slices 2–3 — Formatter and decision-point adoption

## Result

The configured SBE application handler now emits
`astrowoof.sbe_worker_log.v1` as one JSON object per stderr line. The existing
bounded observability adapters now attach their event names and payloads
explicitly; the formatter never reparses message prose to manufacture fields.

## Context implementation

The handler carries separate nullable fields for API run, native run, subject,
invocation, paid action, provider operation, and checkpoint object identity.
The API run value is accepted only from `--api-run-id`,
`ASTROWOOF_API_RUN_ID`, or explicit context binding. Existing `run_id=` calls
remain a compatibility alias for native run identity.

Context managers restore every field and a new thread receives the declared
contextvar defaults rather than the parent's mutable bindings. Foreign root
handlers remain installed during SBE reconfiguration.

## Explicit structured events now emitted

- `workspace_fingerprint`
- `native_state_summary`
- `native_decision_summary`
- `native_stage_evidence_summary`
- `native_validation_evidence_summary`
- `native_publication_evidence_summary`
- `command_exit`
- `finalization_contract_invalid`
- `finalization_contract_error_not_sealed`

These cover the recurring investigation questions at restore, lifecycle
selection, custody/action inventory, optional-stage adoption, deterministic QA,
sealed-result publication, deterministic finalization refusal, and CLI exit.
The existing trace helpers are already called by exact, bounded, lifecycle,
native-transition, reconciliation/closure, and v2 public boundaries.

`native_decision_summary` records a distinct diagnostic
`positive_permission`: provider retrieval, native local work, external-authority
request, terminal delivery, scheduler release, or none. It is derived only from
the validated public decision passed to the helper and remains diagnostic—not
transition authority.

`command_exit` has explicit mutation, publication, and provider-I/O status
fields. Existing callers produce `unknown` until their exact boundary adopts
those optional arguments; this is honest rather than inferred.

## Safety behavior

- Message and exception secrets are redacted before serialization.
- Newlines are normalized; raw traceback is excluded.
- Payloads are catalog-closed and bounded.
- Invalid event extras produce exactly one valid
  `logging_serialization_failed` record without recursive logging or command
  failure.
- Null structured identities are never replaced from message prose.
- Stdout, command-result files, execution-event JSONL, sealed artifacts, and
  native state are unchanged.

## Reporter bridge

Because JSON is now the handler default, the parser has the minimal recognized
v1 path needed to consume these records without breaking the existing
trace-observability regression. It validates the envelope and uses only native
JSON payload/correlation fields. It does not parse `message` to override them.

Slice 4 still owns full migration hardening: mixed files, outer host prefixes,
malformed/truncated JSON, duplicates, ordering, unknown records, and historical
pipe regression fixtures.

## Evidence

The focused trace-observability, qualification, formatter,
structured-contract, execution-event, and run-reporter suite passes: 52 tests,
with two expected optional-schema skips. Provider/network/R2 activity is zero.

This is Voof-paws 2. API relay visibility is deliberately not claimed: Slice 5
must separately qualify reconciliation's verbatim relay and ordinary-resume/v2
configured inheritance or suppression.
