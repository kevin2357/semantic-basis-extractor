# SBE 0.4.27 API Consumer Handoff

## Command and authority routing

| Native evidence | SBE-selected command | API posture |
|---|---|---|
| Provider action due | `provider_reconciliation_cycle` | Invoke only the run-level command; SBE selects the bounded subset. |
| Completed provider evidence, remaining custody not due | `ordinary_resume` | Retain provider authority; allow the exact local fan-in operation. |
| Co-ready prepared successors after custody clears | `await_external_authority` | Validate the exact v2 request and issue one all-or-none aggregate grant if API policy permits. |
| Dispatched successor operations | `provider_reconciliation_cycle` | Release worker capacity until due; retain per-action custody/reservations. |
| Review, ambiguity, contradiction, or unsupported evidence | `none` | Fail closed and retain the relevant API authority for review. |

API must not select reconciliation members, reconstruct native action inventory,
or synthesize request/grant documents from private workspace bytes.

## Aggregate ordinary-v2 authority

One `ordinary_action_set` may contain multiple co-ready successor actions. It is
one admission envelope, not one paid action. Every member keeps its own:

- native action ID and exact binding;
- API reservation/admission record;
- authorization document and document digest; and
- ordered grant member.

The aggregate grant remains all-or-none. Exact replay performs no new create.

## Public qualification artifacts

Use the installed public Python readers/validators or:

`astrowoof-ordinary-v2-happy-path-qa`

The receipt and bundle are closed and canonically joined. Their evidence scope is
`post_fan_in_selector_authority_and_replay`; consumers must not promote them into
proof of upstream provider-result evaluation, QA acceptance, natural successor
generation, or product-policy selection.

## Capacity and ownership

SBE owns native state, checkpoint validity, lifecycle selection, provider identity,
local-operation identity/consumption, and constrained dispatch. API owns leases,
worker capacity, global spend admission, reservations, billing, product policy,
PostgreSQL/R2 persistence, and publication.

Logs and qualification artifacts remain diagnostic/evidentiary. Neither is runtime
authority.
