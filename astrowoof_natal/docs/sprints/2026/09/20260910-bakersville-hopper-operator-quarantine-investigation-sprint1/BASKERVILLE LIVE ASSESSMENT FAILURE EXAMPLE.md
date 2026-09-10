# Baskerville Live Assessment Failure Example

## Observed event

- submission time: `2026-09-10T19:27:22.727Z`
- operator request ID: `02de1a55-b137-499d-9fb4-c327a7fe3116`
- outcome: `refused`
- refusal code: `disposition_assessment_unavailable`
- quarantine applied: no
- Baskerville capacity released: no

API reports that the operator runner restored or attempted the bounded native
assessment path but could not obtain SBE's valid public disposition assessment.
The runner failed closed as designed.

## Proven by this event

- The remembered operator-level failure signature is current and reproducible.
- The request reached the runner and produced a typed refusal.
- Missing admitted assessment evidence prevented quarantine and capacity release.

## Not proven by this event

- Whether SBE failed to construct or serialize an assessment.
- Whether the failure was missing/malformed output, nonzero exit, timeout,
  installed-package/resource mismatch, restore failure, parser rejection, or
  identity mismatch.
- Baskerville's native custody class or actual quarantine eligibility.
- Why Baskerville originally became stuck.
- That the old failed attempt shared this event's cause; only its external
  refusal signature matches.

## Evidence needed to classify the seam

For this exact request, retain or recover where available:

- restored workspace/checkpoint identity and archive-validation outcome;
- installed SBE version, executable/module path, working directory, and
  sanitized subprocess environment;
- bounded stdout bytes, sanitized stderr, exit code, duration, and timeout;
- parser/schema/digest/identity rejection detail;
- attempt count and whether target identity changed;
- API run/job/lease/capacity state before and after refusal.

No retained workspace read or repeat execute is implied. Those require separate
exact authorization and should follow provider-free reconstruction.

