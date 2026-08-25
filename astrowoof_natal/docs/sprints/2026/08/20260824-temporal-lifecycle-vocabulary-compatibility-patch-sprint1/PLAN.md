# Temporal Lifecycle Vocabulary Compatibility — Patch Sprint 1

Date: 2026-08-24
Status: complete; SBE 0.4.18 tagged, published, and verified

## Objective

Release the narrow SBE compatibility correction required for a retained
provider-reconciled workspace to be inspected through the temporal lifecycle
v0.6 reader.

## Finding

The ordinary lifecycle contract defines an action relationship as one of
`blocking`, `independent`, or `superseded`. The producer emits `independent`
for a resolved action. The temporal-v0.6 validator instead accepted
`blocking` or a non-existent `nonblocking` term. A valid retained checkpoint
with resolved initial-wave actions consequently failed before external
authority admission or provider I/O.

## Scope

- Align the temporal validator's closed relationship vocabulary with the
  lifecycle contract.
- Add a regression proving a v0.5-valid `independent` action projects and
  validates as temporal v0.6.
- Qualify and publish a fresh immutable patch release `0.4.18`.

## Non-goals

- No retained workspace mutation.
- No provider retrieval, creation, retry, or spend.
- No reconstruction or change of historical action evidence.
- No API or deterministic-runtime code change.

## Release gate

The release candidate must pass the focused legacy bridge and temporal
lifecycle suites, the full committed-source suite, and an installed-wheel
smoke/qualification appropriate to the project release process.
