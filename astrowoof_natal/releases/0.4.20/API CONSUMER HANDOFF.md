# API Consumer Handoff — SBE 0.4.20

The complete contract and invocation guidance is published in:

- `docs/sprints/2026/08/20260824-external-authority-v2-execution-bridge-sprint1/EXTERNAL AUTHORITY V2 EXECUTION CONSUMER HANDOFF.md`
- the packaged contract catalog;
- the packaged v2 schemas and fixture; and
- `astrowoof-external-authority-v2-qa`.

API supplies the exact validated request, closed v2 grant, and ordered complete
authorization documents. SBE revalidates current native truth under its writer,
publishes the complete intent checkpoint, performs create-only provider I/O outside
the writer, and leaves response observation to reconciliation.

Ordinary v2 Batch dispatch is deliberately deferred. Do not send a Batch ordinary
action to this executor or reinterpret it as Response transport. Existing v1
initial-wave Batch and provider-bound Batch reconciliation remain unchanged.
