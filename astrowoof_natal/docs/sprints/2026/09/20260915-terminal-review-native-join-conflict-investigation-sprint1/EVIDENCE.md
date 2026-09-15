# Evidence register

The authoritative coordinate, identity, digest, and authorization packet is recorded in `BACKGROUND.md`. It is intentionally sufficient to constrain the requested reads without enabling discovery or mutation.

## Slice 0

- Producer digest domain:
  `terminal_review_contracts.build_terminal_action_dispositions()` over the
  closed `_binding()` projection.
- Capture comparison domain:
  `editorial_review_runtime._collect_editorial_review_runtime_evidence()` over
  the complete ledger `binding` mapping.
- Delivery control bypasses the review-only disposition membership join.
- Exact source map and candidate matrix:
  `SLICE 0 - NATIVE JOIN SURFACE AND DIGEST DOMAIN.md`.

## Slice 1

- Read receipts: `r2-read-receipt.witness-a.json` and
  `r2-read-receipt.witness-b.json`.
- Provider operations: two HEAD, two GET, zero list/write/delete.
- Archive and inventory identities: exact matches to `BACKGROUND.md`.
- Exact native readers: accepted both selected result/receipt pairs.
- Top-level joins and retained initial-deck digests: all pass.
- Sealed/projected binding joins: 15/15 pass.
- Sealed/complete binding joins: 0/15 pass.
- Detailed finding: `SLICE 1 - EXACT RETAINED BINDING JOIN FINDING.md`.

## Slice 2

- Provider-free reproducer: `slice2_provider_free_reproduction.py`.
- Result: 2 tests passed in 0.001 seconds.
- Detailed correction fence:
  `SLICE 2 - CAUSAL REPRODUCTION AND CORRECTION FENCE.md`.

## Slices 3–4

- Shared digest helper: `terminal_action_binding_sha256()`.
- Consumer joins corrected: initial pass and optional stage.
- Packet complete-binding digest: preserved.
- New test module: `test_terminal_review_capture_binding_join.py`, registered
  in `test_suite_manifest.json`.
- Python 3.12 focused matrix: 82 passed.
- Python 3.11 focused matrix: 36 passed, 4 expected skips.
- Retained witness A: valid packet, 9 projections, 9 artifacts (7 provider
  responses and 2 distinct decks).
- Retained witness B: valid packet, 13 projections, 11 artifacts (8 provider
  responses and 3 distinct decks).
- Detailed qualification:
  `SLICE 3-4 - SHARED DIGEST CORRECTION AND FOCUSED QUALIFICATION.md`.
