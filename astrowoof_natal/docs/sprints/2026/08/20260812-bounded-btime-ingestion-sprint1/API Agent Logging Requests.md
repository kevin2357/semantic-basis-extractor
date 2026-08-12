# API Agent Logging Requests

```yaml
status: input-for-sprint-planning
author: astrowoof-api-agent
date: 2026-08-12
target: semantic-basis-extractor
sprint: 20260812-bounded-btime-ingestion-sprint1
proposed_contract: sbe.execution_event.v1
```

## Purpose

SBE should emit a stable structured execution-event stream describing work inside
semantic-basis extraction, claim selection, provider authoring, QA, polish, critic,
and delivery construction. AstroWoof's API will separately log orchestration facts
such as queue claims, leases, checkpoints, R2 custody, publication, and public HTTP
state.

The Sarah staging run demonstrates the need. From the OpenAI dashboard, six Luna
Responses appeared to have no output for approximately 30 minutes, followed by one
Terra Response. From the API database during the provider wait, the initial actions
had no provider IDs because the native invocation had not returned to the
coordinator. Only after correlating Render tracebacks, API attempts, SBE
checkpoints, paid-action records, and OpenAI timestamps could we establish that all
six initial passes completed, a creative retry was submitted and reported, and a
subsequent action was denied by the creative-retry spend ceiling.

The desired event stream would make that progression directly observable without
making logs authoritative for recovery.

## Core invariant

> Logs describe execution. They never authorize, resume, reconcile, charge,
> publish, or determine execution state.

`run.json`, the native spend ledger, provider evidence, complete workspace
snapshots, and API-owned durable state remain authoritative. Losing, duplicating,
delaying, or reordering log records must not change behavior. A consumer may build
dashboards and alerts from events, but it must use the authoritative interfaces to
take action.

## Transport and formatting

### Required production form

- newline-delimited JSON, one complete JSON object per physical line;
- UTF-8 without BOM;
- UTC RFC 3339 timestamps with fractional seconds and `Z`;
- stdout for normal structured events;
- stderr for warning/error events if the runtime can preserve the same JSON shape;
- no multiline tracebacks in production JSON mode;
- deterministic event names and closed reason-code vocabularies per schema version;
- `INFO` production default with configurable minimum level; and
- no SBE-owned rotation, shipping, retention, or monitoring-vendor dependency.

Render or another deployment platform owns stream capture. The API/platform
observability layer owns aggregation, retention, alerting, and access policy.

### Optional forms

- human-readable console rendering may be available for local development;
- an optional mirrored `events.jsonl` inside the native run workspace is useful for
  installed smoke and forensic bundles;
- the mirrored file is diagnostic evidence, not required for resume and not part of
  semantic identity; and
- JSON mode must remain available even when human output is selected elsewhere.

## Event envelope

Every event should validate against a packaged schema such as
`sbe.execution_event.v1` and include:

```json
{
  "event_schema": "sbe.execution_event.v1",
  "timestamp": "2026-08-12T09:20:43.867577Z",
  "level": "info",
  "event": "provider.action.reported",
  "sequence": 84,
  "runtime_invocation_id": "opaque-invocation-id",
  "native_run_id": "opaque-native-run-id",
  "stage": "creative_retry",
  "subject_ref": "opaque-subject-ref",
  "pass_ref": "opaque-pass-ref",
  "attempt": 2,
  "duration_ms": 164231,
  "details": {}
}
```

### Required envelope fields

- `event_schema`;
- `timestamp`;
- `level`;
- `event`;
- monotonic per-invocation `sequence`;
- opaque `runtime_invocation_id`;
- opaque stable `native_run_id` when known;
- `stage` when applicable; and
- a structured `details` object, even if empty.

### Conditional correlation fields

- opaque subject reference, never dog name;
- projection-package/input manifest digest;
- generation/authoring profile ID and digest;
- pass reference and pass kind;
- native paid-action ID and action category;
- provider operation ID after it is durable;
- attempt number;
- checkpoint revision and digest;
- model route and service mode; and
- duration in milliseconds.

Opaque IDs may be logged where operational correlation requires them. Storage
object keys, filesystem host paths, user IDs, names, and raw birth facts should not
be used as convenient correlation substitutes.

## Event naming

Use stable dotted names in past or state-transition form. Recommended families:

- `runtime.*`
- `input.*`
- `basis.*`
- `selection.*`
- `provider.*`
- `acceptance.*`
- `repair.*`
- `assembly.*`
- `validation.*`
- `lint.*`
- `polish.*`
- `critic.*`
- `checkpoint.*`
- `authorization.*`
- `delivery.*`
- `run.*`

Free-form messages may accompany events for humans, but consumers must never parse
them for state or reason.

## Runtime and input events

Emit at least:

- `runtime.started`
- `runtime.configuration_validated`
- `runtime.configuration_rejected`
- `input.load_started`
- `input.manifest_validated`
- `input.manifest_rejected`
- `input.source_identity_validated`
- `input.source_identity_rejected`
- `input.projection_set_validated`
- `input.projection_set_rejected`

Safe details should include:

- SBE distribution version and runtime-manifest digest;
- installed resource-set identity;
- input kind: `exact` or `bounded`;
- input schema versions;
- four expected projection contexts received;
- manifest and artifact hashes;
- source identity agreement result;
- authoring profile ID/digest;
- execution mode: live or batch;
- model-route policy identity; and
- validation reason codes.

Do not log full manifests if they contain subject or filesystem information.

## Bounded-input events

The bounded path should add events or details for:

- bounded projected-graph schema and evidence-contract versions;
- proof scope and bounded interval duration, without local datetime or coordinates;
- canonical object and relationship counts;
- root-owner evidence-family counts;
- counts by `invariant`, `conditional`, `variable`, `unavailable`, and
  `inconclusive`;
- reduced-capability flags;
- unsupported feature families;
- consistency of proof scope and source identity across all four contexts; and
- canonical versus evidence-only material made available to extraction.

Recommended events include:

- `input.bounded_contract_validated`
- `input.bounded_proof_scope_validated`
- `input.bounded_capabilities_summarized`
- `input.bounded_context_consistency_rejected`

Counts describe the input surface; they are not confidence, salience, probability,
or independent evidentiary weight.

## Basis extraction and claim-selection events

Emit stage start/completion/failure plus compact counts:

- `basis.extraction_started`
- `basis.candidate_pool_constructed`
- `basis.synthesis_completed`
- `basis.extraction_completed`
- `selection.ranking_started`
- `selection.root_owner_deduplicated`
- `selection.mandatory_placements_evaluated`
- `selection.completed`
- `selection.validation_failed`

Details should include:

- candidate counts by feature family and projection context;
- deterministic versus synthesized counts;
- accepted and excluded counts;
- mandatory-placement eligibility and selection counts;
- root-owner family input and post-deduplication counts;
- configured deck budget and selected deck size;
- deterministic claim-deck or authoring-packet digest;
- elapsed time for extraction, synthesis, ranking, and validation; and
- exclusions by stable reason code.

Recommended bounded-aware exclusion reasons:

- `not_canonically_invariant`
- `variable_prerequisite`
- `conditional_prerequisite`
- `inconclusive_prerequisite`
- `unavailable_capability`
- `unsupported_contract`
- `duplicate_root_owner_family`
- `projection_context_incomplete`
- `selection_budget_displaced`
- `semantic_validation_failed`

Do not log claim prose, evidence excerpts, generated synthesis text, dog names, or
human-readable chart descriptions.

## Provider and spend-boundary events

This is the highest-priority operational family. Emit:

- `provider.action_prepared`
- `authorization.request_published`
- `authorization.accepted`
- `authorization.denied`
- `authorization.released`
- `provider.submission_started`
- `provider.operation_recorded`
- `provider.attach_started`
- `provider.detached`
- `provider.poll_completed`
- `provider.response_completed`
- `provider.response_failed`
- `provider.usage_reported`
- `provider.action_reconciled`
- `provider.submission_ambiguous`

Safe details should include:

- action category;
- native action ID;
- pass and attempt references;
- maximum requested authorization;
- model and service mode;
- provider operation ID only after durable recording;
- provider status;
- input/output/cached/reasoning token counts when reported;
- actual or estimated cost and its classification;
- duration and poll count; and
- stable error/retry reason.

Do not log request or response bodies, prompts, headers, credentials, provider file
contents, or raw model output.

The Sarah timeline should have been legible approximately as:

```text
six provider.action_prepared / authorization.accepted
six provider.operation_recorded
six provider.response_completed / provider.usage_reported
acceptance.rejected for affected passes
creative-retry provider.action_prepared / authorization.accepted
provider.operation_recorded using Terra
provider.response.completed / provider.usage_reported
next authorization.request_published
authorization.denied reason=category_spend_ceiling_exceeded
run.terminal reason=spend_authorization_denied publishable_deck=false
```

## Acceptance, retry, repair, and editorial events

Emit:

- `acceptance.pass_accepted`
- `acceptance.pass_rejected`
- `acceptance.metadata_repair_started`
- `acceptance.metadata_repair_completed`
- `acceptance.creative_retry_required`
- `acceptance.retry_policy_exhausted`
- `assembly.started`
- `assembly.completed`
- `validation.completed`
- `lint.completed`
- `polish.skipped`
- `polish.prepared`
- `polish.completed`
- `critic.started`
- `critic.completed`
- `delivery.package_constructed`

Details should use bounded counts and closed classifications: validation error
counts, lint warning counts, repair category, retry feedback count, polish target
count, critic finding counts by priority/scope/repairability, delivery artifact
hashes, and stage durations. Never include the authored prose or critic diagnosis.

## Checkpoint, detach/resume, and terminal events

Emit:

- `checkpoint.publication_started`
- `checkpoint.published`
- `checkpoint.validation_failed`
- `run.detached`
- `run.resume_started`
- `run.resume_completed`
- `run.review_required`
- `run.completed`
- `run.terminal`

Terminal details should include:

- disposition: `completed`, `failed`, `review_required`, or `cancelled`;
- stable reason code;
- last completed stage;
- publishable-deck boolean;
- resumable boolean;
- provider-active and provider-ambiguous counts;
- prepared, authorized, provider-created, reported, reconciled, released, and
  denied action counts;
- workspace-quiescent and local-continuation-required booleans;
- latest snapshot revision/digest;
- total reported cost; and
- total elapsed duration.

Recommended terminal reason codes include:

- `completed`
- `input_contract_rejected`
- `semantic_basis_failed`
- `creative_retry_exhausted`
- `spend_authorization_denied`
- `provider_failed`
- `provider_submission_ambiguous`
- `checkpoint_integrity_failed`
- `final_validation_failed`
- `operator_review_required`
- `unexpected_internal_error`

## Severity policy

- `debug`: high-volume local diagnostics disabled by default;
- `info`: normal lifecycle transitions, provider progress, completed validation;
- `warning`: creative rejection, retry, detach with long-running provider work,
  reduced capability, denied optional work, recoverable provider condition;
- `error`: terminal inability to deliver, integrity failure, ambiguous submission,
  unsupported input contract, or internal invariant violation.

An expected creative rejection is not an infrastructure error. A hard spend denial
that ends the run should have an informational/warning denial event followed by an
error-level terminal event with the precise reason.

## Privacy and redaction requirements

Ordinary logs must never contain:

- OpenAI keys, authorization headers, cookies, or tokens;
- prompts, Responses, authored cards, critic prose, or claim prose;
- dog or handler names;
- birth date, local/UTC datetime, timezone, address, latitude, or longitude;
- complete source/projected graphs or claim decks;
- raw environment dumps;
- R2 credentials, signed URLs, or full storage keys;
- host-specific secret-bearing paths; or
- unfiltered exception representations that may contain request bodies.

Use allow-listed structured fields. Redaction after arbitrary object serialization
is not sufficient. Exception logging should emit a closed classification, safe
exception type, opaque incident ID, and optionally a sanitized bounded message.

## Schema and compatibility

- Package the JSON Schema and a small sanitized canonical JSONL fixture.
- Publish an event catalog defining every event, required/optional fields, reason
  vocabularies, and severity.
- Additive optional fields may remain within v1; changed meaning, removed required
  fields, or vocabulary changes require a new schema version.
- Consumers must ignore unknown event names only when the schema version explicitly
  permits extension; they must never infer state from an unknown event.
- Event schema version must not be inferred solely from the SBE release number.
- Exact and bounded runs should share the envelope and common lifecycle catalog;
  bounded-only details should be explicit extensions.

## Testing and qualification

Required automated evidence:

1. every emitted event validates against the packaged schema;
2. every documented event has a fixture or executable test path;
3. sequence numbers are monotonic within one invocation;
4. duplicate/replayed events do not affect native execution;
5. attach/detach/resume preserves stable run/action correlation;
6. provider-created identity is not logged before it is durably known;
7. exact and bounded installed-runtime smoke produce valid JSONL;
8. spend denial produces a precise terminal timeline;
9. an ambiguous provider submission is visibly different from a safe denial;
10. a terminal checkpoint can be restored without emitting a new submission;
11. redaction tests seed names, coordinates, datetimes, prompts, responses, keys,
    headers, filesystem paths, and storage keys, then prove none appear; and
12. truncating or deleting the event stream does not alter resume or validation.

Retain one compact exact-run fixture, one bounded-run fixture, and one Sarah-shaped
spend-denial fixture. The latter should be provider-free but preserve six initial
passes, a completed creative retry, an outstanding provider-less authorization,
and denial of further category spend.

## Metrics enabled downstream

This contract should support later derivation of:

- stage and end-to-end latency distributions;
- provider latency by model/mode/action category;
- first-pass acceptance and creative-retry rates;
- retry reasons and retry-policy exhaustion;
- cost per attempted and delivered deck;
- claim candidate, exclusion, synthesis, and selection counts;
- bounded invariant retention and exclusion ratios;
- root-owner deduplication ratios;
- attach/detach/resume counts;
- stalled-provider and spend-denial rates;
- validation, lint, polish, and critic outcomes; and
- completed, review-required, failed, and cancelled run counts by contract/profile.

SBE need not select OpenTelemetry, Sentry, Datadog, or another observability vendor
in this sprint. A stable event schema and safe stdout transport preserve those
options.

## Suggested sprint placement

Use two slices rather than one large retrofit:

### Early slice - Structured execution event contract

Define the schema/catalog, safe emitter, configuration, redaction policy, common
exact-run lifecycle events, provider/spend events, and terminal events. Qualify the
existing exact path before bounded ingestion depends on it.

### Late slice - Bounded observability qualification

Complete bounded input/extraction/selection instrumentation and capture an
installed-runtime bounded fixture. Validate counts, root-owner handling, reduced
capabilities, provider lifecycle, spend denial, QA, delivery, privacy, and replay
behavior.

This ordering makes observability part of the bounded implementation rather than a
post-hoc attempt to infer its novel semantics.

