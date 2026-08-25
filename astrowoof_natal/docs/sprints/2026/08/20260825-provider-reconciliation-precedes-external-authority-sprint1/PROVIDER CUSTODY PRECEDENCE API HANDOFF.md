# Provider Custody Precedence — API Handoff

Status: Slice 5 candidate qualified; API review required before release preparation

## Consumer rule

API continues to consume lifecycle inspection v0.5 or temporal lifecycle v0.6. No
new command, state, or routing inference is introduced.

When retained provider custody exists, invoke only the command selected by SBE:

- due: `provider_reconciliation_cycle`, `eligible_now=true`, with SBE's ordered
  `action_ids` subset (maximum four);
- not due: `provider_reconciliation_cycle`, `eligible_now=false`, with native
  `not_before`; API may run later but never earlier;
- completed evidence requiring fan-in: `ordinary_resume`, `eligible_now=true`.

Do not invoke external-authority admission merely because another API/native action
is prepared. SBE exposes `await_external_authority` only after preceding provider
custody and required fan-in are exhausted and a new checkpoint basis identifies the
exact next paid inventory.

API must invoke the supported run-level command. It must not select, reorder, or
reconstruct reconciliation members from provider IDs, private state, logs, or its
own ledger.

## Stable public meanings

| Public fact | Meaning |
|---|---|
| `provider_reconciliation_due` | bounded SBE-selected retrieval is runnable now |
| `provider_reconciliation_not_due` | release local capacity until native lower bound |
| `ordinary_local_continuation_ready` | deterministic native fan-in/local work is runnable |
| `spend_authorization_required` | no higher-priority custody/fan-in remains |
| `retained_provider_custody_precedes_authority` | contradictory document; refuse |
| `provider_fan_in_precedes_authority` | contradictory completed-evidence document; refuse |

The last two values are semantic-validator predicates/diagnostics, not scheduling
states. A valid candidate should not publish them during ordinary selection.

## Time and checkpoint identity

For one unchanged provider-custody checkpoint basis, trusted API observation time
may change only reconciliation eligibility, SBE's bounded due subset, and derived
`not_before`. External-authority inventory remains absent at both not-due and due
observations.

Retrieval and deterministic fan-in record new native evidence and therefore produce
a new checkpoint basis. Only that successor basis may expose the later authority
request.

## Route and stage matrix

- Exact Natal interactive Response: supported.
- Bounded Natal interactive Response: supported.
- Exact Natal Batch: supported for existing Batch reconciliation.
- Bounded Natal Batch: supported for existing Batch reconciliation.
- Interactive initial/retry/polish/critic/candidate custody uses the same precedence.
- Existing ordinary optional-stage Batch dispatch deferrals remain unchanged.
- One Batch round remains one paid/provider authority; member rows are evidence.

Nonblocking critic custody does not revoke an already publishable delivery. It does
retain its own custody/consumer authority and does not silently authorize unrelated
new provider work.

## Qualification command

Run from an installed wheel without credentials or network:

```text
astrowoof-provider-pending-qa
```

The closed receipt proves:

- six scripted creates and immediate detach;
- not-due custody suppresses a later prepared action;
- due selection is SBE-owned and bounded to four;
- fresh-cycle retrieval is exactly 4+2;
- completed evidence selects fan-in;
- authority appears only in the post-fan-in successor basis;
- no duplicate creates or retrievals; and
- contradictory lifecycle projection is refused.

This command is qualification-only. Its scripted create/retrieve counts are not
provider traffic, spend authority, API reservation evidence, or production state.

## Slice 5 installed-wheel evidence

- Candidate source commit: `c222956e39db0a0aece6751c85038028be83fe85`.
- Candidate wheel (pre-version-bump): SHA-256
  `730315cbbd4cd78fbc592c74e3d7021c8aad7b0cddf8d0ee07fa03418a9b55fb`.
- Installed SPC 0.11.1 wheel: SHA-256
  `fd8b9be60c91f7f102164c45fcf2f89c814f808b334b3c08136f683f1c2b8b5b`.
- Receipt SHA-256:
  `271743902a49eb16ea1be23c3d44f86dc9b15cb877fb6f30e2ca7a61bfc63741`.
- Receipt status: `pass`.
- External network/provider calls and spend: 0.

The wheel still carries version 0.4.21 solely because Slice 6 versioning is gated on
this API review. It is not a publication artifact and must not replace immutable
0.4.21.

## Retained workspace posture

This patch does not repair or resume the frozen QA cohort. After a fresh immutable
release, any retained-run bridge/recovery remains separately reviewed and authorized.
The API must validate the current native snapshot and lifecycle evidence rather than
infer safety from historical dashboard completion.

