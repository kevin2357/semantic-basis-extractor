# Slice 3 — promotion batch 5 collision qualification

## Result

The complete three-module cohort passed the approved bounded collision matrix.
This is evidence for a separate promotion decision; it does not change the
49/44/36 manifest.

## Matrix

Three repetitions launched two independent copies of each candidate together,
for six worker processes per repetition and 18 successful workers total.

| Module | Exact outcome in every copy | Worker-duration range |
| --- | --- | ---: |
| `test_external_authority_qa.py` | 3 tests, 1 optional-schema skip | 16.600–29.200 s |
| `test_bounded_product_qa.py` | 7 tests, 0 skips | 11.033–15.153 s |
| `test_terminal_review_interruption_slice4.py` | 4 tests, 0 skips | 6.558–8.976 s |

All 18 supported-runner receipts report success with exact test/skip
inventories. There were no failures or errors. Because these are the real test
modules rather than substitute probes, green outcomes retain their internal
assertions:

- bounded-product kept its exact scripted provider-stage sequence and proved
  protected sentinels absent from emitted events;
- terminal interruption kept exactly one successful publication plus one
  expected native-lock error, immutable predecessor, contiguous successor,
  repair/replay, and protected-value checks; and
- external-authority qualification retained its package contract assertions
  and the expected optional `jsonschema` skip.

Each copy used the supported provisional measurement route, which creates a
secret-scrubbed child environment and independent work root.

## Interrupted and invalid attempts

The laptop restart interrupted the first attempt before any receipt was
written, so it supplies no evidence. On restart, a mistaken top-level runner
invocation began complete-suite workers because positional modules do not
filter that mode. It was stopped as soon as identified; it also produced no
receipt and is excluded. Neither attempt changed the manifest or production
code. The matrix above is solely the subsequent clean bounded run.

## Next boundary

Pause for the separately required API/owner promotion decision. If approved,
move only these three modules to `parallel_safe`, then run the prescribed
actual-manifest stress proof. No promotion or whole-suite claim is made here.
