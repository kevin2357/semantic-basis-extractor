# API Consumer Handoff — SBE 0.4.25

The normative lifecycle and retry mapping is frozen in:

- `docs/sprints/2026/08/20260825-post-fan-in-retry-matrix-contract-sprint1/SLICE 4 - INSTALLED V2 QUALIFICATION AND API HANDOFF.md`

API must adopt lifecycle inspection v0.7 before routing concrete post-fan-in local
work. For `ordinary_resume`, validate a nonempty local-work inventory and invoke
only the supported run-level ordinary command. Do not select or execute inventory
members directly.

After execution, ingest a successor that either records the prior semantic key in
cumulative `consumed_operation_keys` or selects a different typed disposition.
Provider reconciliation and external authority retain their existing ownership
boundaries: SBE selects native work; API owns leases, reservations, global spend,
admission, persistence, and product policy.

Lifecycle v0.5 and temporal v0.6 remain readable historical contracts, but fail
closed with `local_work_contract_upgrade_required` when this richer proof is needed.
The qualification receipt is evidence only and grants no execution authority.
