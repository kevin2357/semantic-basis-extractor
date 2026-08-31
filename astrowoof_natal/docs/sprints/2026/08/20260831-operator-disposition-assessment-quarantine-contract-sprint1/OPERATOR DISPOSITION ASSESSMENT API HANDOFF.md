# Operator disposition assessment — API consumer handoff

## Status

SBE `0.4.37` is published and post-publication verified. API and owner approved
the immutable release.

## Public surfaces

- Assessment contract: `astrowoof.operator_disposition_assessment.v1`
- Root reader: `read_operator_disposition_assessment(run_dir, ...)`
- Root validator: `validate_operator_disposition_assessment(value)`
- Root schema reader: `read_operator_disposition_assessment_schema()`
- Sanitized eight-class fixture reader: `read_operator_disposition_fixtures()`
- Fixture validator: `validate_operator_disposition_fixtures(value)`
- Read-only CLI: `astrowoof-operator-disposition-assessment --run-dir ...`
- Qualification CLI: `astrowoof-operator-disposition-qa`

The ordinary reader and CLI do not discover a result through availability.
The Python reader's `allow_availability_recovery` default is `False`.
Availability discovery is a deliberate recovery/preflight opt-in; a discovered
ID is still passed through the exact snapshot-valid native-result reader.

## Consumer rule

This document describes native facts only. API may join it to API-owned job,
lease, slot, reservation, billing, and quarantine state, but must not treat
`quarantine_posture=permitted` as an SBE assertion that any API resource was
released. API invokes only a named `supported_next_actions` operation and does
not reconstruct reconciliation members from counts or provider references.

Absent evidence, contradictory evidence, and unknown lifecycle versions fail
closed as `unsupported_or_inconsistent`; they are not represented as false,
empty, or a fallback action. Exact terminal ingress requires exact result and
receipt evidence joined to the current checkpoint. A status or result-index
label is never sufficient.

## CLI boundary

The assessment CLI accepts only `--run-dir` and optional `--output`. It accepts
no provider credentials, grant/authority document, mutation option, recovery
mode, or provider command payload. Output paths inside the native workspace are
refused. The default assessment is printed as canonical JSON.

## Qualification boundary

The qualification is provider-free and qualification-only. It creates a
sanitized temporary fixture workspace, invokes the real public CLI twice in
fresh Python processes, and proves byte-identical assessment replay,
byte-identical native workspace files, run-level reconciliation selection,
default-disabled availability recovery, and privacy-sentinel exclusion.

It performs zero external network calls, provider creates, provider retrieves,
or spend. It does not access retained QA/R2 workspaces.
