# Slice 0 Baseline: Required Denial Without Native Terminalization

Status: complete; pending review.

## Finding

The API report is reproduced. A valid providerless denial resolves the exact paid
action but does not resolve the parent run's control state.

For one authorized required creative retry and for two such actions denied in one
atomic batch:

- requiredness is true at the locked pre-denial observation;
- denial with `external_authority_denied` applies;
- every target becomes `DENIED_PROVIDERLESS` and retains authorization provenance;
- exact replay is idempotent;
- requiredness/provider continuation becomes false;
- the parent status remains `AUTHORING`;
- local dependency remains `retry_preparation / authoring_continuation`;
- inspection remains nonterminal; and
- closeout returns `continuation_required` with no unresolved action IDs.

A real bounded paid-action fixture exhibits the same shared lifecycle seam. After
denial, normal resume raises `AwaitingSpendAuthorization` again for the denied
required action. The provider double records zero submissions, confirming that
provider safety holds while the worker-loop condition remains.

## Diagnosis confidence

High. The action projection and denial protocols behave coherently; the missing
piece is a durable run-level consequence interpreted consistently by the runner,
public state, inspection, and closeout. A closeout-only dependency filter would
hide one symptom but leave normal resume incorrect.

## Slice 1 input

Freeze a state-machine contract covering:

- `BUDGET_EXHAUSTED` plus external-authority cause versus a distinct policy stop;
- required versus optional denial;
- newly prepared versus authorized-unconsumed required actions;
- single versus batch transition evidence;
- pre-delivery versus accepted-delivery precedence;
- runner short-circuit, public outcome, terminal/quiescence, and closeout mapping;
- exact retained-0.4.1 recovery; and
- distinct handling of `reservation_unavailable` if it is retryable rather than a
  final global refusal.

No terminal vocabulary or production behavior is implemented in Slice 0.
