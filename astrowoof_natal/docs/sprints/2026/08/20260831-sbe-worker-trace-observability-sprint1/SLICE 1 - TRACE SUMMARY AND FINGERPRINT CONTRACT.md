# Slice 1 — Trace summary and fingerprint contract

The internal diagnostic vocabulary has four records:

1. `workspace_fingerprint` — emitted only after snapshot validation.
2. `native_state_summary` — bounded counts and safe action/provider identities.
3. `native_decision_summary` — a validated public artifact's schema, command,
   outcome, reason, and returned identities.
4. `command_exit` — command name, code, typed outcome/reason, and authoritative
   output location semantics.

All records are deterministic JSON embedded in the existing `✨🐶` Python log
format. Inventory lists are sorted, capped, and paired with total/overflow
counts. Unknown values remain absent/unknown rather than being turned into
false or zero.

The helper is diagnostic and best effort: formatter/logger/sink failure cannot
alter state, returned bytes, provider behavior, or exit code. It rejects unsafe
keys and never includes prompts, provider payloads/bodies, complete bindings,
authorization documents, credentials, subject data, or private absolute paths.
