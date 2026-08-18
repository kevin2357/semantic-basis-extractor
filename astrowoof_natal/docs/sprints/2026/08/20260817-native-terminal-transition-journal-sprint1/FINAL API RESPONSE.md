# Final API Response — Native Terminal Transition Journal

Date: 2026-08-17
Status: accepted; 0.4.5 published
Recommended release: `astrowoof-natal-authoring` 0.4.5

## Delivered SBE boundary

SBE now publishes native execution truth as a validated journal range, immutable
command result, complete workspace snapshot, and content-addressed publication
receipt. The public reader exposes an exact result only when those artifacts and
their hashes validate together.

The supported consumer boundary is:

```python
read_native_transition_result(run_dir, result_id)
```

The equivalent provider-free CLI is:

```text
astrowoof-native-transition --run-dir RUN --result-id RESULT_ID
```

`--latest` is discovery only. API persistence must re-read the explicit result ID.
CLI output may be written only outside the resolved native run directory.

## API adoption checklist

1. Pin the eventual 0.4.5 wheel and published SHA-256; reject older runtime
   contracts for this ingestion path.
2. Discover a result ID, then call the explicit reader and validate the complete
   `{result, journal_range, receipt}` envelope.
3. In one PostgreSQL transaction, persist the exact native result, bounded journal
   evidence, receipt, provider-operation projections, and terminal disposition.
4. Bind replay to `(run_id, result_id, journal_range.range_sha256)` plus complete
   canonical result and receipt hashes.
5. Derive route/mechanism from validated native evidence, never only from the API
   job request.
6. Preserve unsettled financial authority when usage is unavailable; never map
   absent usage to reported zero cost.
7. Apply terminal-first state before generic subprocess-exit fallback. Exit codes,
   stderr, logs, and events are not transition authority.
8. Retain the complete workspace and snapshot-excluded
   `native-publication-receipts/` namespace in durable storage before deleting
   worker scratch.
9. On any validation or database failure, commit no API transition and retain the
   native workspace for exact replay or review.
10. Keep reservations, quotas, circuit breakers, entitlements, capacity, billing,
    publication policy, PostgreSQL, and R2 ownership in the API.

## Compatibility and route boundary

- Exact Natal Responses: supported.
- Exact Natal Batch: supported.
- Bounded-Natal Responses: supported.
- Bounded-Natal Batch: explicitly unsupported and fail-closed.
- Stable logical absolute workspace restoration remains required.
- The consumer matrix covers delivery, review, provider failure, pending custody,
  ambiguity, conflicting-operation review, replay, and malformed refusal.

## Irreducible limitations

- Provider submission and local identity persistence cannot be made one atomic
  transaction with the provider. If submission may have occurred but no provider
  identity is durable, SBE reports ambiguity and forbids blind resubmission.
- Publication is an atomic validation protocol, not literal multi-file filesystem
  atomicity. Result visibility requires a validating journal range, snapshot,
  hashes, and later-written receipt. Interrupted partial publication fails closed;
  only exact provenance-bound orphan repair is supported.
- The receipt namespace is intentionally outside the native snapshot inventory to
  avoid a hash cycle. API durable capture must include it explicitly.
- SBE cannot prove API transaction, lease, capacity, PostgreSQL, R2, billing, or
  public-state behavior. Those claims remain in API Sprint 26.
- Historical Aster evidence is retained for diagnosis and is not retroactively
  rewritten into the new contract.

## Qualification summary

- Complete source suite: 383 passed, 4 expected skips.
- Windows and Linux Python 3.11 installed smokes: passed.
- Two fixed-epoch candidate builds: byte-identical.
- API validator parity: seven valid/replay/review cases accepted; malformed native
  identity refused.
- Provider operations: 0.
- Paid spend: `$0`.

The SBE-native implementation is published as pinnable 0.4.5. Wheel SHA-256 is
`9b5f1ce0336c791ec4fde906ccd2e8deeac3abc6bc9eac49e94f2c7ea62e71b4`.
