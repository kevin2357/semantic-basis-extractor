# SBE 0.4.2 API Consumer Handoff

For newly denied required work, consume the successful v0.2 result's
`run_transition`. Release API-owned authority only from an exact applied or
idempotently replayed result and matching action evidence. Then obtain a fresh
inspection and closeout; required external denial now produces terminal,
quiescent, dependency-free native state and a `closed` non-delivery result.

Use both status and terminal reason. `BUDGET_EXHAUSTED` with
`external_spend_authority_denied` or
`external_spend_reservation_unavailable` identifies an API/global spend refusal.
`POLICY_STOPPED` identifies product denial or cancellation. Optional stages with
frozen skip policy remain nonterminal, and accepted delivery remains authoritative.

For an affected retained 0.4.1 workspace, restore the complete snapshot at its
stable logical absolute path and invoke normal closeout/resume or:

```text
astrowoof-authoring-lifecycle --run-dir RUN reconcile-required-denial
```

The recognizer accepts only exact native legacy denial evidence with no provider,
consumption, report, ambiguity, contradictory state, or unrelated workspace
change. Anything else remains retained for review. Do not edit or re-snapshot SBE
state manually.

SBE owns native requiredness, action/run state, snapshots, reconciliation,
inspection, and closeout. The API continues to own reservations, quotas, circuit
breakers, entitlements, leases, billing reconciliation, publication policy,
PostgreSQL authority, HTTP status, and workspace deletion.

Complete contracts, examples, recovery rules, and result mappings are in the
packaged contract catalog and
`docs/post_extraction_authoring/Authoring Lifecycle Consumer Handoff.md`.
