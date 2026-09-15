# Log

## 2026-09-15 — Sprint opened

- API supplied two hash-pinned terminal-review checkpoint packets.
- Owner granted one conditional HEAD and one bounded GET for each named object.
- No R2 access, runtime changes, or other mutation has occurred in this sprint.

## 2026-09-15 — Slice 0 complete

- Mapped every capture path that can return `native_join_conflict` before
  packet construction.
- Isolated a review-only leading candidate: the v0.2 producer hashes a closed
  terminal binding projection, while capture recomputes from the complete
  ledger binding.
- Recorded the finite retained comparison matrix and synthetic-test gap.
- Passed Gate A without retained access or runtime changes.

## 2026-09-15 — Slice 1 exact retained proof

- Performed exactly one HEAD and one ETag-bound bounded GET for each named
  checkpoint. Both archive sizes and SHA-256s matched; the access budget is
  consumed.
- Verified 922 and 934 workspace members respectively against the two canonical
  inventory digests, then extracted read-only copies outside Git.
- Ran each exact public reader in a network-disabled container at its original
  logical root. All top-level result/receipt/checkpoint joins and both retained
  initial-deck digests pass.
- All 15 sealed action digests equal the producer projection; none equals the
  complete ledger binding digest. Both public collectors reproduce
  `contradictory_native_evidence` at the first review-only action join.

## 2026-09-15 — Slice 2 reproduction and Gate C

- Added and ran a provider-free realistic-binding reproduction: 2 tests passed.
- Froze the correction boundary around one shared canonical terminal binding
  projection/digest and retained all exact/fail-closed identity checks.
- Ruled out an Alloy update because no modeled semantic transition changes.
- Investigation complete; paused at Gate C before runtime implementation,
  versioning, package work, release, deployment, or live witness.
