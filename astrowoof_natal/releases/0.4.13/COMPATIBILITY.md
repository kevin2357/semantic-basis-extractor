# SBE 0.4.13 Compatibility

- Python: 3.11 or newer.
- Semantic Projection Core: exactly 0.11.0.
- Astrology Graph Foundry input boundary: 0.8.1 through the pinned SPC contract.
- Exact and bounded Natal provider-reconciliation routes remain supported as in
  0.4.12.
- New production admission should require lifecycle inspection
  `astrowoof.authoring_lifecycle_inspection.v0.4`.
- Lifecycle inspection v0.3 remains packaged for historical reading, but does not
  carry the corrected closed command-selection evidence.
