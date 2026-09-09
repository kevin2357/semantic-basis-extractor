# Slice 3 — promotion batch 10 completion

## Result

Following API and owner approval, promoted exactly these five
collision-qualified modules from `provisional` to `parallel_safe`:

- `test_external_authority_public.py`;
- `test_post_fan_in_mixed_custody_slice4b.py`;
- `test_operator_disposition_reader_slice2.py`;
- `test_post_fan_in_retry_matrix_slice3.py`; and
- `test_polish_authority_handoff_qa.py`.

The extracted three-test `test_post_fan_in_retry_matrix_slice0.py` remains
provisional. No production/package code, semantic-closure classification, or
other manifest row changed.

## Manifest and guard evidence

- live manifest moved from 66/30/36 to 71/25/36;
- all 16 runner and manifest-inventory regressions passed; and
- the exactly-once discovery guard confirms the retained Slice 0 module and all
  other active tests remain classified once.

## Actual-manifest stress proof

Two complete two-worker `parallel_only` coordinators ran concurrently against
the updated real manifest and survived a conversation/app interruption without
process restart. Both passed:

- 581 tests;
- 47 expected skips;
- test-inventory digest
  `7aafd8aeb862a700d0d19416bd45f1aa2eb1a30f1a37234644d611ace0522f9c`;
- outcome-inventory digest
  `f8b28e637b6a9bb107b412bea8c670b098b2f068f064d94a21aa797c2e8d1041`;
- manifest digest
  `57091ddf8170c2fd1b3102ad35cf116d5c1290175f7d1af0704fbfeeb2de24a7`;
- wall times 376.533 and 376.562 seconds; and
- empty failure/error inventories and no persisted stderr path in every shard.

The exact matching receipts prove safe composition in the supported weighted
manifest. The longer wall time remains host-contention calibration and is not a
whole-suite performance conclusion.

## Boundary

Batch 10 is complete. Pause for completion review before selecting Batch 11.
The retained Slice 0 module and remaining provisional tail require separate
evidence.
