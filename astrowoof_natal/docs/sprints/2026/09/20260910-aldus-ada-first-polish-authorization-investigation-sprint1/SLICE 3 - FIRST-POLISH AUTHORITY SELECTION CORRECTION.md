# Slice 3 — First-Polish Authority Selection Correction

## Outcome

Implemented the approved narrow correction. A subject-level `FINAL_QA_FAILED`
state no longer forces terminal-review posture when the same immutable state
proves one exact, live, eligible interactive first-polish authority request.
The lifecycle projection preserves that request as
`await_external_authority` / `spend_authorization_required` for API decision.

## Fail-closed predicate

The exception applies only when all of these facts agree:

- the run is awaiting spend authorization and has no committed terminal
  transition;
- exactly one action is PREPARED, at stage `polish`, service level
  `interactive`, and outside bounded route/contract families;
- the action has no authorization, provider identity, reported cost, denial,
  negative authorization, or integrity-review evidence;
- the affected subject is `FINAL_QA_FAILED`;
- exactly one matching polish attempt is `SUBMITTED`, names the same paid
  action, and has the exact subject/attempt route; and
- the current request sidecar has the supported schema, same run and state
  revision, and exactly the same action ID and binding.

Missing, stale, mismatched, ambiguous, denied, provider-owned, reported, or
terminal evidence does not enter the exception. Duplicate matching attempts
are ambiguous and likewise remain closed. Existing terminal review,
providerless-denial, ordinary terminal, batch, bounded, and recovery behavior
therefore remains fail closed.

## Files

- `astrowoof_natal/src/astrowoof_natal_authoring/lifecycle.py`
- `astrowoof_natal/tests/test_first_polish_authority_selection_investigation.py`
- `astrowoof_natal/tests/test_suite_manifest.json`

No public schema or fixture changed.

## Alloy impact

Retrospective assessment: no model change or rerun is required. This correction
changes pre-decision authority-selection precedence, not any editorial
decision, attempt, predecessor, materialization, adoption, continuity,
selection, delivery, or ownership relationship represented by the model. See
[0.4.58 and 0.4.59 Alloy impact assessment](../20260907-editorial-review-packet-collection-contract-sprint1/POSTSCRIPT%20-%200.4.58%20AND%200.4.59%20ALLOY%20IMPACT%20ASSESSMENT.md).

## Qualification

- Initial focused correction group: 15 passed.
- Expanded lifecycle/terminal/providerless-denial group: 47 passed, 6 skipped.
- Manifest plus expanded impacted group after classification: 63 passed,
  6 skipped.
- Raw `unittest discover`: 1,110 tests run, 57 skipped, 18 errors. Seventeen
  errors were caused by invoking discovery without the repository source path
  needed by imports and subprocess module calls. The remaining error correctly
  identified the new test as unclassified; adding it to the suite manifest
  resolved that change-owned failure.

The implementation is ready for API review before any commit or package work.
