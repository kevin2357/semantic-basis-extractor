# Slice 3 — promotion batch 4

## Decision

Following API and owner approval, promote the three collision-qualified modules:

- `test_final_qa_mixed_custody_qa.py`;
- `test_post_fan_in_retry_routing_runtime_slice2.py`; and
- `test_external_authority_v2_route_qualification.py`.

The plan's stale statement that five modules had been promoted was corrected:
the manifest moved from 38 to 46 across the first three batches, meaning eight
prior promotions. This batch brings the cumulative total to eleven.

## Actual-manifest stress proof

Two complete two-worker `parallel_only` groups ran concurrently after the
manifest change. Both passed:

- 340 tests, 43 expected optional-schema skips;
- identity digest
  `2067cf8cc50b6d0d0e1c24fa21571ed27f3e193bd53cf88343d9949f391ad1a8`;
- outcome digest
  `a84bf5dafbed50de93816b7b0665039ed4e6c4f498c67bbcad7a5be493612ba3`;
- wall times 291.909 and 291.781 seconds.

The exact identity and outcome digests match. The stress critical path rose by
about 16.5 seconds while admitting 16 additional tests and 44.448 frozen
isolated seconds. This is compatible with the campaign's infrastructure-first
policy and shows no correctness or isolation instability.

## Manifest and boundary

- before: 46 parallel-safe, 47 provisional, 36 serial-only;
- after: 49 parallel-safe, 44 provisional, 36 serial-only.

No test behavior, production code, public contract, provider activity, or
semantic-closure classification changed. Pause before selecting Batch 5.
