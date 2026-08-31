# API review — Slice 1 schema and semantic contract freeze

## Decision

The contract shape is strong: the opaque root ID, complete digest binding,
closed top-level shape, class/posture/action matrix, deterministic ordering,
and terminal discovery provenance are all aligned with API Sprint 66.

Please make the three narrow semantic corrections below before beginning Slice
2. They are fixes to the promised closed contract, not a replan.

## Required corrections

1. **Lifecycle schema versions must be closed.** The Python validator and JSON
   Schema presently accept any `astrowoof.authoring_lifecycle_inspection.v0.N`
   string. That lets a hypothetical `v0.99` assessment pass despite the plan's
   explicit rule that unknown evidence versions fail closed. Freeze the set to
   the exact released lifecycle versions the reader will support (currently
   v0.5–v0.8, or an equally explicit supported set) and add a mutation test for
   an otherwise valid unknown version.

2. **Evidence categories must be a closed vocabulary.** The plan calls them
   closed, but schema/validator currently permit any safe reference string.
   Define the bounded allowed category tokens, validate every member against
   that set, and ensure `unsupported_or_inconsistent` carries one or more
   applicable tokens. API will display these, not infer an action from them,
   but a closed diagnostic contract still matters.

3. **Enforce summary count relationships.** In particular,
   `completed_unadopted_count` cannot exceed `provider_identity_count`; an
   assessment claiming completed provider evidence with zero provider identity
   currently passes. Freeze every other intrinsic relation now (for example
   bounded refs ≤ identities already exists), then add mutation coverage for
   the completed-without-identity contradiction.

## Approval boundary

Once those corrections are in place, Slice 1 is approved and SBE may proceed
to the snapshot-validating reader/projection in Slice 2. API can then use this
exact schema to begin its own durable admission/persistence mapping, but will
still wait for the released reader/wheel before real runner integration or
local resource release.

No provider work, retained-QA access, workspace mutation, deployment, tag, or
release is authorized by this review.
