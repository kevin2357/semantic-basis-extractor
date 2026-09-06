# Better Stack MCP log-query playbook

## Purpose

Use Better Stack as a read-only investigation index for forwarded Render logs.
It accelerates timeline reconstruction and cross-service correlation; it does not
replace native checkpoints, sealed results, receipts, or API database authority.

## Current QA source

- team: `594312` (`Your team`)
- populated source ID: `2740198`
- table: `t594312.astrowoof_render_logs_2`
- recent log collection: `remote(t594312_astrowoof_render_logs_2_logs)`
- retention reported by the source: three days for logs/spans

An earlier same-named source, ID `2740132`, currently has no discoverable fields.
Do not assume that the display name uniquely identifies a source.

Avoid requesting full source details during routine investigations: the MCP's
read-only source-detail result includes the ingestion token. Use source listing,
field discovery, query help, and query execution instead.

## Investigation order

1. List sources and select by numeric source ID, not display name.
2. Fetch the source field catalog.
3. Fetch query instructions for that source before composing SQL.
4. Start with a short time range, explicit ordering, and a small `LIMIT`.
5. Join on explicit correlation fields, especially API run ID and native run ID.
6. Treat missing rows as an observability gap until forwarding and retention are
   established; never infer that a native transition did not happen solely from
   log absence.
7. Confirm consequential conclusions against public result/receipt/checkpoint
   evidence.

## Useful structured fields

The current source exposes:

- `message.correlation.run_id`
- `message.correlation.native_run_id`
- `message.correlation.job_id`
- `message.correlation.attempt_id`
- `message.correlation.lease_id`
- `message.correlation.checkpoint_id`
- `message.event_name`
- `message.observed_at`
- `message.payload.execution_branch`
- `message.payload.execution_capacity_disposition`
- `message.payload.local_continuation_required`
- `message.payload.outcome`
- `message.payload.reason_code`
- `message.payload.stage`
- `message.producer.runtime_version`

Most ordinary Render stdout/stderr rows are not structured envelopes. Those rows
remain searchable as raw text but cannot participate in reliable field joins.

## Run-summary query

Replace the interval if necessary. Better Stack's current query guidance says the
recent collection covers approximately the last 30 minutes; consult query help
and use the historical collection for older evidence.

```sql
WITH
  JSONExtract(raw, 'message', 'correlation', 'run_id', 'Nullable(String)') AS correlated_run_id,
  JSONExtract(raw, 'message', 'correlation', 'native_run_id', 'Nullable(String)') AS correlated_native_run_id,
  JSONExtract(raw, 'message', 'producer', 'runtime_version', 'Nullable(String)') AS producer_runtime_version
SELECT
  correlated_run_id,
  any(correlated_native_run_id) AS sample_native_run_id,
  any(producer_runtime_version) AS sample_runtime_version,
  count(*) AS event_count,
  min(dt) AS first_seen,
  max(dt) AS last_seen
FROM remote(t594312_astrowoof_render_logs_2_logs)
WHERE
  dt > now() - INTERVAL 30 MINUTE
  AND correlated_run_id IS NOT NULL
  AND correlated_run_id != ''
GROUP BY correlated_run_id
ORDER BY last_seen DESC
LIMIT 20
```

## Exact-run timeline query

Replace `<api-run-id>` with the exact API run UUID.

```sql
WITH
  JSONExtract(raw, 'message', 'correlation', 'run_id', 'Nullable(String)') AS correlated_run_id
SELECT
  dt,
  JSONExtract(raw, 'message', 'event_name', 'Nullable(String)') AS event_name,
  JSONExtract(raw, 'message', 'payload', 'execution_branch', 'Nullable(String)') AS execution_branch,
  JSONExtract(raw, 'message', 'payload', 'outcome', 'Nullable(String)') AS outcome,
  JSONExtract(raw, 'message', 'payload', 'reason_code', 'Nullable(String)') AS reason_code,
  JSONExtract(raw, 'message', 'correlation', 'checkpoint_id', 'Nullable(String)') AS checkpoint_id
FROM remote(t594312_astrowoof_render_logs_2_logs)
WHERE
  dt > now() - INTERVAL 30 MINUTE
  AND correlated_run_id = '<api-run-id>'
ORDER BY dt ASC
LIMIT 500
```

## Initial connection qualification

On 2026-09-06, the MCP successfully:

- listed the Better Stack team and both log sources;
- discovered the populated source's structured field catalog;
- executed bounded ClickHouse queries;
- found two distinct correlated API/native runs; and
- grouped lifecycle and worker events by exact event name.

The initial sample also showed that unstructured forwarded rows substantially
outnumber structured envelopes. This is expected for whole-service forwarding,
but future dashboards and automated investigations should explicitly measure
structured-event coverage rather than treating every ingested row as equivalent.
