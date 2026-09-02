# Pre-sprint huddle

## Starting posture

This is an investigation, not a presumed defect sprint. Crumpet and Baguette
both reached a superficially surprising but potentially legitimate shape:
provider work was reported, provider custody was empty, and native authoring
still ended in review because at least one pass was not accepted.

The immediate source behavior is straightforward: finalization defers unless
every pass is `PASS_QA_ACCEPTED`, and an attempt-exhausted pass can become
`FAILED_REQUIRES_REVIEW`. The investigation therefore needs to explain the
earlier pass truth, not merely rediscover the finalization guard.

## Important distinction

An API action marked `reported` proves that its provider result was durably
reported. It does not by itself prove that SBE:

- adopted the response into the intended pass attempt;
- parsed and validated it successfully;
- ran deterministic QA against it;
- accepted the pass; or
- advanced the pass-level state to `PASS_QA_ACCEPTED`.

Slice 0 must make those joins explicitly for all six passes and both attempts.

## Neutral hypotheses

1. Both runs legitimately exhausted two attempts because deterministic QA
   rejected the retry output.
2. The retry responses were reported but were not fully adopted into native
   pass truth.
3. Retry acceptance evidence exists, but the containing pass state did not
   advance consistently.
4. A shared deterministic-QA predicate is systematically rejecting otherwise
   usable retry output.
5. The two runs only look similar at the API action-summary level and have
   different native causes.

No hypothesis is privileged until the protected checkpoint joins are complete.

The supplied trace export subsequently made hypothesis 1 the leading—but still
unproven—explanation. In both runs, passes 1–5 were logged accepted on attempt
1, while pass 6 was logged rejected on attempts 1, 2, and 3. The trace does not
carry the complete persisted QA/rejection evidence required to decide whether
those three rejections were semantically correct, so the protected checkpoint
comparison remains necessary.

## Evidence discipline

- Trace logs are diagnostic cues, not authority.
- Protected checkpoints, snapshots, native results, receipts, and persisted
  pass/attempt records are authoritative within their documented contracts.
- No response is to be selected, repaired, replayed, denied, or resubmitted.
- No implementation or release should be inferred from Slice 0 alone.
