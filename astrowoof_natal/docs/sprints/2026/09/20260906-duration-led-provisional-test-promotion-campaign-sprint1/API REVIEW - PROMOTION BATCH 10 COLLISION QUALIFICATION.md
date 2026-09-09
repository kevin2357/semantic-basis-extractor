# API review — promotion batch 10 collision qualification

## Decision

Approved to promote exactly these five collision-qualified modules from
`provisional` to `parallel_safe`:

- `test_external_authority_public.py`;
- `test_post_fan_in_mixed_custody_slice4b.py`;
- `test_operator_disposition_reader_slice2.py`;
- `test_post_fan_in_retry_matrix_slice3.py`; and
- `test_polish_authority_handoff_qa.py`.

The extracted three-test `test_post_fan_in_retry_matrix_slice0.py` remains
provisional and is expressly excluded from this decision.

## Evidence accepted

The obsolete v0.5 no-progress republication method is now preserved verbatim
outside routine discovery, with provenance and a pointer to the present v0.7
fail-closed/append-only regressions. The useful helper and three enduring
compatibility tests remain active, and that module did not enter the Batch 10
collision receipts.

For the five approved modules, three controlled two-copy repetitions produced
30 clean secret-scrubbed receipts. Every copy retained its frozen outcome:
12/0, 1/0, 6/0, 3/0, and 4/1 tests/skips. No failure, error, unexpected skip,
expected failure, unexpected success, coordinator stderr, or persisted failure
log occurred. Snapshot/binding fences, mixed-custody precedence, exact-result
nonmutation, closed retry matrix, and provider-free polish authority assertions
all remained active.

## Required next boundary

Move only those five manifest rows, run manifest/inventory checks, then run the
repeated concurrent actual-manifest `parallel_only` stress proof. Require exact
matching identity, outcome, and manifest digests, expected inventory, and empty
stderr. Pause for Batch 10 completion review before Batch 11 selection.
