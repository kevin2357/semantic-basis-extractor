# Compatibility — SBE 0.4.25

- Python: `>=3.11`
- Direct dependency: `semantic-projection-core==0.11.1`
- Lifecycle inspection v0.5: unchanged and readable
- Temporal lifecycle v0.6: unchanged and readable
- New post-fan-in lifecycle inspection: v0.7
- New local-work inventory: `astrowoof.local_work_inventory.v1`
- New installed qualification: `astrowoof.provider_pending_lifecycle_qualification.v2`
- Historical provider-pending qualification v1: unchanged
- External-authority, initial-wave, Batch, spend, custody, and delivery contracts:
  unchanged

Consumers lacking v0.7 support must fail closed at concrete local-work boundaries;
they must not reinterpret v0.5/v0.6 ordinary continuation as equivalent evidence.
