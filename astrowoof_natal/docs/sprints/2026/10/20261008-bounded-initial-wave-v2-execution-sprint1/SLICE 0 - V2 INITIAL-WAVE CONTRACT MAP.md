# Slice 0 — v2 Initial-Wave Contract Map

## Finding

The QA failure is the intentional ordinary-only fence in the v2 adapter, not a
failed provider action or a missing bounded executor.

`temporal_lifecycle.build_external_authority_request_v2()` can represent
`initial_wave_admission` as a request kind, but its current request contains
only the run ID, checkpoint-basis digest, request kind, and ordered action IDs.
`external_authority_v2` subsequently imposes ordinary lexical ordering on the
grant, no-grant result, and grant validator. Finally,
`commit_external_authority_v2_dispatch_intent()` rejects every non-ordinary
request before it writes a v2 intent.

The legacy bounded route is materially richer. Its v1 reader requires exactly
six semantically ordered members and an `initial_wave` projection; its bounded
resume path validates that projection, constructs an aggregate wave envelope,
writes the constrained submit intent under the lifecycle lock, then invokes
the existing bounded initial-wave executor.

## Frozen design direction for Gate A

Introduce a separate v2 initial-wave branch; do not widen the ordinary branch.
The new branch must use:

| Concern | Ordinary v2 | Bounded initial-wave v2 |
| --- | --- | --- |
| Request kind | `ordinary_action_set` | `initial_wave_admission` |
| Ordering | lexical action IDs | six prepared members in canonical semantic order |
| Extra identity | action inventory / checkpoint | canonical initial-wave projection or its independently validated digest, plus bounded route contract |
| Execution | current generic v2 dispatch | shared bounded initial-wave execution helper after v2 intent validation |
| Grant replay | existing v2 semantics | one exact six-member authorization and one constrained initial-wave intent |

The v2 initial request must contain enough sealed information to validate the
semantic wave independently. A request-kind flag plus six action IDs is not
sufficient: it cannot distinguish an arbitrary reordered six-action inventory
from the prepared bounded initial wave. The contract should therefore carry a
canonical bounded `initial_wave` identity projection (or a projection digest
whose canonical source is included in the inspected checkpoint), the bounded
route contract, the exact semantic ordering marker, and the six ordered IDs.

The v2 grant must echo and hash that same identity. Its authorization documents
must join each ordered member's existing binding exactly; it must not issue new
prepared actions, reservations, or spend-policy decisions.

## Durable-state map

The reusable bounded v1 path establishes the required order:

1. Lock the workspace and validate snapshot/current authority request.
2. Validate the complete authority and all six member documents.
3. Verify the stored initial wave remains `AWAITING_SPEND_AUTHORIZATION`.
4. Construct/preflight the aggregate wave authorization.
5. Clone the ledger, authorize the exact six actions, and mark their
   submissions under the existing decision identity.
6. Store the aggregate authorization and one constrained submission intent.
7. Persist the state before any provider operation.
8. Execute the bounded initial-wave helper outside the lock.

The successor must preserve this ordering. The v2 adapter should validate its
own contract, then use a shared internal bounded-initial transition helper;
calling the v1 public resume function with fabricated documents would violate
the schema boundary and undermine immutable provenance.

## Compatibility disposition

The existing 0.4.71 QA witness has a sealed v1 request/grant and is terminal.
It is **not** a v2 migration fixture. The successor must provide a typed,
zero-provider-I/O refusal for a v1 authority presented to the new v2 route.

A future, explicitly designed sealed bridge record could be considered only if
it proves the original v1 request/grant and every member binding unchanged.
No such bridge is in scope. New bounded admissions under the successor profile
will receive new v2 initial-wave authority from API.

## Implementation seams

- `temporal_lifecycle.py`: request/inspection validation and the checkpoint
  authority projection need the new initial-wave identity shape.
- `external_authority_v2.py`: request-kind branch, grant schema/validation,
  no-grant result, and fixtures need separate semantic-order handling.
- `external_authority_v2_execution.py`: durable v2 initial intent must be
  distinct from ordinary intent and delegate to bounded logic only after its
  own validation.
- `bounded_lifecycle.py`: extract or expose a narrowly internal helper for the
  already-proven aggregate initial-wave transition; retain v1 behavior for its
  historical route unchanged.
- Profile/prompt catalogs: create a new immutable bounded successor identity;
  guidance bytes may remain identical, but an old immutable allowlist cannot be
  edited to admit a new profile.

## Qualification additions

In addition to the API handoff's requested cells, the implementation must
prove interruption/replay at the durable intent boundary and after each
provider member identity has been stored. A six-member wave cannot claim
exact-once behavior merely by testing a successful first call.

## Gate A request

API should confirm this contract direction: new v2 initial-wave documents for
new successor runs only, no implicit v1 bridge, canonical six-member semantic
identity in both request and grant, and an immutable successor profile/context.
