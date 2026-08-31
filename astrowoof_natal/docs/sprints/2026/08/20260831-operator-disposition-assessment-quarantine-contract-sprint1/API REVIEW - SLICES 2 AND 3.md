# API review — Slices 2 and 3 reader/projection matrix

## Decision

The snapshot-validating reader, existing-lock-only fence, exact terminal
result/receipt/current-checkpoint join, historical v0.5 fail-closed fallback,
and cross-route matrix align with the intended API boundary. The reader does
not expose a provider retrieval subset or claim API-owned resource facts.

Please make one small correction before packaging.

## Required correction: availability recovery must be opt-in

`read_operator_disposition_assessment()` currently defaults
`allow_availability_recovery=True`. That makes bounded result discovery occur
on the ordinary/default assessment path, contrary to the frozen rule that
availability is only explicit recovery/preflight discovery and never normal
transition authority.

Change the default to `False` (or replace it with an explicit closed recovery
mode), and add a regression test proving that a no-argument/default reader call
does not call availability discovery. A caller that needs recovery may opt in,
then must still pass the discovered ID through the exact result reader as Slice
2 already does.

After that correction, Slices 2 and 3 are approved and SBE may proceed to
packaging/installed qualification.

No provider work, retained-QA access, workspace mutation, deployment, tag, or
release is authorized by this review.
