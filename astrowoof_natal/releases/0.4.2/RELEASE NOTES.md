# AstroWoof Natal Authoring 0.4.2

Status: prepared for immutable release qualification. Tagging and publication are
not yet complete.

This patch closes the required-action providerless-denial lifecycle gap. A denial
accepted for native required work now commits an explicit run-level terminal
outcome rather than leaving the workspace in an impossible local-continuation
loop.

## Added

- atomic required-action terminalization for single and batch providerless denial;
- `BUDGET_EXHAUSTED` with distinct external-spend causes and `POLICY_STOPPED` for
  product denial/cancellation;
- v0.2 successful denial results with exact `run_transition`, ordered denied
  members, and causal required members;
- terminal, quiescent, dependency-free inspection and closed non-delivery closeout;
- narrow provenance-validated recovery for affected retained 0.4.1 workspaces;
- installed `reconcile-required-denial` CLI and matching Python surface;
- interruption recovery at every reconciliation persistence boundary; and
- updated packaged catalog, installed smoke, and API consumer handoff.

Optional-stage skip, accepted-delivery precedence, existing single/batch commands,
provider-safety refusal, snapshot integrity, and API/SBE ownership boundaries are
preserved.

Provider operations and provider spend during implementation and qualification:
zero / `$0`.

## Qualification

Final immutable artifact identity and publication evidence will be recorded after
the exact preparation commit is built and qualified twice on Windows and Linux.
