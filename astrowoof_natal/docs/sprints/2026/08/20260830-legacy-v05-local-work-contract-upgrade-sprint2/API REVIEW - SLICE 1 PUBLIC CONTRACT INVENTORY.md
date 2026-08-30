# API review — Slice 1 public contract inventory

## Decision

Approved for SBE Slice 2 provider-free evidence witness.

The inventory correctly freezes the only upgradeable asymmetry:

- SBE v0.5 accepts an otherwise coherent `ordinary_resume` when completed
  provider evidence establishes local continuation despite an empty
  `local_dependencies` list.
- API's v0.5 consumer currently requires the dependency list to be nonempty.

This is narrow enough to classify positively at API's semantic-validation
boundary. It is not permission to catch a generic contract exception or weaken
another v0.5 invariant.

## Minimum-evidence rule

Approved as written:

- v0.7 suffices only for exact executable local work with no higher-precedence
  provider custody or retry-lineage ambiguity;
- v0.8 is the final scheduling surface for the Diffie-shaped mixed completed/
  pending retry-custody case; and
- missing or incompatible successor evidence becomes stable API review.

## Slice 2 evidence requirements

Please provide an API-consumable, provider-free witness that proves all of the
following against the same restored checkpoint:

1. SBE's released v0.5 validator accepts the legacy document.
2. API's current stricter nonempty-dependency predicate is the *only* rejected
   semantic relation.
3. The v0.7 and, for mixed custody, v0.8 documents validate through their
   released public readers and bind to the same run/revision/snapshot/logical
   root.
4. v0.8 selects provider custody/reconciliation rather than local dispatch for
   the mixed-custody witness.

One guardrail: API should use SBE's public v0.7/v0.8 validators and their
predecessor reconstruction as the canonical action/binding/provider join. API
may independently compare stable shared identities, but should not duplicate
SBE's complete action/provider composition rules from raw documents.

No source change, package change, provider activity, retained-QA access,
deployment, or release is authorized by this review.
