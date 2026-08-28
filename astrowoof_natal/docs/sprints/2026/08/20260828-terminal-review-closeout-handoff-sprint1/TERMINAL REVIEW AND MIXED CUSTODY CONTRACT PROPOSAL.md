# Terminal Review and Mixed Custody Contract Proposal

Status: Slice 1 implementation candidate; API schema/authority review required
before runtime integration.

## Decision

`astrowoof.native_execution_result.v0.1` remains historical and readable. It is
not sufficient for a terminal-review handoff because its action IDs and provider
operations are not strictly joined.

Terminal review uses the fresh closed identity
`astrowoof.native_execution_result.v0.2`. In this first version, v0.2 is
deliberately limited to `outcome=review_required`. Other native outcomes continue
to use v0.1 until separately evolved.

## Exact invocation correlation

The worker must ingest the explicit `result_id` and `receipt_id` returned by the
invocation it launched. `latest` is discovery only and is never command
correlation. The v0.2 result and v0.1 receipt join on run ID, native invocation ID,
result ID/digest, and journal-range digest.

Slice 2 will return a closed command-result envelope on stdout before exit 2. That
envelope carries the exact native invocation ID, result ID/digest, receipt
ID/digest, and outcome produced by that invocation. The worker validates and
ingests those explicit identities before interpreting exit 2. It must not replace
them with the result index's latest member.

The publication receipt deliberately remains
`astrowoof.native_publication_receipt.v0.1`. Its canonical validator supports both
v0.1 execution results and the review-only v0.2 result, while preserving its exact
closed shape. Compatibility is explicit and tested; it is not inferred from a
partial helper check.

## Ordered action disposition

Every ledger action appears exactly once in native ledger order. Each row binds:

- canonical action ID and ordinal;
- digest of the complete public authorization binding;
- stage, route, route family, and provider mechanism;
- exact native action state;
- provider identity/status where durable;
- consumption, reporting, and provider-usage presence;
- one closed custody disposition; and
- immutable providerless-denial evidence digest when applicable.

The complete ordered list is bound by `action_inventory_sha256`.

`binding_sha256` is not standalone authority. During ingress, API must join each
row to its persisted immutable native run/action identity and complete
authorization binding, recompute the binding digest, verify route and stage, and
match any durable provider operation it already records. SBE exposes
`validate_terminal_review_result_v02_against_api_actions()` for this exact join.

## Editorial terminality versus custody finality

`review_required` ends editorial execution. It does not erase provider custody or
API financial authority. `custody_finality` is one of:

- `final`;
- `provider_reconciliation_required`;
- `providerless_denial_required`;
- `mixed_resolution_required`; or
- `ambiguity_review_required`.

`reconciliation_action_ids` and `providerless_denial_action_ids` are exact ordered
subsets derived from the action rows. API never chooses reconciliation members;
it invokes the supported SBE run-level reconciliation command. A providerless API
reservation is releasable only from the existing supported denial result, never
from terminal publication alone.

Every v0.2 result states `new_provider_create_permitted=false`. Reconciliation of
a durable provider identity is GET-only custody observation, not new creation.

When `custody_finality != final`, the outer API run is **review-required with
retained custody**, not generically closed or failed. Only the listed SBE-selected
reconciliation and exact providerless-denial continuations are permitted. The API
must not re-enable authoring, creative retry, polish, critic, candidate generation,
or any provider create.

## Closed custody mapping

| Native evidence | Custody disposition | Supported follow-up |
| --- | --- | --- |
| `PROVIDER_ID_RECORDED` / `WAITING` with durable ID | `provider_reconciliation_only` | SBE-selected run-level retrieval |
| `PREPARED` / `AUTHORIZED` without provider ID | `providerless_denial_only` | Existing exact denial contract |
| `SUBMITTING` / ambiguous submission | `ambiguity_review_only` | Review only; never create/retry |
| reported, denied, skipped, exhausted | `terminally_accounted` | None |

## Ownership

SBE asserts native facts only. It does not assert API reservation release,
capacity, lease, billing settlement, or publication policy. API ingests and joins
the exact sealed result, then applies its own transaction and resource policy.

## Historical retained finding

The hash-valid Pippin and Duchess active checkpoint archives contain no
`review_required` result. Their latest sealed results are
`ordinary_authoring/provider_pending`. This proves a live-route publication gap
alongside the independently identified API ordinary-resume ingestion gap. The
retained workspaces remain evidence and are not repair fixtures.
