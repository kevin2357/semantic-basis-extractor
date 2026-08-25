# Log

## 2026-08-24 — Root cause and implementation

- The retained Aster QA workspace completed its bounded six-member GET-only
  reconciliation and then failed before provider work in
  `build_lifecycle_inspection_v06` with `Checkpoint action metadata is invalid`.
- The failure was reduced to a closed-vocabulary mismatch: lifecycle-produced
  resolved actions use `relationship: independent`, while temporal validation
  accepted `blocking` and `nonblocking`.
- Corrected temporal validation to the existing lifecycle vocabulary:
  `blocking`, `independent`, and `superseded`.
- Added a regression using a v0.5-valid independent action and proving that the
  temporal-v0.6 projection remains valid.
- Focused bridge and temporal suites: 33 passed, 3 existing optional/schema
  skips. No provider or retained-workspace activity occurred in this work.
