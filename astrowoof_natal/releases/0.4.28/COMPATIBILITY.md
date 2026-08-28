# SBE 0.4.28 Compatibility

- Python: 3.11 or newer.
- Semantic Projection Core: exactly 0.11.1.
- Exact Natal interactive Responses: terminal-review v0.2 handoff supported and
  release-qualified.
- Exact Natal Batch and both bounded-Natal mechanisms: unchanged; they remain on
  their existing result behavior and must not be inferred to emit the new
  exact-interactive handoff.
- Native publication receipt remains canonical v0.1 and validates both historical
  execution result v0.1 and terminal-review result v0.2 through the supported
  joined validator.
- Historical result v0.1 remains readable but cannot validate or masquerade as
  terminal-review result v0.2.
- Lifecycle v0.5/v0.7, temporal v0.6, external-authority, provider-spend,
  accounting, denial, and closeout contracts remain otherwise compatible.
