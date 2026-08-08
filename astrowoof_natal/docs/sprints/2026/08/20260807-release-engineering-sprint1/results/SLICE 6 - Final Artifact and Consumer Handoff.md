# Slice 6 - Final Artifact and Consumer Handoff

Status: complete; gate approval pending.

## Final candidate

The approved Slice 5 source commit is
`0f22676410f2c8de83587b55a8b477c0295cc24b`. Two builds used its commit epoch,
`SOURCE_DATE_EPOCH=1786164056`, and produced byte-identical wheels:

- `astrowoof_natal_authoring-0.2.0-py3-none-any.whl`
- 623,777 bytes; 40 entries; no bytecode/cache entries
- SHA-256 `cbc8e82da546c1dd4a13a60544f31c5627365167c8c7c48f3114b5fd1f4c03e4`

The exact wheel was installed without dependencies into a fresh environment.
Its installed release smoke passed from site-packages and verified the UUID
identity path, exact AGF 0.6/SPC 0.10 wheel identities, 50 cards, four
summaries, manifest hashes, 19 packaged resources, and deterministic cleanup.
All 144 repository tests remain green.

## Handoff bundle

`astrowoof_natal/releases/0.2.0/` contains:

- candidate release manifest;
- SHA-256 checksum and hash-pinned API-worker requirement;
- compatibility declaration and release notes; and
- API worker installation, authorization, resume, reconciliation, status,
  snapshot, promotion, and ownership guidance.

All files agree on version 0.2.0, proposed tag
`astrowoof-natal-authoring-v0.2.0`, artifact filename/size/hash, source commit,
Python boundary, resource identity, contract versions, price-book behavior,
and AGF/SPC tuple. Publication fields remain deliberately unset.

## Ownership and guarantees

SBE owns the frozen per-run ledger, exact authorization binding, single-writer
consumption, provider-ID resume behavior, local committed/reported accounting,
append-only reconciliation references, minimized disclosure, snapshots,
acceptance, provenance, QA, and delivery construction.

The API retains transactional reservations across runs, user/account quotas,
global circuit breakers, product entitlements and critic policy, authoritative
billing reconciliation, queues/leases, storage, and promotion decisions. The
handoff explicitly documents the provider atomicity gap and does not represent
deterministic request keys as proof of OpenAI idempotency.

## Gate

The artifact and consumer handoff are ready for review. No tag, publication,
push, release asset upload, or authenticated download has occurred. Those
actions remain Slice 7 and require explicit approval.
