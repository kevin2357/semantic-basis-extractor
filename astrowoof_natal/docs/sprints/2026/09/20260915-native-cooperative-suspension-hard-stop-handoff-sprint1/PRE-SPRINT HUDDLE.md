# Pre-Sprint Huddle

## Meeting-of-the-minds position

The API force fence and SBE cooperative suspension are complementary but
different operations. API can contain future progress before SBE cooperates.
SBE can later describe the exact native boundary it reached. API process
supervision can establish that one exact child exited. None may impersonate the
others.

## Contract points to preserve

### Launch identity comes first

The invocation identity must exist before child creation and bind the run, job,
attempt, lease, native run, command digest, worker boot, invocation generation,
and bounded grace. PID, process group, and non-recycled start evidence may be
added after launch but cannot replace the envelope.

### Control capability is narrow

A credible first design is a request-isolated, worker-owned control directory
outside the executable workspace. Its identity is passed at launch; API writes
one canonical digest-bound request atomically; SBE reads it only at declared
safe points. Voof-paws A selected this control-file design for v1 rather than an
inherited pipe. The pre-launch envelope binds the canonical absolute control
root, and relocated copies reject the capability before request parsing. A
signal may wake the child but is neither request authority nor a transaction
boundary.

Relocated assessment copies must be unable to use the channel. Restart and
replay must not cause a new invocation to honor a stale request.

### Results are append-only evidence

The original API fence and initial ambiguity remain immutable. SBE publishes a
new exact suspension result/receipt; API publishes later process observations
and resolution successors. A current projection may select a validated
successor, but cannot rewrite history.

### Existing results win

If ordinary terminal or delivery publication commits before SBE observes the
stop request, that native result remains authoritative. Suspension must not
replace or downgrade it. The force fence may still prohibit later ordinary API
scheduling while API performs settlement.

### Resource questions remain separate

- API authority revocation is immediate.
- API worker execution capacity needs exact child-exit evidence.
- Run-level SBE allocation follows a separate explicit scheduling policy.
- Provider, spend, workspace, checkpoint, and native custody remain held unless
  exact public evidence authorizes a named later operation.

## Pause points

Voof-paws A approved exact interactive ordinary-v2 dispatch and response
reconciliation as the complete v1 route scope. Initial-wave fan-out, bounded,
legacy direct, and Batch remain unsupported/deferred.

Voof-paws B is the joint Gate B contract review and is mandatory before runtime
mutation, signal handling, or process-control integration. Later implementation
and release gates remain separate.
