# Pre-sprint huddle — log the evidence at the decision, not the whole workspace

## Design stance

The existing `native_decision_summary` answers **which branch won**. This sprint
adds the bounded evidence needed to answer **why that branch was justified**.

The preferred implementation is a small closed family of projections sharing
one sanitizer and one bounded-inventory policy. It should not become a second
schema system or a free-form dump of whatever happens to be nearby.

## Proposed event family

### `native_stage_evidence_summary`

Emitted after a stage-specific consumer has durably classified completed
provider evidence. Candidate fields include stage, attempt number, action and
provider identity, typed outcome, findings before/after, bounded reason codes,
and sanitized exception classification.

### `native_validation_evidence_summary`

Emitted after deterministic validation/lint/finalization has produced the
report that the next decision consumes. Candidate fields include structural
status, acceptance status, warning/error/rejection counts by code, report
digests, and explicitly bounded/truncated inventories.

### `native_publication_evidence_summary`

Emitted from the native writer/publication boundary. It joins the explicit
outcome/cause to final validation evidence, optional-stage history, action and
custody totals, lifecycle posture, and exact public result/receipt/checkpoint
identities. A sealed publication is not presumed terminal.

### Existing summaries

Enrich `native_decision_summary` and refusal traces only where required to join
the new evidence summaries. Avoid duplicating the same large projection in
multiple events.

## Central guardrails

- Project only already-validated native/public evidence.
- Closed code vocabularies where available; unknown values remain explicit.
- Counts and deterministic digests for large inventories; bounded prefixes only
  when individual identifiers materially aid diagnosis.
- Logging failure remains isolated and cannot affect native behavior.
- Protected-sentinel tests cover every new event and exception path.
- Event names/fields remain machine-parseable by the run reporter.
- The public artifact named by a trace always outranks the trace itself.

## Expected escalation ladder

1. Read sanitized trace summaries.
2. Read the exact public result/receipt/report named by the trace.
3. Use packaged readers or the offline inspector.
4. Restore a checkpoint only for missing/contradictory evidence or byte-level
   forensic proof.
