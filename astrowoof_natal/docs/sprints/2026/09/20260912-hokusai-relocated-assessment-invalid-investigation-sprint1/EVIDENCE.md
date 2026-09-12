# Evidence — Hokusai relocated-assessment refusal investigation

## Frozen facts

- API's operator trace establishes the exact stage reached: restore succeeded; relocated assessment began; strict assessment became unavailable.
- The failure happened before an SBE disposition posture was accepted by API.
- API retained normal provider/workspace/spend custody and made no capacity release as part of the refusal.

## What is not yet established

- The specific SBE `ValueError`/`TypeError` or rejected join.
- Whether the durable checkpoint's documented logical root represents a contract mismatch, a harmless catalog representation, or neither.
- Whether SBE needs a code change, versus API needing a more precise consumer diagnostic classification.

## Slice 0 provider-free evidence

- Hokusai's SBE worker trace preserves native logical root
  `/work/runs/workspace-5d5294a3-6d1d-4fe4-9a36-c0e2b067414a/sbe`.
- API source independently constructs authoring logical path
  `/work/runs/{api_run_id}/sbe`; the supplied catalog packet reports
  `/work/deterministic-domain`. Neither is equivalent to the native root.
- A provider-pending relocated fixture succeeds with authority bound to the
  native workspace-contract root and refuses at original-root binding when
  authority uses `/work/deterministic-domain`: `2 passed`.
- Existing relocation contract/reader/capability suites remain green:
  `14 passed`.
- The new test module is registered in `test_suite_manifest.json`.

The exact live authority document remains unavailable, so this proves the
compatible causal boundary but does not fictionalize which non-native root API
actually supplied.
