# AstroWoof Natal Authoring 0.4.7 Known Limitations

- Provider acceptance and local provider-ID persistence cannot be made one atomic
  transaction. Identity-less interruption remains ambiguous and fail-closed.
- Deterministic request keys are not asserted as OpenAI idempotency guarantees.
- Six concurrent creates increase instantaneous rate pressure. API-owned global
  reservations, quotas, and circuit breakers remain authoritative controls.
- Provider retrieval remains independently capped at four due actions per short
  cycle, so a six-member wave may reconcile in two subwaves.
- Batch remains one paid round/API reservation with member-level evidence.
- Polish, qualitative critic, and qualitative candidate remain interactive
  Responses operations after Batch initial authoring.
- Missing Batch member usage retains consumer billing authority; SBE does not infer
  zero or partial final settlement.
- Unknown-time suppression, variable basis sizes, Quick/Complete modes, hierarchy
  redesign, and critic product policy remain deferred.
