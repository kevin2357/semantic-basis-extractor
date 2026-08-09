# SBE 0.2.1 Polish Checkpoint Recovery Advisory

Use `astrowoof-repair-polish-checkpoint` only when its default dry run reports
`eligible: true`. The command requires the exact original Linux logical path,
the external authorization solely as binding evidence, and the complete
retained native workspace.

Apply requires:

- an API-owned exclusive run lease reference;
- a separate byte-identical complete backup;
- the original action-2 authorization file; and
- no concurrent worker or provider-connected invocation.

Apply does not authorize, consume, submit, poll, cancel, or delete provider
work. It reconstructs missing subject/attempt state and republishes a validated
snapshot. Preserve its report outside the workspace. If the process is
interrupted, do not retry blindly: validate the native snapshot and compare
state/ledger evidence with the backup first.

The canonical acceptance run remains unrepaired. Its API owner must separately
authorize canonical mutation and any later provider-connected resume.
