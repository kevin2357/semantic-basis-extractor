# AstroWoof Natal Authoring 0.4.5 Known Limitations

- Provider submission and local provider-ID persistence are not one atomic
  transaction. Identity-less interrupted submission remains ambiguous and forbids
  blind resubmission.
- Native publication is an atomic validation protocol, not literal multi-file
  filesystem atomicity. Partial writes fail closed; repair is limited to an exact
  provenance-bound orphan.
- Publication receipts are excluded narrowly from the snapshot inventory to avoid
  a hash cycle. Durable consumer capture must retain that namespace explicitly.
- Workspaces must be restored at their stable logical absolute path with every
  authoritative member present and unchanged.
- Bounded-Natal Batch is unsupported and rejected.
- SBE does not prove or own API transactionality, queues, leases, capacity,
  reservations, PostgreSQL/R2 persistence, billing reconciliation, or public-state
  publication.
- Historical Aster evidence remains forensic history and is not rewritten into the
  0.4.5 contract.
- Unknown-time claim suppression, variable basis sizes, Quick/Complete product
  policy, hierarchy redesign, and critic product policy remain deferred.
