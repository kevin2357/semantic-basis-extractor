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
