# SBE 0.4.13 Known Limitations

- `execution_branch.action_ids` is SBE's bounded diagnostic selection, not API
  authority to choose members or construct provider calls.
- The API remains responsible for queueing, leases, capacity, reservations,
  quotas, billing reconciliation, and product state.
- A retained 0.4.12 workspace must be restored completely at its stable logical
  path and freshly inspected with 0.4.13. No native bytes may be manually blessed
  or rewritten.
- Provider submission ambiguity remains fail-closed and cannot be repaired by a
  deterministic local key.
- The installed qualification receipt is diagnostic evidence, never production
  execution or spend authority.
