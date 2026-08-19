# Response Retrieval Observability Patch Sprint 1 Evidence

Status: exact 0.4.10 artifact qualified for authorized publication.

## Exact 0.4.10 release artifact

- Artifact source commit:
  `5a3c4354d91134b46847b49c03221356bf97524b`.
- Wheel: `astrowoof_natal_authoring-0.4.10-py3-none-any.whl`.
- Bytes / SHA-256: 843,325 /
  `e27a4ea740f8492672f059209dbd743432cf3fd9bdcbf91e12a17a4be2ff437e`.
- Two fixed-epoch builds: byte-identical.
- Wheel boundary: 125 entries / 74 resources / zero tests or bytecode /
  `py.typed` present.
- Release-focused source tests: 100 passed in 16.005 seconds.
- Exact installed Windows CLI/schema and scripted one-GET API probe: pass.
- Provider GETs / submissions / spend: 0 / 0 / USD 0.

## Qualification summary

- Focused/directly affected source suites: 100 passed in 16.308 seconds.
- Covered response diagnostic API/CLI, completed/pending/provider-failed
  classification, 401/404/429, timeout, malformed return, ID mismatch, redaction,
  closed fields, output-path refusal, durable cycle linkage, fresh snapshot,
  retrieval concurrency, lifecycle contracts, initial wave, deployed QA, execution
  events, and native transitions.
- Manual closed validator accepted the packaged fixture and rejected added fields.
  The optional third-party `jsonschema` library was unavailable in the local source
  runtime, so no claim of an independent JSON-Schema-engine pass is made.
- Non-published wheel: `astrowoof_natal_authoring-0.4.9-py3-none-any.whl`, 843,314
  bytes, SHA-256
  `688419f873a879c0460732b65ed261bb8f88e1cce56cb4e1261e4b106e0fb197`.
- Installed-wheel console schema discovery, public Python probe with one scripted
  GET, and packaged module/schema/fixture inspection: pass.
- The installed scratch environment's `pip check` could not be claimed because
  its locally available SPC wheel requires `jsonschema`, which was not available
  in that isolated scratch environment. This is an environment dependency absence,
  not an SBE package-metadata failure.
- No live provider request or paid operation occurred.

## Durable diagnostic shape

- Artifact path:
  `lifecycle/provider-reconciliation/<action-id>.attempt-<ordinal>.json`.
- Cycle records bind each diagnostic by action/attempt identity, logical path,
  bytes, and SHA-256.
- Artifacts are written before the normal workspace snapshot and validated through
  a fresh lifecycle inspection.
- Response evidence, custody, backoff, and public cycle-result vocabulary remain
  unchanged.

## Confirmed seam

- Interactive due actions are retrieved concurrently in
  `astrowoof_natal_authoring/reconciliation.py`.
- The retrieval worker returns the caught exception to the single-writer reducer.
- Provider identity mismatch has a distinct fail-closed path.
- Other exceptions currently retain only `transport_warning` and backoff state,
  without exception class, sanitized message, HTTP status/request ID, endpoint,
  or measured duration.

## Provider activity

- Provider GET operations: 0.
- Provider submissions: 0.
- Spend: USD 0.
