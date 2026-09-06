# Slice 0 — cohort characterization and interval grammar

## Result

Slice 0 confirms that the shared-axis swimlane is useful and reproducible, but
also finds a contract boundary that the hand-built prototype concealed.

The existing reporter can parse SBE `astrowoof.sbe_worker_log.v1` records into
semantic epochs. It does **not** currently normalize the API worker wrapper's
`astrowoof.execution_event.v1` envelopes. Those envelopes carry the exact
cohort facts needed for:

- deterministic job start/completion;
- SBE job claim, defer, and lease release;
- SBE cycle start/completion and elapsed duration;
- the selected execution branch;
- capacity disposition;
- closeout and publication; and
- the relative handoff from one run to the next.

The current parser counts an execution-event envelope as JSON evidence but does
not add it to the normalized event stream or run reducer. Therefore a faithful
timeline cannot be implemented solely as a new HTML renderer over today's
`report.json` v1. Slice 1 should define a separate closed cohort projection and
an explicit diagnostic adapter for a small approved subset of execution-event
v1. This preserves the existing exact-key report consumer and keeps API-owned
observations distinct from native SBE evidence.

## Observed cohort

Source: Better Stack source `AstroWoof Render Logs` (`2740198`), queried on
2026-09-06 for the complete event window beginning at `18:03:00Z`. The source
contains interleaved wrapper execution events and SBE structured trace records.
The table below uses Mountain Daylight Time for readability; canonical evidence
remains UTC.

| API run | Native run | First job start | First SBE cycle | Final observed outcome |
|---|---|---:|---:|---|
| `70423106-000c-4bc1-a790-fdbf6a2dfb4d` | `aa60af4c2e6c65f613fb276d61ce0a8c246d42b401c244de4b086eff7c23e966` | 12:03:29.653 | 12:05:16.986 | native editorial review at 12:14:57.060 |
| `67a369ac-1953-447c-b3ae-bb19fd7cd994` | `3c59bd1668a29b0735375528630d13c66c2b80a108be3b5c802868dd121199fb` | 12:05:14.856 | 12:07:10.455 | delivery published at 12:25:51.260 |
| `665cd3d2-332a-4ba7-9c0b-bb3fb4e1a177` | `468479aa4a8d818392b2705919817c2ebca44cab78e3868657f8746b5e50f50e` | 12:06:47.863 | 12:15:41.651 | delivery published at 12:30:40.234 |

The final two outcomes arrived after the first preview of the cohort. The Slice
0 fixture must use the complete window rather than freeze the earlier partial
posture as final.

## Findings visible on the common clock

1. Deterministic preparation overlapped: run two began immediately after run
   one's deterministic successor was enqueued, and run three began immediately
   after run two's deterministic successor was enqueued.
2. SBE active cycles were serialized in this one-slot cohort.
3. Runs spent materially more wall-clock time outside active cycles than inside
   them. Those gaps are not all semantically identical.
4. A directly evidenced fairness handoff occurred when run two's cycle completed
   at `12:15:41.548` and run three's next SBE cycle began at `12:15:41.651`, a
   103 ms observed boundary using the rounded log timestamps (102 ms when using
   the earlier displayed truncation). The artifact must retain exact timestamps
   and compute rather than hard-code the duration.
5. Run one reached a typed `terminal_closed` / `retain_for_review` outcome while
   runs two and three continued.
6. Runs two and three later reached `delivery_accepted`, closeout, publication,
   and completed job evidence.

These are observations from logs, not lifecycle, settlement, custody, or
capacity authority.

## Evidence ownership

| Evidence family | Producer/owner | Safe diagnostic use | Forbidden inference |
|---|---|---|---|
| `astrowoof.sbe_worker_log.v1` | native SBE runtime | native state summaries, command boundaries, stage/reconciliation detail | API queue ownership or resource release |
| `astrowoof.execution_event.v1` `worker.job.*` | API worker wrapper | observed job start, claim, defer, completion, failure | native lifecycle truth from the event name alone |
| `astrowoof.execution_event.v1` `worker.lease.*` | API worker wrapper | observed lease acquire/release windows | global capacity availability or admission facts |
| `astrowoof.execution_event.v1` `sbe.cycle.*` | API wrapper around SBE invocation | exact invocation start/end, branch, duration, returned disposition | mutation/settlement truth beyond the typed result consumed by API |
| checkpoint/result/receipt contracts | their public readers | authoritative facts expressly validated by those readers | facts absent from the closed document |

The adapter must stamp every normalized event with its evidence family and
producer so renderers cannot flatten wrapper observations into native truth.

## Frozen interval pairing grammar

### Active deterministic work

- Start: `worker.job.started` for the deterministic job identity.
- End: matching `worker.job.completed` or `worker.job.failed`.
- `worker.successor.enqueued` may be annotated inside the interval but is not a
  substitute end unless the job-completion event is missing.
- If completion is absent, render an open interval ending at the export boundary
  and label it incomplete.

### Active SBE cycle

- Start: `sbe.cycle.started`.
- End: `sbe.cycle.completed` with the exact same API run, job, attempt, and lease
  identities.
- The branch comes from the completion payload (`initial_wave`,
  `provider_reconciliation`, `external_authority_v2`, or
  `delivery_validation`). It must not be guessed from surrounding native logs.
- The reported `duration_ms` is checked against timestamps within an explicit
  tolerance; a mismatch is surfaced as contradictory timing evidence.
- Nested native SBE trace events enrich this interval but do not create a second
  wall-clock allocation interval.

### Deferred/queued boundary

- Start: a matching `worker.job.deferred`, or a cycle completion whose closed
  capacity disposition explicitly releases/defer-until-due and is followed by
  the matching defer event.
- End: the next matching `worker.job.claimed`/`worker.lease.acquired` for that
  run and job lineage.
- Label as **API deferred/queued**, not `provider wait`, unless a validated
  lifecycle/result decision separately proves retained provider custody or a
  not-due posture.
- Absence of another run's activity does not turn this interval into capacity
  ownership.

### Provider wait

- Requires an accepted native lifecycle/result observation that explicitly
  describes provider-pending or not-due custody.
- Its outer wall-clock bound may be joined to matching defer and next-claim
  evidence, but the artifact retains both evidence owners.
- A bare gap between SBE cycles is never classified as provider wait.

### Local-work wait

- Requires an accepted lifecycle local-work decision and a subsequent matching
  local command boundary.
- `continue_local_cycle` alone is not a sufficient semantic classification; it
  describes capacity behavior, not the kind of native work.

### Terminal review

- Requires a sealed, reader-valid native terminal result or the exact invocation
  result identity transported through the wrapper.
- A wrapper `worker.job.failed` is not enough, and the substring `review` in a
  status or message is not enough.
- API terminal settlement remains distinct from native editorial review.

### Delivery

- Active interval: `sbe.cycle.started` to matching `sbe.cycle.completed` with
  `execution_branch=delivery_validation`.
- Completion marker: `delivery_accepted` plus matching
  `reading.publication.completed` or typed closeout evidence.
- A completed cycle without publication is not rendered as delivered.

### Failure/refusal

- Requires a registered typed result, refusal, contradiction, or wrapper failure
  classification.
- Generic stderr prose cannot define the class.

### Unknown/open

Use an unknown/open interval when:

- start or completion evidence is missing;
- identities do not match;
- timestamps reverse;
- duplicate records disagree;
- a partial export begins or ends inside activity; or
- the visual gap has no closed semantic evidence.

The renderer may leave truly unsupported gaps blank, but its accessible summary
must state that blank time is unclassified rather than idle.

## Pairing precedence

1. Exact run + job + attempt + lease identity.
2. Exact run + invocation/command identity when the event family lacks a lease.
3. Exact run + closed predecessor/successor relationship expressly permitted by
   that event contract.
4. No temporal-nearest fallback.

Events with the same timestamp retain source order. Exact duplicate events may
collapse visually only while preserving all source lines and raw digests.

## Schema decision

Do not widen `astrowoof.sbe_run_evolution_report.v1`. It is closed and already
packaged. Slice 1 should define an additive projection, provisionally:

`astrowoof.sbe_run_cohort_timeline.v1`

The projection should bind one or more validated run reports plus the approved
normalized execution-event subset. This allows the epoch matrix to remain an
SBE-native diagnostic view while the cohort timeline explicitly joins native
and wrapper observations without erasing ownership.

## Slice 1 gate

Slice 1 may begin after review confirms:

- the separate projection/version choice;
- the approved execution-event subset;
- the identity join and pairing precedence;
- the conservative wait classifications; and
- the distinction between observed wrapper scheduling and authoritative native
  state.
