# API Slice 1 review — terminal review and mixed custody contract

Date: 2026-08-28
Status: approved in direction; make the small corrections below before Slice 2
runtime integration.

## Retained-evidence finding

The controlled QA checkpoint inspection resolved the major uncertainty. Pippin
and Duchess have hash-valid retained histories, but neither has a sealed
`review_required` result. Their final sealed results remain
`ordinary_authoring/provider_pending`. That proves a real live-route SBE
publication gap; it does not merely show an API omission.

The API ordinary-resume ingestion gap remains independently real. The fix must
therefore retain both halves: SBE must produce the exact terminal result, and API
must ingest the invocation-bound result before interpreting a nonzero terminal
exit or a later inspection result.

## Contract assessment

The proposed v0.2 shape is the correct direction:

- an immutable v0.1 history remains readable rather than silently widened;
- every ledger action is represented exactly once in canonical ledger order;
- reported, durable-provider, providerless-authorized, and ambiguous custody
  are distinct;
- editorial terminality (`outcome=review_required`) is separated from custody
  finality and follow-up inventories;
- no result permits new provider creation; and
- providerless release still requires the established denial result rather than
  being inferred from terminal review.

The invocation/result/receipt join is also essential. API must receive the exact
result identity from its just-launched native invocation; an index's latest entry
is diagnostic discovery only.

## Required corrections before runtime mutation

1. **Remove accidental duplicate code.**
   `terminal_review_contracts.py` currently duplicates `_REVIEW_CAUSES`, route
   checks, provider-status checks, denial/usage/reported checks, and substantial
   portions of result validation. `__init__.py` also imports and exports the five
   new public symbols twice. This does not appear to alter the focused behavior,
   but it is a clear Slice 1 merge/copy artifact and should be removed before a
   public contract is frozen.

2. **State the API verification join explicitly.**
   v0.2 publishes `binding_sha256`, not a full binding. That is reasonable for
   the public result, but the contract must explicitly require API ingress to
   match each result row against the immutable API-side authorization/action
   binding, run identity, route/stage, and any durable provider operation it
   already knows. A digest that merely has the right shape cannot itself prove
   the SBE action is the API action.

3. **Specify receipt compatibility and result identity transport.**
   The existing receipt remains v0.1 while the result becomes v0.2. Slice 2 must
   show that the canonical receipt validator accepts and binds the new result
   version deliberately, not merely through this helper's subset check. It must
   also define how the worker returns `result_id` and `receipt_id` for the exact
   invocation even when the command exits 2.

4. **Make outer-run posture unambiguous.**
   The contract correctly calls review editorially terminal. State plainly that
   if `custody_finality != final`, API must not call the outer run generically
   closed/failed: it is review-required with only the listed reconciliation and
   denial continuation permitted. No authoring, retry, polish, critic, or new
   provider create may be re-enabled.

5. **Add one contract test for the consumer-critical joins.**
   In addition to mutation/re-hash tests, reject a rehashed action row whose
   `binding_sha256` is valid-looking but fails an independently supplied
   immutable action-binding join, and reject a v0.2 result paired with an
   otherwise valid v0.1 receipt that carries a mismatched result schema/identity
   through the canonical receipt reader.

## Slice 2 authorization

Once the duplicate cleanup and the above semantics are reflected in the contract
and tests, API approves Slice 2 to centralize live-route publication-before-exit
for exact interactive. Do not broaden that runtime change to Batch or bounded
routes until their stated matrix evidence exists.

No provider work, retained-run recovery, deployment, or release is approved by
this review.
