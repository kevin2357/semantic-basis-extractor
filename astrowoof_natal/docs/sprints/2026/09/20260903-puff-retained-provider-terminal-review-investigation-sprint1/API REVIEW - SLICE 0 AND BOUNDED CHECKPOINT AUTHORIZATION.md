# API review — Slice 0 and bounded checkpoint authorization

## Review decision

Approved. The causal framing is appropriately conservative:

- Pastiche proves an advisory/rejection coincidence, not an advisory-only rejection.
- Puff proves completed polish retrieval followed by a failed semantic-consumption fence, not the exact stale/missing native join that caused it.

The timeline correctly leaves the unproven fields to retained-workspace inspection. It does not mistake non-authoritative worker logs for custody authority, and it identifies `local_work_progress_contradiction` as a terminal record of a contradiction rather than a resolution of the retained provider action.

One wording guardrail for later slices: the API receipt was persisted at `13:53:56.647801Z`, while native result publication was at `13:53:21.071482Z`; preserve that distinction when presenting the cross-boundary timeline. It does not alter the current causal classification.

## Authorization

The owner authorizes SBE to perform exactly one HEAD and one GET for each of the three immutable, protected checkpoint objects below, solely to inspect the artifacts named in the Slice 0 gate:

1. Pastiche final workspace: pass-6 attempts 2 and 3 acceptance artifacts and their complete issue/status/exit fields.
2. Puff generation 21: the pre-contradiction, `bounded-progressed_local` state.
3. Puff generation 22: the terminal/frozen retained-provider state.

No storage listing, alternate object access, write, delete, provider request/retrieval, resume, reconciliation, repair, run mutation, deployment, or release is authorized. A HEAD must match the listed byte size and SHA-256 before its corresponding GET is interpreted. Credentials, signed URLs, and unrelated secrets must not be recorded in sprint artifacts.

## Immutable coordinate packet

All objects: storage environment `qa`; namespace `checkpoint`; protection class `protected-operator`; checkpoint contract `astrowoof.sbe-workspace-checkpoint.v1`; compatibility identity `astrowoof.qa.sbe0440-post-provider-finalization-boundary.v2`.

### Pastiche final workspace — generation 17

```json
{
  "api_run_id": "8517847a-2c13-4149-964a-95276d594882",
  "native_run_id": "e9a72ba7695dddddc977da162388396a854a0813139c5475ce0b290d038c4ffb",
  "checkpoint_id": "0d1c1398-a318-4004-86cf-cfe52edfd2c6",
  "job_id": "c1d29b51-99b1-4ee5-8ce2-8a76c0d7514b",
  "attempt_id": "1af5766a-8f8f-44c0-b548-5cb0a3bf7235",
  "generation": 17,
  "state": "active",
  "storage_object_id": "89fd321d-613c-413c-b6c5-d33d22d81e3f",
  "archive_sha256": "a1627407ad6b9e07c42a409db382a40c75305191b6d9fa860abfda0caa2daba5",
  "archive_byte_size": 4418469,
  "inventory_sha256": "652a58149e62ef5a01742f24d6646de84cbcfa3f95bbf82ce56949e64f1e5b7a",
  "logical_restore_path": "/work/runs/8517847a-2c13-4149-964a-95276d594882/sbe",
  "native_lifecycle_status": "FAILED_REQUIRES_REVIEW",
  "provider_version": "a60a544882dd76959c38428ecd11a21e"
}
```

### Puff pre-contradiction workspace — generation 21

```json
{
  "api_run_id": "181ae153-1496-4e80-acd3-c7f18a4c9607",
  "native_run_id": "84a24f8facd330a80ad42c19986ccc0f5fde2287e307d30ccbf6e3f85f3c30be",
  "checkpoint_id": "f75acc2d-8a40-4ea0-9dd6-460f7604f78e",
  "job_id": "b1bf8c7f-0c9a-46b5-b84a-4c2c4aa5dde9",
  "attempt_id": "7a909b2f-2474-4904-b975-1a9ed5ea484b",
  "generation": 21,
  "state": "superseded",
  "storage_object_id": "e49cdb61-1cbb-4a34-85ac-5a37e61769ea",
  "archive_sha256": "e2422a2c6a001e3844f68e86bdc1e98939514f3356bbec1d24db111e8cb9ab03",
  "archive_byte_size": 5546428,
  "inventory_sha256": "56b439ab403c5c95c89ccf444e18b9fb3cecd0df78bf9cd179d4025afe7b5b2b",
  "logical_restore_path": "/work/runs/181ae153-1496-4e80-acd3-c7f18a4c9607/sbe",
  "native_lifecycle_status": "bounded-progressed_local",
  "provider_version": "9f2059b1a37e4a0766ee1dfe4a5e3f63"
}
```

### Puff terminal/frozen workspace — generation 22

```json
{
  "api_run_id": "181ae153-1496-4e80-acd3-c7f18a4c9607",
  "native_run_id": "84a24f8facd330a80ad42c19986ccc0f5fde2287e307d30ccbf6e3f85f3c30be",
  "checkpoint_id": "5ac7f732-8d9c-45a9-abe5-2e7c6049a1c0",
  "job_id": "b1bf8c7f-0c9a-46b5-b84a-4c2c4aa5dde9",
  "attempt_id": "20c0822e-40a8-46f7-8847-15b2524fb173",
  "generation": 22,
  "state": "active",
  "storage_object_id": "e696d16b-d331-40c9-8cd0-9be8a10ac3a0",
  "archive_sha256": "10bf1acf9163e2ace26f2d6bf42eb4a42bc2c3708f292c7db1cf44bd3e7a9468",
  "archive_byte_size": 5619737,
  "inventory_sha256": "affe29a768c35d55b3842d484fd141756a00f2ed0c344527b4e35a8497ba492f",
  "logical_restore_path": "/work/runs/181ae153-1496-4e80-acd3-c7f18a4c9607/sbe",
  "native_lifecycle_status": "WAITING_FOR_RESPONSE",
  "provider_version": "04132404562ef8bc4fe164a9113b4d09"
}
```

The terminal result/receipt joins to inspect are `nres_dac25445bfa8c6613d0d0ca0` and `nreceipt_d38140389b21ae33e151f1fe`.
