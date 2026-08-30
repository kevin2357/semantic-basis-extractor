# Slice 2 — provider-free causal reproduction

## Result

The retained Pippin/Duchess topology is deterministically reproducible without a
provider. Two independent native defects compose into the observed API outcome.
Neither depends on `theme_group_coverage`; any legitimate pass-QA rejection can
exercise the same path.

## Reproduction A — one pass/attempt produces two bindings

The focused runtime test enters the real exact-interactive retry loop with two
completed rejected attempts and no network-capable transport:

1. The first entry computes retry feedback from completed attempt 2, appends
   attempt 3, and prepares an exact paid action for
   `<pass>:attempt-003`.
2. That exact action is authorized and persisted.
3. On re-entry, attempt 3 is now the final incomplete attempt. The current
   feedback lookup examines that incomplete attempt, finds no QA rejection, and
   returns no feedback.
4. The provider request bytes therefore change. `SpendController` joins actions
   by route **and request digest**, does not match the already-authorized action,
   and prepares a second action for the same pass/attempt route.
5. Execution exits again at external authority. Provider calls remain zero.

The resulting states and binding shape match both retained workspaces:

- one `AUTHORIZED` action and one `PREPARED` action;
- identical stage/route/pass/attempt identity;
- different request SHA-256 values;
- neither has provider identity;
- the pass attempt points at the new prepared action, orphaning the earlier
  authorization from ordinary pass progression.

This is direct provider-free runtime evidence. Confidence: high.

## Reproduction B — review projection masks provider custody

A production-shaped fixture then composes:

- a provider-bound `WAITING` attempt-2 action;
- a reported duplicate attempt-2 action;
- an authorized/providerless attempt-3 action;
- a prepared duplicate attempt-3 action.

Base lifecycle inspection correctly chooses `provider_reconciliation_cycle` and
names the SBE-selected retained provider action. The v0.7 post-fan-in inspector
then detects the authorized/providerless action and unconditionally rewrites the
decision to:

- selected command `none`;
- capacity disposition `retain_for_review`;
- empty due-action inventory;
- reason `authorized_providerless_action_requires_constrained_dispatch`.

The API maps that nonterminal `retain_for_review` result to
`native.review.requires_review` and fails/releases the execution job. Thus the
later API event is fully explained without a native editorial-terminal state.

This is direct provider-free public-inspection evidence. Confidence: high.

## Failure-modality check

The fixture was run once with historical `theme_group_coverage` metadata and once
with a generic legitimate QA-rejection code. The public lifecycle projections are
identical. Theme groups triggered the historical retry, but are not part of either
causal defect.

Confidence: high.

## Required correction boundary

The smallest ownership-correct correction has four parts:

1. **Stable attempt binding.** Once a pass attempt has prepared an action, all
   continuation must reuse that exact action/request artifact/binding. Re-entry
   must not rebuild a semantically new request for the same attempt.
2. **Stable feedback lineage.** Retry feedback must be derived from completed
   predecessor attempts, not hidden by the current incomplete attempt. Any
   reconstructed payload must exactly match the persisted action binding before
   authorization can be consumed or provider create can occur.
3. **Duplicate-lineage refusal.** Native validation must reject multiple distinct
   bindings for one `(run, stage, route/pass, attempt)` lineage. It must not
   silently select the newest action or permit a second create.
4. **Custody precedence.** Retained provider custody must continue to select the
   bounded reconciliation command even when a separate providerless authorization
   requires review. Only after custody clears may the remaining authorization be
   routed through its exact constrained executor or a typed review/refusal path.

API should continue to invoke only the SBE-selected run-level command. It must not
choose reconciliation members or repair native action lineage. Its companion
mapping should distinguish a nonterminal native safety review from an editorially
terminal result and must not erase retained custody.

## Qualification run

Command:

`python -m unittest astrowoof_natal.tests.test_review_required_pending_retries_investigation_slice2 astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice3 astrowoof_natal.tests.test_provider_reconciliation_precedes_authority_slice0 -v`

Result: 12 passed. External provider/network operations: 0. Spend: USD 0.
Retained QA workspace operations: 0.
