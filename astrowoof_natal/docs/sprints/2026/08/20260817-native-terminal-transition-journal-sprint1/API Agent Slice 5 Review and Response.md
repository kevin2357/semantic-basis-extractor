# API Agent Slice 5 Review and Response

Status: accepted after committed CLI read-only correction.

## Accepted boundary

The public Python surface is the correct API-worker boundary:

```python
read_native_transition_result(run_dir, result_id)
```

It returns the frozen `{result, journal_range, receipt}` envelope and validates the
current workspace, retained result/range, historical snapshot/basis, and publication
receipt before exposing it. The explicit result identity is correctly authoritative;
`latest_native_transition_result()` and CLI `--latest` are appropriately derived
discovery conveniences only. The API will use discovery only to obtain an ID and
will then read that exact result ID for validation/persistence.

The route-neutral fixture matrix, non-authoritative `native.result_published` event,
hand-off guidance, installed-wheel smoke, and provider-call sentinel are all aligned
with API Sprint 26. No API-side contract change is needed for exact Responses,
exact Batch, or bounded Responses; bounded Batch remains refused.

## Resolved correction: keep the CLI workspace-read-only

`astrowoof-native-transition` currently permits `--output` at an arbitrary path.
If that path is inside `--run-dir`, the declared inspection/export command can write
into the native workspace, which conflicts with the Slice 5 and handoff guarantee
that it performs no native mutation.

Implemented fix:

- reject an `--output` path that is equal to, or a descendant of, the resolved
  `--run-dir`; and
- add a test covering both the allowed external output case and the refused
  workspace-descendant case, with byte-for-byte workspace comparison.

Writing an explicit consumer-owned export outside the workspace is fine. The API
worker will use stdout/direct Python return rather than `--output`.

## API implementation note

The next API slice can now use this supported reader/CLI instead of parsing
`run.json`, stderr, or a mutable latest-result index. It will validate and persist
the exact returned envelope before generic command-exit fallback. Receipt parsing is
already implemented on the API side; provider-observation ingestion and terminal
job/lease disposition will be added atomically at that worker boundary.
