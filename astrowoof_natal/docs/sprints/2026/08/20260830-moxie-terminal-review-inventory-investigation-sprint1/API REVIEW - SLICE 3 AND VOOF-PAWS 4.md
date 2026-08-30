# API review — Slice 3 and Voof-paws 4

## Decision

Approved. The characterization reaches the relevant real boundaries: native
resume, post-fan-in lifecycle/progress fencing, terminal-review publication,
command result/result reader, and strict API action join. Its one controlled
local-authoring mutation is appropriately narrow and provider creation is
forbidden.

The reproduction proves the correction belongs primarily in SBE native runtime
ordering, not in a new API inventory-scope contract:

1. reconcile/validate retry-2's completed provider result into the canonical
   pass/attempt truth;
2. perform deterministic pass QA from that validated result;
3. only then select a successor retry, if QA requires one; and
4. if a successor is prepared, finish consuming the predecessor local operation
   and publish the normal exact external-authority request before any terminal
   review can be sealed against API's action inventory.

API continues to own strict admission/dispatch and must never manufacture or
retrospectively deny a native-only action from terminal-review evidence.

## Important implementation fence

Do **not** implement the correction as a blind pass-state flip whenever the
ledger says a provider action is complete. “Adopt” must mean the existing
native/provider-result validation, response parsing, binding/identity checks,
and deterministic pass-QA path have succeeded. If that material is unavailable,
invalid, ambiguous, or incompatible, preserve the typed existing custody/review
route—do not prepare a successor and do not call the predecessor consumed.

The legitimate-retry path must obtain its external-authority inventory from a
post-consumption successor inspection, not construct an equivalent request from
private state. This preserves the API/SBE grant fence.

## Next step

Voof-paws 4 is satisfied. Select **SBE runtime fan-in adoption ordering** as
the primary correction in Slice 4, with a provider-free test matrix covering:

- accepted provider result → no successor;
- QA-rejected validated result → exactly one prepared successor and exact
  external-authority request;
- invalid/ambiguous/unavailable result → no successor and no consumption;
- no terminal-review result containing a native-only successor before its
  authority request can be observed.

Update the plan's now-resolved early hypotheses while making that decision.
Pause before implementation/package work if the correction needs a new public
contract rather than the existing native fan-in path.
