# Editorial runtime-capture native diagnostics

## Purpose

Add bounded ✨🐶 observability to SBE's public
`build_editorial_review_runtime_capture(...)` path so a future live failure can
identify its first native phase and safe source frame without exposing native
contents or changing capture behavior.

This is an observability sprint, not a correction to editorial packet,
lifecycle, selection, custody, or transport semantics.

## Trigger

Two live SBE 0.4.61 witnesses, Bembo Brioche and Morris Madeleine, entered API's
terminal-observer capture boundary with exact result authority and the correct
logical-root string, then returned `unavailable` after a caught `TypeError`.
Neither reached envelope, preflight, HTTP, or artifact handling.

The completed investigation is:

`../20260915-bembo-morris-runtime-capture-typeerror-investigation-sprint1/`

Its provider-free matrix proved two materially different public escape paths:

1. a `TypeError` during evidence collection before packet assembly's existing
   guard; and
2. a second `TypeError` during typed-status construction that masks a guarded
   assembly failure.

Owner-authorized exact checkpoint reproduction did not reproduce either live
exception. Bembo built a delivery packet at every public layer. Morris returned
typed `unsupported / contradictory_native_evidence` at evidence collection and
both capture exports. API review therefore approved no SBE semantic correction
or package release from that evidence.

## Existing logging surface

SBE already has the appropriate host-compatible mechanism:

- module loggers created with `logging.getLogger(__name__)`;
- structured `event_name` and catalog-bounded `event_payload` extras;
- `application_logging` formatters that project those extras into the SBE
  worker JSON record;
- the checked-in `sbe-worker-log-event-catalog.v1.json`; and
- fail-silent operational-summary helpers in `trace_observability.py`.

The operator-disposition assessment diagnostics demonstrate that an exported
SBE library call hosted in another process can emit structured started,
completed, fingerprint, and phase-bounded failure records through the host's
existing formatter. The terminal capture callable can use the same approach.

## Desired diagnostic resolution

A future failure should establish, at minimum, whether it occurred during:

- root normalization;
- exact native result reading;
- eligibility classification;
- exact source/subject proof;
- state/action inventory interpretation;
- pass-attempt evidence collection;
- optional-stage evidence collection;
- packet assembly;
- packet validation;
- typed unsupported-status construction; or
- final capture return.

On failure, diagnostics may include only closed phase/reason tokens, normalized
exception class, a safe SBE function name and source line number, exact public
result ID, already-proven native/subject correlation IDs, branch once known,
root-string SHA-256, and a deterministic error fingerprint. They must never
include exception prose, paths, deck/report contents, prompts, responses,
bindings, credentials, or arbitrary persisted values.

## Non-goals

- No provider, R2, Better Stack, API, queue, lifecycle, or workspace mutation.
- No retry, replay, resume, reconciliation, or live-run action.
- No broad exception normalization or conversion of malformed evidence into a
  successful or typed result.
- No public contract/schema change to editorial packets or capture statuses.
- No claim that logging itself fixes or identifies the Bembo/Morris defect.
