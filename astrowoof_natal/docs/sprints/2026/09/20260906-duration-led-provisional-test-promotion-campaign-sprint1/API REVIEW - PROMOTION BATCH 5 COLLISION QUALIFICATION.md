# API review — promotion batch 5 collision qualification

## Decision

**Approved.** Promote only these three collision-qualified modules from
`provisional` to `parallel_safe`:

- `test_external_authority_qa.py`;
- `test_bounded_product_qa.py`; and
- `test_terminal_review_interruption_slice4.py`.

Then run the prescribed actual-manifest stress proof before selecting any later
cohort.

## Evidence accepted

- The clean matrix consists of three independent repetitions, each with two
  concurrent copies of every named module: 18 green worker receipts total.
  Exact inventories stayed at 3 tests / 1 expected optional-schema skip,
  7 / 0, and 4 / 0 respectively, with no failures or errors.
- The tests preserve the meaningful assertions rather than merely proving that
  subprocesses exit successfully: exact local provider-stage behavior and
  protected-sentinel absence; one-result native-lock behavior, replay, and
  immutable lineage; and external-authority package/fixture qualification.
- The secret-scrubbed, independent-work-root route is the correct supported
  harness. The interrupted pre-receipt attempt and the stopped invalid
  complete-suite invocation are honestly excluded and do not weaken the clean
  evidence set.

## Next boundary

Apply the narrow manifest-only classification change, then run two concurrent
actual-manifest groups under the supported worker profile. Require matching
exact identity/outcome inventories and preserved skip posture. Record measured
contention candidly, but do not infer a whole-suite speedup yet. No
semantic-closure movement, production/package change, or blanket promotion is
authorized by this approval.
