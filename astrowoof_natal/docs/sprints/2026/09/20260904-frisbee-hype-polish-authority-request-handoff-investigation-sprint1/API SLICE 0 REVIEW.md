# API Review — Slice 0

## Decision

**Approved to begin Slice 1 contract/implementation work**, with the two
identity guardrails below made explicit in the frozen invariant and positive /
negative fixture plan.

The paired logs, source topology, and provider-free projection establish the
causal boundary without an R2 read: `FINAL_QA_WARN` is a legitimate input to
enabled polish, but `finalization_conclusion()` currently treats that same
provisional state as a globally dominant terminal-review conclusion. That
suppresses the exact ordinary-v2 request after SBE has already prepared the
polish action. API must not synthesize the missing request.

The stated separation remains correct:

- a genuinely committed terminal-review conclusion remains terminally dominant;
- a warning without an elected pending optional action remains a valid
  review-closeout; and
- generic resume/reconciliation cannot create or infer provider authority.

## Required Slice 1 precision

### 1. Make provisionality exact and subject-local

Do not define provisional `FINAL_QA_WARN` as merely “a prepared action exists
somewhere in the ledger.” The exception must require one exact current polish
attempt for the same subject, whose `paid_action_id` matches one exact current
ledger action, whose binding is `stage=polish`, and whose durable state is an
eligible pre-provider state. The subject/action/binding relation—not the
presence of any `PREPARED` record—must beat the provisional finalization
conclusion.

That prevents a stale action, a different subject's polish action, an unrelated
optional action, or an already provider-bound/completed action from masking a
real terminal review.

### 2. Freeze the negative matrix beside the positive witness

In addition to the currently captured warning-with-no-polish negative, add
provider-free negative controls for at least:

- mismatched subject versus prepared polish action;
- mismatched attempt `paid_action_id` versus ledger action;
- stale/non-eligible action state; and
- a genuinely committed terminal-review conclusion.

Those controls should prove the reader emits no request and preserves terminal
dominance in each case. The positive witness must then expose exactly one
ordinary-v2 request with the matching action identity and current observation /
snapshot basis.

## API ownership confirmation

Once SBE exposes that exact request, API can evaluate it at its normal
single-writer external-authority admission boundary. API should receive, bind,
authorize, and later intake only that request; it must not create a successor
or reclassify a requestless `AWAITING_SPEND_AUTHORIZATION` workspace.

No retained Frisbee/Hype recovery, provider work, R2 access, API mutation, or
release activity is approved by this review.
