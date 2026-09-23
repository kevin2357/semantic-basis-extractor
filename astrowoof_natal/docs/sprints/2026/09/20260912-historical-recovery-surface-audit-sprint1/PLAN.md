# Historical Recovery Surface Audit — SBE Plan

## Status

Active — inventory and classification only.

## Slice 0α — Incident-driven native change-set reconnaissance

Before the current-tree inventory, independently trace the SBE companion work
for the API incident-era starting set: API Sprints 26, 27, 32, 33, 35, 37, and
38. Use cross-repository sprint references, Git commit chronology, release
notes, and actual production diffs to identify the matching SBE sprint(s); do
not assume a same-numbered or same-date directory is a companion.

For each API sprint, record in `SBE Recovery Surface Inventory.md`:

- the identified SBE companion sprint(s), relevant SBE commits, and the exact
  production surface introduced or changed;
- whether the change repaired a generic current native contract, introduced a
  deliberately supported versioned migration, preserved a fixture-only shape,
  or appears to be historical recovery residue;
- accepted workspace/journal/result/receipt versions and all public CLI,
  Python export/reader, package-resource, API-caller, and ordinary-worker
  reachability;
- the authority/evidence it consumes, its current typed failure disposition,
  and targeted/current regression coverage; and
- negative findings where a historical incident produced no retained SBE
  recovery branch.

The inventory must use the same per-record format and level of evidence as the
regular Slice 0/1 native inventory, not a prose-only sprint timeline. Preserve
historical fixtures and released-contract readability even if a future review
removes a production-only bridge.

**Exit:** an API-sprint-to-SBE-companion map and evidence-backed native records
for every identified production change, with no removal recommendation.

## Slice 0 — Native recovery inventory

Inventory SBE production commands, workspace/journal readers, compatibility bridges, retained-artifact readers, recovery dispositions, and legacy fixtures that can influence an operator-facing runtime route.

For each, record the full required inventory record from `BACKGROUND.md`:
source/provenance, accepted evidence/version, runtime-versus-fixture scope,
public invocation/export/resource/API/worker reachability, authority
boundaries, typed failure disposition, test coverage, and historical fixture
preservation requirements. Record the results in `SBE Recovery Surface
Inventory.md`, extending the Slice 0α records rather than creating a second
format.

## Slice 1 — API join and supported-artifact reachability

Map each native surface to the API consumer or confirm it is native-only or
fixture-only. Identify which historical workspace/journal/result versions are
deliberately supported by current contracts, and distinguish a versioned public
migration from an undocumented historical bridge.

## Slice 2 — Joint classification

With API, classify all surfaces as durable capability, supported migration, test-only support, or one-off removal candidate. Do not change behavior in this slice.

## Slice 3 — Removal contract proposal

For confirmed one-off candidates, define clean typed fail-closed behavior, required fixture preservation, and provider-free regression gates for a later implementation sprint.
