# SBE 0.4.11 Known Limitations

- Log text and the default formatter are operational conveniences, not stable
  machine-readable contracts.
- SBE logs native scheduling/custody facts but does not claim ownership of API
  worker leases, reservations, billing, or product state.
- INFO is intentionally useful and may be verbose during multi-pass authoring;
  deployments may select WARNING or install their own handler/formatter.
- No live-provider qualification was performed for this logging-only patch.
