# Slice 3 — promotion batch 5

## Decision

Following API and owner approval, promote only the three collision-qualified
modules:

- `test_external_authority_qa.py`;
- `test_bounded_product_qa.py`; and
- `test_terminal_review_interruption_slice4.py`.

This brings the cumulative promotion count to fourteen modules.

## Actual-manifest stress proof

Two complete two-worker `parallel_only` groups ran concurrently after the
manifest change. Both passed:

- 354 tests, 44 expected skips;
- test-inventory SHA-256
  `990a6e6fa9d567d14433f7d3b2c693663b6e64478c279740b006160814ee1197`;
- outcome-inventory SHA-256
  `1cd734bd05404e415fe2fb8f160b5ba0281f319fcb0da4838f805a8b9ad705a3`;
- manifest SHA-256
  `6ebb31465ddf10a877ab092d5ca5bd99c5f75c7dde5373d7a1f30251a3cad0c2`;
- wall times 424.409 and 420.131 seconds; and
- empty runner stderr for both groups.

The exact identity, outcome, and manifest digests match. The shared-host stress
critical path is materially slower than prior batches, but this run intentionally
placed four child processes and qualification-heavy work on the laptop at once.
Under the agreed infrastructure-first policy this is calibration evidence, not
a correctness veto: outcomes, skip posture, isolation, and cleanup were stable.
No whole-suite speedup is inferred.

## Manifest and boundary

- campaign basis before: 49 parallel-safe, 44 provisional, 36 serial-only;
- campaign-basis projection after: 52 parallel-safe, 41 provisional, 36
  serial-only; and
- observed live shared manifest after: 52 parallel-safe, 44 provisional, 36
  serial-only, because three newly added editorial-contract modules entered
  `provisional` concurrently with this campaign.

No test behavior, production code, public contract, provider activity, or
semantic-closure classification changed. Pause before selecting Batch 6.
