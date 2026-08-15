# Slice 2 Result: Atomic Required-Denial Terminalization

Status: complete; pending review.

## Implemented

New single and batch providerless denials now derive one run consequence from the
locked pre-denial state and persist it in the same native revision as every action
denial.

- Required `external_authority_denied` and final `reservation_unavailable` produce
  `BUDGET_EXHAUSTED` with distinct external-spend terminal causes.
- Required `product_policy_denied` and cancellation produce `POLICY_STOPPED` with
  distinct causes.
- Mixed required batches use the approved policy-stop precedence while preserving
  each action's exact denial reason.
- Successful v0.2 results return ordered `denied_action_ids` and the exact causal
  `required_action_ids` subset.
- Existing accepted delivery wins over unused-action cleanup and is not downgraded.
- An already terminalized run preserves its first terminal authority when other
  providerless actions are later denied.
- Optional stages with frozen `skip` policy are denied/skipped rather than
  terminalizing. A real bounded polish fixture continues to delivery without a
  second provider submission.
- Public state exposes only bounded terminal outcome, cause, and state revision.
- Inspection reports the exact external cause, no local/provider continuation,
  and quiescence; closeout returns `closed` with no unresolved action IDs.
- Exact and bounded runners return the durable terminal state before authorization
  consumption or provider invocation.
- First terminalization emits one redacted `terminal.transitioned` observation;
  replay and later cleanup do not duplicate it.

Historical v0.1 durable results remain readable. New successful denials return
v0.2. Refusals remain non-mutating and retain their existing typed behavior.

## Atomicity boundary

Batch all-or-none preflight, action mutation, run transition, private/public state,
artifact promotion, and snapshot publication remain under the existing
single-writer protocol. The run status is protected from `update_run_status()`
recomputation by its durable terminal-transition authority.

This slice does not yet add the separately planned legacy 0.4.1 recognizer or
expand interrupted-write recovery evidence for every new transition member; that
work remains Slice 3.

## Evidence

```text
focused lifecycle ladder: 70 passed in 19.637s
complete repository suite: 301 passed in 121.713s
provider operations: 0
paid spend: $0
API key: not used
```

## Review focus

- Status/cause mappings match the approved contract.
- Optional polish denial reaches delivery with exactly one prior initial-authoring
  provider-double submission and no resubmission.
- Accepted delivery and first-terminal precedence are preserved.
- V0.2 causal lists remain exact for single and batch results.
- Retained 0.4.1 reconciliation and exhaustive new-write recovery intentionally
  remain in Slice 3.
