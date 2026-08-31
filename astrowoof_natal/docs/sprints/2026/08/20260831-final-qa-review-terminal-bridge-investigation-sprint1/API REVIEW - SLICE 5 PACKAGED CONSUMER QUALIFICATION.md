# API review — Slice 5 packaged consumer qualification

## Decision

**Approved — Voof-paws 6 may proceed to release preparation.**

## Review findings

The new `astrowoof-final-qa-mixed-custody-qa` command is an appropriate
deployment gate:

- it is closed, provider-free, and accepts no retained-workspace, authority,
  provider-credential, or subject input;
- it drives the public ordinary-v2 command through the actual final-QA warning
  plus polish path, rather than testing only a private reducer;
- it proves the corrected durable-custody projection is nonterminal and selects
  reconciliation;
- it proves the post-intent terminal contradiction is refused before payload
  resolution or provider I/O, using the new exact v4/v3 result pair; and
- it retains the existing terminal-review qualification as the distinct control
  case for a genuinely sealed review terminal.

The adjacent reconciliation correction is also correctly narrow. It strictly
joins a pre-existing sealed v0.2 `review_required` result from the native result
index, permits GET-only settlement of provider custody that already existed at
that terminal boundary, and preserves the review status. It does not authorize
new authoring or reuse a providerless authorization.

I independently ran the new source qualification test module:

```text
python -m unittest astrowoof_natal.tests.test_final_qa_mixed_custody_qa
Ran 3 tests ... OK
```

The candidate wheel's already-published `0.4.34` identity is properly described
as qualification evidence only. Release preparation must assign and freeze a new
version from committed source; API should not treat this candidate as deployable.

## API integration note

No API code change is required before the release is available. After the new
wheel is released, API deployment/attestation should add the provider-free
qualification command as a release gate and accept command-result v3 only for
the typed `post_intent_lifecycle_contradiction` refusal path. Existing successful
ordinary-v2 result v2 consumption remains unchanged.
