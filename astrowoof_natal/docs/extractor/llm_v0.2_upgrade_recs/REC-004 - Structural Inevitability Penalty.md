# REC-004 — Structural Inevitability Penalty

## Problem Statement

A portfolio optimizer that scores candidates independently tends to overvalue observations that are merely *structurally inevitable*. Some semantic claims appear important because they are implied by many neighboring structures, are duplicated through multiple derivation paths, or are nearly guaranteed to occur for broad classes of source graphs. Left uncorrected, these candidates consume limited authoring budget while contributing comparatively little discriminating information.

The optimizer therefore requires an explicit mechanism that distinguishes **structural inevitability** from **semantic importance**.

## Recommendation

Introduce a Structural Inevitability Penalty as a component of candidate evaluation.

The penalty should reduce the effective utility of candidates whose presence is largely explained by predictable structural consequences rather than distinctive semantic information.

The intent is not to discard inevitable candidates automatically, but to ensure they compete fairly against candidates that contribute genuinely new information.

## Design Principles

A Structural Inevitability Penalty should:

- operate as a bounded utility adjustment rather than an exclusion rule;
- preserve deterministic behavior;
- avoid penalizing foundational dependency candidates required for portfolio coherence;
- compose with the broader utility vector rather than replacing existing utility metrics.

## Rationale

Structural frequency is not synonymous with informational value.

Candidates that are nearly guaranteed by graph topology frequently exhibit high apparent support while contributing little additional explanatory power. Penalizing inevitability encourages the optimizer to preserve observations that better differentiate one semantic portfolio from another.

## Quality Assurance

Validation should demonstrate that:

- distinctive candidates are no longer consistently displaced by structurally inevitable ones;
- dependency closure remains unaffected;
- repeated executions produce identical adjusted scores for identical inputs.

## Summary

The Structural Inevitability Penalty prevents highly predictable semantic consequences from dominating bounded authoring portfolios, improving informational diversity while preserving deterministic optimization behavior.
