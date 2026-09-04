# API Slice 2 — product decision

## Decision: approved

Remove dormant theme-group cardinality and balance enforcement from the
post-polish/final editorial validator and its packaged handoff bundle.

Theme groups are no longer a current acceptance or assembly feature.  A deck
must therefore not fail final validation because theme-group data is absent,
incomplete, or imbalanced.  Legacy theme-group fields remain tolerated for
historical-workspace compatibility, but are not evaluated as editorial quality
criteria and must not affect a final-validation outcome.

## Evidence basis

The bounded inspection verifies the same result for both independent runs:

- all six initial authoring acceptances were accepted with no editorial or
  advisory codes;
- polish was adopted exactly;
- post-polish lint passed with zero warnings; and
- final validation failed only `theme_group_cardinality` under the identical
  stable issue digest
  `cecc9ea012e6dd75a9e0773bbf3830ff91e063e4cba08da324e7cd88ced5fd22`.

That is decisive evidence of a dormant final-validator policy, not a provider,
custody, optional-stage adoption, or API terminal-projection defect.

## Scope and regression boundary

This is a narrow SBE/package correction.  It must not change the meaning of
other validation rules, approval/assembly ownership, provider routes, or the
API/SBE lifecycle contract.  The implementation should prove both:

1. a deck with no theme-group data can pass final validation when all still-live
   editorial rules pass; and
2. legacy theme-group fields may be present without contributing a
   cardinality/balance error, while unrelated live validation failures remain
   enforced.

No retained-QA recovery, provider activity, reconciliation, or API mutation is
authorized by this decision.  A subsequent release and fresh qualification
cohort can validate the behavior through the normal boundary.
