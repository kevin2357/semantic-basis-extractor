# API Review — Slice 2 and Pinned R2 Coordinates

Approved. Slice 2 correctly excludes root drift, release-pair skew, terminal
result substitution, and any demonstrated Better Stack request. The common
`capture_or_preflight` result remains too broad to assign a first internal
failure boundary from telemetry alone.

The next justified evidence step is a read-only, network-disabled reproduction
against the exact terminal checkpoint for each distinct native producer route.
The following packets came from API's authoritative PostgreSQL coordinate
catalog. They are not latest-object discovery and must not be expanded to any
other workspace/result.

## Aldine Apricot — terminal review v0.2

| Field | Value |
| --- | --- |
| API run | `6a683b9a-fa00-4ad6-8e23-b6d8d5d9524a` |
| Native run | `3ab7cd6e857b6f3ee5947ca6302adab41a0054b988bafdc99697e8f3425e4d96` |
| Checkpoint ID / generation | `5361c9c2-1824-4b5c-bdb4-f005f6243cd4` / `9` |
| Storage object ID / R2 key | `9cba9f68-bbb0-42f9-a39d-6c0ed32bade4` / `v1/checkpoint/9cba9f68bbb042f9a39d6c0ed32bade4` |
| Archive bytes / SHA-256 | `5,108,295` / `707bd5ca64e5741a2949e5684bd6940d6fd6bac89dfe1d3312d16bc4276af695` |
| Inventory SHA-256 | `cb91ad312fce3704b3cb7225573473f6260bb4e47669117d0dbc560108861082` |
| Logical restore root | `/work/runs/workspace-5ee951a5-650c-4fbf-8e89-88525171c9e0/sbe` |
| Exact terminal result / SHA-256 | `nres_d0568048c5fc2d9cfd68d7c7` / `d0568048c5fc2d9cfd68d7c75186f238662986b112798eb24785abf2dc919802` |
| Exact receipt / SHA-256 | `nreceipt_39f8305f65dcfe9b36751f65` / `39f8305f65dcfe9b36751f6564300c2dff2a12c5092df53c80e0918cbb5ae1c9` |
| Receipt checkpoint basis | `283b5e1ac53d18225b02c403b611ecc2b65c7292cb85eed7e2988b9d710a38bc` |

## Moxon Muffin — accepted delivery v0.1

| Field | Value |
| --- | --- |
| API run | `137f3968-239b-4a01-9d8e-61b98ed6601e` |
| Native run | `3ebaec3c5c954a63b14519a7b0e8ba300384263be3ea0fd079ca181701e52520` |
| Checkpoint ID / generation | `9aad740a-5ec8-4303-aab0-6ee06cd528a9` / `9` |
| Storage object ID / R2 key | `aefb19c0-d2be-4c82-8ff9-4429639262ac` / `v1/checkpoint/aefb19c0d2be4c828ff94429639262ac` |
| Archive bytes / SHA-256 | `5,026,273` / `565f2047d01828a6d4c7bbbcefd3fdc51feb836ad44b474708913ebf28754d90` |
| Inventory SHA-256 | `8ac31acfed44700ff6e4bd37ae1cdc7dbc83e64bf01839689f5ca4a763b341c8` |
| Logical restore root | `/work/runs/workspace-9b2cafdd-046e-4e6d-ab45-f52b7ed8c959/sbe` |
| Exact terminal result / SHA-256 | `nres_5a90fadd039f369c7303ecd3` / `5a90fadd039f369c7303ecd3383486dda7133025a5a0235b442e233587196042` |
| Exact receipt / SHA-256 | `nreceipt_1cd1e0f6f12880de36648d0a` / `1cd1e0f6f12880de36648d0ac256f9f5310260dc8821f170da544d77a2d4cd01` |
| Receipt checkpoint basis | `2e4629777c978d7187c438f1a37a63d060f1602ecb80731f029c63c8fe21350e` |

## Access fence

The database does not persist an R2 ETag/version identifier. Therefore the
first conditional HEAD is the only authorized mechanism to bind that live
object metadata to the fixed key and digest. This review does **not** itself
grant R2 access. Before extraction, request owner authorization for exactly one
conditional HEAD and one bounded GET for each named key above; require the HEAD
size and SHA/inventory expectation to agree before the GET. No listing,
alternate-key discovery, provider call, resume, reconciliation, or mutation is
approved.
