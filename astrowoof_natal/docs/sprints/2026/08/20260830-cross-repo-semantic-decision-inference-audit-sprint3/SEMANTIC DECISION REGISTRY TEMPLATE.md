# Semantic decision registry template

One row represents one API decision. Split a call site into multiple rows when it
performs independently authorized actions—for example, native-result ingestion,
API terminalization, reservation release, lease release, and publication.

| Field | Required content |
|---|---|
| Registry ID | Stable audit identifier |
| API decision | Exact state change, command invocation, release, or returned disposition |
| API source | File, function, and relevant lines |
| Reachable routes/stages | Exact/bounded; interactive/Batch; initial/retry/polish/critic/candidate/closeout |
| Installed identity | SBE package version, wheel/compatibility identity, and API pin/deployment context |
| SBE artifact/version | Exact authoritative document schema and reader/validator |
| Required SBE facts | Exact fields and closed values |
| Positive permission | The explicit permission consumed; never merely an inventory/state proxy |
| Required identity joins | Run, action, binding, provider, invocation, result, receipt, snapshot, predecessor/successor |
| Required API-owned facts | Lease, reservation, admission, transaction, product policy, or settlement facts |
| Current implementation | Actual predicate/helper and persistence order |
| Proxy/inference used | Status word, `sealed`, exit code, presence, emptiness, null, negation, default, or none |
| Evidence precedence | Exact invocation result, recovery discovery, exit code, logs/events |
| Absent evidence outcome | Typed result and retained authority/custody posture |
| Contradictory evidence outcome | Typed review/refusal and mutation prohibition |
| Unknown-version outcome | Typed unsupported/review posture |
| Replay/concurrency fence | Idempotency identity and duplicate-invocation prevention |
| Expected tests | Positive, negative, mutation, replay, crash-seam, and installed-wheel fixtures |
| Finding class | API mapper / SBE gap / join gap / docs / historical / safe |
| Severity | Paid-work, authority, capacity, terminal, delivery, accounting, or diagnostics impact |
| Correction owner | API, SBE, or joint |
| Evidence links | Source, schema, fixture, test, incident, and review references |

## Mandatory split examples

The following must never be compressed into one row:

- validate and persist a native terminal result;
- mark the API job/run/reading terminal;
- release a worker lease or capacity slot;
- release a provider reservation or consumer authority;
- settle provider/API billing; and
- publish or expose reader delivery.

Likewise, provider retrieval and provider creation are separate decisions with
different positive permissions.

## Evidence precedence template

```text
exact invocation-returned result ID
  → validate exact result + receipt + snapshot/journal joins
  → consume typed outcome
  → use exit code only as transport/process diagnostic

no exact returned result ID
  → only a named recovery/preflight path may use availability discovery
  → validate availability + discovered exact result + receipt + joins
  → discovery alone performs no transition
```

