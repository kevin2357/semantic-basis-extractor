# Slice 0 — Complete trace evidence

## Outcome

Complete. The capped 15-minute file 07 has been replaced by three unfiltered
five-minute exports, none of which reaches Render's 1,000-line cap. The
replacement proves that Turing has the same observer signature as Bodoni.

## Frozen export inventory

| File suffix | Bytes | Lines | First physical timestamp | Last physical timestamp | SHA-256 |
| --- | ---: | ---: | --- | --- | --- |
| 01 | 1,222,656 | 703 | 2026-09-14 23:11:35 | 2026-09-14 23:21:19 | `6d51700a350fefe0138225dda8c856bdfca286f4c690dc803d63a15f13cc8639` |
| 02 | 0 | 0 | — | — | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 03 | 0 | 0 | — | — | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 04 | 653 | 3 | 2026-09-15 00:00:15 | 2026-09-15 00:00:45 | `841e2215cc4187a6ed578de2d2d774f12482aa7388e46cc57ed065610dc348ca` |
| 05 | 0 | 0 | — | — | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| 06 | 308,386 | 138 | 2026-09-15 00:31:21 | 2026-09-15 00:41:07 | `ad5221d9307b6e6b62530dce01c4204b2caa3e0111261cd8484f473acafff62e` |
| 07-01 | 819,155 | 513 | 2026-09-15 00:41:41 | 2026-09-15 00:46:19 | `a8b88993a42e507f9220dff77ecb879ee102fb97b6bfdef4e5120a1e1905749c` |
| 07-02 | 601,726 | 356 | 2026-09-15 00:46:51 | 2026-09-15 00:51:34 | `c226a81a3062c4e9e88e487b510a22e2ffe222dd724fd3a48d317b0b5be320ef` |
| 07-03 | 582,973 | 326 | 2026-09-15 00:51:35 | 2026-09-15 00:55:59 | `594cea6be8d0f3dab9ac12b961c05505674997aaf771f29cbd4873db5b0e534b` |
| 08 | 0 | 0 | — | — | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Physical timestamps describe lines actually emitted; empty space within a
requested interval is not itself truncation. The three replacement line counts
and their contiguous requested windows establish that the formerly capped
interval was split below the export limit.

## Exact observer chronology

| Witness | Selection | Wrapper entered | Capture entered | Wrapper returned |
| --- | --- | --- | --- | --- |
| Bodoni | 00:50:28Z, exact review authority | 00:50:28Z | 00:50:28Z | 00:50:28Z, `unavailable` |
| Turing | 00:55:58Z, exact review authority | 00:55:58Z | 00:55:58Z | 00:55:59Z, `unavailable` |

Neither sequence contains capture completion, capture failure, envelope,
preflight, POST, artifact, observer-completed, or observer-failed evidence.
Because wrapper return is present for both, each call returned an API outcome
rather than escaping to the outer wrapper exception path.

No retained workspace, provider, API state, or Better Stack destination was
accessed or mutated in this slice.
