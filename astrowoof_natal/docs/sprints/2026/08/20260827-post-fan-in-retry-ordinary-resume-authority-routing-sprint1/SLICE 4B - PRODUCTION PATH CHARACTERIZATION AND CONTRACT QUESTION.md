# Slice 4B — Production-Path Characterization and Contract Question

Status: characterization complete; API interpretation required before runtime and
fixture freeze.

## Mixed provider-completion finding

A provider-free production-shaped workspace was created with two distinct
interactive creative-retry actions. The action ordered first remained pending while
the later action returned completed evidence.

Native reconciliation correctly persisted both facts and returned
`progressed_local`. Lifecycle inspection then produced:

- capacity disposition `continue_local_cycle`;
- capacity reason `local_work_ready`;
- provider custody `known_operations_pending` containing both action IDs; but
- selected command `none` with reason `terminal_or_no_continuation`.

The local-work v0.7 adapter consequently had no command from which to derive the
completed-evidence fan-in operation. This is a real mixed-custody selector gap. The
narrow correction is for the native branch selector to choose `ordinary_resume`
when validated provider custody contains completed evidence, even if the older
local-dependency projection is empty. The v0.7 inventory then provides the concrete
SBE-selected semantic operation and retains the still-pending provider action.

## Authority topology after the correction

Existing provider-custody precedence prevents fresh paid authority from outranking
the other retained provider operation. Therefore the truthful sequence is:

1. later-ordered retry completes;
2. SBE selects and consumes that completed-evidence local operation;
3. its successor may become prepared, but no new provider dispatch is selected
   while the earlier retry remains provider-pending;
4. the earlier retry later completes and is consumed through its own distinct local
   operation; and
5. the prepared successors are exposed through the existing ordinary-v2 action-set
   boundary.

Each successor remains a distinct paid action with its own exact action ID, binding,
authorization document, and ordered grant member. Under the existing contract they
may be members of one aggregate `ordinary_action_set` request/grant rather than two
temporally separate request envelopes.

Forcing two separate request envelopes would require either allowing fresh authority
to outrank retained provider custody or artificially withholding one prepared
successor. Either would change the recently approved custody/authority model and is
not appropriate as an incidental qualification-fixture change.

## Requested API interpretation

Confirm that the Slice 4B phrase “each successor requires its own distinct ordinary
v2 authority request” is satisfied by distinct exact member/action authorization
inside one aggregate ordinary-v2 action-set request after both local operations are
consumed.

If separate temporal request envelopes are required instead, Slice 4B becomes a
contract/topology change and must explicitly revisit provider-custody precedence
before implementation.

## Downstream-stage characterization

Interactive polish is supported by ordinary external-authority v2, but a truthful
retry-to-polish witness must first complete the accepted-pass/final-assembly
prerequisites through normal exact-Natal orchestration. Slice 4B should use polish
only through that production path. It must not manufacture a prepared polish action
beside an incomplete retry workspace.

No provider network call, spend, or retained-QA access occurred during this
characterization.
