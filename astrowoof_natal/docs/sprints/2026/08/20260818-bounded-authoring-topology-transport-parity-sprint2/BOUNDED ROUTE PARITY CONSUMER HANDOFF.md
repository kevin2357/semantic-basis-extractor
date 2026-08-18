# Bounded Route-Parity Consumer Handoff

Status: Slice 7 consumer-review candidate

## Supported boundary

SBE exposes bounded interactive and bounded Batch through the same public lifecycle
vocabulary already used by exact Natal. Consumers must validate native lifecycle
inspection v0.3 and reconciliation-cycle result v0.2. Product route records, logs,
or subprocess exit codes are not substitutes for that native evidence.

The installed package also publishes two sanitized, provider-free adoption
resources:

- `astrowoof.route_parity_transition_oracle.v2`; and
- `astrowoof.bounded_route_parity_traces.v1`.

Read them with `read_route_parity_oracle()` and
`read_bounded_route_parity_traces()`, or export them with:

```text
astrowoof-route-parity-evidence --kind oracle
astrowoof-route-parity-evidence --kind bounded-traces
```

The readers reject unknown fields, unknown schema versions, duplicate names,
unordered steps, and values outside the closed lifecycle vocabulary. The traces are
consumer adoption evidence only. Native inspection, cycle results, transition
journal, immutable execution result, publication receipt, and complete snapshot
remain authoritative for an actual run.

## Authority and cardinality

Bounded interactive creates one paid SBE action per pass attempt. Its immutable
binding includes route, assignment, logical pass, attempt, stage, and request
digest.

Bounded Batch creates one paid SBE action and one aggregate maximum commitment per
Batch round. Its ordered members are pass-level audit and settlement evidence; they
must not become separate API global reservations. Both mechanisms remain bounded by
the immutable run authority.

The API owns transactional cross-run reservations, quotas, circuit breakers,
entitlements, actual capacity allocation, account billing reconciliation, and
publication policy. SBE reports which exact native actions require retained
consumer authority; it does not claim ownership of API spend exposure.

## Custody and cost

`resume_not_before` is SBE's durable lower-bound recommendation. An earlier cycle is
strictly `not_due`, performs no provider retrieval, and creates no checkpoint.
Known provider identity is retrieval-only on resume; it never authorizes another
submission.

Provider retrieval custody and consumer financial authority are separate. After a
terminal Batch has been retrieved, integrity review or missing usage can retain
consumer authority without requiring endless provider polling. Complete usage for
every potentially billable member is required before a round is classified
`provider_usage_reported`. Any mixed or absent member usage remains
`provider_usage_unavailable_billing_reconciliation_pending`; it is never settled as
partial or zero cost.

## Required adoption traces

The packaged bundle covers:

- bounded interactive multi-pass continuation and pass-local retry;
- Batch pending, early `not_due`, due reclaim, and delivery;
- partial member failure followed by a one-pass retry round;
- retrieved output with unavailable usage and retained consumer authority;
- ambiguous submission retained for review; and
- terminal provider failure followed by explicit continuation authority.

These trajectories use no new public lifecycle states. The API must nevertheless
run them through its effective transition oracle; enum compatibility alone is not
route adoption evidence.

## Transport and optional stages

Interactive and Batch requests preserve the same frozen bounded logical pass bytes,
apart from documented provider-envelope controls. Batch covers initial authoring
and creative-retry rounds. Polish, critic, and qualitative-candidate stages remain
interactive Responses operations under this release contract, regardless of the
initial transport. Optional-stage Batch support is deferred.

## Failure and migration rules

- Bounded v1 one-operation workspaces are never synthesized into six-pass history.
  They fail closed with `legacy_bounded_topology_unsupported`.
- A provider identity/output/member conflict retains authority for review. Once
  terminal files are retrieved, this does not imply continued retrieval custody.
- Identity-less interrupted submission is ambiguous and fail-closed. Deterministic
  local keys are not proof of provider idempotency.
- Batch upload and creation cannot be made atomic with native persistence. After a
  durable provider ID, SBE can guarantee retrieval without duplicate submission.
  Before that identity is durable, the irreducible provider atomicity gap is
  represented as ambiguity, not silently retried.
- Logs and execution events are redacted, non-authoritative, and failure-isolated.

## API adoption checklist

1. Validate inspection v0.3 and its native route/mechanism/action identity.
2. Preserve one API reservation per Batch round, never per member.
3. Do not poll before `resume_not_before`.
4. Distinguish retrieval custody from retained consumer/billing authority.
5. Ingest terminal native results and receipts before translating API state.
6. Run every packaged route-specific trace through the API transition oracle.
7. Prove the new worker image and every API/worker runtime use matching compatibility
   identities and a fresh immutable generation-profile ID.
8. Prove a newly created run binds that profile before production admission.
