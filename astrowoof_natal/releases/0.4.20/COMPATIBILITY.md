# Compatibility — SBE 0.4.20

- Python: `>=3.11`
- Direct dependency: `semantic-projection-core==0.11.0`
- Existing v1 initial-wave exact/bounded interactive and Batch contracts: preserved
- Temporal lifecycle v0.6 and external-authority request v2: preserved and now
  paired with the constrained execution bridge
- Legacy lifecycle versions: fail closed where v2 authority is required
