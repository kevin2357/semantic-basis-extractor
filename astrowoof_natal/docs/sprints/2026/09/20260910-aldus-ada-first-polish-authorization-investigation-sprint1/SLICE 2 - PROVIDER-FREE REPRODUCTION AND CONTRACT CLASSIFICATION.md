# Slice 2 — Provider-Free Reproduction and Contract Classification

## Outcome

The immutable first-polish defect reproduces without a provider, API, retained
workspace, or protected editorial payload.

With one exact PREPARED polish action, a matching authorization-request sidecar,
an awaiting-spend run status, a matching submitted polish attempt, and a
`FINAL_QA_FAILED` subject, post-fan-in lifecycle selection returns:

- `selected_command=none`;
- `capacity_disposition=retain_for_review`;
- `reason_code=native_review_or_ambiguity`; and
- no external-authority request.

The reproducer also proves that the request sidecar still contains the exact
action and a binding equal to the ledger. The request is lost only at lifecycle
selection.

## Contrast with the existing control

The existing polish handoff contract test uses the same valid PREPARED action
and matching submitted attempt with subject state `FINAL_QA_WARN`. That control
correctly selects `await_external_authority` and emits one v2 request.

Changing only the subject state to `FINAL_QA_FAILED` makes terminal/review
dominance hide the already-elected polish continuation. This is the precise
gap represented by Ada and Aldus: final QA failure is the reason polish exists,
but it is also incorrectly allowed to dominate that live polish action.

## Contract classification

This is an SBE priority/selection defect, not malformed authority evidence and
not an API consumer defect.

The missing invariant is:

> A subject-level final-QA failure with a matching live PREPARED optional-stage
> action is provisional while that action remains eligible for external
> authority. It is not terminal-review evidence by itself.

Terminal review must continue to dominate when there is genuine closed evidence:
explicit providerless denial, budget or attempt exhaustion, ambiguous provider
submission, invalid finalization contract, a committed terminal transition, or
an editorial failure for which no matching optional continuation was elected.

The narrow implementation seam is the post-spend-boundary selection used by
`checkpoint_spend_boundary(..., terminal_review_v02=True)`. It currently treats
`selected_command=none` plus `retain_for_review` as sufficient to publish a
terminal review. The selection must first preserve a structurally valid live
first-polish request.

Do not change the v0.2 terminal custody projection merely to make PREPARED mean
nonterminal inside an already-valid terminal review. The problem occurs earlier:
terminal review must not be entered for this live request. API's strict terminal
action-inventory comparison also remains unchanged.

## Reproducer

`tests/test_first_polish_authority_selection_investigation.py` constructs the
minimal exact-route state, persists the ordinary request sidecar, and records
the current contradictory lifecycle result. It performs no provider operation.

Slice 2 is complete. Implementation remains gated on API/owner approval of this
classification and the proposed narrow selection correction.
