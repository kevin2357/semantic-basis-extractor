# Slice 2 — first collision and promotion batch

## Decision

Promote both audited candidates to `parallel_safe`:

- `test_bounded_lifecycle.py`
- `test_waffle_scone_finalization_slice0.py`

Safety and reproducibility are the admission gates. Timing on the current
laptop is calibration evidence rather than a veto unless contention creates
instability or a clearly pathological slowdown. This preserves the longer-term
value of a manifest that can exploit stronger hardware and a larger suite.

No production code or test semantics changed. No semantic-closure test moved,
was renamed, or changed classification.

## Bounded lifecycle evidence

The 39-test module passed every collision class with zero skips, failures, or
errors: three two-copy self-collision repetitions; its imported-helper and
logging-sensitive neighbors; an existing qualification-heavy parallel module;
and the first-candidate pairing with Waffle/Scone.

Self-collision worker durations were 120.34/120.16, 111.63/111.21, and
124.03/124.00 seconds. This is stable relative to the 122.434-second frozen
isolated median and shows no material collision penalty.

## Waffle/Scone evidence

The six-test module passed every collision class with zero skips, failures, or
errors: three two-copy self-collision repetitions, the full 98-test serial
semantic-closure neighbor, and qualification-heavy
`test_happy_path_qa_slice4b.py`.

The first two self-collision repetitions showed CPU/disk contention
(232.71/232.54 and 220.90/220.02 seconds), while the third measured
138.85/138.63 seconds. The semantic-closure pairing took 170.86 seconds for
Waffle/Scone and the qualification pairing took 190.56 seconds. This confirms
resource sensitivity but no shared-state, identity, privacy, or correctness
failure. Worker-count calibration remains Slice 4 work.

## Actual-manifest stress proof

After promotion, two complete two-worker `parallel_only` runs were launched
concurrently, producing four active child workers as an additional stress
case. Both runs passed:

- 281 tests and 40 expected optional-schema skips;
- identity digest
  `84a5d22c08558e8152d4ed3c036223a5f8e2e68b0783c0379f38fc28a910bfb9`;
- outcome digest
  `b93079452e3c7ec7afdf8f6d3c109b3860c7336cbb37621d1d89762dfdc0eef1`;
- wall times 226.964 and 226.712 seconds.

The exact identity and outcome digests match across repetitions.

## Manifest result and boundary

- before: 38 `parallel_safe`, 55 `provisional`, 36 `serial_only`;
- after: 40 `parallel_safe`, 53 `provisional`, 36 `serial_only`.

The promoted weights retain the frozen isolated medians: 122.434 seconds for
bounded lifecycle and 122.645 seconds for Waffle/Scone.

This reaches Campaign paws-point 2. Do not expand to further provisional
modules until this batch is reviewed. Semantic closure remains serial and
unchanged.
