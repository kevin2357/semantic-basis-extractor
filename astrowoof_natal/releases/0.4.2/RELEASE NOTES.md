# AstroWoof Natal Authoring 0.4.2

Status: qualified for immutable annotated tag
`astrowoof-natal-authoring-v0.4.2`. Publication is pending.

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

- complete repository suite: 310 passed;
- two independent fixed-epoch builds were byte-identical;
- wheel SHA-256:
  `cb63b4ff8a014a1e5848071a52c280bd14c2b69293388b1c2576a5e9940f7366`;
- wheel bytes/entries/resources/cache entries: 726711 / 84 / 44 / 0;
- fresh installed lifecycle smoke passed on Windows and Linux CPython 3.11 using
  the exact candidate bytes; and
- artifact source commit:
  `9516a601929334dea287a4fc5ae0560d23c437c1`.

Tagging and publication remain pending until the release-record commit is locked.
