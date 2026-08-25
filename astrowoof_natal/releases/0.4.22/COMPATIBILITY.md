# Compatibility — SBE 0.4.22

- Python: `>=3.11`
- Direct dependency: `semantic-projection-core==0.11.1`
- Lifecycle inspection: v0.5, tightened in place
- Temporal lifecycle: v0.6, tightened in place
- Routes: exact Natal and bounded Natal
- Provider mechanisms: interactive Response and existing Batch reconciliation
- Retrieval subset: SBE-selected, ordered, maximum four per cycle
- API routing: unchanged; invoke only the SBE-selected run-level command

The compatibility change from SBE 0.4.21 is the exact SPC pin from 0.11.0 to
0.11.1. Published 0.4.21 metadata remains unchanged.
