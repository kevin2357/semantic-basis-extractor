# Plan — final-QA mixed-custody qualification fixture correction

## Status

Slices 0–1 and Voof-paws 1 complete. Slice 2 source/full-suite qualification is
complete for fresh version `0.4.47`; deterministic wheel and API release-pair
qualification remain.

## Scope and invariants

This is a provider-free fixture/test correction. It MUST NOT weaken terminal
dominance, synthesize an external-authority request after a committed native
finalization conclusion, touch QA/R2/provider state, or change production
lifecycle/dispatch contracts.

The qualification must prove two lawful orderings:

1. a provider identity becomes durable before later final-QA review evidence;
   retained provider custody then selects reconciliation and suppresses terminal
   closeout; and
2. a valid authority request and native dispatch intent become durable before a
   contradictory terminal outer-status spelling appears; dispatch then seals a typed
   `post_intent_lifecycle_contradiction` refusal before payload resolution or
   provider call-entry.

## Slice 0 — reproduce and freeze cause

- Reproduce the API release-pair failure from the source qualification.
- Trace fixture construction through temporal inspection and the v2 request
  builder.
- Prove the checkpoint lacks an authority request because committed finalization
  evidence correctly dominates new qualitative work.
- Record the `0.4.46` test-selection omission separately from runtime semantics.

Exit: exact source failure and causal ordering are recorded without proposing a
production relaxation.

## Slice 1 — correct fixture chronology and regression

- Build the polish request/grant from a coherent pre-finalization checkpoint.
- For the pending case, dispatch once, durably record the scripted provider
  identity, then add final-QA review evidence and prove custody-first lifecycle
  projection selects reconciliation.
- For the refusal case, inject the terminal outer-status contradiction only after the native
  intent checkpoint and prove typed refusal, zero payload resolution, zero
  provider I/O, immutable refusal history, and fresh-authority requirement.
- Add a negative regression proving finalization-first construction cannot mint
  a new authority request.
- Preserve the existing closed mixed-custody v1 receipt surface and
  provider-free guarantees.

Exit: the focused source qualification passes and the old impossible chronology
is explicitly rejected.

## Voof-paws 1 — API review

Pause for API review of the corrected chronology and receipt compatibility. API
should confirm that no release-pair consumer change is needed beyond pinning the
replacement wheel.

## Slice 2 — replacement-wheel release gate

- Select a fresh unused patch version before release-bound testing.
- Run the corrected qualification tests plus terminal-dominance, terminal-review,
  provider-custody, and ordinary-v2 authority/dispatch adjacent tests.
- Run `git diff --check` and inspect the complete tracked/package-data diff.
- Run the full maintained suite because the prior release omitted a transitive
  packaged qualification and confidence must be restored.
- Build the committed source twice with one fixed epoch and require byte-identical
  wheels.
- Install the exact candidate into a clean environment, run `pip check`, and run
  `astrowoof-final-qa-mixed-custody-qa` plus the relevant terminal qualifications.
- Have API rerun the exact Sprint 76 release-pair command against the candidate
  wheel before paid cohort admission.
- Record honestly whether the broad/full suite was omitted.

Exit: owner and API release approval for a fresh immutable wheel, followed by the
canonical tag/publish/download-verification procedure.
