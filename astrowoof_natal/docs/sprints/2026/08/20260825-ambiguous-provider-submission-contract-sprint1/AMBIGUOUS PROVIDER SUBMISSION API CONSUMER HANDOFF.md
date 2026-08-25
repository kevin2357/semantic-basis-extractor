# Ambiguous Provider Submission — API Consumer Handoff

Status: Scenic Waypoint 3 candidate; API fixture review pending

## Supported public pair

Consumers must validate the complete pair exposed by the pinned SBE release:

- `astrowoof.external_authority_provider_dispatch_result.v3`; and
- `astrowoof.external_authority_v2_command_result.v2`.

Use the packaged Python validators or the provider-free command:

```text
astrowoof-provider-dispatch-result --input command-result.json --output validated.json
astrowoof-provider-dispatch-result --packaged-fixtures --output fixtures.json
```

The command accepts no workspace, grant, credential, provider, URL, response ID,
or submission option. It performs validation/export only.

## Consumer decision table

| Native result | API interpretation |
|---|---|
| `pre_provider_refusal` / `not_attempted` | Release the exact provably unspent reservation(s) joined from the ordered invocation evidence; preserve the rejected grant audit. Any later work requires fresh inspection and authority. |
| `ambiguous_submission` / `create_entered_unknown` | Release execution capacity, retain ambiguity/review custody, and prohibit provider creation. |
| `detached_provider_pending` / `provider_identity_durable` | Release execution capacity and retain retrieval-only provider custody. |
| `exact_replay` | Apply no new capacity or authority transition. `provider_identity_durable` describes custody, not new replay I/O. |
| malformed or contradictory evidence | Fail closed and preserve relevant authority for review. |

For an aggregate refusal, `provider_bound_action_ids` is the exact ordered
provider-bound prefix and `refused_action_ids` contains the single causal member.
All following ordered members were provably unentered and the sealed old grant
cannot dispatch them. SBE archives their prior authorization evidence and makes
them eligible only through the supported fresh-inspection path. If a bound prefix
exists, reconciliation has native precedence before fresh authority is exposed.

## Authority boundary

SBE proves native request/grant/action/binding lineage, execution phase,
provider identity or ambiguity, state revision, and snapshot identity. The API
joins its own admission/reservation records and remains authoritative for global
spend policy, capacity, leases, product state, billing, and operator workflow.
SBE does not assert those API-global facts.

Pre-provider refusal is nonterminal and is not provider ambiguity. Ambiguity is
never an automatic retry. Provider-pending work is retrieval-only. Historical
v2 ambiguity cannot be reclassified from missing IDs, logs, or reconstructed
payloads.

Logs and events are diagnostic only. No prompt, payload, subject data,
credential, authorization header, or protected provenance belongs in the public
result or diagnostic fields.
