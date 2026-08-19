# SBE 0.4.10 Known Limitations

- The diagnostic probe is a read-only QA tool, not a health check or lifecycle
  transition command.
- Successful process exit does not mean the provider Response completed
  successfully; inspect the closed diagnostic outcome and provider status.
- HTTP status/request ID are present only when the supported transport exposes
  them.
- Sanitized operational diagnostics cannot establish provider nonexistence,
  authorize retry, settle billing, or release API authority.
- This patch instruments interactive Response retrieval. It does not redesign
  Batch retrieval diagnostics.
- No live-provider qualification was performed for this observability-only patch.

