# Slice 3 — promotion batch 6 collision qualification

## Result

The two audit-approved candidates passed the bounded collision matrix. This is
evidence for a separate promotion decision; it changes neither the live
52/44/36 manifest nor the historical witness disposition.

## Matrix

Three repetitions launched two independent copies of each candidate together,
for four worker processes per repetition and 12 successful receipts total.

| Module | Exact outcome in every copy | Worker-duration range |
|---|---|---:|
| `test_batch_negative_authorization.py` | 18 tests, 0 skips | 8.250–9.744 s |
| `test_external_authority_v2_intent_fence.py` | 17 tests, 0 skips | 7.360–10.593 s |

Every worker used the supported secret-scrubbed provisional-measurement route,
an independent work root, and a separate result receipt. All 12 workers passed
with empty stderr and no failures or errors.

Because the real modules ran, the result retains their substantive assertions:

- all-or-none negative authorization, refusal nonmutation, crash recovery,
  exact replay, ordered events, and competing native-lock behavior; and
- durable v2 intent commitment, call-entry ambiguity, provider-identity fencing,
  safe pre-entry retry, exact replay, snapshot validation, and zero unintended
  provider calls.

## Historical witness remains held

`test_completed_retry_duplicate_submission_investigation_slice0.py` was not
included. It remains provisional pending the explicit retain/archive/replacement
decision recorded in the state-surface audit. This qualification neither deletes
it nor treats reproduction of an old defect as a present-tense safety invariant.

## Next boundary

Pause for a separate promotion decision. If approved, move only the two named
collision-qualified modules to `parallel_safe`, then run the repeated concurrent
actual-manifest stress proof. No semantic-closure movement, production/package
change, or historical-test disposition is authorized here.
