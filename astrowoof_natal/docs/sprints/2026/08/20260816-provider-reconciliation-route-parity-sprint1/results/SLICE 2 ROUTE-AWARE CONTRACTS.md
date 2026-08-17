# Slice 2 Route-Aware Contracts and Dispatch

Date: 2026-08-16  
Status: complete; awaiting gate review  
Provider operations: 0  
Paid spend: `$0`

## Outcome

The approved route-parity safety contract is now executable and strict without
prematurely enabling either deferred provider adapter.

## Implemented contract surface

- Promoted runtime lifecycle inspection to
  `astrowoof.authoring_lifecycle_inspection.v0.3`.
- Added strict `native_route` identity with closed `exact_natal` and
  `bounded_natal` families and exact native contract IDs.
- Extended every provider-custody action with route family, service level,
  provider operation kind, provider operation ID, and native operation/round ref.
- Added independent `consumer_authority` state and per-action retention reason and
  cost disposition.
- Published provider reconciliation policy v0.2 with separate Response and Batch
  schedules and I/O limits.
- Published cycle-result v0.2 with strict provider-operation summaries and explicit
  cost disposition.
- Preserved inspection v0.1/v0.2, policy v0.1, and cycle-result v0.1 as historical
  packaged contracts and catalog identities.

## Route-aware classification

One native classifier now distinguishes:

| Identity | Classification in Slice 2 |
|---|---|
| Exact + interactive Response | `exact_interactive` supported baseline |
| Exact + Batch initial/retry | Valid identity, `exact_batch_deferred` |
| Bounded + interactive Response | Valid identity, `bounded_interactive_deferred` |
| Bounded + Batch | Invalid, `bounded_batch_unsupported` |
| Unknown/contradictory route, stage, service, provider kind, round, or ID | Invalid/unsupported |

Exact Batch identity is validated against exactly one native round with the same
`batch-round-NNN` reference and Batch ID. Bounded Response identity is validated
against the actual bounded run contract and route prefix.

Deferred identities remain `unsupported_retain_capacity`; recognition alone does
not authorize worker release. Slices 3 and 4 must explicitly enable their adapters.
This also fixes the Slice 0 bounded accidental-inheritance defect.

## Custody versus consumer authority

Provider-pending actions appear in both retrieval custody and consumer authority.
An action with
`provider_usage_unavailable_billing_reconciliation_pending` appears only in
consumer authority after retrieval custody ends. Tests prove it has no due provider
action and cannot be interpreted as reported zero usage.

Ambiguous submission also retains consumer authority even when there is no safe
provider ID to poll.

## Compatibility

Existing v0.1 timing attached to retained exact interactive actions remains
accepted. New timing uses policy v0.2's unchanged Response delays. Exact
interactive cycle results now emit v0.2 with inspection v0.3 and operation/cost
summaries; historical fixtures remain valid under their original schema versions.

## Tests

Focused contract, route, lifecycle, consumer, release-catalog, bounded, and Batch
baseline coverage passed all 77 tests in 22.831 seconds.

The complete repository suite passed all 343 tests in 133.889 seconds.

`git diff --check` is required at the final gate. No network transport, API key,
provider endpoint, build, or release operation was used.

## Gate conclusion

Only exact interactive work can currently advertise a releasable provider wait.
Every inspection now supplies strict native route/mechanism evidence and separate
consumer-authority evidence. Exact Batch and bounded interactive are ready for
their route-specific adapter slices without another public identity redesign.
