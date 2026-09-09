# Slice 3 — promotion batch 6 completion

## Decisions applied

Following API and owner approval:

- promote `test_batch_negative_authorization.py`;
- promote `test_external_authority_v2_intent_fence.py`; and
- archive `test_completed_retry_duplicate_submission_investigation_slice0.py`
  beside its original incident evidence as non-discoverable `.py.txt` forensic
  source, with a provenance README.

The historical witness was not deleted or rewritten into a misleading modern
success case. It was removed from routine discovery and the manifest because
its passing condition is reproduction of the obsolete duplicate-create defect.

## Actual-manifest stress proof

Two complete two-worker `parallel_only` groups ran concurrently after the
manifest and archival changes. Both passed:

- 389 tests, 44 expected skips;
- test-inventory SHA-256
  `1db0a080802cedb4c40b5ddcc80a7c6c008bcf20533d3c7b667b293a2bccf1bc`;
- outcome-inventory SHA-256
  `ed4a1ab0a6dcb1a7283d6876a3e99f17be121af2d61788c59373607805182da7`;
- manifest SHA-256
  `7e7336125a48eed2fea19d5486286e77299d019f4786c04b45374f8c95b4e79e`;
- wall times 384.030 and 383.823 seconds; and
- empty runner stderr for both groups.

Exact identities, outcomes, skips, manifest digest, and stderr posture match.
No whole-suite speedup is inferred from this parallel-only stress result.

## Manifest and boundary

- live shared manifest before: 52 parallel-safe, 44 provisional, 36
  serial-only;
- live shared manifest after: 54 parallel-safe, 41 provisional, 36 serial-only;
- the active test inventory decreases by one because the obsolete historical
  witness leaves discovery; and
- against the frozen campaign basis, the projected classification is 54/38/36,
  with the three concurrent editorial-contract modules accounting for the live
  provisional difference.

No production/package behavior, public contract, provider activity, or
semantic-closure classification changed. Pause before selecting Batch 7.
