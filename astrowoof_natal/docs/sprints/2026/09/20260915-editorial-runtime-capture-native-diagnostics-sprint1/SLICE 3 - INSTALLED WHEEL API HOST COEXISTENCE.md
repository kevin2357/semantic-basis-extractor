# Slice 3 — installed-wheel/API-host coexistence

## Result

Passed. The committed SBE diagnostics implementation coexists with the real API
host logging arrangement and preserves the existing capture surface from an
installed wheel. Review Gate B is reached.

This is a disposable pre-version-bump package gate, not a release candidate.
Its `0.4.61` metadata names an already-published release and therefore these
bytes must never be tagged, published, or substituted for a fresh candidate.

## Candidate identity

- Source commit: `8b52a90acc32b2eb84f2e494b988d3e49a16b207`
- Recorded `SOURCE_DATE_EPOCH`: `1789467559`
- Wheel: `astrowoof_natal_authoring-0.4.61-py3-none-any.whl`
- Size: 1,386,829 bytes
- SHA-256: `be7c59eb70b3c61adc2dedee13af6dfa62595697615c22e3d2d858f02c6e7f24`
- Independent builds: two; byte-identical
- Wheel members: 310
- Forbidden cache/bytecode/test members: zero
- Missing required runtime, formatter, or event-catalog members: zero

The installed `editorial_review_runtime.py` and
`sbe-worker-log-event-catalog.v1.json` SHA-256 values exactly matched their
committed source counterparts. Imports resolved under the isolated installed
site, outside the checkout. Dependency checking reported no broken
requirements when the candidate was prepended to the actual API host
environment.

## Real host coexistence proof

The provider-free probe imported API's production
`configure_sbe_application_logging()` and therefore invoked SBE's installed
`configure_logging(level="INFO", force=False)` path.

It proved:

- one pre-existing API host handler remained installed;
- exactly one recognized SBE handler existed after initialization;
- API's production event emitter wrote exactly one valid `process.started` and
  one valid `process.stopped` JSONL record to its stdout sink;
- SBE wrote 16 formatter/catalog-valid application records for three capture
  invocations, with exactly one start and one terminal record per invocation;
- the normal typed-unsupported branch returned
  `unsupported_result_version` unchanged;
- a pre-assembly `TypeError` escaped unchanged and was classified at
  `pre_assembly_evidence_collection`;
- the injected typed-status double fault escaped as the exact same exception
  object and was classified at `typed_status_construction`; and
- neither injected exception prose nor the temporary workspace root appeared
  in emitted SBE records.

Provider operations, network operations, spend, and authoritative workspace
mutation were all zero.

## Installed functional parity

Fifteen tests ran against the pre-imported installed package and passed:

- all 11 editorial runtime ingress tests, including the ordinary delivery
  packet, exact review route, source-proof failures, and typed unsupported;
- all four diagnostics tests, including logging-handler failure,
  pre-assembly failure, typed-status double fault, and closed formatter output.

The earlier source gates remain applicable: 45 focused tests passed, and the
broader provider-free matrix passed 99 tests with one expected skip. The test
manifest contains the new diagnostics module as serial-only and
logging-sensitive.

## Qualification notes

Two harness/environment corrections were made transparently:

1. The first synthetic API event used `qualification`, which is not in API's
   closed environment vocabulary. API correctly rejected it before capture
   began; the harness then used the production-valid `test` token.
2. A newly created system-site venv inherited the bundled base interpreter,
   not API's venv dependencies, and consequently lacked optional `jsonschema`.
   The decisive dependency check was rerun with the candidate installed site
   prepended to the actual API host interpreter and passed.

Neither correction changed SBE source, the candidate wheel, or capture behavior.

## Gate ruling

Slice 3 is complete and Review Gate B is open. No Alloy update is required:
these are non-authoritative observations only, with no lifecycle, authority,
selection, custody, packet, or transition-semantic change.

Before any release, freeze a fresh unused version and rerun the playbook's
release-bound qualification against that exact committed identity. Tag,
publication, deployment, and a live witness remain separately gated.
