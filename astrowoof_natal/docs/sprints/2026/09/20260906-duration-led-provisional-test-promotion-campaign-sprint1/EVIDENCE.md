# Evidence — duration-led provisional test promotion campaign

## Status

Slices 0, 0A, 1, 1A, and 2 complete; paused at Campaign paws-point 2 before
broader promotion or semantic-closure behavioral-family movement.

## Baseline intake

- framework/source commit: `d9129f6`
- default supported runner profile: one worker
- baseline result: 1,118 tests, 58 skips, pass
- baseline wall time: 1,122.983334 seconds
- test inventory SHA-256:
  `64540bf668560c4fcb3989673fac93fbead58aab9b9d56d46d2a9e53eef53c69`
- outcome inventory SHA-256:
  `a400a525811fd41fa58bf97e45957110b0a29a85d0c955f06143c18133e593de`
- manifest inventory: 38 parallel-safe, 55 provisional, 36 serial-only

## Provisional timing inventory

- 55/55 modules passed independently.
- summed isolated duration: 520.767606 seconds.
- top-two contribution: 46.1%; top-ten contribution: 80.4%.
- `test_bounded_lifecycle.py` samples: 122.434, 121.750, 144.843
  seconds; median 122.434, range 23.093.
- `test_waffle_scone_finalization_slice0.py` samples: 117.633, 146.773,
  122.645 seconds; median 122.645, range 29.140.
- full ranked table and methodology:
  `SLICE 0 - PROVISIONAL DURATION INVENTORY.md`.

## Semantic-closure feasibility

- manifest classification: `serial_only`.
- discovered test methods: 98.
- isolated duration samples: 213.528685, 192.969556, and 215.110382 seconds;
  median 213.528685, range 22.140826.
- median share of the frozen supported broad-suite wall time: 19.0%.
- complete serial-only calibration: 36/36 modules passed, summed isolated
  duration 448.964333 seconds.
- semantic-closure share of that complete measured serial-only tail: 47.9%.
- behavioral families mapped: 7.
- state-surface indicators: 79 temporary-directory references, 27 patch
  calls, 6 threading references, 3 subprocess references, and 2 explicit
  sleeps.
- detailed boundary/risk/recommendation:
  `SLICE 0A - SEMANTIC CLOSURE DECOMPOSITION FEASIBILITY.md`.

## Promotion batches

No manifest classification has changed.

Slice 1 audited the two dominant provisional modules:

- `test_bounded_lifecycle.py`: temporary-root-owned, fake-provider,
  subprocess-free, environment-stable; eligible for collision qualification.
- `test_waffle_scone_finalization_slice0.py`: temporary-root-owned and
  provider-free but resource-heavy, with inherited semantic-closure fixture and
  two full public qualification calls; eligible for collision and contention
  qualification, not presumptively promotable.

Detailed surface inventory and probes:
`SLICE 1 - FIRST BATCH STATE SURFACE AUDIT.md`.

Slice 2 promoted both candidates after the complete collision matrix:

- bounded lifecycle: three two-copy self-collision repetitions plus imported
  helper, logging-sensitive, and qualification-heavy neighbor probes passed;
- Waffle/Scone: three two-copy self-collision repetitions plus full
  semantic-closure and qualification-heavy neighbor probes passed;
- no failures, errors, identity drift, protected-content leakage, provider I/O,
  or external-system activity occurred; and
- manifest inventory is now 40 parallel-safe, 53 provisional, 36 serial-only.

Two complete promoted two-worker groups were run concurrently as a four-process
stress case. Both passed 281 tests with 40 skips and exact matching identity
and outcome digests:

- identity: `84a5d22c08558e8152d4ed3c036223a5f8e2e68b0783c0379f38fc28a910bfb9`;
- outcome: `b93079452e3c7ec7afdf8f6d3c109b3860c7336cbb37621d1d89762dfdc0eef1`;
- wall seconds: 226.963869 and 226.712321.

Full record: `SLICE 2 - FIRST COLLISION AND PROMOTION BATCH.md`.

## Slice 1A serial-equivalence support extraction

- pre-extraction source checkpoint: `e6b38f3`.
- frozen exact identities: 98.
- pre/post identity SHA-256:
  `09e21da6a7941622e1af6388e8ae36973099d2568d82e40d9e602f650c797ed8`.
- pre/post outcome SHA-256:
  `36f64afd5edbd4ee1c69a2bf3a2e71500a8cdb445a4ef3a8ff65a86033e60c97`.
- final post-extraction semantic-closure result after per-test packet
  isolation: 98 passed, no skips, failures, errors, expected failures, or
  unexpected successes; 206.185926 seconds.
- support module: `_semantic_closure_support.py`, excluded from test discovery.
- direct consumers: 70 unique tests. Quiet negative-control result: 69 passed,
  one logging-sensitive failure, zero errors. The affected manifest-declared
  logging-sensitive module then passed all 11 tests unquiet in 40.816739
  seconds.
- final direct-consumer supported-posture pair: 59/59 quiet passed in
  292.218333 seconds; 11/11 logging-sensitive unquiet passed in 50.318792
  seconds. The two child processes overlapped without shared-state failure.
- focused runner/support guard: 16 passed.
- no manifest or production-package change.

## Whole-suite equivalence

Pending Slice 5.

## External-activity attestation

No provider, R2, Render, QA, production, package publication, or release action
is authorized by this campaign plan.
