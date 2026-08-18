# SBE 0.4.5 API Consumer Handoff

Use the public explicit-result reader:

```python
from astrowoof_natal_authoring import read_native_transition_result

view = read_native_transition_result(run_dir, result_id)
```

The returned `{result, journal_range, receipt}` envelope is exposed only after SBE
validates the restored workspace, historical checkpoint basis, bounded journal
range, immutable result, complete snapshot, and publication receipt together.

The provider-free CLI equivalent is:

```text
astrowoof-native-transition --run-dir RUN --result-id RESULT_ID
```

`--latest` is discovery only. Re-read the explicit result ID before persistence.
Any `--output` path must resolve outside `--run-dir`.

In one API-owned transaction, persist the exact native evidence, provider-operation
projections, and terminal disposition before generic subprocess-exit fallback.
Bind replay to `(run_id, result_id, journal_range.range_sha256)` and the complete
canonical result/receipt hashes. Derive route/mechanism from native evidence, not
only the requested product job.

Retain the snapshot-excluded `native-publication-receipts/` namespace in durable
workspace capture. Missing usage remains unsettled and is never reported as zero.

Detailed adoption and limitations are documented in:

- `docs/sprints/2026/08/20260817-native-terminal-transition-journal-sprint1/FINAL API RESPONSE.md`;
- `docs/sprints/2026/08/20260817-native-terminal-transition-journal-sprint1/NATIVE TRANSITION CONSUMER HANDOFF.md`;
- `docs/post_extraction_authoring/Authoring Lifecycle Consumer Handoff.md`;
- the packaged contract catalog and native-transition schemas; and
- packaged fixture `consumer-ingestion-cases.v0.1.json`.

SBE owns native state, provider identities, journal/result/snapshot/receipt
integrity, and local continuation. The API owns leases, capacity, reservations,
global spend, billing reconciliation, PostgreSQL/R2 authority, and publication
policy.
