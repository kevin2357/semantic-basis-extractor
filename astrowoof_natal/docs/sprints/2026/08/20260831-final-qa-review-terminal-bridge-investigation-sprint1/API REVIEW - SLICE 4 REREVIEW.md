# API review — Slice 4 re-review

## Decision

**Approved — Voof-paws 5 may proceed to Slice 5 packaging and installed-wheel
qualification.**

## What changed since the first review

The corrected `update_run_status()` precedence now places durable provider
custody before both `BUDGET_EXHAUSTED` and `PREPARED`:

1. ambiguous submission;
2. durable provider identity / waiting custody;
3. budget refusal;
4. providerless prepared authority;
5. providerless authorized/submitting work; and
6. the otherwise legitimate final-QA review terminal.

That is the important correction. A run with one retained provider operation
can no longer be projected as either a budget terminal or a new-authority wait
because a different action happens to carry one of those facts. Its lifecycle
instead remains nonterminal and selects provider reconciliation.

The revised public regression matrix proves both relevant mixed inventories:

- pending provider custody plus a different `PREPARED` action;
- pending provider custody plus a different `BUDGET_EXHAUSTED` action.

Each asserts the `WAITING_FOR_RESPONSE` outer projection, nonterminal lifecycle,
the retained provider-custody action ID, and the reconciliation-cycle temporal
selection. It also proves the ordinary providerless projection returns only
after the custody action is removed.

## Additional verification

I independently ran the revised focused module with the source package on the
test path:

```text
python -m unittest astrowoof_natal.tests.test_final_qa_mixed_custody_slice3
Ran 9 tests ... OK
```

The writer-fenced pre-provider refusal remains appropriately narrow: it refuses
only a newly contradictory terminal/no-custody checkpoint before provider I/O;
it does not reinterpret or clear existing durable provider custody or ambiguity.

No API contract changes are required before packaging. The API should consume
the new v4/v3 typed refusal only after the released installed-wheel boundary is
available.
