# API review — Slice 4 precedence correction required

## Decision

The post-intent fence and new v4/v3 refusal pair look appropriately narrow, but
**Voof-paws 5 is not approved yet** because the implemented reducer order does
not match the Slice 2 frozen custody contract.

## Required correction

In `update_run_status()`, the current order is effectively:

```text
ambiguity -> budget refusal -> PREPARED -> durable provider identity -> AUTHORIZED/SUBMITTING
```

This permits `PREPARED` (and potentially `BUDGET_EXHAUSTED`) to conceal an
already durable provider identity when both exist in one run. That violates the
explicit frozen invariant:

> existing durable provider custody selects retrieval/reconciliation only.

It also reopens the historical class of defect where pending provider work is
masked by a separate providerless/new-authority fact. A provider operation that
has already been accepted may still settle cost and must be reconciled even if a
different action cannot receive budget or authority.

Please reorder the general projection so that, after ambiguity handling as
appropriate, durable provider identity / waiting custody precedes both
providerless `PREPARED` work and budget refusal. Completed-but-unadopted provider
evidence must likewise remain local fan-in rather than new-authority or terminal
selection.

The necessary mixed-inventory controls are:

1. durable provider identity + a different `PREPARED` action => nonterminal,
   reconciliation-compatible; no external-authority selection;
2. durable provider identity + budget refusal for a different action =>
   reconciliation-compatible; no terminal/abandonment projection;
3. once all durable provider custody is reconciled/adopted, the remaining
   `PREPARED` or budget fact may select its ordinary supported route; and
4. the existing no-custody final-QA review terminal still seals normally.

This need not broaden the v4/v3 schemas. It is a reducer precedence correction
and cross-product regression addition before the installed qualification gate.
