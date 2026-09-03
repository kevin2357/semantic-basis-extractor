# API review — Slice 2 reproduction and implementation gate

## Optional-stage reproduction

Approved. The expected-failure reproducer is the right production-boundary test:
it exercises the real `closure.main()` ordinary-v2 resume path, retains exact
completed reconciliation evidence, forbids provider transport, and exposes the
missing join without fabricating an API-side state transition.

The stage matrix is also correctly narrow. Polish, qualitative critic, and
qualitative candidate share the unsafe consumer-boundary ordering, but their
persisted attempt records are not interchangeable. The implementation must use
a stage-aware adapter and preserve candidate predecessor binding. Initial and
creative pass attempts remain the control case; Batch and bounded remain
excluded absent their own topology evidence.

For implementation/qualification, retain the Slice 1 requirements and add two
specific assertions:

1. The unpatched expected failure must fail because the exact completed
   evidence is unadopted—not because the fixture has a looser malformed state.
2. The patched replay must prove zero provider transport calls and must not
   publish terminal review merely as a side effect of executing the fixed path.

The implementation may begin for this native repair. No API source, schema, or
deployment work is presently required.

## Theme-group QA dormant policy

The proposed dormant posture is coherent and appropriately separates inactive
theme-group product behavior from structural editorial gates. It should remain
a distinct implementation/release unit from the Puff adoption repair.

However, this review does **not** itself authorize deleting or disabling
runtime theme-group QA. That is an owner product-policy decision, not an
inference from the checkpoint evidence. Before Slice 4 implementation, obtain
an explicit owner confirmation of the exact dormant boundary in `PRODUCT
DECISION - THEME GROUP QA DORMANT.md`. Once confirmed, the stated non-invocation
and non-theme-gate regressions are the correct acceptance criteria.
