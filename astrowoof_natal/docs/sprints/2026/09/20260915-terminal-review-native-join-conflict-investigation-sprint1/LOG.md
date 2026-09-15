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

## 2026-09-15 — Gate C approved

- API approved the narrow SBE correction and preserved the exact digest-domain
  boundary.
- Added API's qualification nuance: artifact assertions derive from each
  fixture's real action and distinct-deck inventory rather than assuming the
  delivery control's eleven rows.
- Froze one additional implementation fence: terminal disposition membership
  uses the projected digest, while packet decisions retain their existing
  complete-ledger binding digest and delivery bytes.

## 2026-09-15 — Slices 3–4 complete

- Added one shared terminal binding digest helper and used it in the producer,
  terminal/API validator, and both editorial-review disposition joins.
- Preserved complete-ledger binding digests in packet decisions and made no
  delivery-path or sealed-projection change.
- Added a manifest-registered realistic no-polish/two-polish regression with
  inventory-derived artifact assertions and strict negative cases.
- Focused qualification passed: 82 tests on Python 3.12; 36 tests with four
  expected skips on Python 3.11.
- Corrected public capture against the two retained witnesses now produces
  valid review packets with 9 and 11 inventory-derived artifacts respectively.
- Reached Gate D. No version bump, broad/package qualification, release,
  deployment, provider operation, or live witness occurred.
