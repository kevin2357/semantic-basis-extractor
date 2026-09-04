# API Slice 1 — bounded checkpoint coordinate packet

## Review disposition

API approves SBE Slice 0's causal framing.

- Havoc is independently evidenced as an exact polish adoption followed by a
  post-polish validation failure; the supplied trace does not establish the
  individual issue codes.
- Mischief's supplied per-run extract ends before its corresponding
  polish/adoption/final-validation events.  That is an export-coverage limit,
  not evidence against the API-recorded terminal result.

The packet below authorizes the requested bounded read-only inspection.  It is
not authority to resume, reconcile, mutate, list storage, call a provider, or
otherwise alter either retained run.

## Immutable outer-object coordinates

| Subject | API run | Native run | Final accepted checkpoint | Generation | Opaque storage object ID | Archive SHA-256 | Bytes | Inventory SHA-256 |
| --- | --- | --- | --- | ---: | --- | --- | ---: | --- |
| Havoc von Hooligan | `18d29fd9-2e74-4803-8de9-f65324c69a10` | `8fe16b99856c96c5a6fd67c59e9a9bd4f89199725101456a60ae3456ba410b7b` | `14efd1f6-fbfb-48cb-b647-127203fc57bf` | 10 | `5f0bc3a6-9f24-4d8c-8714-235fb71213e1` | `c202b11cbf5c9c1e8c72bc8b6c7369fdece37c5d6262cf6839fe696bd4dcbf22` | 4,850,622 | `3c0a144c6cb4febd943133e8c20acaa3aa85d8615e6d3d9ffb329d4d9feab4d9` |
| Mischief McMuffin | `273dbea7-50c8-4dee-b1ac-3f99e68be5ea` | `e41cee4362fc2ba3ce7fcfdcf633d99bc1762a66a05fb2d76424c6908a8b2ebb` | `cbfb0d16-f255-4f97-b64e-982c84b8ffea` | 8 | `321dd51b-f003-4854-8339-9fc05925984c` | `c94e166cb88b4e44b734335226393fc9df30864d86e82d0613d128c1e3132ece` | 4,645,099 | `b0e05d0adc7d9e10209a3411d1c5d69ffecd3bf9d684be2f907eeb3a5b751343` |

Both checkpoint records are `active`, use checkpoint contract
`astrowoof.sbe-workspace-checkpoint.v1`, compatibility identity
`astrowoof.qa.sbe0443-zero-paid-terminal-review.v1`, and storage contract
`astrowoof.storage-receipt.v1` in `qa/checkpoint/protected-operator`.

| Subject | Provider version / ETag | Logical restore root | Native lifecycle status |
| --- | --- | --- | --- |
| Havoc | `0fd6bde20ddf7b79d141b2ddf1500654` | `/work/runs/18d29fd9-2e74-4803-8de9-f65324c69a10/sbe` | `bounded-progressed_local` |
| Mischief | `a1f25273909bcb0287e0e8adeb664ef2` | `/work/runs/273dbea7-50c8-4dee-b1ac-3f99e68be5ea/sbe` | `bounded-progressed_local` |

`protected_payload_reference` is intentionally null for both records.  The
opaque `storage_object_id` is the API-issued storage coordinate; this packet
does not manufacture a bucket/key, signed URL, or alternate reference.

## Authorized bounded reads

For **each** named outer object, SBE is authorized for exactly one `HEAD` and
one `GET`, pinning the request to the stated provider version where the storage
client supports conditional reads.  On retrieval, it must verify archive byte
size and SHA-256 before extracting any member.  The outer archive's signed
inventory must verify to the stated inventory SHA-256.

No R2 prefix/bucket listing is authorized.  No write, deletion, provider
access, reconciliation, resume, repair, or retained-run/API mutation is
authorized.

The inspection is restricted to the following known members after outer-archive
verification:

### Havoc

- `workspace-snapshot.json`
- `final/dog-9d41ad92-9668-4192-91b0-81b28403a1cc/polish/attempt-001/validation-report.json`
- `final/dog-9d41ad92-9668-4192-91b0-81b28403a1cc/polish/attempt-001/lint-report.json`
- `passes/dog-9d41ad92-9668-4192-91b0-81b28403a1cc_{1,2,3,4,5,6}/attempt-001/authoring-pass-acceptance.json`

### Mischief

- `workspace-snapshot.json`
- `final/dog-6afb1a5b-b4c8-4600-9ed8-193e1e14c726/polish/attempt-001/validation-report.json`
- `final/dog-6afb1a5b-b4c8-4600-9ed8-193e1e14c726/polish/attempt-001/lint-report.json`
- `passes/dog-6afb1a5b-b4c8-4600-9ed8-193e1e14c726_{1,2,3,4,5,6}/attempt-001/authoring-pass-acceptance.json`

The brace notation above is a fixed six-member set, not a glob or an authority
to enumerate.  `workspace-snapshot.json` is included solely to join the exact
polish input/output, acceptance, and validation records already bound by the
verified archive inventory.  No individual member digest is asserted here: the
API retains the verified outer archive and inventory digests, not invented
per-member object identities.
