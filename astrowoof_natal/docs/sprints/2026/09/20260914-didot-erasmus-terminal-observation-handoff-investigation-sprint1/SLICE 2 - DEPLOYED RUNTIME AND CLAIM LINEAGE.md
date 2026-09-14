# Slice 2 — Deployed Runtime and Claim Lineage

## Deployed identity

The retained `qa-sbe0461-scripted-rollout-v1` evidence binds the QA SBE worker
to:

- API source revision `e412caf58dc4e47908559227ef69ecf37ba3ed23`;
- SBE `0.4.61` wheel SHA-256
  `8dd151fced3fc7823ef914c7642798a977eca93d19b1136bf34da55b589ef723`;
- SBE-worker image digest
  `sha256:c4979464eeb15f45a3f814fd011ef525088af186ab0121e11c82d72b26c2bca1`;
- activated profile `astrowoof.qa.sbe0461-scripted-rollout.v1`.

Git ancestry proves observer commits `bcc45ee3` and `9ffb3b5c` are ancestors of
`e412caf`. Inspecting that exact revision confirms the command-bearing review
call site and success/failure logging were present. This is not an old-image
explanation.

## Erasmus claim lineage

Attempt 11 committed a non-retryable terminal close and emitted its failure and
lease-release events. Seventy seconds later attempt 12 newly claimed the same
job under a distinct attempt and lease. Ordinary
`ExecutionQueueService.fail(..., retryable=False)` sets the job to `failed`,
fails the run/reading, and schedules no claim.

The subsequent bounded database audit corrected this provisional conclusion.
Attempt 11 remained active despite terminal-looking events, expired, and was
requeued by ordinary expired-lease collection. See Slice 3 for the exact source
omission. There was no external operator reactivation.

## Observer classification

At attempt 11, one of these remains possible:

1. the deployed process did not retain the command in its in-memory cycle
   result despite SBE emitting it;
2. the observer call occurred but both its terminal log and downstream packet
   logs were lost or filtered;
3. an unobserved process/runtime boundary interrupted the post-commit hook.

Current source, deployed ancestry, and provider-free reproduction make a simple
code-version omission unlikely. Attempt 12 cannot repair attempt 11 because its
generic sealed preflight carries no invocation-bound review command.

## Review-gate decision needed

Slice 3 should jointly decide:

- API's durable representation for Didot's exact delivery identity across
  publication retry;
- whether API should durably retain a validated Erasmus review command at first
  ingress so observation is idempotent and recoverable after reactivation;
- ensure terminal events are emitted only after the matching queue transition
  commits.

No SBE schema change is supported. No live access, mutation, provider call, R2
read, or deployment occurred.
