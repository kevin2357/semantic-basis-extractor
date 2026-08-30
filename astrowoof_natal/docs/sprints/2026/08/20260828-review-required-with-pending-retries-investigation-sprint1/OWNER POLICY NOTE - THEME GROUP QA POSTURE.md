# Owner policy note — theme-group QA posture

## Status

Recorded non-driving product context. This document does not change runtime
behavior and does not add a theme-group implementation track to this sprint.

## Product context

Theme groups were introduced as optional discovery/filter metadata: a user could
eventually narrow a WoofMap to cards associated with a topic such as curiosity
and play. The UI does not currently implement that filtering behavior. The
present registry/taxonomy was an early design and has not been established as a
generally applicable final product vocabulary.

The owner does not want an otherwise acceptable authored deck rejected—and paid
creative retries generated—solely to satisfy distribution constraints for this
unshipped, potentially revisable filtering feature.

## Important evidence refinement

The two retained runs did not fail the specific `theme_group_balance` predicate.
They failed `theme_group_coverage` in both pass-6 attempts: at least one registered
theme group was unused, or an unregistered group was assigned. The distinction is
technically important, but the same product-policy concern applies to both:
coverage and balance are taxonomy-quality constraints for an optional feature,
not evidence that the authored cards themselves are unusable.

## Possible later policy boundary

For the immediate product posture:

- theme-group coverage, balance, minimum-size, and cross-section variety should
  not be blocking authoring-pass or final-deck acceptance predicates;
- those conditions may remain available as advisory diagnostics so future UI and
  taxonomy work has evidence to inspect;
- basic structural safety should remain if theme-group fields continue to ship:
  placeholders must be resolved, identifiers must be syntactically valid, and a
  card must not reference an identifier absent from its emitted registry;
- disabling optional taxonomy-quality gates must not disable unrelated authoring,
  schema, lint, provenance, or editorial-quality validation;
- changing this policy does not repair or excuse duplicate paid-action lineage,
  mismatched retry bindings, provider-custody masking, or incorrect transition
  selection.

Whether theme-group authoring itself should later be removed, replaced with a new
taxonomy, or redesigned as multi-tag metadata is outside this investigation.

## Sprint consequence

Theme-group behavior is not a causal implementation focus for this sprint. Slice
2 may use `theme_group_coverage` to reproduce the historical bytes, but must also
prove the transition behavior with a generic legitimate QA rejection. The target
is stable action lineage, exact authorization binding, custody precedence, and
idempotent progress regardless of the rejection reason.

Disabling a particular rejection predicate would only avoid one trigger. It would
not correct the duplicate attempt actions, mismatched bindings, provider-custody
masking, or review mapping already present in the retained evidence. Any later
theme-group policy change should be planned independently after the lifecycle
correction is understood.
