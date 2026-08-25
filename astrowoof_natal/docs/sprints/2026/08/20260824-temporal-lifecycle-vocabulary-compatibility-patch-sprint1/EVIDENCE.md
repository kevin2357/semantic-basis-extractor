# Evidence

## Contract join

- Lifecycle schema relationship vocabulary: `independent`, `superseded`,
  `blocking`.
- Lifecycle producer: `blocking` for necessary actions and `independent` for
  resolved actions.
- Pre-patch temporal validator: `blocking`, `nonblocking`.
- Post-patch temporal validator: the exact lifecycle vocabulary.

## Regression evidence

`test_temporal_projection_accepts_resolved_independent_action` first validates
the synthetic inspection as v0.5, then builds and validates v0.6. It fails
against the pre-patch validator and passes with this correction.

The test uses no provider transport and no retained subject data.
