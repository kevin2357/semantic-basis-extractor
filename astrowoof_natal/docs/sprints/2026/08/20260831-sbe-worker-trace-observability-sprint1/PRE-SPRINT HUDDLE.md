# Pre-sprint huddle — explain the handoff before opening the workspace

## Working thesis

The best trace is not a second state machine. SBE should log the identities and
safe projections it has already validated while making the real decision.

A normal investigation should be able to answer:

1. What exact workspace/checkpoint did this invocation begin from?
2. What durable actions, provider custody, local work, intent, and result chain
   did SBE observe?
3. Which branch and supported command did SBE select, and which predicate made
   that branch win?
4. Did the invocation mutate or publish anything?
5. What exact artifact/result/checkpoint identity did it return to API?
6. Why did the process exit with its particular typed outcome?

If those answers are available in bounded `✨🐶` logs, an operator should not
need to download the workspace merely to reconstruct routine state.

## Proposed trace units

### Workspace fingerprint

Emitted after snapshot/restoration validation, before branch selection. It
joins the invocation to exact native bytes using safe public identities and
digests. Missing optional metadata is explicitly `unknown`, never invented.

### Native decision summary

Emitted after public lifecycle/result construction and validation. It includes
the selected command/disposition/reason, safe action/custody/local-work/intent
summaries, and the public artifact digest or ID.

### Mutation/publication summary

Emitted after a durable checkpoint, result, receipt, or successor is sealed.
It states the pre/post revision and digest identities and whether provider I/O,
authority consumption, or native mutation occurred.

### CLI exit summary

Emitted once per public command path immediately before return. A sealed typed
result outranks the numeric exit code; the line names both without treating
either log field as authority.

## Bounded inventory policy

Small inventories may include canonical ordered action IDs and binding digests.
Larger inventories must include deterministic counts/digests and an explicitly
truncated bounded prefix. Truncation must never be silent.

## Safety posture

- One sanitizer/formatter, not hand-built redaction at every call site.
- Logging/event sink failure cannot change state, returned bytes, provider I/O,
  authority consumption, or exit behavior.
- Exception logs include class, sanitized message/fingerprint, operation,
  duration/status/request ID where available, and safe native correlation.
- DEBUG may add safe detail but may not relax the privacy boundary.
- Qualification uses protected sentinels and intentionally failing sinks.

## Expected outcome

Routine operational diagnosis becomes log-first. Public-artifact fetch is the
second step when exact bytes must be validated. R2 checkpoint inspection is
reserved for crash-before-handoff, missing/historical logs, artifact mismatch,
or suspected persistence corruption.
