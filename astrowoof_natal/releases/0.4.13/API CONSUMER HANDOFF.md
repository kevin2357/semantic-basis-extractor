# SBE 0.4.13 API Consumer Handoff

Consume lifecycle inspection v0.4 as a closed contract.

- `execution_branch.command=provider_reconciliation_cycle` and
  `eligible_now=false`: retain provider/consumer authority, release local capacity
  when the checkpoint is safe, and schedule no earlier than `not_before`.
- The same command with `eligible_now=true`: invoke the supported run-level
  provider-reconciliation command. Do not invoke ordinary `--resume`.
- `execution_branch.command=ordinary_resume`: invoke ordinary resume only when
  `eligible_now=true`.
- `await_external_authority` or `none`: invoke neither execution command.
- Reject contradictory branch, capacity, custody, timing, and continuation fields.
- Never use `action_ids` to choose members; SBE owns its maximum-four retrieval
  subset.

Installed provider-free qualification:

```text
astrowoof-provider-pending-qa
```

Detailed contract and recovery guidance is in the Sprint 3 lifecycle-classification
handoff and the authoring lifecycle consumer handoff.
