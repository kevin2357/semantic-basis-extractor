# Slice 3 — promotion batch 3

## Decision

Following owner approval of the state-surface audit, promote:

- `test_post_fan_in_retry_qa_slice4.py`;
- `test_post_fan_in_retry_composed_runtime_slice3.py`; and
- `test_optional_stage_completed_evidence_adoption_slice2.py`.

No test-only repair was necessary. No test identity, production behavior,
semantic-closure classification, or external contract changed.

## Collision matrix

Three repetitions launched two independent copies of all three candidates
together. All 18 workers passed:

| Module | Result per copy | Repetition durations (seconds) |
|---|---|---|
| post-fan-in retry QA | 10 tests, 1 optional-schema skip | 23.67/23.38; 23.37/23.32; 22.86/22.65 |
| composed runtime | 7 tests, 0 skips | 23.00/22.57; 21.46/21.39; 21.39/21.13 |
| optional-stage adoption | 6 tests, 0 skips | 21.47/21.13; 21.01/20.85; 21.34/21.23 |

The close paired timings show no material resource contention. Provider-I/O
fences, per-test action/marker identities, local locks, process-local packet
copies, and scoped patches remained intact.

## Actual-manifest proof

After promotion, two complete two-worker `parallel_only` groups ran
concurrently. Both passed:

- 324 tests, 43 expected optional-schema skips;
- identity digest
  `752c07c1ce7bf7f4bf1024645681f2d84a27a92298c7b52e47f1586271bf5ef0`;
- outcome digest
  `c58bbbcab0eab12d89c520a80840d8e40955a34a92823c156a72ae5f6c7b9249`;
- wall times 275.326 and 275.186 seconds.

The exact inventory and outcome digests match. The parallel group gained 23
tests while the four-process stress critical path remained effectively
unchanged from Batch 2's approximately 275.4 seconds.

## Manifest and boundary

- before: 43 parallel-safe, 50 provisional, 36 serial-only;
- after: 46 parallel-safe, 47 provisional, 36 serial-only.

This is the requested combined review point. Pause before selecting or
promoting another cohort. Semantic closure remains unchanged and serial.
