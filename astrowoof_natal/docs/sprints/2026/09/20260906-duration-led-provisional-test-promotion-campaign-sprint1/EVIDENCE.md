# Evidence — duration-led provisional test promotion campaign

## Status

Slices 0 and 0A complete; paused for review before any promotion or semantic-
closure decomposition.

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

None. No manifest classification changed.

## Whole-suite equivalence

Pending Slice 5.

## External-activity attestation

No provider, R2, Render, QA, production, package publication, or release action
is authorized by this campaign plan.
