# AstroWoof Natal Authoring 0.4.51

SBE 0.4.51 replaces pipe-delimited ordinary worker traces with closed,
one-object-per-line structured JSON and makes high-value native decisions
directly queryable without changing any authority-bearing command or artifact.

## What changed

- New packaged `astrowoof.sbe_worker_log.v1` schema and closed event catalog.
- Structured correlation for API/native runs, subjects, invocations, paid
  actions, provider operations, and checkpoint objects without inferring absent
  identities.
- Explicit bounded decision evidence at workspace restore, lifecycle selection,
  provider custody, checkpoint publication, external authority, terminal result,
  and CLI-exit boundaries.
- The run reporter reads historical pipe logs, structured JSON logs, and mixed
  exports with deterministic ordering and malformed/duplicate accounting.
- API relay qualification covers reconciliation, ordinary resume, and
  constrained-v2 routes while preserving their separate authoritative result
  transports.

## Compatibility

- Lifecycle, external-authority, provider-custody, terminal-result, and API
  disposition contracts are unchanged.
- Logs remain diagnostic only and never grant transition authority.
- Historical pipe logs remain readable by the reporter.
- `semantic-projection-core==0.11.1` remains the supported dependency.

## Qualification

Release-bound regression, reproducible-build, installed-wheel, and public
qualification evidence will be recorded before the immutable release tag is
created.
