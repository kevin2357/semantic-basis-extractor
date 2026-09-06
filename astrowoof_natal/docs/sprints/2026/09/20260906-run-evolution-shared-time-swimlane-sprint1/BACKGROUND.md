# Background — shared-time cohort swimlane for the run evolution reporter

## Why this sprint exists

The installed `astrowoof-run-report` already turns SBE worker logs into a
closed diagnostic JSON artifact plus Markdown, interactive matrix, and Mermaid
views. Those views are strong for inspecting one run's semantic epochs and
finding repeated posture, but they do not make resource sharing and relative
progress across a qualification cohort immediately visible.

During the 2026-09-06 three-run QA cohort, a manually constructed horizontal
swimlane placed all runs on one Mountain-time axis. It made several facts
visually obvious:

- deterministic preparation overlapped across runs;
- only one run occupied the SBE execution slot at a time;
- provider waits and queue waits were much longer than active native cycles;
- capacity rotation occurred promptly after a durable defer boundary;
- one run reached editorial review while the other two continued and were
  ultimately delivered; and
- later runs made progressive forward movement rather than repeating an
  indistinguishable posture.

This was the clearest cohort-level view produced so far. The useful behavior
should become a deterministic output of the existing reporter rather than
remain a hand-built Better Stack analysis.

## Existing foundation

The current reporter already provides:

- pipe-delimited and structured-JSON `✨🐶` parsing;
- native-run partitioning;
- source-line and raw-line SHA-256 provenance;
- a closed `astrowoof.sbe_run_evolution_report.v1` artifact;
- semantic epoch reduction;
- direct-evidence timing summaries;
- exact and semantic-republication no-progress candidates;
- privacy-bounded safe-field handling;
- deterministic Markdown, HTML, and Mermaid renderers; and
- provider-free installed qualification.

Slice 0 found an important boundary in that foundation: the parser understands
SBE's `astrowoof.sbe_worker_log.v1` records, but the common-clock intervals in
the observed cohort also rely on API worker-wrapper
`astrowoof.execution_event.v1` envelopes (`worker.job.*`, `worker.lease.*`, and
`sbe.cycle.*`). The current parser recognizes those lines only as generic JSON
envelopes; it does not normalize them into reducer events. A faithful cohort
timeline therefore needs an explicit, separately provenance-labeled diagnostic
adapter for the approved execution-event fields. It must not pretend those
API-owned observations are native SBE state.

The sprint should extend those foundations. It should not build another log
parser or invent a parallel understanding of lifecycle semantics.

## Proposed product shape

Add a cohort-level timeline projection and a self-contained HTML swimlane view:

```text
worker log export
    -> existing strict parser / report reducer
    -> closed per-run events and provenance
    -> evidence-bounded interval projection
    -> shared absolute time axis
         lane A: deterministic | initial wave | wait | reconcile | ...
         lane B: deterministic | queued       | initial wave | ...
         lane C: deterministic | queued       | initial wave | ...
```

Each bar must be derived from directly joined evidence. An unpaired start,
missing boundary, partial export, or ambiguous overlap must remain visibly
unknown/open; the reporter must not fill gaps by guessing what a run was doing.

## Evidence and authority boundary

The swimlane is diagnostic only. It cannot authorize or prove lifecycle,
custody, settlement, capacity release, terminalization, or provider work.

In particular:

- a blank span means the export contains no classified interval evidence;
- a grey wait/queue span must have an observed boundary that supports that
  classification;
- missing logs do not prove inactivity;
- a command result or checkpoint remains authoritative through its own public
  contract, not because the timeline renders it;
- API-owned queue/allocation truth must not be reconstructed from SBE labels;
  and
- cross-service API/SBE joining remains a separate contract unless explicit
  API events are part of an approved input shape.

## Initial acceptance target

Given one exported log containing an arbitrary number of interleaved runs, one
reporter command should produce the existing outputs plus a self-contained
cohort timeline that:

1. uses one common absolute time axis;
2. displays one horizontal lane per run;
3. distinguishes active command families, provider/retrieval waits, queue or
   capacity waits, delivery, review, failure, and unknown gaps without relying
   on color alone;
4. exposes exact start/end/duration and evidence pointers for each interval;
5. makes overlapping work and serialization obvious;
6. marks no-progress candidate windows from the existing detector;
7. behaves legibly for one run, three-run QA cohorts, and larger cohorts; and
8. remains byte-deterministic, provider-free, network-free, and privacy-safe.

## Out of scope

- live Better Stack querying or credentials;
- automatic polling or dashboard hosting;
- changes to runtime scheduling or lifecycle semantics;
- automatic repair, retry, denial, quarantine, or release decisions;
- inferred API allocation ownership without API-owned evidence;
- private workspace inspection; and
- replacing the epoch matrix, which remains the better detailed single-run
  semantic view.
