# Log — quiet tests and safe parallel execution

## 2026-09-06 — Slices 0–1

- Adopted the owner decision to suppress routine console sparkle-dog output via
  a test-only log-level boundary; production and sink behavior stays unchanged.
- Mapped CLI/root logging configuration and identified the protected
  observability modules.
- Measured a representative CLI test at INFO and with test-only INFO
  suppression.
- Classified all 128 test modules conservatively.
- Found a hidden import-order dependency: direct module shards require explicit
  `PYTHONPATH=astrowoof_natal/src`.
- Ran the same 39-module safe-candidate inventory with one, two, and four
  processes. All corrected runs agreed on 239 tests, 41 skips, and success.
- Recommended two deterministic weighted workers for the first supported
  prototype; four round-robin workers were badly imbalanced.
- Made no production logging, test-runner, CI, or release-playbook change.
