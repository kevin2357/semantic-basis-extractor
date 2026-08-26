# Background — Post-Fan-In Retry Matrix Contract Sprint

## Why this exists

A fresh QA cohort traversed the initial six-member fan-out/fan-in successfully
under SBE `0.4.24`, then exposed an unqualified post-fan-in retry route.

For the Crumpet run, authoritative API evidence shows:

1. all six initial actions reached reported state;
2. a first `creative_retry` received a provider identity;
3. a second `creative_retry` was prepared/authorized but did not receive a
   provider operation at observation time; and
4. subsequent native inspection selected `ordinary_resume` / API-observed
   `local_resume`, while reporting zero provider-local dependencies and
   continuing to require local continuation.

The worker repeatedly completed quiescent local-resume cycles. The API did not
invent provider authority; it honored the native branch/readiness result.

This is a contract-qualification problem, not a request to make Crumpet
special. The desired result is a provider-free public matrix that proves the
post-fan-in behavior of the lifecycle routes that production can actually
select.

## Existing public proof and its boundary

`run_provider_pending_lifecycle_qualification()` currently proves:

```text
six initial provider identities
  -> bounded retrieval/fan-in
  -> one await_external_authority action
```

The API consumes that closed receipt successfully. It does **not** presently
receive supported SBE fixture/receipt evidence for:

- post-fan-in creative retry creation;
- retry retained as provider-pending;
- first retry reconciled followed by a second retry request;
- retry exhaustion or terminal native outcome; or
- ambiguous retry lineage.

Those cases must not be invented in API fixtures and presented as native proof.

## Proposed provider-free matrix

The new or expanded SBE qualification must expose closed public evidence for
the following mutually exclusive outcomes:

| Case | Native circumstance | Required public disposition |
| --- | --- | --- |
| A | fan-in succeeds; no retry | terminal/next deterministic route |
| B | fan-in selects one creative retry | `await_external_authority`, exact one-action inventory |
| C | retry has provider identity | `provider_reconciliation_cycle`, retained provider inventory and due/not-due evidence |
| D | retry #1 reconciles; retry #2 is needed | `await_external_authority`, exact retry-#2 inventory |
| E | retry fails/exhausts | typed terminal/refusal, no further create authority |
| F | retry lineage cannot be joined | typed review/refusal, no invented recovery |

For each case, prove the selected command, eligibility, reason code, ordered
action inventory, time gate where relevant, capacity disposition, provider
custody inventory/count, and an explicit local-work inventory when
`ordinary_resume` is selected.

The key contract rule is:

```text
ordinary_resume + no retained provider work
  requires a non-empty, public local-work inventory.
```

Without that inventory, a consumer cannot distinguish valid local work from a
quiescent self-loop by parsing state names or inferring intent.

## API companion work already begun

API Sprint 49 added a provider-free disposition oracle. It accepts the current
known-good one-action external-authority receipt, accepts explicit retained
provider reconciliation, and deliberately classifies the Crumpet shape as
unqualified unless it includes a local-work inventory. It is qualification-only
and does not alter production scheduling.

## Related naming correction: v1 → v2

The owner also requested that the outstanding identifier/name correction from
`v1` to `v2` be included in this contract-focused work. Before changing any
name, inventory the exact current occurrence and distinguish:

1. immutable legacy v1 schemas/receipts that must remain readable and retain
   their historical names; from
2. a current v2 route/receipt/fixture that is merely mislabeled `v1`.

Only the second category is eligible for a rename. The correction must update
the emitting code, JSON Schema, packaged fixture(s), CLI/reader evidence, and
API consumer handoff atomically, with an explicit compatibility statement.
No blanket v1-to-v2 rename is authorized by this background document.

## Scope and non-goals

- Provider-free fixtures/tests and closed public schemas only until their
  contract is accepted.
- No provider request, retained-run mutation, recovery, deployment, or release
  is implied.
- No Crumpet-specific bypass or retry heuristic.
- The API/SBE boundary remains: SBE selects and proves native next action;
  API validates, grants/records authority where applicable, and schedules only
  according to the proved disposition.
