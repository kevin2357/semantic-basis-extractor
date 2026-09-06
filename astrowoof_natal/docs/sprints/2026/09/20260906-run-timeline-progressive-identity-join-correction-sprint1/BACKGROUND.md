# Background — run timeline progressive identity join correction

SBE `0.4.52` introduced the diagnostic shared-time cohort swimlane. Its first
use against the complete deployed three-run Better Stack export exposed a
production-shape mismatch that the sanitized qualification fixture did not
contain.

Real API wrapper start events such as `sbe.cycle.started` and
`worker.lease.acquired` carry the API run, job, attempt, and lease identities,
but do not yet carry `native_run_id`. Their matching completion/release events
carry both the API and native run identities. The released adapter rejects the
start records for lacking `native_run_id`, and its pairing keys redundantly
require that identity. The result is a report containing many unpaired API
events despite coherent matching boundaries in the source.

This differs from the approved Slice 0 interval grammar, which pairs wrapper
boundaries by the exact API run/job/attempt/lease identities and then joins the
native lane using later evidence that explicitly carries both run identities.
The hand-built prototype followed that progressive join and rendered the same
cohort more usefully.

The retained production-shaped input is:

`C:\tmp\astrowoof-most-recent-three-pup-cohort-inner-20260906.log`

The correction is diagnostic tooling only. It must not turn log proximity into
authority, relax mismatched identity handling, or alter authoring/lifecycle
runtime behavior.

