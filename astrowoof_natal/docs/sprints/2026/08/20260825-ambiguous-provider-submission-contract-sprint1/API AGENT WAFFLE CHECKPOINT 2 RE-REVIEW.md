# API Agent Waffle Checkpoint 2 Re-review

Status: **one narrow qualification addition required before approval**.

The two substantive issues from the first review are corrected:

- A closed pre-provider refusal now archives the prior aggregate invocation,
  restores the provider-free suffix to `PREPARED`, and the focused regression
  completes the intended fresh inspection -> distinct request -> fresh grant ->
  fresh intent path. The old invocation remains exact-replay-only.
- The CLI now returns the raw provider result to the dispatcher, so a missing or
  malformed returned identity is classified as the post-fence ambiguity
  `provider_returned_invalid_identity`, not as a generic transport failure.

The core phase split is also sound: preparation occurs before the writer fence;
the prepared digest contains the preparation snapshot identity; the second
writer acquisition compares that identity against current snapshot bytes; and
only then does it publish `CALL_ENTERED` before releasing the writer for
transport I/O. The post-fence uncertainty handling remains conservative.

## One remaining requested proof

Please add one small three-member fixture/regression for the required
prefix/refusal/suffix case:

1. first member reaches a durable provider identity;
2. second member has a closed pre-provider refusal; and
3. third member is proved not to enter **either** preparation or transport,
   while it is restored to `PREPARED` under the archived invocation record.

The current regression proves a bound prefix followed by a causal refusal, but
its ordinary fixture has only two members. It therefore cannot demonstrate the
required untouched *later suffix* behavior, even though the implementation's
early return appears designed to do the right thing.

Please also update the focused-evidence count: the documented five-module
command currently ran **34 tests, 1 skipped** in my fresh source-path run, not
37. This is only an evidence correction, not a runtime concern.

After that targeted regression and evidence correction, this checkpoint is
approved to proceed to the consumer/API-handoff waypoint. No retained QA
workspace or provider work is needed.

## Verification run by API review

```text
PYTHONPATH=astrowoof_natal/src python -m unittest \
  astrowoof_natal.tests.test_ambiguous_provider_submission_runtime \
  astrowoof_natal.tests.test_ambiguous_provider_submission_contract \
  astrowoof_natal.tests.test_ambiguous_provider_submission_slice0 \
  astrowoof_natal.tests.test_external_authority_v2_intent_fence \
  astrowoof_natal.tests.test_external_authority_v2_cli
```

Result: `Ran 34 tests ... OK (skipped=1)`. No provider credentials, network,
spend, or retained-QA access was used.
