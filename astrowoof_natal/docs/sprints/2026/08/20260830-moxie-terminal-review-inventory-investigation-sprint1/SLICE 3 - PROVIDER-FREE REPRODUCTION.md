# Slice 3 — Provider-free production-boundary reproduction

## Result

The retained Moxie ordering is reproducible through the real top-level resume,
local-work inspection/progress fence, native terminal publication, command-result
output, result reader, and strict API join validator. Two candidate corrected
orderings are also proven with the public local-work inspection/commit boundary.

No fixture invokes provider creation, retrieval, network access, or spend.

## Retained bad ordering

The characterization starts with seven native actions matching API authority:

- six reported initial actions;
- retry attempt 2 with durable completed provider evidence in the spend ledger;
- pass attempt 2 still marked `AMBIGUOUS_PROVIDER_SUBMISSION`; and
- no retry attempt 3 action.

The real `closure.main()` resume boundary first selects the completed retry-2
local operation. Its controlled provider-free local authoring step then reproduces
the retained defect by preparing retry 3 without consuming retry 2. The unmodified
local-work progress fence observes the same semantic operation, invokes the real
terminal-review publisher, emits the real command envelope, and exits 2.

Assertions prove:

- the result is `review_required / local_work_progress_contradiction`;
- all eight native ledger rows appear;
- retry 2 retains reconciliation custody;
- retry 3 is providerless-denial-only;
- `new_provider_create_permitted` is false; and
- the strict API validator refuses the original seven-action join.

This is a production-boundary characterization, not a provider-adapter test. The
one controlled seam is the deterministic local authoring mutation; provider create
is separately patched to fail the test if reached.

## Corrected ordering A — adopt without a successor retry

The fixture first adopts retry 2 into both durable ledger and pass/attempt truth,
then commits the prior local operation. The result:

- retry 2 becomes terminally reported and pass-QA accepted;
- the completed-evidence operation key is durably consumed;
- no retry-3 action is created; and
- no external-authority decision is selected for nonexistent work.

## Corrected ordering B — adopt, then prepare a legitimate retry

The fixture first adopts retry 2 as reported and pass-QA rejected, then prepares
retry 3 and commits the prior local operation. The successor inspection:

- consumes the retry-2 local operation;
- selects `await_external_authority`;
- publishes exactly retry 3 in the ordered authority inventory;
- leaves retry 3 `PREPARED` and providerless; and
- performs no provider create.

This ordering supplies the API-visible authority boundary that Moxie's retained
history lacked.

## Tests

New characterization:

```text
python -m unittest \
  astrowoof_natal.tests.test_moxie_terminal_review_inventory_slice3

Ran 3 tests — OK
```

Focused adjacent regression:

```text
python -m unittest \
  astrowoof_natal.tests.test_moxie_terminal_review_inventory_slice3 \
  astrowoof_natal.tests.test_post_fan_in_retry_runtime_slice2 \
  astrowoof_natal.tests.test_completed_retry_duplicate_submission_slice2

Ran 11 tests — OK
```

`git diff --check` passes for the new test.

## Voof-paws 4 decision

The reproduction proves that either corrected ordering is mechanically safe. It
does not yet choose runtime policy. The next review should select whether the
native runtime must always adopt completed provider evidence into pass truth
before successor selection, and whether the no-retry versus legitimate-retry
choice remains determined solely by deterministic pass QA.

No implementation change is included in Slice 3.
