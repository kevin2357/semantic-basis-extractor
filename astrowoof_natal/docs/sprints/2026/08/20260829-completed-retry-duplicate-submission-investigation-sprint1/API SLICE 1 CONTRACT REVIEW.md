# API Slice 1 contract review

## Decision

Approved with the operational refinement below. The proposal correctly uses the
existing lifecycle v0.8, external-authority v2 constrained dispatcher, and native
result v0.2 contracts instead of introducing a parallel provider-submission state
machine.

## Approved positions

1. For applicable exact-Natal interactive ordinary action sets, external-authority
   v2 constrained dispatch is the sole create-capable boundary. Generic ordinary
   resume may inspect/prepare only.
2. `local_work_progress_contradiction` is an appropriate new closed native-result
   v0.2 review cause. It does not require a new lifecycle status.
3. API should map a sealed result with that cause to its stable
   `review_required`/operator-review posture while retaining the exact native cause,
   action inventory, provider custody, and reservation evidence. A second API
   disposition is unnecessary at this stage.
4. Initial-wave v1, Batch, bounded, and historical recovery remain out of scope
   unless a shared-path characterization later proves otherwise.

## Required refinement — typed generic refusal

Invariant A must not make the now-prohibited generic `--spend-authorization` path
terminate as an untyped nonzero subprocess failure. That would preserve provider
safety but recreate an API retry loop.

When generic invocation encounters an applicable create-capable ordinary action,
it must produce the existing machine-readable v2-style pre-provider refusal /
no-new-create conclusion, with a stable reason such as
`external_authority_v2_dispatch_required`, before any action consumption, provider
I/O, or state mutation. The API can then re-inspect and invoke only the SBE-selected
supported v2 command. It must not retry the generic command.

This refusal need not fabricate a terminal authoring result; it needs a valid
public command/dispatch conclusion that carries zero provider work and is safe for
the queue to classify deterministically.

## Atomicity clarification

For `local_work_progress_contradiction`, the terminal-review v0.2 result,
checkpoint/snapshot binding, action dispositions, and publication receipt must be
sealed from the same writer-fenced custody state. It is not enough to log a cause
and later attempt to reconstruct provider custody from scratch. After that sealed
outcome, all succeeding commands for those action IDs are retrieval/review-only.

## Slice 2 test additions

In addition to the listed tests, assert:

- prohibited generic invocation returns the typed refusal with exit/result shape
  accepted by API, and causes no retryable `command_failed` classification;
- API-facing consumer behavior routes that refusal to fresh v2 inspection rather
  than resubmitting generic work;
- the terminal-review receipt contains the same snapshot/action-inventory digest as
  the fenced custody checkpoint.

The existing characterization remains useful for the restore/replay seam, but the
new Slice 2 tests must exercise the unpatched constrained dispatcher and real
call-entry fence.
