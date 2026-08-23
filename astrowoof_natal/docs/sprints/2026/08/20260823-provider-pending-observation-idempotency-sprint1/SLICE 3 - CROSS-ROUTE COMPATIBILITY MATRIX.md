# Slice 3 — Cross-Route Compatibility Matrix

Date: 2026-08-23
Status: complete; API fixture review pending

| Native route | Provider mechanism | v0.6 scheduling contract |
|---|---|---|
| Exact Natal | Response/interactive | Supported for initial, retry, and enabled optional stages |
| Exact Natal | Batch | Supported for initial and creative-retry rounds |
| Bounded Natal v2 | Response/interactive | Supported for initial, retry, and enabled optional stages |
| Bounded Natal v2 | Batch | Supported for initial and creative-retry rounds |
| Bounded Natal v1 | Batch | Fail closed as unsupported |
| Unknown/future route | Any | Fail closed as unsupported |

Optional polish, critic, and candidate provider actions use the interactive
Response adapter when enabled, including after an initial Batch authoring route.
An action that itself claims Batch transport for an optional stage remains
unsupported; the contract does not invent an adapter that production lacks.

## Qualification

For all four supported route/mechanism pairs, provider-free fixtures prove:

- one basis digest across not-due and due observations;
- exact route family and contract retained in the basis;
- canonical temporal eligibility progression; and
- SBE-owned due subset selection.

Interactive exact and bounded fixtures additionally cover all three enabled
optional stages. Exact and bounded Batch mechanism fixtures cover initial-round
custody; existing production-path bounded Batch tests prove detach/retrieve
identity and retrieval-only reconciliation.

## Fail-closed correction

The bounded Batch adapter previously accepted a legacy bounded v1 run when its
action route string happened to use the v2 Batch prefix. The adapter now also
requires the native `astrowoof.bounded_natal.authoring_run.v2` contract. This
prevents a string-shaped v2 operation from upgrading a legacy workspace.

## Public-state impact

No new public lifecycle state, capacity disposition, branch command, or API
scheduling behavior is introduced. The work supplies a strict v0.6 evidence
shape over existing supported routes and strengthens legacy refusal.
