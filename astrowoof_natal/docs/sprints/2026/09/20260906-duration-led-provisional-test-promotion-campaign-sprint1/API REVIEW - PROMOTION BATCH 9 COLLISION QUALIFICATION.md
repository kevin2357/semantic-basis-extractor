# API review — promotion batch 9 collision qualification

## Decision

Approved to move exactly the five audited Batch 9 modules from `provisional` to
`parallel_safe`:

- `test_review_required_pending_retries_investigation_slice2.py`;
- `test_spend_enforcement.py`;
- `test_external_authority_empty_inventory_investigation.py`;
- `test_lifecycle_closeout.py`; and
- `test_checkpoint_repair.py`.

This approval covers only those manifest rows and their runner checks. It does
not authorize later cohort movement, semantic-closure work, package/product
changes, or a generalized speed claim.

## Evidence accepted

Three controlled repetitions ran two independent copies of each candidate, for
30 successful secret-scrubbed worker receipts. Every copy retained its exact
inventory—4, 18, 13, 10, and 8 tests respectively—with zero skips, failures,
errors, expected failures, unexpected successes, coordinator stderr, or
persisted failure logs.

The matrix preserves the reason these are useful tests: exact retry reuse and
custody precedence; spend/ambiguity/provider-call ordering; closed external
authority refusal and diagnostic non-authority; durable closeout/interruption
recovery; and backup-gated checkpoint repair.

## Required next boundary

After promoting only these five modules, pass the manifest/inventory suite and
run the repeated concurrent actual-manifest `parallel_only` proof. Require
complete matching identity, outcome, and manifest digests with expected
inventory and empty stderr. Pause for Batch 9 completion review before choosing
another cohort.
