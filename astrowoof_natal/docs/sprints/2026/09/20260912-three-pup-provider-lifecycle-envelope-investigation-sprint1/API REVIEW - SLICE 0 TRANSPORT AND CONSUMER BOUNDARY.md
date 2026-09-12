# API Review — Slice 0 Transport and Consumer Boundary

## Decision

Approved. Slice 0 establishes an API-owned, closed-stream demultiplexing
defect introduced by API commit `c1b4c3a05ea6e5d128650a98ed4a3d18b493320b`.

The API production reconciliation invocation requests
`--events-stdout-jsonl`; the exact installed SBE 0.4.59 public command then
lawfully emits four `sbe.execution_event.v1` diagnostic envelopes before its
one ordinary `sbe.command_result.v1` reconciliation envelope. The API capture
implementation added in that same commit requires every JSONL line to be a
command-result envelope, so it rejects ordinal 1 before the valid ordinary
result can be selected and validated.

The API-side source review independently confirms that exact every-line test:
`_ReconciliationStreamCapture.reconciliation_output` rejects any envelope
whose `schema_version` is not `sbe.command_result.v1` or whose
`envelope_type` is not `command_result`.

## Answers to Voof-paws 1

1. **Yes.** `c1b4c3a` introduced the closed-stream consumer bug. The
   provider-free replay establishes causality; the source/history boundary
   explains why the replay reaches the observed production error.
2. **Yes.** Waive all three retained R2 HEAD/GET pairs. Generation 2 predates
   the failed reconciliation subprocess and cannot establish or refute the
   rejected stdout ordering. The authorized objects should not be read merely
   because they are available.
3. **Yes.** API owns the correction and the production-path regression suite.
   SBE's existing public released command is the emitting surface and has
   supplied sufficient provider-free proof.
4. **No additive SBE release is currently justified.** A checked-in or
   package-qualified mixed-envelope fixture may be useful later if it adds
   durable cross-repository regression value, but it is not a prerequisite to
   repairing this API consumer. Do not version-bump SBE merely to duplicate
   the already reproducible 0.4.59 public command behavior.

## Approved API correction boundary

Implement a closed demultiplexer in the reconciliation capture only:

- allowlist known `sbe.execution_event.v1` envelopes as diagnostics and retain
  them only for bounded observability;
- allowlist `sbe.command_result.v1` envelopes as the sole transition authority;
- require exactly one ordinary
  `astrowoof.provider_reconciliation_cycle_result.v0.2` result;
- retain the existing terminal-review/delivery companion cardinality,
  precedence, and schema checks; and
- fail closed on malformed JSON, invalid envelope structure, unknown envelope
  schema/type, unknown command-result schema, duplicate ordinary results, or
  conflicting/duplicate companions.

This must **not** become a permissive rule that ignores arbitrary stdout.
Diagnostic execution events must never become lifecycle transition authority.
No provider operation may be repeated due to this consumer-side repair.

## Scope and next gate

No R2 access, QA resume, reconciliation, recovery, reset, deployment, or paid
activity is approved by this review. The suspended QA SBE worker remains
suspended.

The next artifact should be the API correction plan and provider-free
production-path tests covering the exact five-record stream plus all current
negative cases. A joint fixture can be reconsidered only if API implementation
shows the public command alone is insufficient to preserve the exact contract.
