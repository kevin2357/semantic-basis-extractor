# Slice 1 — public contract inventory and upgrade predicate

## Status

Contract inventory complete. No source, schema, package, provider, retained-QA,
or runtime change was required to produce this gate.

## Exact upgradeable v0.5 predicate

The compatibility seam is one asymmetric semantic relation, not a generic
contract failure.

SBE's released v0.5 semantic validator accepts `ordinary_resume` when all of the
ordinary branch facts agree and native local continuation is evidenced by either:

- a nonempty `local_dependencies` inventory; or
- at least one `provider_custody.actions[]` member whose
  `custody_classification` is `completed_provider_evidence`.

The API v0.5 consumer separately requires `len(local_dependencies) > 0` for every
`ordinary_resume`. It can therefore reject the following otherwise coherent
native-produced projection:

| Field/relation | Required value |
| --- | --- |
| `schema_version` | `astrowoof.authoring_lifecycle_inspection.v0.5` |
| `execution_branch.command` | `ordinary_resume` |
| `execution_branch.eligible_now` | `true` |
| `execution_branch.reason_code` | `ordinary_local_continuation_ready` |
| `execution_branch.action_ids` | empty |
| `execution_branch.not_before` | null |
| `execution_capacity.disposition` | `continue_local_cycle` |
| `execution_capacity.reason_code` | `local_work_ready` |
| `execution_capacity.local_work_ready_now` | `true` |
| `execution_capacity.resume_not_before` | null |
| `terminal.local_continuation_remains` | `true` |
| `local_dependencies` | empty |
| completed evidence | at least one custody member classified `completed_provider_evidence` |

Every other closed v0.5 schema, identity, route, observation, capacity, custody,
terminal, authority, branch, and external-authority invariant must validate.
The API adapter may intercept only the final nonempty-local-dependency predicate
for this complete relation. It must not parse a generic exception message or
turn another `SbeProviderContractError` into an upgrade request.

The provider-free characterization is
`test_completed_retry_beside_pending_retry_has_local_work_but_no_dependency`.
It proves the public shape; it does not reconstruct Diffie's missing bytes.

## Same-checkpoint identity across lifecycle versions

The canonical cross-version join is not equality of the version-specific
`checkpoint_basis_sha256`. v0.7 adds the local-work inventory to its basis and
v0.8 adds retry lineage, so their basis digests correctly differ.

API must instead require equality of the underlying immutable native observation
and identity facts:

- top-level native `run_id`;
- `observation.operator_state_revision`;
- `observation.snapshot_sha256`;
- `observation.logical_workspace_root`;
- `native_route.route_family` and `native_route.route_contract`;
- the closed action inventory and provider-custody facts projected from that
  checkpoint; and
- where present, the exact local-work inventory identity joined by run ID,
  revision, snapshot digest, and logical root.

The released v0.7 validator reconstructs and validates its v0.6 predecessor,
then enforces the local-work inventory join against the observation. The released
v0.8 validator removes its lineage extension and reconstructs an exact valid
v0.7 predecessor, then joins every retry-lineage member to the checkpoint action
inventory, binding, route/attempt coordinates, provider mechanism, provider
identity, and provider custody.

Consequently:

- changing time alone may change a temporal due decision under the same native
  checkpoint where that lifecycle contract permits it;
- changing revision, snapshot, logical root, route, action/binding inventory, or
  provider identity is a different checkpoint or contradictory successor; and
- a later v0.7/v0.8 observation is scheduling authority only after these joins
  validate. Reader availability alone grants nothing.

## Minimum newer-evidence table

| Native posture | Minimum public evidence | Supported disposition |
| --- | --- | --- |
| Provider custody pending and not due, with no unresolved lineage question | validated v0.7 | `provider_reconciliation_cycle`, ineligible until native `not_before`; release capacity until due |
| Provider reconciliation due, with no unresolved lineage question | validated v0.7 | SBE-selected bounded reconciliation subset; API invokes only the run-level command |
| Exact executable local work and no higher-precedence provider custody or retry-lineage ambiguity | validated v0.7 | execute the exact advertised local operation once; prior inventory becomes unusable after checkpoint progress |
| Mixed completed/pending retry custody; pending member not due; lineage consistent | validated v0.8 | execute only the exact completed-evidence fan-in operation while retaining the other provider custody; no provider create |
| Mixed completed/pending retry custody; pending member due | validated v0.8 | SBE-selected provider reconciliation precedes local fan-in for the due cycle |
| Retry-lineage conflict with retained provider custody | validated v0.8 | reconciliation remains permitted; forward provider dispatch remains forbidden |
| Retry-lineage conflict after provider custody clears | validated v0.8 | `none / retain_for_review` with `retry_lineage_conflict_requires_review` |
| Missing, stale, malformed, differently bound, or contradictory successor | none | stable typed API review; no generic resume, provider create, retrieval, or repeated upgrade loop |

For the Diffie-shaped mixed-custody seam, v0.8 is the required final scheduling
surface because custody and retry lineage must be joined. That does not mean
pending-but-not-due custody idles already completed deterministic fan-in. With
consistent lineage, v0.8 may select the exact local fan-in while retaining the
other provider custody; provider create remains forbidden. When retained custody
is due, the SBE-selected reconciliation cycle takes precedence. v0.7 remains an
immutable intermediate observation, not the final API routing authority for this
mixed case.

## Released public surface inventory

SBE 0.4.31 already packages and publicly exports:

- `inspect_post_fan_in_lifecycle()` and
  `validate_lifecycle_inspection_v07()`;
- `read_lifecycle_inspection_v07_schema()` and the packaged
  `temporal-lifecycle-contracts.v2.schema.json`;
- `inspect_retry_lineage_lifecycle()` and
  `validate_lifecycle_inspection_v08()`;
- `read_lifecycle_inspection_v08_schema()`,
  `read_lifecycle_inspection_v08_fixture()`, and the packaged v0.8 mixed-custody
  fixture;
- `astrowoof-authoring-lifecycle ... inspect-local-work` for the public v0.7
  read boundary;
- `astrowoof-post-fan-in-retry-qa` for provider-free post-fan-in progression;
  and
- `astrowoof-retry-lineage-qa` for provider-free lineage/custody qualification.

Package data already includes all JSON contracts and fixtures under
`resources/contracts` and `resources/fixtures`. The current inventory therefore
finds no SBE runtime or schema gap and does not recommend a new SBE release.
Slice 2 should prefer an API-consumable witness assembled from these released
surfaces. Slice 3 activates only if that exercise proves a missing packaged
artifact rather than an API adapter need.

## Refusal boundaries

The compatibility adapter must refuse rather than upgrade when:

- the v0.5 document is not structurally valid;
- any invariant other than the exact dependency/completed-evidence asymmetry
  fails;
- no completed provider evidence exists;
- run, revision, snapshot, logical root, route, action/binding inventory, or
  provider identity changes across the read;
- v0.7 advertises `ordinary_resume` without a concrete local-work operation;
- local work conflicts with provider-custody precedence;
- v0.8 lineage does not exactly cover checkpoint retry actions; or
- the same checkpoint repeatedly requests upgrade after a newer observation was
  already persisted.

These are stable review/integrity outcomes. None authorizes generic resume or
provider work.

## API implementation gate

API may now implement a narrow classifier at its v0.5 semantic-validation
boundary. The classifier should be expressed as a positive predicate over the
complete parsed document, not an exception-string match. It must append the
validated newer observation to durable history, preserve the original v0.5
document, and use API lease/custody fencing to keep repeated reads idempotent.

No retained Diffie/Hellman operation, provider access, deployment, or release is
authorized by this inventory.
