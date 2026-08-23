# Compatibility — SBE 0.4.16

- Distribution: `astrowoof-natal-authoring==0.4.16`
- Python: 3.11 or newer
- Astrology Graph Foundry: 0.8.1
- Semantic Projection Core: 0.11.0
- Normal and bounded Natal authoring: supported
- Interactive and Batch provider mechanisms: supported
- Lifecycle inspection v0.6: supported through explicit temporal reader/API
- Lifecycle inspection v0.5: retained unchanged for existing consumers
- Legacy bounded-v1 Batch timing: fail closed

The API must deploy and attest the exact SBE wheel, worker image, compatibility
identities, and selected immutable generation profile before admitting new runs.

