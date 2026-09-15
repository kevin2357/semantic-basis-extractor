# Plan — editorial runtime-capture native diagnostics

## Objective

Instrument the public editorial runtime-capture path with fail-silent,
catalogued ✨🐶 events that identify its exact safe phase and innermost approved
SBE frame when an exception escapes, while preserving the exception object,
traceback, return value, I/O behavior, and all native/editorial semantics.

## Frozen fences

- Diagnostics are observational and non-authoritative.
- Logging failure or formatter/catalog rejection must never change capture's
  return or exception behavior.
- Do not catch an exception unless it is immediately re-raised unchanged after
  best-effort logging. Do not broaden typed `unsupported` behavior.
- Never log exception messages, paths, native values, packet contents, reports,
  prompts, responses, bindings, provider data, environment values, or secrets.
- A frame is retainable only when its module belongs to the approved SBE
  capture implementation surface; retain basename, function, and positive line
  number only. Otherwise use `unknown`.
- Root identity is SHA-256 of the exact call-time root string; never emit the
  string itself.
- Use exact supplied result identity only. No latest-result discovery.
- No provider, network, R2, Better Stack, workspace, lifecycle, queue, or API
  mutation during implementation or qualification.

## Slice 0 — Freeze event and phase contract

1. Inventory the existing SBE application formatter, event catalog, safe-field
   validators, and host propagation behavior.
2. Define the smallest event family, expected initially as:
   - `editorial_runtime_capture_started`;
   - `editorial_runtime_capture_phase_completed`;
   - `editorial_runtime_capture_completed`; and
   - `editorial_runtime_capture_failed`.
3. Freeze closed phase tokens that distinguish pre-assembly collection,
   guarded assembly, and typed-status construction, including narrower reader,
   source-proof, inventory, pass, optional-stage, and validation boundaries.
4. Freeze required/optional fields and correlation placement. Prefer one phase
   transition record per architectural boundary, never per pass member or
   artifact.
5. Specify safe traceback selection: innermost approved SBE frame, function and
   line only, with deterministic class/phase/frame fingerprint.

Acceptance: catalog-ready event definitions identify both escape routes proven
by the predecessor sprint and contain no content-bearing field.

## Review Gate A — Contract and privacy

Joint API/SBE review approves event names, phase vocabulary, payload fields,
frame allowlist, cardinality, and fail-silent behavior before source
instrumentation.

## Slice 1 — Catalog and fail-silent diagnostic helper

1. Add the approved events to
   `sbe-worker-log-event-catalog.v1.json` and its schema/contract tests.
2. Implement one internal helper that validates/sanitizes closed values,
   computes the root digest and failure fingerprint, selects only an approved
   frame, and emits through `logging.getLogger(__name__)` using `event_name` and
   `event_payload` extras.
3. Make the helper catch all of its own projection/logging failures and return
   no authority or control value.
4. Test unsafe frame, malformed identity, logging-handler failure, catalog
   rejection, and nonserializable input cases. Assert the underlying simulated
   capture return or exception remains byte/object-equivalent.
5. Add every new test module to `test_suite_manifest.json` immediately.

Acceptance: diagnostics survive hostile logging conditions without altering
the observed operation and produce records accepted by the real formatter and
catalog validators.

## Slice 2 — Capture-path instrumentation

1. Add phase tracking around the public capture path and its private evidence
   collector boundaries without changing public parameters or return shapes.
2. Emit started once, bounded phase-completed records, and exactly one completed
   or failed terminal diagnostic per public capture invocation.
3. Preserve the current distinction among:
   - exceptions escaping before assembly's guard;
   - exceptions translated by guarded assembly into typed unsupported status;
   - exceptions escaping from typed-status construction.
4. On an escaping exception, log best-effort diagnostics and use bare `raise` so
   the exact exception and traceback remain intact.
5. Exercise delivery, review, typed unsupported, malformed pre-assembly,
   guarded assembly refusal, and typed-status double-fault controls. Prove no
   event includes native text or path material.

Acceptance: each predecessor matrix branch has a distinct accepted event
sequence and unchanged functional result/exception behavior.

## Slice 3 — Host coexistence and package qualification

Status: complete as a disposable pre-version-bump package gate; see
`SLICE 3 - INSTALLED WHEEL API HOST COEXISTENCE.md`.

1. Run the actual SBE application formatter with `force=True` for deterministic
   unit qualification.
2. Have API install the candidate wheel and prove normal `force=False`
   in-process coexistence: API stdout events and SBE capture diagnostics both
   remain valid structured records without duplicate handlers or swallowed
   events.
3. Prove package-root export behavior, installed-wheel/source parity, zero
   provider operations, and zero workspace mutation.
4. Run focused suites, manifest enforcement, provider-free broad qualification,
   build-twice wheel identity, release-lock checks, and API consumer review.

Acceptance: the exact host arrangement that produced Bembo/Morris emits usable
native diagnostics while ordinary capture behavior remains unchanged.

## Review Gate B — Release decision

Review the implementation and installed-wheel/API-host evidence before any
version bump, tag, publication, deployment, or live witness. A later live test
requires its own API rollout and owner approval; this sprint grants neither.

Status: reached. Fresh release identity, release-bound suites, tag,
publication, deployment, and live witness remain unstarted and require the
next review/authorization.

## Alloy ruling

Expected outcome is no model change: the work adds non-authoritative
observations without changing lifecycle, authority, selection, custody, packet,
or transition semantics. Record that ruling explicitly during implementation.
If any functional behavior changes, stop and reassess the model before release.
