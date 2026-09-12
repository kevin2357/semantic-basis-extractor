# Slice 1 — Batch 12 actual-manifest stress blocker

## Outcome

The authorized Batch 12 manifest promotion is applied and its focused guards
pass. The paired actual-manifest stress gate is not green because both complete
coordinators encountered the same unrelated current-main frozen BRE packet-
digest mismatch.

This is not evidence of a Batch 12 collision. The failing assertion reproduces
immediately in a single isolated test process.

## Promoted manifest

- `parallel_safe`: 85 modules
- `provisional`: 14 modules
- `serial_only`: 37 modules
- `logging_sensitive`: 12 modules
- manifest SHA-256:
  `ee50924668beb037f9958f24467c6fa625a60fae9706361bb4ff87a8ba6e6a3b`
- focused runner/manifest guard: 16 passed

Only these approved modules moved, with their current-source weights:

- `test_editorial_review_contract_fixtures.py`: 8.450852 seconds
- `test_editorial_review_contract_qualification.py`: 7.621098 seconds
- `test_editorial_review_contract_foundation.py`: 2.274651 seconds
- `test_editorial_review_runtime.py`: 2.123262 seconds

## Paired stress result

Two complete two-worker `parallel_only` coordinators ran concurrently against
the exact manifest above.

| Copy | Tests | Skips | Test inventory SHA-256 | Outcome inventory SHA-256 | Wall time |
|---|---:|---:|---|---|---:|
| 1 | 680 | 51 | `d327504eb664b04a0b0426c881a67eb1d0a2d00a8957b82257b9a529624b8c46` | `71548a766853a98a70ce6cfd7c6ebc6acb11316dcddf3ad8f788d064f7fd6043` | 663.746952 s |
| 2 | 680 | 51 | `d327504eb664b04a0b0426c881a67eb1d0a2d00a8957b82257b9a529624b8c46` | `71548a766853a98a70ce6cfd7c6ebc6acb11316dcddf3ad8f788d064f7fd6043` | 663.342134 s |

Each copy failed only:

`astrowoof_natal.tests.test_bounded_sprint_baseline.TestBoundedSprintBaseline.test_frozen_exact_bre_replay`

The assertion expected packet SHA-256
`d13a7d456ddc6dfd1b6f959d6b36108fe44699f30c95274843a8fa6e46ca54a4`
but current source produced
`5af594bfa3520e5e2b73fa92405d4f3fc37a69e49825664b9e196861d0260f63`.
Both coordinator stderr files were empty; the detailed unittest failure remained
inside the runner-owned failed-group log as designed. No matching child process
remained afterward.

Raw receipts are retained under
`C:\tmp\sbe-batch12-manifest-stress-20260912`.

## Isolated causal check

The exact failing test also fails alone in 0.116 seconds with the same expected
and actual digests. Reconstructing every frozen value produced this comparison:

| Frozen field | Expected versus current |
|---|---|
| candidate count | 103 = 103 |
| candidate SHA-256 | exact match |
| selected count | 50 = 50 |
| selected SHA-256 | exact match |
| rejected count | 53 = 53 |
| QA SHA-256 | exact match |
| QA status | `pass` = `pass` |
| packet SHA-256 | **only mismatch** |

No `extractor.py` commit exists between the Batch 11 checkpoint and current
`HEAD`. Multiple packaged-resource commits do exist in that interval. The
compiled packet carries resource provenance, so the evidence supports a narrow
stale frozen packet digest rather than changed bounded semantics.

## Requested decision

Review should either:

1. authorize updating only the frozen `exact_bre_replay.packet_sha256` to the
   independently reproduced current digest, followed by the direct baseline
   module, runner guards, and the same paired actual-manifest stress gate; or
2. identify additional provenance validation required before that correction.

No unrelated baseline field, Batch 12 test, production/package behavior,
provider/external system, semantic-closure classification, or release authority
should change. Batch 12 must not be called complete until the paired gate is
green and separately reviewed.
