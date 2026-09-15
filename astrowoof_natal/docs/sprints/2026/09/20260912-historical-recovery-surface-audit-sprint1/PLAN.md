# Historical Recovery Surface Audit — SBE Plan

## Status

Active — inventory and classification only.

## Slice 0 — Native recovery inventory

Inventory SBE production commands, workspace/journal readers, compatibility bridges, retained-artifact readers, recovery dispositions, and legacy fixtures that can influence an operator-facing runtime route.

For each, record source location, accepted evidence/version, invocation and caller path, authority boundaries, failure disposition, test coverage, and historical provenance.

## Slice 1 — API join and supported-artifact reachability

Map each native surface to the API consumer or confirm it is native-only/test-only. Identify which historical workspace or result versions are deliberately supported by current contracts.

## Slice 2 — Joint classification

With API, classify all surfaces as durable capability, supported migration, test-only support, or one-off removal candidate. Do not change behavior in this slice.

## Slice 3 — Removal contract proposal

For confirmed one-off candidates, define clean typed fail-closed behavior, required fixture preservation, and provider-free regression gates for a later implementation sprint.
