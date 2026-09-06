# API coordinate packet — Frisbee final editorial checkpoint

## Scope and authorization

API authorizes this exact bounded, read-only extraction for the Frisbee editorial
audit:

1. exactly one HEAD for the named R2 object; and
2. exactly one conditional GET of the same object, proceeding only when the HEAD
   identity and `ETag`/provider version equal this packet.

No R2 listing, write, delete, provider call, reconciliation, resume, recovery,
workspace mutation, or API/database mutation is authorized. The downloaded archive is
evidence only; preserve its digest and do not use it as authority to progress the run.

## Frozen API/native/checkpoint join

| Field | Exact value |
| --- | --- |
| API run | `e2d7f0ce-8c2a-4209-b79f-eb2187a58b15` |
| native run | `cfdd79f1f50bbe940ba40d2c42743bf8b009cc02eef0f44895f0697b0d46be98` |
| checkpoint UUID | `503f8655-6a78-418e-a747-7a00595ebb29` |
| checkpoint generation / sequence | `11` / `11` |
| job / attempt / lease | `ece96e75-92e1-43d2-b402-e665e7f775a0` / `78b6af9c-9381-4e3b-bb43-6b71f9f4b074` / `75f3c54c-46bc-4048-8c0e-c0ff1364cd3c` |
| native lifecycle status | `bounded-review_required` |
| checkpoint contract | `astrowoof.sbe-workspace-checkpoint.v1` |
| compatibility identity | `astrowoof.qa.sbe0450-terminal-reconciliation-handoff.v1` |
| checkpoint state | `active` |

The retained lifecycle checkpoint basis separately joins the same API/native run
(`authoring_run_id` `7fe3d4b0-05c0-48af-bff6-f41a4cf83616`), so the archive is not
being inferred from label or time alone.

## R2 coordinate and integrity envelope

| Field | Exact value |
| --- | --- |
| storage environment / bucket | `qa` / `astrowoof-qa-artifacts` |
| namespace | `checkpoint` |
| storage object UUID | `00b6c31b-262d-45ae-8b1a-29ecc4cb40c6` |
| exact R2 key | `v1/checkpoint/00b6c31b262d45ae8b1a29ecc4cb40c6` |
| provider version / ETag | `"6148734c493e27681c6ae0987d3f2be3"` |
| archive bytes | `5002462` |
| archive SHA-256 | `b9a916e15daf33c6dbc54958a3e6f6d9c4eea37d043ecebcff42ca490cff6de3` |
| inventory SHA-256 | `b2afa16f27a8d80066a74900bc47dfc5e40ac0a343a9b20d7dedde1de2421bf8` |
| media type | `application/vnd.astrowoof.checkpoint+zip` |
| protection class | `protected-operator` |
| storage contract | `astrowoof.storage-receipt.v1` |
| logical restore root | `/work/runs/e2d7f0ce-8c2a-4209-b79f-eb2187a58b15/sbe` |

The archive GET must be bounded to `5,002,462` bytes, use the exact provider
version/ETag as its precondition, and verify both archive SHA-256 and inventory
SHA-256 before extraction/replay. A changed/missing ETag, size, digest, or inventory is
a typed evidence failure, not permission to fetch another object or retry broadly.
