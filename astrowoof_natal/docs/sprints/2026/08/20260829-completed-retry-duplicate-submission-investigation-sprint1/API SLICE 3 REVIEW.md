# API Slice 3 Review

## Decision

Approved. Slice 3 supplies the right SBE-owned, provider-free contract fixtures
for API implementation and installed-wheel qualification. It does not by itself
enable a live legacy generic invocation or retained-QA recovery.

Focused validation against the working source passed:

```text
test_completed_retry_duplicate_submission_slice3.py
Ran 4 tests — OK (1 optional jsonschema test skipped)
```

`git diff --check` passes as well.

## What is now available

The closed bundle correctly provides two distinct API-facing cells:

1. an exit-zero `astrowoof.generic_provider_dispatch_refusal.v1` object with
   exact state identity, no provider I/O, and the sole next step
   `fresh_lifecycle_inspection`; and
2. a complete terminal-review v0.2 result, receipt, and invocation-bound
   command-envelope join for `local_work_progress_contradiction`, including a
   provider-bearing `provider_reconciliation_only` disposition.

The nested validators and mutation cases are meaningful: recomputing the outer
bundle digest cannot hide an altered refusal disposition, terminal cause,
receipt binding, or removed provider identity. The fixture is also appropriately
privacy-bounded.

## Scope clarification for the handoff

This is correctly an **API-consumer contract fixture**, not a synthetic API
database fixture. Its fixture run/action IDs and binding digests are SBE test
values and should not be inserted into API persistence. API will construct its
own database-backed vertical fixture with matching immutable action bindings
when it proves ingress.

The API work that remains is therefore explicit:

- capture and strictly validate the exit-zero generic-refusal object;
- route it directly to fresh lifecycle inspection and then the selected v2
  dispatch path, never to generic-resume success/retry;
- consume the terminal review envelope through existing exact-result ingress;
- prove the provider-bearing action stays in supported reconciliation custody;
  and
- use malformed and replay cases to prove no second create occurs.

Please retain the stated installed-wheel gate: the next release qualification
must prove these JSON resources are included and readable from the built wheel,
not merely from the source checkout.
