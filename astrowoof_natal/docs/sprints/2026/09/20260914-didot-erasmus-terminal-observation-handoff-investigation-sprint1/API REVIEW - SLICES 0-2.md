# API Review — Slices 0–2

**Status: approved.** Slices 0–2 establish a sufficiently narrow, evidence-led
classification and correctly leave SBE implementation paused.

## Accepted findings

1. Didot is an API retry-lineage loss. SBE supplied the exact delivery command,
   result, receipt, and invocation on the first terminal attempt. The later
   successful delivery-validation result has no sealed result ID, so API has no
   observer authority at its current call site. No SBE schema change is
   indicated.
2. Erasmus is not a generic-result-ID problem. SBE supplied the exact
   invocation-bound terminal-review command on attempt 11; current API source
   and the provider-free production-constructor test both select one observer
   call for that route. Attempt 12 is a separate post-close claim and its
   sealed preflight cannot lawfully recreate the first command's authority.
3. The deployed API revision includes the relevant observer source. This rules
   out the simple old-image explanation, but does not yet distinguish a
   deployed configuration/logging interruption from an unobserved control-flow
   or claim-lineage event.

## Slice 3 decision fence

Do **not** decide to persist a terminal-review command merely to make attempt
12 observable. First determine why a non-retryable attempt 11 was reactivated.
If API created that later claim, its operation must be corrected or fenced;
durable observer authority is a separate idempotency design question.

API may now perform one bounded, read-only audit of Erasmus's two exact
attempts, queue/job transition history, and operator/control-plane audit rows
between `2026-09-14T16:11:21Z` and `2026-09-14T16:12:31Z`. The purpose is only
to identify the reactivation writer or prove it is absent from API persistence.
No mutation, retry, recovery, or provider/R2 access is authorized.

For Didot, Slice 3 may design API-owned carry-forward only after strict
terminal ingress has authenticated the same native run, job, result, receipt,
and invocation. It must reject missing, conflicting, cross-job, cross-run, and
newer-result candidates; it must not discover a "latest" result.

## Observability guardrail

Even if the Erasmus observer call did execute, no current evidence proves its
log or HTTP side effects reached Render/Better Stack. Qualification must record
function entry independently of logging and separately exercise logger and
best-effort transport outcomes. Neither outcome may affect authoritative
publication or terminal closeout.
