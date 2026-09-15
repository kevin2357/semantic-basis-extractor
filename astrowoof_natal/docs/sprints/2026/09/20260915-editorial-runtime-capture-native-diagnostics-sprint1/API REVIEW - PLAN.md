# API review — logging-sprint plan

## Decision

Approved to begin Slice 0 and prepare the Gate A contract.  This is the right
next intervention: bounded internal diagnostics, not a speculative semantic
fix and not unrestricted application logging.

## Required diagnostic shape

The event family and one-public-call terminal invariant are appropriate.  Keep
the emitted cardinality bounded to one `started`, a small number of
architectural boundary completions, and exactly one `completed` or `failed`
record.  Do not emit per pass, artifact, deck member, or provider response.

The frozen phase vocabulary must contain distinct closed tokens for:

1. root normalization;
2. exact result reader;
3. eligibility classification;
4. exact source/subject proof;
5. pre-assembly evidence collection;
6. guarded packet assembly;
7. packet validation;
8. typed unsupported-status construction; and
9. final return.

That explicit split is essential because the prior provider-free matrix proved
two distinct escaping paths: collector-before-guard and status-construction
double-fault.  A single generic `capture_failed` phase would repeat the current
blind spot.

## Safety refinements

- `source_line` must be a positive integer; frame fingerprint input must be
  limited to approved module basename, function, line, normalized exception
  class, and closed phase token.
- If adding a shape diagnostic, use only a closed expected/actual **type-name**
  pair (for example `mapping` / `list`); never stringify the value or an
  exception.
- The diagnostic helper must log after an exception is caught but before bare
  re-raise, and must not replace, chain, or otherwise alter the original
  traceback.
- The installed-wheel/API-host coexistence gate is mandatory.  Bembo/Morris
  failed only in the actual API-hosted invocation; source-only tests cannot
  claim the sprint solves that boundary.

## Non-authorization

This review does not authorize a release, deployment, live cohort, Better
Stack change, R2 access, provider work, or runtime semantic change.  No Alloy
model change is expected if those fences hold.
