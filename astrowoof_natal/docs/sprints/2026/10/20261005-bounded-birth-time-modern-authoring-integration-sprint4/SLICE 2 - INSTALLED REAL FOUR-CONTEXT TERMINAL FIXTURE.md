# Slice 2 — installed real four-context terminal fixture

## Scope

This is the SBE-side provider-free proof for an **eligible** bounded source
family. It uses API Sprint 128's sealed representative SPC workspace inputs,
an installed local wheel, and SBE's fake lifecycle provider. It makes no
network or provider call and does not create an API/WWW public delivery.

## Candidate to use

| Field | Value |
| --- | --- |
| Wheel | `astrowoof_natal_authoring-0.4.70-py3-none-any.whl` |
| Retained path | `C:\tmp\sbe-0.4.70-bounded-slice2-candidate\astrowoof_natal_authoring-0.4.70-py3-none-any.whl` |
| SHA-256 | `0e01f2ab293e88f1ea20a5d866094bced28e34d69cad1354bcc8db0ad19187bc` |
| Bytes | `1,439,082` |
| Wheel members | `328` |
| Installed SBE / SPC | `0.4.70` / `0.11.1` |

This candidate is superseded for the joint API gate by the later v2 eligibility
candidate recorded in the Slice 2B addendum. It remains valid evidence for the
receipt-backed eligible terminal route. Neither candidate is a tag,
publication, deployment, activation, or provider approval.

## Real source-family proof

The replay consumed the four API Gate B SPC projections from
`C:\tmp\astrowoof-sprint128-gate-b-docker-replay\workspace\spc`:

- `bounded_direct_to_dog.json`
- `bounded_general.json`
- `bounded_handler.json`
- `bounded_hybrid.json`

The installed wheel admitted all four contexts as
`bounded_admission:06b54d7c11191d86777bc2e8`, with source artifact SHA-256
`826d17e18d1d2df86cfefcf3de63fdf47a1ddee6fe3145e4ed8afd8895407913`.
The invariant-only selector retained exactly 50 candidates and rejected 442.

Using `FakeBoundedLifecycleProvider`, the run reached `DELIVERY_COMPLETE` and
sealed:

| Field | Value |
| --- | --- |
| Native result ID | `nres_0efcee9da41daf3a8f035ba5` |
| Result SHA-256 | `0efcee9da41daf3a8f035ba5f1a218213f563c44846eb1c9f45fbd3abb830b78` |
| Native receipt ID | `nreceipt_6ed609b894374aa7ae2cedcb` |
| Terminal command schema | `astrowoof.terminal_delivery_command_result.v0.1` |

`validate_terminal_delivery_command_result_against_publication()` accepted the
command only when it joined that exact sealed result and receipt.

## Fail-closed variants

| Alteration | Result |
| --- | --- |
| Omit one required projection | `bounded_context_count` refusal |
| Change one projection's bounded contract version to `9.9.9` | `bounded_contract_version` refusal |
| Replace terminal command receipt SHA with zeroes | exact-publication join refusal |

## Correction made before qualification

The real executable path found that the durable workspace binding is nested,
while the API frozen under-floor eligibility result accepts a smaller flat
projection. The CLI now explicitly derives and validates that closed projection
instead of passing the workspace object through as though it were the public
contract. Focused regression coverage proves the emitted result has the exact
flat binding shape.

## Boundary

This establishes native bounded admission, invariant selection, lifecycle,
sealing, and exact terminal-command custody from real deterministic inputs.
It does **not** claim API receipt ingress/idempotency, API/WWW accepted public
delivery, QA deployment, profile activation, or provider-backed content. Those
remain later cross-repo gates.
