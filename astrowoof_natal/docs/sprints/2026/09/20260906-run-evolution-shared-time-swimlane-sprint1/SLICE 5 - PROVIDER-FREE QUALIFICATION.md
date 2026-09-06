# Slice 5 — provider-free qualification

## Outcome

Added a packaged qualification command and closed receipt for the complete
source-level cohort reporter boundary.

`astrowoof-run-timeline-qa` invokes the actual public reporter CLI against a
sanitized three-run mixed-evidence export, reads the resulting timeline through
the public reader, and binds the projection and HTML digests into a strict
receipt.

## Proven cohort

- Three runs on one absolute time axis.
- Two observed delivery outcomes.
- One native terminal-review outcome.
- One exact 102 ms witnessed cross-run handoff, explicitly not an SLA.
- One unmatched start retained as an open interval.
- One existing semantic-republication no-progress candidate joined from the
  run-report detector.
- Zero provider calls.

The fixture includes no prompts, request bodies, credentials, endpoints,
generated content, retained workspaces, or live identifiers.

## Defect found by qualification

The first complete fixture found that reducer-generated final postures carried
the marker interval ID where the v1 contract requires a constituent boundary
ID. The reducer now carries the exact marker boundary ID. The public reader and
three-outcome qualification lock this join against regression.

## Gate

The source qualification and focused suite are green. Clean installed-wheel
execution, reproducible build evidence, and release review remain pending under
Slice 6 if this packaged feature is released.
