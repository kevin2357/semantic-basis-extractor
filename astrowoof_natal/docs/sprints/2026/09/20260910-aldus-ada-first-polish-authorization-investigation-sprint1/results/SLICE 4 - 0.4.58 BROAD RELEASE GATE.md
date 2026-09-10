# Slice 4 — 0.4.58 Broad Release Gate

## Candidate identity

- distribution: `astrowoof-natal-authoring`
- version: `0.4.58`
- interpreter: `C:\Users\kevin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`
- suite profile: checked-in manifest coordinator, one worker

The version was frozen before release-bound testing. `0.4.58` was unused
locally and had no component-scoped tag.

## Gate selection

Broad/full qualification is required because the patch changes shared
lifecycle and external-authority selection. The affected focused matrix ran
first and passed: 82 tests, 7 skips, zero failures.

The relational contract and Alloy model are unaffected. The patch does not
change chronology, action ownership, transition vocabulary, artifact scope,
delivery selection, provider joins, or observation authority. It corrects the
runtime projection of an already modeled PREPARED authority request by proving
an exact ledger/attempt/sidecar join. Executable tests remain the enforcement
boundary; no Alloy update or rerun is warranted for this release.

## Broad/full result

Command:

`python astrowoof_natal/scripts/run_test_suite.py`

Result:

- success: true
- tests: 1,163
- skips: 60
- failures/errors: 0
- wall time: 942.577944 seconds
- worker count: 1
- manifest SHA-256:
  `a5c8070c97ab0352a4506df384f5abfe7a35c1276ad2b46f6b190b00824d9037`
- test inventory SHA-256:
  `9b6f963f769b71633311ff5e7b58ae284fad2798671b8e8a505f5d9a3d63825d`
- outcome inventory SHA-256:
  `f8ba33e30151d6b9d39fb0aae5cf80f3d2619025797eea886ebca8c3af381db4`

The broad gate is green. Reproducible build and clean installed-wheel
qualification remain before the release-lock review boundary.
