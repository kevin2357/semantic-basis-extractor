# API Slice 1 Review — Exact Provisional-Polish Join

## Decision

**Approved to proceed to Slice 2.**

The correction is appropriately narrow and resolves the Frisbee/Hype contradiction
without creating an API-side recovery path or weakening genuine terminal review.

## What I verified

- `finalization_conclusion()` now treats `FINAL_QA_WARN` as provisional only for
  the exact subject whose current polish attempt is `SUBMITTED` and whose exact
  action is provably the one prepared for that attempt.
- The helper requires one—and only one—matching ledger action, with the exact
  `<subject>:polish:<attempt-number>` route, `stage=polish`, interactive service,
  `PREPARED` state, and no authorization, provider, or consumption evidence.
  Mismatched, stale, Batch, bounded, and unrelated evidence therefore remains
  fail-closed.
- A sealed `terminal_transition` still dominates even if old workspace bytes
  contain a superficially matching prepared action.
- The authorization-pause path persists the returned `paid_action_id` onto the
  already-created polish attempt before re-raising. That supplies the durable
  attempt-to-ledger identity join the production traces lacked.
- The public lifecycle projects the matching action as exactly one ordinary-v2
  external-authority request; it does not relabel it as local work.

## Verification

Ran locally, provider-free:

```text
python -m unittest \
  astrowoof_natal.tests.test_polish_authority_handoff_slice0 \
  astrowoof_natal.tests.test_terminal_dominance_slice1 -v

Ran 9 tests in 0.167s — OK
```

## Slice 2 requirements

The packaged/public qualification should keep the positive case and the
requestless controls separate. It should prove that API receives the exact
ordinary-v2 action identity only in the positive case, while every other
identity/custody/terminal mismatch remains terminal-review/no-request. API must
continue to consume the native request as provided and must never manufacture a
polish request or invoke generic resume to obtain one.
