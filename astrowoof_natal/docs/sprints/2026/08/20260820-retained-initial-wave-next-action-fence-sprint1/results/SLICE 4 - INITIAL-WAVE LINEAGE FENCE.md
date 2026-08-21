# Slice 4 — Initial-Wave Lineage Fence

Date: 2026-08-20
Status: complete; awaiting review
Provider/network use: none

## Outcome

An exact-interactive run may now prepare at most one distinct initial-wave
inventory. Freshness is no longer inferred merely because pass-attempt arrays are
empty. If the stored wave is absent while any native initial-authoring lineage
survives, SBE raises `initial_wave_lineage_unjoinable` before preparation,
authorization mutation, result publication, or provider I/O.

The refusal carries only closed redacted evidence categories through
`InitialWaveError.evidence_categories`. Categories distinguish prior initial paid
actions, provider identity, consumption/reporting, response evidence, ambiguity,
missing join artifacts, and conflicting native evidence. Lifecycle v0.5 will place
the same causal evidence into the already frozen closed
`external_authority_refusal` object rather than asking API to infer it.

## Exact stored-wave reuse

The presence of a stored object is not sufficient by itself. Before it is returned
as reusable, SBE proves:

- the stored wave is a valid exact-Natal six-member contract;
- the binding bundle validates against that exact wave;
- each member resolves to exactly one ledger action with the identical binding;
- the request inventory is exact and every private payload still hashes to the
  member request digest; and
- every member joins to its recorded initial pass attempt.

Provider state does not manufacture a new wave. A valid detached stored wave with
six durable Response IDs remains the same inventory and proceeds only through its
existing reconciliation semantics.

## Dispatcher and reader coverage

The fence runs both inside preparation and before generic interactive dispatch.
The second location matters when orphaned pass attempts would otherwise make the
initial-wave branch ineligible and fall through to ordinary authoring continuation.

The public external-authority reader applies the same orphan-lineage classification
before considering ordinary prepared actions. Historical initial actions can never
be relabeled as an `ordinary_action_set` request.

## Qualification

- Missing bundle, changed payload bytes, duplicate action, and missing attempt:
  typed pre-I/O refusal.
- Prior provider identity, consumption, reported cost, and ambiguity without a
  stored wave: typed pre-I/O refusal with the expected closed category.
- Generic public resume with retained attempts: byte-identical run/snapshot and
  zero provider creates.
- Valid stored wave with durable identities: exact reuse, six original actions,
  zero provider creates.
- Full semantic-closure suite: 92 passed.
- Focused lineage/public/execution: 22 passed; combined lineage/execution and
  initial-wave/spend compatibility: 52 passed.

No retained Aster evidence was opened or mutated. This establishes the native
one-wave safety rule; it does not declare Aster recoverable.
