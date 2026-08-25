# Compatibility — SBE 0.4.19

- Python: `>=3.11`.
- Direct dependency: `semantic-projection-core==0.11.0`.
- Operator retirement v1 supports exact Natal only.
- Existing lifecycle, provider reconciliation, spend authorization, authoring,
  bounded-Natal, Batch, and delivery contracts remain unchanged.
- Consumers must use the packaged schemas and Python validators; unsupported routes
  and historical/contradictory workspaces fail closed.
