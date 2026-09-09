# Slice 1ε.1 — positive fixtures and deterministic qualification

## Result

Complete. The executable contract now has two separate package-owned,
provider-free, privacy-safe positive worlds:

| Fixture | Packet events | Artifacts | Canonical gzip bytes | Fixture SHA-256 |
| --- | ---: | ---: | ---: | --- |
| accepted delivery | 12 | 18 | 8,147 | `395b4fd8750ba7f978bb06c35301e76dc600790ede4e9bfe6e6b0ab623fa5765` |
| editorial closeout | 14 | 17 | 8,816 | `0b8959fb09a5e78884932d7c6c6083a6f475372fff1300b4e50c3ac2255ac0c8` |

These are invented content and identities. They contain no retained-run data,
prompt, credential, provider request body, endpoint, or attributable user data.

## Positive topology

Both fixtures contain exactly six initial-pass decisions without a false
predecessor chain. The accepted fixture then exercises creative-retry adoption
and a later polish decision; its selected deck is exactly its delivered deck.
The closeout fixture exercises both non-materialization and a later
materialized-but-not-adopted polish candidate; it selects a retained deck but
does not fabricate delivery.

Together they cover exact action/binding/Response identities, contiguous deck
evolution, both validation owner classes, advisory and rejecting evidence, all
three population modes, one projection per native member, and packet-scoped
deck/Response artifacts.

Editorial evidence is independently complete: removing all artifact batches
does not alter editorial event bytes, and the public request validator still
returns `valid`. Artifacts are payload delivery, never hidden authority.

## Determinism and readers

The public surface constructs, strictly reads, and validates both bundles.
Fresh-process tests vary temporary directory, hash seed, and timezone. Bundle
bytes remain stable, transitively freezing native event bytes plus fixed
synthetic-envelope JSON/gzip expectations. Nothing claims identity with a
future live API observation envelope.

The semantic manifest now binds the closed fixture-bundle schema and has
SHA-256 `ff6e7d5548edf8ff94be191064070f0ebe6407987f0a68d94416df250e007a20`.

## Capture-status absence fixtures

Six typed `not_captured` objects cover ineligible route, unsupported result,
incomplete evidence, contradictory evidence, event-count overflow, and byte
overflow. Their closed shape has native correlations and a safe detail code,
but no packet/projection bytes, IDs, or digests.

## Verification

```text
Focused contract foundation + positive fixtures:
Ran 18 tests in 1.353s
OK (skipped=1)

Suite-manifest integrity:
Ran 16 tests in 0.614s
OK
```

## Next boundary

Slice 1ε.2 remains responsible for the rehashed mutation campaign,
no-side-effect fencing, compact qualification receipt, and API handoff. The
9 MiB safe compressed threshold remains explicitly deferred to Voof-paws 1ε;
it is not needed to accept these small positive fixtures.
