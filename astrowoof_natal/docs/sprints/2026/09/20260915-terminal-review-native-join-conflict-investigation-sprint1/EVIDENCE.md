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
