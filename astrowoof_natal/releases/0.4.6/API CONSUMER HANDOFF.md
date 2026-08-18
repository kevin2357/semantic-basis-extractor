# SBE 0.4.6 API Consumer Handoff

Status: consumer-approved Slice 7 contract; final artifact pending

The authoritative integration boundary remains lifecycle inspection v0.3,
reconciliation-cycle result v0.2, transition journal, immutable execution result,
publication receipt, and complete validated snapshot. Logs, events, subprocess exit
codes, and packaged oracle traces are not native run authority.

## Frozen consumer-fixture identities

The API accepted these Slice 7 installed resources. Their identities must remain
unchanged in the final wheel:

| Contract | SHA-256 |
|---|---|
| `astrowoof.route_parity_transition_oracle.v2` | `c355a3c47b69fcbc78622df97b89572172133253f34d0342ae18e609e1e4d97d` |
| `astrowoof.bounded_route_parity_traces.v1` | `02d8aba73028c144c97e8c806cd0f8b3505fe4ca3410284d4bc8e2d4c33f0268` |

Use `read_route_parity_oracle()` and `read_bounded_route_parity_traces()`, or the
provider-free `astrowoof-route-parity-evidence` command.

## Authority rules

- Bounded interactive uses one paid action per pass attempt.
- Bounded Batch uses one paid action and one API reservation unit per Batch round;
  members are audit/settlement evidence only.
- `resume_not_before` is a native lower bound. Earlier reconciliation is
  nonmutating `not_due`.
- Known provider identity permits retrieval only, never resubmission.
- Provider retrieval custody and consumer financial authority are independent.
- Missing or partial member usage remains
  `provider_usage_unavailable_billing_reconciliation_pending`, never partial or
  zero settlement.
- SBE owns native execution truth. The API owns cross-run reservations, quotas,
  circuit breakers, entitlements, capacity, account reconciliation, and
  publication policy.

API adoption must run every packaged route trace through its transition oracle and
prove a newly registered immutable generation profile binds the exact deployed API
and worker compatibility identities.
