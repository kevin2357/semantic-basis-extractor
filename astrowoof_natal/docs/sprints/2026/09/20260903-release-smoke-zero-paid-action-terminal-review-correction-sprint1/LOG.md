# Log

- 2026-09-03: Sprint created from API GHCR build failure `33834841337`.
  No retained-QA, provider, deployment, or release action has occurred in this
  companion sprint.
- 2026-09-03: Slice 0 reproduced the installed 0.4.42 smoke path locally with
  no provider I/O. The fixture reaches `FINAL_QA_FAILED` and records the
  expected terminal transition, then fails in `build_terminal_action_dispositions`.
  Its state omits `spend_ledger` entirely rather than declaring `actions: []`.
  This is the exact fixture/contract seam: a future zero-action path must be
  explicit and versioned; the existing paid-action contract remains strict.
- 2026-09-03: API approved the v0.3 explicit-zero-paid-actions contract. SBE
  implemented it as a sibling of strict paid-action v0.2, with a matching v0.2
  command envelope. The smoke explicitly creates `spend_ledger.actions: []`
  before resume; omitted/null/malformed/nonempty inventory remains refused.
  A source provider-free smoke sealed and read a v0.3 result/receipt with zero
  provider operations. Slice 2 packaged/installed qualification is next.
- 2026-09-03: Slice 2 installed a disposable candidate wheel under fresh
  `site-packages`, verified both new schema resources, and ran the real
  provider-free release-smoke command with `--require-installed`. It passed
  with an explicit v0.3 zero-action terminal result and receipt. No provider,
  network, R2, retained-QA, or production run activity occurred.
- 2026-09-03: Prepared fresh `0.4.43` candidate wheel
  `ccf8c3ad0035f345cc8ccf6ad0182913b7a1f23f00179cdfa2e0beaace1003b6`.
  Focused terminal/native/smoke suite passed (36 tests, 3 expected optional
  schema skips). The candidate remains uncommitted and unpublished pending
  final release review.
- 2026-09-03: Committed source as `b2c2296`, then rebuilt `0.4.43` twice with
  byte-identical SHA-256
  `6249a0daaee01daa067c4f0c0136bfdc4983ab0294e2ae4b1266e21b8252c894`.
  The final wheel passed the public provider-free installed smoke from fresh
  `site-packages`. Awaiting owner authorization for the release record, tag,
  publication, and push.
