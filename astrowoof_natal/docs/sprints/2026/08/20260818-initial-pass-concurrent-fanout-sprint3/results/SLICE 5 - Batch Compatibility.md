# Slice 5 — Exact and Bounded Batch Compatibility

Status: complete; awaiting Kevin review before commit.

## Outcome

Both Batch routes retain their released authority topology after interactive fan-out:

| Route | Native paid authority | Logical members | API reservation shape |
|---|---:|---:|---|
| Exact Natal Batch | one action per round | six initial passes | one reservation per round |
| Bounded Natal Batch | one action per round | six initial passes | one reservation per round |

Neither Batch state contains `initial_authoring_wave`; that contract is exclusively
for six separately created interactive Responses. Batch member rows remain audit,
request, validation, and settlement evidence beneath the one round action. They do
not multiply global reservation authority.

Exact and bounded request-parity regressions prove that each route's interactive
and Batch forms share the same frozen logical pass request after removing only the
documented transport/background envelope difference. Exact and bounded packet bytes
are not compared to each other.

## Conservative cost correction

The audit found and corrected one exact-Batch asymmetry. Exact Batch previously
normalized a missing member usage object to zero and could settle the aggregate paid
action from the remaining members. It now requires usage evidence for every
potentially billable member before reporting aggregate cost.

If any member lacks usage:

- the round and paid action report
  `provider_usage_unavailable_billing_reconciliation_pending`;
- `estimated_micro_usd` remains `null` rather than becoming a partial total;
- terminal provider retrieval custody may end; and
- API consumer/financial authority remains retained for reconciliation.

This matches the already-released bounded-Batch rule. A provider-reported zero
remains distinguishable from unavailable usage.

## Preserved behavior

- Partial output/error membership fails closed without partial ingestion.
- Duplicate, unknown, malformed, and identity-conflicting members require review.
- A rejected or errored member creates only its pass-local retry round.
- Terminal provider failure, unavailable usage, detach/not-due/reclaim, and
  retrieval-only resume keep their existing typed outcomes.
- Batch replay never uploads or creates a second provider operation after a durable
  Batch ID exists.
- Interactive fan-out does not change Batch request bytes, round settlement, or
  optional-stage transport policy.

## Verification

- Focused cross-route authority/request parity: 4 tests passed in 12.288 seconds.
- Mixed-usage parity: exact plus bounded regressions passed (2 tests in 9.722
  seconds); exact inspection additionally proves zero provider custody and retained
  consumer authority.
- Complete Batch-focused four-route suite: 29 tests passed in 138.277 seconds.
- Compile and `git diff --check`: pass.
- Provider operations: zero.
- Paid spend: `$0`.
