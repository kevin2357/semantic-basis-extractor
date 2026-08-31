# Slice 3 — provider-free cross-route matrix

## Status

Complete; paused at Voof-paws 3 before packaging.

## Matrix exercised

The real snapshot-validating reader was exercised against production-shaped
fixture workspaces for:

- exact interactive provider custody;
- exact Batch provider custody;
- bounded interactive provider custody;
- bounded Batch provider custody;
- mixed completed-unadopted plus pending custody;
- ambiguous call-entry evidence plus other known custody;
- legacy bounded Batch timing/evidence that is unsupported; and
- provider-free and exact sealed-terminal controls from Slice 2.

## Results

- All four supported route cells produce the same closed
  `provider_pending_known_identity` class and run-level
  `provider_reconciliation_cycle` next action.
- Completed provider evidence dominates separately pending work and yields
  `completed_unadopted` / `native_prior_action_required`.
- Ambiguity dominates separately known provider custody and preserves both
  subsidiary counts.
- Unsupported legacy bounded Batch evidence is explicit
  `unsupported_or_inconsistent` / `prohibited`; it is never interpreted as an
  interactive action.
- Every assessment path remains provider-free and nonmutating.

The assessment never exposes or asks API to reconstruct the SBE-selected
retrieval subset.
