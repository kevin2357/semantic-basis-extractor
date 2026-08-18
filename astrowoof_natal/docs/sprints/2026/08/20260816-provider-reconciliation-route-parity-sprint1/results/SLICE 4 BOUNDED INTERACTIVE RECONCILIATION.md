# Slice 4 Bounded-Natal Interactive Reconciliation

Date: 2026-08-17  
Status: complete; awaiting gate review  
Provider operations: 0  
Paid spend: `$0`

## Outcome

Bounded-Natal interactive work now participates in the same bounded worker-release
and fresh-worker reconciliation contract as exact-Natal Responses while retaining
its separate route-local orchestration, schemas, evidence, and editorial trust
boundary.

## Implemented behavior

- Lifecycle inspection now recognizes validated `bounded_natal` plus `response`
  actions as supported rather than accidentally inheriting exact behavior or
  remaining deferred.
- Optional-stage eligibility is read from bounded Natal's frozen
  `optional_stages` profile, not exact Natal's QA profile.
- The high-level reconciliation entry point dispatches completed bounded evidence
  into `resume_bounded_run()` with a reconciliation-only spend controller.
- Reconciliation retrieves only durable Response IDs, with the frozen 15-second
  request timeout, zero transport retries, four-action cycle bound, and existing
  bounded backoff schedule.
- Newly unblocked bounded validation, creative-retry preparation, optional-stage
  progression/skipping, and delivery work are exhausted before detach.
- Reconciliation may prepare the next action and stop at external authorization,
  but cannot submit it—even if stale external authorization happens to exist.
- Provider operation summaries now carry the native route family instead of
  hard-coding exact Natal.
- Provider-terminal failed/cancelled/incomplete Responses enter typed review with
  billing reconciliation retained; they do not become an automatic retry or a
  fabricated zero-cost settlement.

## Restart and trust-boundary coverage

The route matrix covers authoring initial, creative retry, polish, qualitative
critic, and qualitative candidate. Tests also cover pending work, transport
warning, provider-ID conflict, terminal provider failure, optional-stage policy,
delivery, and complete snapshot validation.

Failure injection covers interruption after raw provider evidence, after bounded
local continuation, and after the final result snapshot. The first injection found
an important restart seam: completed provider evidence could exist durably while a
subsequent cycle expected another due retrieval. A provider-free local-continuation
replay path now consumes the durable response without a second GET or POST.

Provider-authored bounded output still passes through the existing immutable-field
rehydration, provider-minimized payload check, bounded validation, four-context
provenance, claim-authority, disposition, and delivery code. This slice changes
scheduling and recovery, not bounded semantic authority.

## Tests

Focused bounded lifecycle, bounded provider, scheduling, and contract coverage
passed all 66 tests in 27.313 seconds.

The complete repository suite passed all 354 tests in 265.958 seconds.

No network transport, API key, provider endpoint, build, version bump, release, or
tag operation was used.

## Gate conclusion

All supported bounded-Natal interactive stages can release local capacity while a
known Response is pending and can resume from a complete restored workspace
without duplicate paid work. Bounded Batch remains explicitly unsupported.
