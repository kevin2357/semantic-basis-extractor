# Slice 0 — public evidence inventory and classification table

## Decision

The proposed assessment is feasible as a read-only projection over existing
public, snapshot-validating SBE readers. It must not project directly from
private `run.json`, status strings, result-index presence, logs, or API state.

One correction is required before schema freeze: the original seven custody
classes omitted concrete deterministic local work that is neither provider
fan-in nor external authority. The contract therefore adds
`native_local_work_ready`. Calling such a checkpoint quiescent would be false;
calling it inconsistent would discard a supported `ordinary_resume` decision.

## Public evidence sources

| Evidence | Supported reader / validator | What it proves | What it does not prove |
|---|---|---|---|
| Lifecycle v0.5 | `inspect_lifecycle`, `validate_lifecycle_inspection_v05` | snapshot observation, exact action inventory, provider custody, consumer-authority retention, branch, v1 authority request/refusal | concrete local-operation identity; API capacity or lease state |
| Temporal v0.6 | `inspect_temporal_lifecycle`, v0.6 validator | immutable checkpoint basis separated from API-supplied observation time; SBE-selected due subset | local-operation identity; retry lineage |
| Local-work v0.7 | `inspect_post_fan_in_lifecycle`, v0.7 validator | exact concrete local operations, stable operation keys, consumed history, supported `ordinary_resume` | retry-lineage conflict details |
| Retry-lineage v0.8 | `inspect_retry_lineage_lifecycle`, v0.8 validator | retry lineage joined exactly to checkpoint inventory and custody; conflict precedence | API queue or admission state |
| External authority v1/v2 | embedded validated lifecycle request/refusal and their public validators | exact ordered providerless inventory and request identity | a grant, provider-create permission, or API reservation |
| Exact native result | `read_native_transition_result(run_dir, result_id)` | result content identity, bounded journal range, current snapshot, immutable receipt, retained snapshot and checkpoint basis | which result API has ingested or whether API terminalized a job |
| Result availability | `read_native_transition_result_availability` | bounded discovery of an exact result ID from a snapshot-valid, closed publication inventory | transition authority, terminal meaning, or permission to choose “latest” during normal invocation |
| Operator retirement assessment | `assess_operator_retirement` and strict validator | precedent for provider-free dry-run assessment, exact checkpoint/request binding, and zero-side-effect assertions | generic quarantine or API resource release |
| Installed compatibility | package version plus native route/contract compatibility identity | deployed reader capability associated with the assessment | deployment health or API pin state |

The v0.5 observation currently carries `logical_workspace_root`, and older
workspaces may expose an absolute restored path there. The new assessment will
not repeat it. It will expose a bounded opaque logical identity,
`logical_workspace_root_id = "lroot_" + sha256(UTF-8 public logical-root)[:24]`,
and bind the complete source value only through the assessment digest and the
validated lifecycle-evidence digest. The validator will reject path separators,
drive-letter forms, URI schemes, `.` and `..` segments in the public identifier.

## Assessment identity freeze

`assessment_sha256` commits to every other field using canonical UTF-8 JSON,
sorted object keys, preserved array order, no insignificant whitespace, and no
NaN/Infinity. The assessment binds:

- native run ID;
- route family and route contract;
- installed SBE release and compatibility identity;
- native state revision;
- snapshot SHA-256 and checkpoint-basis SHA-256;
- opaque logical-root ID;
- lifecycle schema version and canonical lifecycle document SHA-256;
- exact result ID/result SHA-256 and receipt ID/receipt SHA-256 when used;
- exact availability-document digest when bounded recovery discovery was used;
- custody class, subsidiary assertions/counts, posture, actions, and reason.

Any changed member requires a fresh assessment. Observation timestamps are not
identity substitutes and do not weaken the checkpoint joins.

## Canonical next-action semantics

`supported_next_actions` is always present and is an ordered list of distinct
closed vocabulary values. No-action is represented only by `[]`. The token
`none` does not exist. An absent field, `null`, or `none` mixed with an action
is invalid.

The list names supported native operations only. It never carries an action
subset, creates authority, or directs API-global scheduling. If a lifecycle
reader publishes an SBE-selected bounded retrieval subset, API invokes the
named run-level command; it does not reconstruct the subset from this summary.

## Classification and compatibility table

| Dominant class | Positive public proof | Disqualifiers / precedence | Native quarantine posture | Supported next actions |
|---|---|---|---|---|
| `unsupported_or_inconsistent` | invalid/unknown public contract, failed snapshot or digest join, contradictory closed fields, or no complete classification | first precedence; never flattened to false/empty evidence | `prohibited` | `[]` |
| `submission_ambiguous` | v0.5+ action/custody evidence shows entered/submitting or explicit ambiguity without one coherent durable provider identity | snapshot must still validate; ambiguity outranks all forward work and terminal-looking labels | `permitted` | `operator_review`, `fresh_disposition_assessment` |
| `completed_unadopted` | validated custody item is `completed_provider_evidence` and lifecycle/local-work evidence proves adoption/fan-in remains | ambiguity outranks; completed evidence outranks merely pending identities and providerless authority | `native_prior_action_required` | `ordinary_resume` |
| `provider_pending_known_identity` | validated custody has one or more durable provider identities with incomplete result adoption; lifecycle says due or not due | ambiguity and completed-unadopted outrank; subsidiary providerless authority remains visible | `permitted` | `provider_reconciliation_cycle` |
| `native_local_work_ready` | v0.7/v0.8 validates a nonempty concrete local-work inventory and `ordinary_resume` is eligible now | provider ambiguity/custody and completed-unadopted precedence apply first | `native_prior_action_required` | `ordinary_resume` |
| `providerless_authority` | validated request/refusal/action evidence shows providerless prepared, authorized-fenced, or denial-required work and no higher custody | never inferred from `PREPARED` alone when a closed authority request/refusal is required | `permitted` | exactly the applicable one of `external_authority_v1`, `external_authority_v2`, `providerless_denial`, or `operator_review` |
| `sealed_terminal` | explicit result ID is successfully read through `read_native_transition_result`; result, receipt, retained snapshot, checkpoint basis, journal, run, route, and current snapshot join; no contradictory live custody/local work | status labels and index entries are insufficient; any live higher-precedence custody wins | `permitted` | `terminal_result_ingress` |
| `provider_free_quiescent` | validated lifecycle proves no provider custody, ambiguity, authority, executable local work, or unresolved result transition | a terminal-looking status is neither required nor sufficient | `permitted` | `[]` |

`native_prior_action_required` means only that SBE cannot attest that the
checkpoint is locally idle: a supported native operation must first consume or
reclassify current truth. It does not assert that API presently owns a worker
slot or must retain a particular lease.

`permitted` means only that current native evidence does not require an
ordinary local authoring worker to remain scheduled. Provider custody,
authority history, settlement, and API-owned resources remain untouched.

## Subsidiary facts

Dominant classification does not erase mixed state. The assessment will carry
bounded counts and booleans for:

- provider identities retained;
- provider results completed but unadopted;
- ambiguous submissions;
- concrete local operations;
- providerless prepared/authorized/denial-required actions;
- retry-lineage conflicts;
- sealed exact results; and
- overflow for every bounded identity inventory.

These are diagnostic assertions joined to the lifecycle evidence. They are not
an action inventory and API cannot select work from them.

## Exact terminal-reader rule

Normal invocation handling must use the result ID returned by that invocation.
Only an explicitly documented recovery/preflight flow may use
`read_native_transition_result_availability`; it discovers one exact ID but is
not transition authority. In either case `read_native_transition_result` must
validate the exact result/receipt/checkpoint join before `sealed_terminal` is
possible. “Latest,” an index position, a terminal-looking status, or a sealed
filename never establishes terminal classification.

## Route and minimum-version notes

- v0.5 is sufficient for known provider custody, ambiguity, v1 external
  authority, and basic quiescence only when no local continuation is claimed.
- v0.6 is required when due/not-due temporal selection is part of the proof.
- v0.7 is required for any positive local-work/ordinary-resume assertion.
- v0.8 is required when retry-lineage conflict or mixed retry custody affects
  classification.
- v2 external authority is read from its exact validated temporal request join;
  it is not reconstructed from action IDs.
- Exact and bounded interactive routes share the classification vocabulary,
  but unsupported Batch evidence fails closed rather than being projected as
  an interactive action.

## Slice 1 contract consequences

The schema/validator must enforce the table mechanically, including all
class/posture/action combinations, exact joins, path-private rejection,
subsidiary-count consistency, and terminal-reader provenance. Unknown versions
and contradictory evidence produce a typed read failure or the explicit
`unsupported_or_inconsistent` artifact; they never collapse to `False`, `[]`,
or a fallback branch.
