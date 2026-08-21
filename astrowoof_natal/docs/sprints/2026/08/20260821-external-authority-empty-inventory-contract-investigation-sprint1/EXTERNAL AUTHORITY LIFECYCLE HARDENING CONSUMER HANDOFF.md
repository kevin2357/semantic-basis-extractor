# External Authority Lifecycle Hardening — Consumer Handoff

Status: Slice 5 API-approved; release preparation pending.

## Consumer boundary

SBE keeps lifecycle inspection contract
`astrowoof.authoring_lifecycle_inspection.v0.5` and tightens combinations that were
already semantically invalid. This is not a new scheduling choice and requires no
new API public state.

An API worker may select external-authority processing only when the complete
snapshot-validated inspection satisfies all of these conditions:

- `execution_branch.command == "await_external_authority"`;
- `execution_branch.eligible_now == false`;
- `execution_branch.reason_code == "spend_authorization_required"`;
- `execution_branch.action_ids` contains 1–32 exact ordered action IDs;
- `execution_branch.not_before == null`;
- `execution_capacity.disposition == "await_external_authority"`;
- `execution_capacity.reason_code == "spend_authorization_required"`;
- `execution_capacity.local_work_ready_now == false`;
- `execution_capacity.resume_not_before == null`;
- `external_authority_request` is present and
  `external_authority_refusal == null`; and
- outer run/observation/root identity, ordered branch IDs, and embedded request
  identity join exactly.

A native-review refusal must instead have `execution_branch.command == "none"`,
empty `action_ids`, no timing recommendation, no embedded request, and one closed
`external_authority_refusal`. It must not be interpreted as authority to invoke a
provider-capable command.

Contradictory documents fail schema or semantic validation. The API must not repair,
default, or infer missing predicates from `run.json`, logs, provider IDs, or product
job state.

## Compatibility

- Valid v0.5 request and refusal documents retain their existing shape and meaning.
- Lifecycle inspection v0.4 remains non-authorizing for this boundary.
- No API database, queue, lease, reservation, or public-state ownership moves to
  SBE.
- Existing API strict validation is expected to reject the same contradictory
  combinations now rejected natively.
- The retained incident's exact rejected predicate is unknown because that raw
  inspection was not preserved. This sprint does not relabel that uncertainty as a
  proven empty inventory.

For a retained workspace, restore its complete exact snapshot at its stable logical
absolute path and read a fresh supported lifecycle inspection. A valid joined
request may enter normal API authority evaluation. A typed refusal or invalid
inspection remains retained for review. Do not override native integrity evidence,
manufacture action IDs, or resubmit provider work.

## Installed-wheel qualification

Run from the installed candidate wheel:

```text
astrowoof-external-authority-qa \
  --output external-authority-qualification-receipt.v2.json \
  --fixtures-dir consumer-fixtures
```

The command is provider-free, credential-free, network-free, input-free, and
qualification-only. Its receipt contract is
`astrowoof.external_authority_qualification.v2`, validated by the packaged
`external-authority-qualification.v2.schema.json`. The v1 receipt remains immutable;
v2 adds explicit proof that request and typed-refusal lifecycle conditionals reject
mutations.

The receipt and fixtures in `results/` were produced from an isolated installation
of the candidate 0.4.14 wheel with SHA-256
`59053ac273d21f6d7b252d34b23a0757bacf1420baa855aee2b7612676d3f12b`.
The receipt is qualification evidence only and is never native execution authority.

## Diagnostics

Existing typed event names now carry redacted branch evidence: counts, canonical
digests, presence flags, closed refusal reasons, and deterministically sorted failed
predicate names. Text logs provide the corresponding operator explanation. Neither
surface contains authorization documents, bindings, provider payloads, credentials,
or subject data; neither is authoritative state. Diagnostic sink failure is isolated
from inspection bytes, native state, snapshots, authority, and provider behavior.
