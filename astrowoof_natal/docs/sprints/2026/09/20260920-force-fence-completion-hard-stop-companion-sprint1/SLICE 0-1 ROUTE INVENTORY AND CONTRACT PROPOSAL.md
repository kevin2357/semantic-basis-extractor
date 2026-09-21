# Slices 0-1 — route inventory and completion-contract proposal

## Decision requested at Gate A

Reuse the existing native-suspension v1 result, receipt, and command-result
contract for the first active-route completion cell: interactive response
`provider_reconciliation`. Do not create an SBE “unsupported but releasable”
result. A route without a proven cooperative safe point remains an unresolved
escalation until API supplies exact parent-exit or platform-replacement proof.

## Route inventory

| Route family | Existing SBE control support | Exact safe boundary | Proposed completion class |
| --- | --- | --- | --- |
| `external_authority_v2_dispatch` | Existing 0.4.66 foundation. | Existing `dispatch_*` safe points. | Cooperative SBE stop when exact public handoff validates. |
| Interactive response `provider_reconciliation` | Existing observer accepts `command_kind=provider_reconciliation`. | `reconciliation_before_provider_get`; `reconciliation_after_response_checkpoint`. | First required extension/activation cell: cooperative SBE stop. |
| Batch reconciliation | No equivalent observer call is established by the current inventory. | None established. | Unresolved escalation; API parent/platform proof required unless a separately reviewed SBE safe point is added. |
| Any route with missing/stale/contradictory control evidence | Observer refuses or does not publish. | None. | Unresolved escalation; no capacity release from SBE silence. |

## Response reconciliation chronology

`reconcile_authoring_provider_cycle()` acquires the native single-writer lock,
loads and validates the workspace snapshot, then offers
`reconciliation_before_provider_get` before any provider retrieval. It uses a
bounded thread-pool wave for known provider-operation GETs. After all selected
responses return, it persists `run.json`, writes the reconciliation-cycle
record and workspace snapshot, and offers
`reconciliation_after_response_checkpoint`.

The post-response point is the relevant completion boundary for a fence that
arrives while GETs are in flight: it does not claim provider cancellation or
terminalization; it seals the exact observed checkpoint and retained provider
custody, then exits cooperatively before another local cycle.

## Exact handoff and precedence

The existing `NativeSuspensionControlObserver` already binds its publication
to the exact supervision capability, later force fence, request, invocation,
native run, command kind, observed/post-publication checkpoint bases, and
provider-boundary inventory. It publishes one result, receipt, and stdout
command result; replay follows the fixed indexed result rather than discovery.

API must continue to treat this as evidence of a cooperative SBE stop, not as
provider cancellation, native terminalization, workspace deletion, or an SBE
capacity release. API may release its local allocation only after its parent
also observes the child return through that exact handoff and completes the
separate API-owned transaction.

An ordinary native result that precedes the suspension observation remains
authoritative under the existing observer precedence guard. A late artifact
from a retired worker boot is not a valid substitute for either cooperative or
platform completion; API owns retired-boot exclusion.

## Refusal/escalation contract

There is deliberately no SBE document meaning “no safe point, release the
slot.” A missing request, timeout, malformed control document, unsupported
batch reconciliation posture, stale/mismatched identity, or no observed SBE
result is an unresolved escalation. It must drive the approved exact
parent-exit or worker-replacement lane; it may never be interpreted as child
exit or release authority.

## Verification

Executed provider-free from this checkout with `PYTHONPATH=astrowoof_natal/src`:

```text
python -m unittest astrowoof_natal.tests.test_native_suspension_runtime_slice3
Ran 11 tests ... OK
```

The suite includes reconciliation observation before any provider GET and
public coordinator propagation through the post-response checkpoint boundary.
