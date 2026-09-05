# Slice 3 — Durable runtime wiring

## Implemented boundaries

- `save_state()` compares the previously durable subject evidence with the
  newly persisted state and emits stage/validation summaries only for newly
  durable classifications.
- Polish covers accepted, improved-partial, rejected, no-change, error, and
  budget-skipped outcomes without logging edit paths or prose.
- Qualitative review covers completed critic/candidate dispositions and typed
  errors while excluding target paths and provider bodies.
- `publish_native_execution_result()` emits publication evidence only after the
  result, snapshot, and receipt seal is complete. Interrupted receipt repair
  emits the same projection after repair succeeds.
- The run reporter recognizes all three events and places stage/validation
  evidence in the local-work lane and publication evidence in the checkpoint
  lane.

## Important semantic correction

The initially proposed `native_terminal_evidence_summary` name was rejected
during implementation. The native writer also publishes provider-pending,
continuation, and authority-wait results. The final name is
`native_publication_evidence_summary`, and it carries explicit result schema,
outcome, and cause. Sealing alone never implies terminality.

## Route boundary

- Exact interactive and Batch coordinators share `finalize_subjects()` and the
  persisted subject evidence adapter.
- Bounded finalization has a distinct public/native shape and no equivalent
  optional polish report pair. It is not force-fit into the exact adapter;
  route-independent sealed-publication evidence still applies.
- Creative retry retains the existing `authoring_attempt_*` traces because its
  pass-attempt lineage is distinct and already exposes accepted/rejected/error
  progress. It is not mislabeled as an optional-stage record.

## Verification

Focused observability, reporter, optional-stage adoption, polish authority,
native transition, and mixed-custody qualification matrix:

- 58 passed;
- 1 expected optional-schema skip;
- zero provider/network/R2/retained-QA activity.
