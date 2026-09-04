# API review — Slice 1 explicit zero-action terminal contract

**Decision: approved to implement.**

The proposal correctly separates a fixture that has no action lineage from a
paid run whose ledger happens to be incomplete. The required present
`spend_ledger.actions: []` predicate is the right admission boundary: omitted,
null, malformed, or nonempty evidence must continue to refuse.

The closed v0.3 fields are sufficient for this fixture-only terminal result:

- `action_inventory_kind: explicit_zero_paid_actions`
- `paid_action_count: 0`
- `provider_operation_count: 0`
- `new_provider_create_permitted: false`

Please retain these implementation guardrails:

1. Keep `astrowoof.native_execution_result.v0.2` strict and unchanged for
   existing paid-action terminal lineage.
2. Do not route v0.3 through API's ordinary terminal-result consumer or ask API
   to infer the zero-action case. The SBE release smoke validates it directly;
   v0.2 readers should fail closed on the new schema.
3. Make the fixture's empty ledger explicit at its creation boundary, not by
   adding a late terminal-review special case for all absent ledgers.
4. Include a mutation proof that a one-action v0.2 state cannot produce v0.3,
   and that adding any provider/authorization/custody field to the v0.3 case is
   rejected.
5. Keep the Docker image smoke gates unchanged: both release smoke and deployed
   QA qualification remain required after the patch.

No API source change is needed before the corrected immutable SBE artifact is
released. API will admit that exact wheel and rerun its GHCR image build before
the already authorized QA reset/deployment proceeds.
