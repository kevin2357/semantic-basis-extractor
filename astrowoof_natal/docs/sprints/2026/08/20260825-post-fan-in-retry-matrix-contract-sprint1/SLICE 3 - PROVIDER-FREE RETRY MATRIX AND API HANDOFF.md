# Slice 3 — Provider-Free Retry Matrix and API Handoff

Status: implemented and ready for API review.

## Consumer rule

The API validates lifecycle v0.7 and invokes only the SBE-selected run-level
command. It does not reconstruct local operations, choose provider members, or
infer authority from API-side authorization rows.

The supported reader is:

```text
astrowoof-lifecycle --run-dir <workspace> inspect-local-work \
  --observed-at <canonical UTC> --native-exclusive-access declared
```

Existing `inspect` and `inspect-temporal` retain their v0.5/v0.6 shapes but fail
closed with `local_work_contract_upgrade_required` when concrete v0.7 local work
would be necessary. They never silently reinterpret that work.

`local_work_inventory.operations` is native evidence and audit lineage. It is
never a menu of independently invocable API operations.

## Frozen interactive matrix

| Case | Native evidence | v0.7 result |
| --- | --- | --- |
| A | no retry; accepted authoring awaits assembly | `ordinary_resume` with `final_assembly_and_qa` |
| B | one exact PREPARED retry | `await_external_authority`, empty local inventory |
| C | retry provider identity pending | `provider_reconciliation_cycle`; due/not-due remains SBE-selected |
| D | retry #1 evidence complete; retry #2 PREPARED | `ordinary_resume` with one fan-in/evaluation operation; after consumption, one exact retry-#2 authority request |
| E | retry exhausted / native review terminal | `none`, empty local and authority inventories |
| F | historical lineage cannot join one exact wave | `none` with `initial_wave_lineage_unjoinable` refusal |
| G | native `AUTHORIZED` but providerless | `none`; exact constrained dispatch is required |
| H | call entered / `SUBMITTING` without identity | `none`, ambiguity/review custody |

Exact and bounded interactive retry topologies use the same scheduling meanings,
while their route identities and native artifacts remain distinct.

## Batch classification

This slice does not invent a Batch-local retry executor. Existing exact and bounded
Batch preparation/reconciliation contracts remain authoritative. A Batch route may
publish v0.7 local work only where the same concrete native fan-in/assembly evidence
can be constructed; otherwise it fails closed with no `ordinary_resume`. No member
is elevated into independent paid authority.

## No-spin rule

For every eligible `ordinary_resume`:

1. the inventory is nonempty and snapshot/revision bound;
2. the invoked command must consume at least one advertised semantic operation or
   select a different typed disposition;
3. cumulative consumed keys may never shrink; and
4. a consumed key may never be advertised again.

`commit_local_work_progress()` performs this proof beneath the native writer. A
snapshot-only no-op is refused without changing authoritative bytes.

## Authority distinction

An API database row described as authorized does not prove native SBE `AUTHORIZED`
or intent state. Native PREPARED actions continue through the exact external
authority request/grant contract. Native AUTHORIZED/providerless actions are
fenced and non-dispatching through generic resume. SUBMITTING without a durable
provider identity remains ambiguity/review.

## Fixture and safety

Sanitized matrix:

- `fixtures/post-fan-in-retry-matrix.v1.json`

The matrix performs no provider create, retrieval, network operation, credential
access, spend, or retained-QA workspace access. Provider custody and ambiguity
precedence remain unchanged.

## API review questions

1. Does the eight-cell mapping give the API sufficient closed routing evidence?
2. Is `AUTHORIZED`/providerless correctly non-dispatching pending its exact
   constrained executor, rather than being treated as ordinary local work?
3. Is the explicit Batch classification sufficiently fail-closed for this release?
4. May Slice 4 package the v2 installed-wheel qualification around this matrix?
