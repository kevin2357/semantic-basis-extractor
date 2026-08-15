# SBE 0.4.1 API Consumer Handoff

Replace a sequential loop over one stale lifecycle observation with one call to:

```python
deny_providerless_actions(run_dir, request)
```

or:

```text
astrowoof-authoring-lifecycle --run-dir RUN deny-providerless-batch --request REQUEST.json
```

The request binds one exact run and observed lifecycle/snapshot identity to an
ordered list of 1–32 exact action IDs, immutable bindings, denial reasons, and
bounded external-authority references. SBE validates every member under one
single-writer lock and applies all or none.

The API may release matching API-owned authority only when the top-level outcome
is `applied` or `idempotent_replay` and the exact returned member has
`release_eligible: true`. A refused batch releases nothing, including members
reported merely `eligible`.

Exact replay means the identical canonical request, including the original
observation timestamp and ordered members. A reordered or changed request is not
a replay. Provider identity/evidence, consumption, or ambiguous submission blocks
providerless denial and takes diagnostic precedence over generic staleness.

SBE owns native workspace state, eligibility, mutation, snapshot identity, and
native recovery. The API retains ownership of reservations, capacity, leases,
PostgreSQL records, publication, and cross-run policy. Events are redacted,
failure-isolated operational observations and are not authority.

Complete contracts, examples, recovery rules, and result mapping are in the
packaged contract catalog and
`docs/post_extraction_authoring/Authoring Lifecycle Consumer Handoff.md`.
