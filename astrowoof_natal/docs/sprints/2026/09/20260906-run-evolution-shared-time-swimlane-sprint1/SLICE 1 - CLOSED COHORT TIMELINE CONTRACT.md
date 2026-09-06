# Slice 1 — closed cohort timeline contract

## Voof-paws 2 mechanical clarifications

- `native_sbe` boundaries normatively use `message.timestamp`.
- `api_worker_wrapper` boundaries normatively use `message.observed_at`.
- Witnessed handoffs are ordered by their exact from-end/to-start chronology;
  digest is only the final tie-breaker for identical times.

These are enforced by both the schema/validator surface and mutation tests;
they are not renderer conventions.

## Decision

The shared-clock view uses a new diagnostic contract:

`astrowoof.sbe_run_cohort_timeline.v1`

The existing closed `astrowoof.sbe_run_evolution_report.v1` remains unchanged.
This prevents an additive visualization from breaking exact-key consumers and
keeps the detailed native matrix independently usable.

## Public surface

- Packaged schema:
  `resources/contracts/sbe-run-cohort-timeline.v1.schema.json`
- Reader: `read_run_cohort_timeline(path)`
- Schema reader: `read_run_cohort_timeline_schema()`
- Validator: `validate_run_cohort_timeline(value)`

These are exported from the package root. The reducer/builder intentionally
waits for Slice 2.

## Closed projection shape

The projection binds:

- diagnostic-only and canonical-UTC declarations;
- every source log's name, byte digest, and line count;
- every source run report's report, source, and normalized-trace digests plus
  parser version;
- ordered API/native run identities and time bounds;
- ordered intervals with derived identities and durations;
- exact start/end boundary evidence;
- no-progress candidates by identity;
- explicitly non-authoritative final observed postures; and
- calculated cross-run handoff witnesses that explicitly are not SLAs.

Every boundary preserves:

- canonical event timestamp;
- the field that supplied that canonical timestamp;
- outer record timestamp when present;
- clock agreement/disagreement classification;
- source and raw-line digests;
- source line;
- event name;
- evidence family;
- producer service/component; and
- API run, native run, job, attempt, lease, invocation, action, and event
  correlation identities when available.

## Time rule

Axis placement uses the event family's canonical typed timestamp:

- SBE worker log: `message.timestamp`;
- API wrapper execution event: `message.observed_at`.

The outer record timestamp is retained but does not silently replace the event
clock. The validator checks the declared relationship:

- `exact` — zero difference;
- `within_tolerance` — greater than zero and at most five seconds;
- `disagrees` — greater than five seconds; or
- `outer_unavailable` — no outer timestamp exists.

Presentation may translate canonical UTC to Mountain or another requested
timezone. Display timezone is deliberately not stored in or digested into the
canonical projection.

## Authority and ownership rules

- `native_sbe` and `api_worker_wrapper` are the only v1 evidence families.
- Every interval declares all evidence families used by its direct boundaries.
- Boundary correlation, when present, must join the containing API/native run.
- A terminal-review interval must include native SBE evidence. A wrapper
  `worker.job.failed` cannot manufacture an editorial conclusion.
- Final posture always carries `not_authoritative_current_state=true`.
- Lease evidence can later render an **observed execution-allocation/lease
  window**. It cannot be labeled global slot ownership.
- Cross-run handoff duration is recomputed from the exact source interval end
  and destination interval start, and carries `witness_only_not_sla=true`.

## Closed classifications

Intervals use exactly one of:

- `deterministic_work`
- `initial_provider_wave`
- `provider_reconciliation`
- `external_authority_v2`
- `local_native_work`
- `delivery_validation`
- `observed_execution_allocation`
- `api_deferred_or_queued`
- `provider_wait`
- `terminal_review`
- `delivered`
- `failure_or_refusal`
- `unknown`

Status is exactly `complete`, `open`, or `contradictory`. Open intervals have no
end or duration. Completed and contradictory intervals require exact end
evidence and an exactly derived nonnegative duration.

## Mechanical guarantees

The Python validator goes beyond the structural schema and proves:

- exact root and nested keys;
- supported schema version;
- canonical projection digest;
- declared source/report joins;
- unique sorted run identities;
- unique sorted source and no-progress identities;
- stable boundary, interval, and handoff digests;
- canonical UTC timestamp syntax and clock relation;
- interval/run identity joins;
- chronological interval ordering and run containment;
- exact duration derivation;
- evidence-family closure;
- final-posture boundary membership; and
- witnessed handoff identity, membership, chronology, and duration.

## Review gate

Slice 2 should not implement the event adapter/reducer until review confirms the
closed projection is sufficient and does not accidentally elevate wrapper
events into native or API-global authority.
