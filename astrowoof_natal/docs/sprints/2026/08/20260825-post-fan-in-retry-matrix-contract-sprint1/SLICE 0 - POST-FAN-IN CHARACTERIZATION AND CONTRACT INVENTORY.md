# Slice 0 — Post-Fan-In Characterization and Contract Inventory

Status: complete; awaiting owner/API schema-freeze review

## Result

The Crumpet structure is reproducible provider-free in both exact and bounded
interactive lifecycle projections. The leading cause is confirmed:

```text
retry #1: WAITING + durable completed provider evidence
retry #2: PREPARED + no provider identity
run: AWAITING_SPEND_AUTHORIZATION

=> provider custody says completed evidence needs local work
=> status-derived dependency says retry preparation
=> selector chooses ordinary_resume
=> retry #2 external authority remains masked
```

Once deterministic ingestion changes retry #1 from `WAITING` to `REPORTED`, the
same native model immediately exposes retry #2 as the exact one-action
`await_external_authority` inventory. Provider-pending retry evidence continues to
select due/not-due reconciliation, while identity-less `SUBMITTING` continues to
select typed review.

## The no-progress cycle

The focused characterization also exercised the production `SpendController`
boundary for retry #2. An ordinary path that reaches retry #2 without its compatible
authority receives `AwaitingSpendAuthorization`; the action truthfully remains
`PREPARED` and providerless. Republishing the native checkpoint can then select the
same `ordinary_resume` shape again because retry #1 still carries completed evidence.

The republished state revision/snapshot makes the checkpoint digest different even
though no advertised local operation was consumed and the next disposition did not
change. This explains how repeated cycles can evade a simplistic byte-identical-
basis check. The required invariant must therefore be stronger:

```text
an eligible ordinary_resume invocation must consume an advertised operation and
advance semantic native work, or return a different typed disposition
```

A revision increment caused only by republishing is not progress.

## Contract defect

`local_dependencies` currently describe broad blocking/continuation conditions.
They are useful closeout and diagnostic evidence, but they do not identify an exact
executable operation. Lifecycle v0.5 validation accepts any nonempty dependency
list as sufficient support for `ordinary_resume`.

Recommended correction:

- retain `local_dependencies` for explanatory/blocking semantics;
- publish a new closed lifecycle version containing a distinct concrete
  `local_work_inventory`;
- bind that inventory into the immutable temporal checkpoint basis;
- allow `ordinary_resume` only when the inventory is nonempty;
- after invocation, require consumption of at least one advertised member or a
  different typed disposition.

## Operation granularity recommendation

For the first contract, use native durable checkpoint granularity rather than
internal function granularity:

1. `provider_result_fan_in` consumes completed provider evidence and updates the
   corresponding attempt/action lineage.
2. `retry_evaluation_and_preparation` evaluates the rejected attempt and, when
   required, publishes the exact next prepared action/request.

If production code performs both beneath one durable writer/checkpoint, advertise
one combined `provider_result_fan_in_and_retry_evaluation` member instead. Slice 1
should freeze the vocabulary only after locating that exact checkpoint boundary.

## Authorized-without-provider interpretation

The API evidence says retry #2 was authorized, but no rejected lifecycle document
or native action bytes were retained in this sprint package. Native SBE distinguishes:

- API admission/grant persistence outside SBE;
- native `PREPARED` action awaiting constrained grant execution;
- native authorization/intent durability;
- call-entry ambiguity; and
- durable provider identity.

The reproduced safe shape is `PREPARED`, not native `AUTHORIZED`. It requires the
exact external-authority request/grant executor, not generic resume. If Slice 1
receives evidence that the native action was actually authorized or intent-committed,
that must be classified separately under the existing v2 fence. No generic
authorized-action heuristic is recommended.

## Exact/bounded parity

Both exact and bounded lifecycle projections reproduce the completed-retry masking
shape and expose retry #2 after retry #1 becomes `REPORTED`. Route-specific runtime
builders remain separate; this result authorizes shared contract shape, not shared
editorial implementation.

## v1/v2 naming inventory

The exact current v1 surface is:

- schema identity constant in `pending_lifecycle_qa.py`:
  `astrowoof.provider_pending_lifecycle_qualification.v1`;
- public Python function/export:
  `run_provider_pending_lifecycle_qualification`;
- installed CLI:
  `astrowoof-provider-pending-qa`;
- focused source test: `test_pending_lifecycle_qa.py`;
- historical installed receipt under the 20260819 lifecycle sprint.

The v1 receipt has no separately packaged JSON Schema/reader. Its implementation
proves six initial creates, 4+2 retrieval, fan-in, and first authority selection.
Those bytes and that historical identity remain truthful and must remain readable.

Recommendation: add a separate closed
`astrowoof.provider_pending_lifecycle_qualification.v2` receipt, JSON Schema,
strict Python reader/validator, and neutral installed CLI that cover the post-fan-in
matrix. Retain the v1 function/CLI behavior as a compatibility proof; do not rename
unrelated v1 contracts.

## Focused evidence

Command:

```text
python -m unittest astrowoof_natal.tests.test_post_fan_in_retry_matrix_slice0 -v
```

Result: 4 tests passed.

Proved cells:

- exact and bounded completed retry + prepared next retry → ordinary resume;
- repeated semantic no-progress decision after a providerless authority refusal;
- deterministic ingestion of retry #1 → exact retry-#2 authority inventory;
- pending retry → provider reconciliation;
- identity-less submitting retry → review/no create.

Provider/network/spend activity: zero.
Retained Crumpet access or mutation: zero.

## Slice 1 decisions requested

1. Approve lifecycle next-version ownership of `local_work_inventory`, preserving
   closed v0.5 unchanged.
2. Approve v2 qualification as a new contract rather than a v1 rename.
3. Approve durable-checkpoint operation granularity and the semantic progress rule.
4. Confirm whether the available API evidence can distinguish API-side grant
   persistence from native SBE `AUTHORIZED`/intent state. If not, retain the
   `PREPARED` reproduction as the contract basis and classify native intent states
   independently.
