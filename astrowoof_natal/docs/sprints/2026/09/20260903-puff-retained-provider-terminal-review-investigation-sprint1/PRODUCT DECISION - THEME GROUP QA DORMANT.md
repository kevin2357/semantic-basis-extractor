# Product decision — theme-group QA is dormant

## Decision

Theme groups are not a currently delivered product feature. Their values may
remain in deck artifacts for compatibility and possible future use, but SBE
must stop evaluating them as QA policy.

The dormant posture covers all theme-group-specific editorial checks,
including:

- assignment quality;
- coverage; and
- balance.

SBE must not run those checks, emit their findings or advisories, log their
results, reject or retry a pass because of them, affect finalization because of
them, or publish terminal review because of them.

This is intentionally stronger than converting another subset of findings to
advisory. Advisory computation has no present product value, still adds
operational noise, and can be accidentally promoted back into control flow by
another consumer.

## Compatibility boundary

- Preserve existing theme-group fields and registry shapes so old decks remain
  readable and no unrelated schema migration is introduced.
- Do not change the pass-6 provider prompt in this patch. Its output may still
  contain theme-group metadata, but that metadata is inert and untrusted for
  acceptance.
- Preserve non-theme structural and editorial checks unchanged.
- Existing tests whose sole purpose is to execute or enforce theme-group QA
  should be removed or replaced with a dormant-feature regression. Commented
  out tests are not a durable contract.
- The dormant regression should fail if the acceptance/finalization paths call
  a theme-group evaluator or translate a theme-group finding into a decision.

## Why this is now warranted

Theme-group findings have contributed to three joint investigation/release/
deployment cycles while the associated filtering feature remains unimplemented.
Pastiche confirms that the residual hard `theme_group_assignment` check can
still exhaust all attempts for an otherwise useful deck. The operational cost
is no longer justified by the dormant feature's value.

## Reactivation rule

Reactivation requires a new product decision and an end-to-end contract that
jointly defines:

1. the user-facing filtering behavior;
2. the canonical theme vocabulary;
3. the provider prompt and assignment semantics;
4. evaluation criteria calibrated against that prompt;
5. whether findings are diagnostics, advisories, or gates; and
6. API/UI consumption and qualification.

Historical failure rates under the current prompt are not treated as useful
calibration evidence for that future design.
