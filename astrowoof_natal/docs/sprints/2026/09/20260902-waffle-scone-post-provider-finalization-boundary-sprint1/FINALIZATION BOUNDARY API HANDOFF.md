# Finalization Boundary API Handoff

Status: API-approved and published in immutable SBE `0.4.40`.

## Consumer rule

The exact command-returned `astrowoof.terminal_review_command_result.v0.1`
envelope is primary authority. API validates and joins its exact `result_id` and
`receipt_id`; discovery of another sealed result is not transition authority and
is limited to the already documented recovery case where no envelope returned.

For a validated native-result v0.2 carrying:

```text
outcome: review_required
cause_code: finalization_contract_invalid
custody_finality: final
new_provider_create_permitted: false
```

API may use its existing terminal-review ingress. It must additionally validate
the complete action-disposition digest and join every action to API's immutable
native run/action identity, full binding, route/stage, and provider-operation
identity. SBE does not assert API job, lease, reservation, settlement, or
resource-release facts.

Live provider custody or ambiguity outranks this disposition. SBE refuses to
seal `finalization_contract_invalid` unless every native action is terminally
accounted for. An exit code, log line, outer status, or presence of a sealed
artifact cannot substitute for validation of the returned envelope and exact
sealed result.

## Failure classes

- `AssemblyContractError` means deterministic native assembly evidence is
  contradictory after provider work has been fully accounted for. It is the
  only error caught by this boundary.
- `OSError`, `CalledProcessError`, timeout, interruption, provider failure, and
  unexpected programming errors retain their conservative operational behavior.
  They do not acquire terminal meaning merely because they occurred during
  finalization.
- Theme-group distribution findings (`theme_group_coverage`,
  `theme_group_balance`, and `cross_section_theme_mirroring`) are advisory and
  do not produce this result. Structural registry/assignment contradictions
  remain hard deterministic contract failures.

## Packaged qualification

Run the provider-free installed command:

```text
astrowoof-finalization-boundary-qa --output receipt.json
```

The closed `astrowoof.finalization_boundary_qualification.v1` receipt proves:

- Waffle-shaped 14/2/2/2 distribution reaches delivery;
- deterministic contradiction returns exit 2 only after sealing the exact
  result and receipt;
- the result validates against an API-shaped immutable action/binding set;
- exact replay returns the same command/result identity;
- operational failure publishes no native result; and
- external network, real provider creation, and spend are all zero.

The qualification command is evidence only. It accepts no credentials,
provider transport, retained workspace, grant, or production input and grants
no recovery or execution authority.
