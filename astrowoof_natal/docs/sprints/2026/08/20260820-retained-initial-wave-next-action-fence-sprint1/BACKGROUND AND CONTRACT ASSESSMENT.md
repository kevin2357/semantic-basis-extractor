# Background and Contract Assessment

## Incident summary

AstroWoof API Sprint 32 granted one audited recovery attempt to a retained Aster
job. The API already held one immutable initial-wave authority and six original
provider-operation records. SBE's retained workspace nevertheless entered its
fresh exact-interactive wave path, prepared a distinct six-action inventory, and
created six new OpenAI Responses. The API correctly rejected the incompatible
native publication and did not invent database provenance for those calls, but that
post-publication rejection occurred after the external side effect.

API Sprint 33 now refuses this shape before invoking native resume. Its request to
SBE is intentionally narrower and more durable: publish the exact external-authority
request SBE intends to consume, then require the continuation command to bind to it.

## Current SBE behavior

SBE 0.4.13 improved provider-pending command selection through lifecycle inspection
v0.4. That work does not solve external-authority admission:

- `_execution_branch()` selects `await_external_authority` but returns an empty
  `action_ids` list;
- inspection therefore cannot expose an exact consumable action/wave inventory;
- existing prepared-wave and binding-bundle readers cover fresh initial-wave
  authority input, but they are not a general lifecycle next-action contract;
- generic resume is not bound to an inspection/request digest;
- the exact-interactive routing condition treats either a stored wave **or all
  passes with no attempts** as initial-wave mode;
- `prepare_exact_interactive_initial_wave()` returns a stored wave when present,
  but when absent it can prepare a new wave from pass state without first proving
  that no historical initial-wave spend/provider lineage exists.

The API cannot safely close this gap by reading private `run.json`. It needs an SBE
public artifact and native execution fence.

## Existing contracts to reuse

The patch should compose rather than replace:

- lifecycle inspection v0.4 branch/capacity/custody evidence;
- prepared initial-wave v1;
- initial-wave binding bundle v1;
- initial-wave authority inputs v1;
- wave authorization v1 and six ordinary spend authorizations;
- spend-ledger prepare/authorize/consume state transitions;
- workspace snapshot, logical-root, and single-writer invariants;
- provider reconciliation's distinct retrieval-only command;
- native transition publication and immutable receipt protocol.

The missing layer is a route-neutral, lifecycle-owned request saying: “at this
validated snapshot, these are the only native actions this external-authority
continuation may consume.”

## Recommended approach

Add lifecycle inspection v0.5 with the complete closed external-authority request
embedded inline. Include
complete public action bindings rather than digests alone: the API must validate and
persist exact bindings and issue ordinary authorization documents without reading
private state. Each binding also receives its digest, and the complete ordered
request receives a canonical digest.

For an initial wave, join the request to the already public prepared-wave and
binding-bundle identities. Do not duplicate prompts or provider request payloads.

Require a small API-issued aggregate grant that binds the exact request, ordered
actions and bindings, snapshot/wave identity, and ordinary authorization documents
as one all-or-none decision. Ordinary actions use lexical action-ID order; an
initial wave preserves its existing semantic member order.

Add a constrained continuation boundary that revalidates the request and aggregate
grant under native single-writer control, applies authorization, and durably records
pre-submit intent. Release the writer during slow provider I/O and reacquire it to
persist provider identity. A crash after intent without a durable provider identity
is ambiguity, not permission to create again.
Generic resume without that identity must refuse from `await_external_authority`.

Separately strengthen fresh-wave admission. A retained run containing any prior
initial-wave action/provider evidence but lacking one exact reusable wave is not a
fresh run. It produces the typed `initial_wave_lineage_unjoinable` refusal with no
external-authority request and no provider-create permission. Publish that result
through a closed `external_authority_refusal` companion object so consumers never
infer refusal semantics from a null request plus unrelated branch fields. That is
a safety result, not an automatic migration.

## Important distinction

Three situations must remain machine-distinct:

1. **Fresh admission:** one exact prepared inventory exists and may be submitted
   only after matching API authorization.
2. **Exact retained continuation:** the same inventory and durable provider lineage
   are reused/reconciled; no new create occurs.
3. **Unjoinable historical lineage:** prior evidence exists but cannot prove one
   safe current inventory; continuation is refused before provider I/O.

Treating case 3 as case 1 caused the incident. Treating it as case 2 without proof
would fabricate provenance. The patch must do neither.

## Scope boundary

This sprint changes SBE's native/public contract and command preflight only. It does
not recover Aster, cancel its duplicate Responses, alter API reservations, redesign
queueing, or infer authority from logs. Any future retained recovery remains a
separate, explicit, evidence-qualified operation.
