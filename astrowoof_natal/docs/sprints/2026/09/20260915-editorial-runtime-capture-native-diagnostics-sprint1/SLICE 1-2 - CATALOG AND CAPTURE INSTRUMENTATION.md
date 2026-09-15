# Slices 1–2 — catalog and capture instrumentation

## Implementation

The checked-in worker-log event catalog now declares four closed editorial
runtime-capture events. `editorial_review_runtime.py` adds one private,
fail-silent diagnostic projection surface and threads an internal phase record
through exact reading, eligibility, exact-source proof, evidence collection,
guarded assembly, packet validation, typed-status construction, and final
return.

Public signatures and return schemas are unchanged. Existing direct eligibility
and evidence-collection calls remain observationally quiet; the event family
belongs to one invocation of the public capture builder.

The functional boundaries remain distinct:

- an exception before assembly escapes exactly as before after a failed event;
- assembly's existing caught exception classes still become typed
  `incomplete_native_evidence`;
- a second exception in typed-status construction still escapes exactly as
  before, now under the distinct `typed_status_construction` phase; and
- successful packet and typed unsupported returns retain their original branch
  and payload.

## Privacy and failure posture

- Root references are SHA-256 only.
- No exception object or `exc_info` is passed to the formatter.
- No exception prose, native path, persisted value, packet content, report,
  prompt, provider response, action binding, or credential is projected.
- Unsafe frame modules/functions fall back to `unknown`; source lines are
  positive integers.
- Logging projection, handler, formatter, or sink failure returns no authority
  and cannot alter capture behavior.

## Tests

New manifest-classified logging-sensitive test:

`test_editorial_runtime_capture_diagnostics.py`

It proves:

- a normal typed unsupported result produces catalog-valid formatter records
  with no raw root;
- a genuine pre-assembly ordering `TypeError` is logged at
  `pre_assembly_evidence_collection` and re-raised;
- a typed-status double-fault is logged at `typed_status_construction`, retains
  the exact exception object, and exposes neither the first nor second
  exception prose; and
- a raising logging handler does not change the typed capture result.

Focused qualification: 45 tests passed across capture diagnostics, existing
editorial runtime capture, structured/application logging, and test-manifest
enforcement. The broader provider-free editorial/logging/release-contract set
passed 99 tests with one expected skip. Targeted Ruff
import/blind-exception/simplification checks and `git diff --check` pass.

## Alloy ruling

No model change. These events are non-authoritative projections and do not
change lifecycle, selection, authority, custody, packet, result, or transition
semantics.

## Remaining gate

Slice 3 requires an installed candidate wheel and API-host `force=False`
coexistence qualification. No version bump, wheel candidate, release,
deployment, or live test is authorized yet.
