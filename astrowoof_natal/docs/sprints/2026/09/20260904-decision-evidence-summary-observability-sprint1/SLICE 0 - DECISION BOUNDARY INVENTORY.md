# Slice 0 — Production decision-boundary inventory

## Finding

The existing observability layer covers control-flow identity well. The missing
surface is bounded evidence classification at three durable boundaries. Adding
events elsewhere would mostly duplicate existing state and increase noise.

## Boundary map

| Boundary | Durable fact available | Current trace | Decision |
| --- | --- | --- | --- |
| Optional-stage consumer | Completed provider evidence has been parsed and classified into a native attempt/review state | Stage-specific prose logs, state summary later | Add `native_stage_evidence_summary` after classification |
| Deterministic validation/lint | Exact report consumed by finalization is available | Counts sometimes appear in nearby prose logs | Add `native_validation_evidence_summary` after report validation |
| Lifecycle selector | Validated public inspection and selected branch | `native_decision_summary` | Retain; add only evidence-summary join digests if needed |
| External-authority dispatch/refusal | Validated result plus provider-I/O assertion | Typed command result and decision/exit traces | Retain; add typed evidence classification/join only where absent |
| Native publication writer | Result, snapshot, receipt, action/custody inventory, and subject evidence are simultaneously knowable | Publication and decision summaries omit evidentiary substance | Add `native_publication_evidence_summary` after complete seal; do not infer terminality |

## Optional-stage placement

### Polish

`polish_subject()` owns the durable distinctions that investigations repeatedly
need:

- `POLISH_ACCEPTED`;
- `POLISH_IMPROVED_PARTIAL`;
- `POLISH_REJECTED`;
- `POLISH_NO_CHANGE`;
- `POLISH_ERROR`; and
- `POLISH_SKIPPED_BUDGET_EXHAUSTED`.

It also owns the before/after warning/error counts, report paths, action/provider
metadata, edited-field count, and bounded exception. Emit only after the attempt
record has been updated. Never log editable paths or replacement prose.

### Qualitative critic/candidate

The qualitative path owns `NO_ELIGIBLE_FINDINGS`, `DIAGNOSIS_COMPLETE`,
`CANDIDATE_NO_CHANGE`, candidate-ready/rejected outcomes, and
`QUALITATIVE_REVIEW_ERROR`. Emit after the review record reaches one of those
classified states. Target paths and prose remain protected; counts and closed
state/reason values are sufficient.

### Creative retry

Creative retry has a structurally different pass-attempt lineage. Reuse the
same projection vocabulary only after mapping its exact durable attempt record;
do not infer equivalence from the stage name.

## Validation placement

`finalize_subjects()` consumes each subject's exact structural validation and
editorial lint reports. Exact and Batch reconciliation coordinators call this
same boundary; bounded finalization has separate report shapes and must use an
adapter rather than guessed common fields.

Safe useful evidence:

- structural status and error/warning counts;
- lint status and warning count;
- deterministic acceptance status;
- counts by closed error/warning/rejection code;
- report content digests;
- explicit absent/unknown values; and
- a digest of the complete normalized code multiset.

Unsafe or noisy evidence:

- deck prose, excerpts, field contents, prompts, or payloads;
- arbitrary paths from finding details;
- unbounded claim/card/subject inventories; and
- full validation/lint report serialization.

## Terminal placement

`publish_native_execution_result()` is the correct final join boundary. After
the result, workspace snapshot, and receipt have been sealed, it can project:

- exact result/receipt/invocation/checkpoint/snapshot identities;
- native outcome and cause;
- action/provider/custody counts;
- final subject-state distribution;
- final validation/lint classification;
- optional-stage attempt-state distribution and last-attempt summaries; and
- whether detailed evidence artifacts exist.

The event must be emitted after the receipt exists. The current
`native_decision_summary` remains the branch/result summary; publication
evidence should not duplicate its bounded action inventory.

## Field safety classification

| Class | Examples | Treatment |
| --- | --- | --- |
| Safe scalar | stage, attempt number, typed state, status | Emit directly after closed normalization |
| Closed reason code | validation/lint rejection code, terminal cause | Emit bounded counts/distribution |
| Public identity | action ID, provider ID, result/receipt ID | Emit only where correlation is necessary; otherwise count/digest |
| Digest | report, snapshot, checkpoint basis | Emit validated lowercase SHA-256 or `unknown` |
| Bounded diagnostic | exception class and sanitized fingerprint/message | Use the existing sanitizer and length cap |
| Protected | prompt, response body, deck prose, edit values, authorization document | Never emit |
| Private path | absolute workspace/report/payload path | Never emit; use content digest/presence flag |

## Event-volume decision

At most:

- one stage summary per classified optional-stage attempt;
- one validation summary per subject report set actually consumed; and
- one terminal summary per newly sealed result (or an explicitly marked replay
  summary without duplicating evidence inventories).

This is sufficient for the 90% log-first target without converting logs into a
parallel event-sourced state machine.
