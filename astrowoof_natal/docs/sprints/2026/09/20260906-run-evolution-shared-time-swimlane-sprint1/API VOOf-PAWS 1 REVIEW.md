# API Voof-paws 1 review — shared-time cohort swimlane

## Decision

**Approved for Slice 1.** The reporter should add a separately versioned,
diagnostic-only cohort projection rather than widen the closed
`astrowoof.sbe_run_evolution_report.v1` artifact. The Slice 0 evidence map,
execution-event adapter boundary, interval pairing precedence, and
unknown/open handling are aligned with API ownership.

## What is specifically approved

- Parsing the narrowly enumerated `astrowoof.execution_event.v1` wrapper
  records as an explicitly API-owned evidence family alongside the existing
  native SBE structured records.
- Exact identity pairing by run/job/attempt/lease before any temporal
  interpretation, with no nearest-timestamp fallback.
- Rendering observed deferred/claimed/lease boundaries as diagnostic API
  scheduling observations, while keeping provider custody and native state
  governed by their own public contracts.
- A separate `astrowoof.sbe_run_cohort_timeline.v1` projection that binds its
  report/source digests and preserves each interval's evidence pointers.
- Conservative blank, unknown, partial, and contradictory intervals instead
  of visual inference.

## Small precision requirements for Slice 1

1. Preserve the raw canonical event timestamp, source line/digest, and the
   producer/evidence family on every interval boundary. If input families can
   supply different timestamp fields, freeze which one is canonical for axis
   placement and surface a disagreement rather than silently selecting a
   convenient clock.
2. In renderer labels and written claims, call a wrapper lease span an
   **observed execution-allocation/lease window**. Do not call it global slot
   occupancy or global capacity availability unless the approved API record
   expressly proves that stronger claim.
3. Likewise, the 102–103 ms handoff is a witnessed boundary in this cohort,
   not a general latency/SLA promise. Retain the exact evidence and calculate
   it; do not encode the number as a policy assertion.
4. A `worker.job.failed` may render an API wrapper failure observation, but it
   must not by itself manufacture a native terminal-review or editorial
   conclusion. The approved terminal-review and delivered pairing rules
   already capture this distinction correctly.

No API runtime, scheduling, custody, provider, workspace, or retained-run
mutation is implicated by this approval. The output remains a local,
provider-free diagnostic artifact.
