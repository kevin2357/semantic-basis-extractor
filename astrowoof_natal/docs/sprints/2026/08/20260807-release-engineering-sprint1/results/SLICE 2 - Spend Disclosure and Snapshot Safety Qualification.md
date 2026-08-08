# Slice 2 — Spend, Disclosure, and Snapshot Safety Qualification

## Result

Slice 2 deterministic qualification passes and awaits gate approval. No live
provider request, package-coordinate change, build, tag, or publication
occurred.

## Paid-route and persistence matrix

The prepare/authorize/execute seam was exercised for interactive initial
authoring, Batch initial authoring, creative retry, polish, qualitative critic,
and qualitative candidate. Every prepared action binds the exact run, frozen
profile digest, state revision, stage, route, request digest, model, service
level, maximum output, conservative commitment, and versioned price book.

Regression coverage confirms preparation durability, exact authorization
matching, single-writer consumption, pre-creation submission persistence,
machine-distinguishable ambiguity when provider-ID persistence fails, separate
reported estimates and commitments, append-only reconciliation references,
and zero new commitment when polling known provider work.

Optional-stage exhaustion remains generation-profile-driven, while required
work becomes hard `BUDGET_EXHAUSTED`. Creative retry is a separate paid stage.
Legacy paid runs without the durable ledger remain fail closed.

## Provider atomicity qualification

SBE claims no provider/local transaction and no exactly-once creation
guarantee. Available provider documentation does not establish a transaction
joining creation to SBE persistence, an exactly-once/retention guarantee for
`Idempotency-Key`, or idempotent Batch creation. Deterministic Response keys
are request identity only. An ambiguous creation is never automatically
replayed.

## Provider disclosure

Interactive and Batch authoring, including creative retries, share the
protected-field-stripping Markdown renderer. Polish, qualitative critic, and
candidate use minimized subject transports. Tests seed birth date/datetime,
coordinates, location, and precision and prove they do not enter provider
payloads. Full values remain in protected local provenance. No editorial
exception is declared for this release.

## Durable snapshot matrix

Restoration at the original stable logical absolute path validates. Missing,
changed, additional, truncated, and relocated workspaces fail closed against
the complete hashed inventory before provider work. Concurrent worker saves
remain atomic; only the quiescent coordinator attests the complete snapshot.

## Verification

- focused spend and snapshot regressions: 14 passed;
- complete repository suite: 140 passed;
- `git diff --check`: pass;
- machine-readable matrix: `slice2-safety-matrix.json`.

This qualifies SBE per-run enforcement only. Transactional cross-run
reservations, account quotas, circuit breakers, entitlements, authoritative
billing, and billing reconciliation remain AstroWoof API-owned.
