# SBE 0.4.14 API Consumer Handoff

Use lifecycle inspection v0.5 as the sole next-action authority projection.

- `external_authority_request` and `external_authority_refusal` are mutually
  exclusive closed objects.
- For `initial_wave_admission`, reserve/authorize the exact ordered six-action set
  atomically in API authority, then supply the complete aggregate grant and six
  ordinary authorization documents.
- Persist authority documents outside the native workspace.
- Invoke only the route-specific constrained command selected by the contract.
- Ingest the resulting native checkpoint before changing API lease/capacity state.
- Once provider IDs exist, invoke only the run-level provider-reconciliation cycle;
  SBE selects the bounded due subset.
- Never treat generic resume, logs, response IDs, private `run.json`, or packets as
  create authority.
- `initial_wave_lineage_unjoinable` is a native review refusal, not permission to
  reconstruct or create another wave.

Installed provider-free qualification:

```text
astrowoof-external-authority-qa --output receipt.json --fixtures-dir fixtures
```

The receipt is qualification evidence only. It is not native execution authority,
an API reservation, or billing evidence.

Detailed sequencing and ownership are in the Sprint 1
`EXTERNAL AUTHORITY CONSUMER HANDOFF.md`.
