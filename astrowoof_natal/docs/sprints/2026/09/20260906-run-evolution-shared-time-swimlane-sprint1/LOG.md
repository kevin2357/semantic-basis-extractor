# Log

## 2026-09-06 — Slice 0

- Created the shared-time cohort swimlane sprint.
- Reviewed the existing run reporter contract, parser, reducer, HTML renderer,
  tests, operator guide, and original reporter sprint.
- Queried the complete current three-run cohort from Better Stack and extended
  the earlier partial view through both successful delivery outcomes.
- Mapped active deterministic work, initial wave, reconciliation, v2 dispatch,
  delivery, defer/queue, review, and publication boundaries to their actual
  events and evidence owners.
- Identified that API wrapper `astrowoof.execution_event.v1` records are required
  for the cohort clock but are currently recognized only as generic envelopes by
  the SBE reporter.
- Froze conservative pairing and unknown-gap rules.
- Selected a separate additive cohort projection rather than widening the closed
  run-evolution report v1.
- No runtime, schema, package, provider, R2, workspace, or API state was changed.

## 2026-09-06 — Slice 1

- Incorporated API Voof-paws 1 precision requirements.
- Added the separately versioned, closed
  `astrowoof.sbe_run_cohort_timeline.v1` contract.
- Added a packaged JSON Schema plus public reader and strict Python validator.
- Preserved both canonical event time and outer record time on every boundary,
  with explicit clock agreement classification.
- Required exact source, raw-line, producer, evidence-family, and correlation
  provenance for every interval boundary.
- Required interval and handoff durations to be recomputed from their exact
  timestamps.
- Encoded cross-run handoffs as witnessed cohort facts with
  `witness_only_not_sla=true`.
- Prevented API wrapper evidence alone from manufacturing a native terminal
  review conclusion.
- Kept observed lease/allocation evidence distinct from global capacity or slot
  ownership.
- Added closed-shape, schema, digest, identity-join, clock, evidence-family,
  terminal-review, and handoff mutation tests.

## 2026-09-06 — Voof-paws 2 corrections and Slice 2

- Made evidence ownership mechanically select the canonical clock:
  `native_sbe` requires `message.timestamp`; `api_worker_wrapper` requires
  `message.observed_at`.
- Made observed handoff ordering chronological by exact witnessed end/start
  times, with digest used only as the final tie-breaker.
- Added the closed API execution-event adapter with accepted, refused, and
  unsupported-event accounting.
- Added the deterministic mixed native/API interval reducer.
- Preserved exact source-byte and normalized-trace joins to run-report v1.
- Projected provider-reconciliation, initial-wave, deterministic-work, and
  observed allocation windows without converting them into scheduler authority.
- Kept unpaired accepted wrapper boundaries visible as `unknown`; unmatched
  starts remain `open`; end-before-start evidence remains `contradictory`.
- Added deterministic source-binding, mixed-evidence, orphan-event,
  contradictory-clock, unsupported-event, and malformed-event tests.
- No provider, network, R2, retained workspace, or API state was accessed.

## 2026-09-06 — Voof-paws 3 verification

- Verified that both reported contract mismatches were already corrected in the
  current working tree: `adapter_coverage` is a required closed root member and
  `observed_execution_allocation` is a closed interval classification in both
  the packaged schema and Python validator.
- Strengthened the real reducer test to require nonzero adapter coverage, paired
  lease/allocation intervals, an artifact write, and a read through the public
  `read_run_cohort_timeline()` boundary.
- Confirmed the restored public artifact exactly equals the reducer output.

## 2026-09-06 — Slice 3

- Added `render_run_cohort_timeline_html()` as a public deterministic renderer
  over the validated cohort projection.
- Added one common absolute time axis and one horizontal lane per run.
- Added local controls for run highlighting, hiding/showing wait intervals, and
  highlighting existing no-progress candidates.
- Added keyboard-accessible interval buttons with exact evidence family,
  duration, status, source lines, and interval identity details.
- Added visible handling for open and contradictory intervals and a compact
  text-plus-color legend.
- Added responsive narrow-width layout and light/dark presentation.
- Validated display timezone names while leaving canonical UTC and timeline
  digest unchanged.
- Added deterministic, self-contained, invalid-contract, invalid-timezone, and
  script-terminator escaping tests.

## 2026-09-06 — Slice 4

- Added `astrowoof-run-report timeline` for explicit cohort projection and
  rendering from a local exported log.
- Added `render --format timeline-html` through the public timeline reader.
- Made ordinary `build` add `report.timeline.json` and
  `report.timeline.html` only when timeline-capable evidence exists; the four
  legacy outputs remain unchanged for native-only input.
- Added display-timezone support without altering canonical timeline data.
- Rejected network URL inputs at argument parsing.
- Added CLI integration tests for explicit timeline, combined build, public
  artifact re-rendering, timezone display, and local-only input.
- Updated the reporter guide and Better Stack query playbook.

## 2026-09-06 — Slice 5 source qualification

- Added the packaged `astrowoof-run-timeline-qa` console command and closed
  `astrowoof.sbe_run_cohort_timeline_qualification.v1` receipt/schema.
- Exercised the real public timeline CLI with a sanitized three-run fixture.
- Proved two delivered runs, one terminal-review run, one 102 ms witnessed
  handoff, one explicit open interval, one existing no-progress candidate,
  deterministic receipt/HTML bytes, and zero provider calls.
- The qualification exposed and fixed a reducer join bug: final posture evidence
  incorrectly carried the marker interval ID rather than its exact boundary ID.
- Added fail-closed receipt mutation tests, packaged schema validation, CLI
  receipt output, and privacy checks.

## 2026-09-06 — Slice 6 source regression

- Bumped the release candidate to fresh version `0.4.52` before regression.
- Updated the release-derived providerless-denial qualification fixture and its
  canonical receipt digest before running the broad suite.
- Passed the expanded focused matrix: 69 tests in 28.584 seconds, 5 skips.
- Passed the full provider-free suite on the first correctly versioned run:
  1,103 tests in 1,083.232 seconds, 58 skips.
- Observed very high routine `INFO` trace volume; recorded its optimization as
  a separate test-infrastructure sprint so the release candidate is not changed
  during qualification.
