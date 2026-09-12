# Evidence — Hokusai relocated-assessment refusal investigation

## Frozen facts

- API's operator trace establishes the exact stage reached: restore succeeded; relocated assessment began; strict assessment became unavailable.
- The failure happened before an SBE disposition posture was accepted by API.
- API retained normal provider/workspace/spend custody and made no capacity release as part of the refusal.

## Exact live causal join

- Exact restored SBE checkpoint: `c1726aeb-f091-45d4-956a-4f628bb96439`,
  generation `3`, active.
- API checkpoint and authoring-row root:
  `/work/runs/00667fb9-c068-415e-a045-8d4059ac549e/sbe`.
- Native durable root:
  `/work/runs/workspace-5d5294a3-6d1d-4fe4-9a36-c0e2b067414a/sbe`.
- API constructed authority from the first root; SBE correctly rejected it
  against the second at original-root binding.
- The earlier `/work/deterministic-domain` packet selected the wrong job's
  checkpoint through a run-wide catalog query and is irrelevant to the restore.

The live cause is therefore an API identity-source defect. SBE needs no reader,
schema, release-pair, or diagnostic correction.

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

The exact job-bound API join supplies the previously missing live identity
fact. No R2 access is needed.
