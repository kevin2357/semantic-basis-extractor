# Slice 5 Consumer Interfaces, Fixtures, and Handoff

Date: 2026-08-17
Status: complete; API fixture contract accepted

## Outcome

The API now has a packaged, route-neutral, provider-free ingestion boundary. It can
strictly ingest a specified immutable native result, bounded journal range, and
publication receipt without reading private run state, stderr, logs, or a mutable
latest index.

## Public interfaces

Python:

```python
from astrowoof_natal_authoring import read_native_transition_result
view = read_native_transition_result(run_dir, result_id)
```

CLI:

```text
astrowoof-native-transition --run-dir /stable/run --result-id nres_...
```

The typed view contains exactly `result`, `journal_range`, and `receipt` after full
native validation. `latest_native_transition_result()` and CLI `--latest` are
explicitly documented as derived conveniences, not ingestion authority.

CLI `--output` is permitted only when its resolved path is outside the resolved
native run directory. Equal and descendant paths fail during argument handling,
before result reading, directory creation, or file writing.

Tests hash every workspace file before and after explicit/latest CLI calls and
prove exact equality. A patched network entry point raises if provider access is
attempted.

## Packaged fixture matrix

`consumer-ingestion-cases.v0.1.json` contains:

- exact Response delivery;
- exact Response review;
- exact Batch provider failure;
- exact Response pending custody;
- bounded Response ambiguity;
- malformed-result refusal;
- exact replay; and
- conflicting second-operation refusal/review.

Accepted cases carry canonical record/result/receipt identities. The malformed
case intentionally violates result content identity. Fixtures contain no provider
credentials, tokens, birth data, or protected subject material.

## Handoff

`NATIVE TRANSITION CONSUMER HANDOFF.md` freezes:

- transactional API ingestion order;
- `(run_id, result_id, journal_range.range_sha256)` replay identity plus complete
  canonical hash comparison;
- monotonic journal cursor behavior;
- route, outcome, custody, and unsettled-cost mapping;
- API ownership of reservations, quotas, capacity, billing, and publication;
- strict backwards refusal and stable-path requirements;
- R2 retention of the snapshot-excluded receipt namespace; and
- irreducible identity-less provider submission ambiguity.

## Events and smoke

`native.result_published` provides redacted non-authoritative observability with
result ID, receipt ID, and outcome. The native artifacts remain authoritative.

Source verification:

- 101 contract, route, consumer, event, and lifecycle tests passed in 44.459
  seconds.
- Source lifecycle smoke passed.
- Draft 2020-12 meta-schema and strict packaged fixture validation passed.

Installed verification:

- candidate wheel SHA-256:
  `baca8ae1cedb050d15ba2240406b34acd83707e857e31b8e5f03c8a2fc58b2dc`;
- installation loaded from an external `site-packages` directory;
- lifecycle smoke passed with packaged native schemas and fixtures;
- `py.typed` and the `astrowoof-native-transition` entry point were present; and
- explicit CLI export returned the expected result/receipt without changing any
  run bytes.

The isolated qualification tree was removed. Provider operations were zero and
paid spend was `$0`.

## Gate

API review accepted the fixture contract after the resolved-output boundary was
hardened and tested. Slice 6 joint qualification is authorized but has not begun.
