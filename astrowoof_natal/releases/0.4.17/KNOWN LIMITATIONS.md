# Known Limitations — SBE 0.4.17

- The retained-workspace bridge is retrieval-only; it cannot submit, recreate, or
  retry provider work.
- `review_required` intentionally carries no detailed refusal reason in the closed
  v0.2 result. The redacted typed event provides optional diagnostics only.
- A binding contradiction refuses the whole cycle; there is no member-local bypass.
- The patch does not prove that any particular retained workspace is eligible.
  Restore and validate the complete exact snapshot before an operator decision.
- The API continues to own leases, capacity, global spend authority, reservations,
  billing reconciliation, product policy, and retained-workspace custody.

