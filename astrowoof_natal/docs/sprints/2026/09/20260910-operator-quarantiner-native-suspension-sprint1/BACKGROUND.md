# Background

AstroWoof API Control Room issue 18 asks for a universal emergency stop for an
exact active or otherwise unsafe authoring run. The existing assessed-quarantine
foundation intentionally cannot release local capacity for native postures such
as `native_local_work_ready`, `completed_unadopted`, or
`unsupported_or_inconsistent`: a read-only assessment cannot truthfully prove
that an active native process has stopped or reached a safe checkpoint.

This sprint defines the native half of a custody-safe suspension protocol. It
does not make SBE the owner of API jobs, leases, queue eligibility, process
termination, capacity accounting, provider cancellation, spend release, or
retention policy. It also does not broaden the existing disposition assessment
until a new native result can prove materially stronger facts.

Related Control Room work:

- API issue 9: assessed quarantine and custody-safe disposition foundation;
- API issue 18: generic emergency execution stop and custody-safe suspension;
- API issue 17: lifecycle-safe R2 retention and reclamation, which must preserve
  suspended, quarantined, ambiguous, and held evidence.

