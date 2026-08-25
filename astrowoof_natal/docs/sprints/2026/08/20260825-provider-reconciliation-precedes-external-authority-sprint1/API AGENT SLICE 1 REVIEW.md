# API Agent Slice 1 Review

Date: 2026-08-25

## Verdict

Approved to proceed to Slice 2.

The v0.5/v0.6 validator hardening correctly treats the mixed custody/authority
output as an invalid combination rather than inventing a new consumer-visible
state. Failing closed before the selector is fixed is the right intermediate
posture.

## Confirmed points

- The predicate is tied to retained `provider_custody.action_ids`, so it covers
  both due and not-due custody rather than only one timing branch.
- `completed_evidence_pending_local_work` receives the more precise fan-in
  predicate in addition to the general custody predicate.
- Temporal v0.6 independently refuses an authority-bearing basis with retained
  custody, which prevents a digest-valid but semantically contradictory result.
- Authority-only observations retain their intended stable digest behavior.

## Slice 2 guardrails

Implement the shared selector reorder so public inspection returns the existing
reconciliation/fan-in branches rather than relying on the new validation error.
Preserve SBE-selected subset ordering and the four-action cap. The not-due branch
must remain nonmutating and should expose the existing `not_before`; no provider
creation, authority consumption, API-global capacity assertion, or frozen-QA
access is authorized by this review.
