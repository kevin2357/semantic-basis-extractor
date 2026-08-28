# Slice 3 — Review Custody Settlement Without Authoring Reopen

## Three-class public witness

The exact-interactive public command now has a production-shaped provider-free
witness containing all three incident-relevant action classes at once:

1. a reported action;
2. a WAITING action with one durable Response ID; and
3. an AUTHORIZED action with no provider identity.

Before exit 2, the command seals a v0.2 result with
`custody_finality=mixed_resolution_required`, exact ordered reconciliation and
providerless-denial inventories, and `new_provider_create_permitted=false`. The
command-result envelope joins the exact invocation, result, and receipt.

## Completed retained provider work

The supported reconciliation command may GET an already-submitted Response after
editorial review. If that Response completes, SBE records its returned usage and
cost availability and terminally accounts the paid action. It deliberately does
not pass the response content through authoring, finalization, retries, polish,
critic, or candidate generation.

This separates two truths:

- provider evidence and financial settlement may arrive after editorial review;
- editorial review remains terminal and cannot be reopened by that arrival.

The regression makes the ordinary authoring and finalization functions fatal test
sentinels. The completed reconciliation succeeds without reaching either one.

## Unused authority

The providerless AUTHORIZED action remains separately denial-only. The existing
exact providerless-denial operation validates its full binding and observation,
records immutable negative-authorization evidence, and accepts no provider
transport. Publication of review status alone is not reservation-release evidence.

## Final posture

After the completed provider operation is accounted and the unused action is
denied, closeout reports:

- native terminal: true;
- provider continuation remains: false; and
- local continuation remains: false.

This is native evidence only. API still owns reservation release, capacity, lease,
billing reconciliation, and public job disposition.
