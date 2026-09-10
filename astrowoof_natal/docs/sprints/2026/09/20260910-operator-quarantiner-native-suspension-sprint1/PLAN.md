# Plan

## Status and authority

The plan is revised after the live Baskerville assessed-quarantine refusal and provider-free SBE/API reconstruction. Only Slice 0 is authorized.

This plan authorizes no live workspace read, provider operation, quarantine execution, capacity release, process termination, native mutation, or suspension-contract implementation.

## New proven boundary

The current nice path fails deterministically before custody classification:

```text
API restores exact checkpoint bytes
  -> request-specific <operator-root>/<request-id>/sbe directory
  -> SBE read_operator_disposition_assessment()
  -> validate_workspace_snapshot()
  -> stable logical absolute-path mismatch
  -> no assessment
  -> API disposition_assessment_unavailable
```

SBE requires an executable workspace to remain at the exact logical absolute path recorded in `run.json` and `workspace-snapshot.json`. The operator runner deliberately restores into a fresh request-isolated directory. A provider-free reproduction proved that assessment succeeds at the original path and fails after byte-exact relocation.

The exact persisted live exception has not been read, so this remains the leading explanation for Baskerville rather than a claim of exact historical identity.

SBE's existing structured sparkle formatter also works in-process when deliberately configured. Native assessment diagnostics are being handled separately and do not resolve the path contract.

## Slice 0 — Read-only relocated assessment design

### Objective

Design the narrowest additive contract that permits SBE to assess a byte-exact, checkpoint-verified workspace restored at a different physical path without granting execution, mutation, publication, provider, or native-authority rights to that relocated copy.

The intended distinction is:

```text
authoritative executable workspace
  -> exact stable logical absolute path remains mandatory

relocated assessment view
  -> exact checkpoint/archive evidence
  -> explicitly read-only and assessment-only
  -> never resumable or publishable
```

### 0A — Freeze existing invariants

Record which guarantees the stable-path rule currently supplies:

- prevention of accidental execution from an arbitrary copy;
- stable logical workspace identity across native lifecycle evidence;
- snapshot-member and digest integrity;
- exact checkpoint lineage and compatibility identity;
- writer-fence meaning at the authoritative location; and
- protection against treating a diagnostic copy as current native state.

The design must preserve these guarantees or replace each with an equally explicit proof.

### 0B — Inventory API restore evidence

Jointly map what API can prove before calling SBE:

- exact checkpoint database identity and generation;
- archive SHA-256, byte size, storage receipt, and compatibility identity;
- recorded logical restore path/root identity;
- target directory isolation and freshness;
- archive extraction limits and member validation; and
- relationship among API run/job, native run, and checkpoint.

This is source and fixture inspection only. No R2 read is authorized.

### 0C — Design explicit relocation authority

Do not add a general `ignore_path` or `skip_validation` flag. Define an exact, canonical relocation authority or assessment context that binds at minimum:

- operation fixed to read-only operator-disposition assessment;
- native run ID;
- original logical workspace-root identity or digest;
- restored physical-root identity or digest, without publishing raw paths;
- checkpoint generation and checkpoint/archive digest;
- compatibility identity;
- caller request identity and bounded freshness where appropriate;
- assertions that provider I/O and workspace mutation are forbidden; and
- canonical authority digest.

Decide whether this authority is supplied as a validated document, an API-created context object, or through an installed public reader dedicated to relocated assessment. It must not be inferable merely because the current path differs.

### 0D — Define relocated validation

The relocated reader must still prove:

- `run.json` and snapshot schema validity;
- snapshot member inventory and member digests;
- snapshot logical root equals the authority's original logical root;
- actual restored root differs only under explicit relocation authority;
- checkpoint/archive and compatibility evidence join the authority;
- native run identity matches exactly;
- no writer or mutable execution claim is manufactured at the restored path; and
- bytes remain unchanged throughout assessment.

The assessment should record that its evidence view was relocated, along with safe digests sufficient for audit. Whether this requires an additive assessment schema version or an additive evidence field must be decided explicitly; do not silently change v1 meaning.

### 0E — Capability fence

Prove structurally that relocation authority cannot be reused by:

- semantic-closure resume;
- provider reconciliation or dispatch;
- local native work consumption;
- checkpoint, result, or receipt publication;
- retirement or cooperative suspension mutation;
- latest-result discovery; or
- ordinary lifecycle writers.

The simplest acceptable implementation may be a separate read-only public entrypoint rather than weakening shared workspace validation.

### 0F — Provider-free qualification design

Plan tests for:

- original-path assessment remains valid and unchanged;
- exact relocated assessment succeeds for permitted, prohibited, and native-prior-action fixtures;
- missing, wrong-run, wrong-root, wrong-checkpoint, wrong-generation, wrong-archive, incompatible, expired, duplicate-conflicting, and digest-corrupt authority fail closed;
- relocated bytes changed before or during assessment fail closed;
- no lock, snapshot, state, result, receipt, or other workspace member is created or changed;
- provider/network/spend counters remain zero;
- logs contain safe fingerprints and relocation classifications but no raw paths; and
- every executable/mutating command continues to reject the relocated workspace.

At least one installed-wheel API consumer test must use API's real checkpoint-restore shape and SBE's real reader. Fake restore plus fake assessment is insufficient.

## Required Slice 0 conclusion

Pause for SBE/API/owner review with:

1. the exact relocation authority shape;
2. schema-versioning decision;
3. original-path invariants preserved;
4. explicit capability exclusions;
5. failure and privacy matrix;
6. API/SBE ownership split; and
7. proposed provider-free cross-package gate.

## Later slices, not yet authorized

After Slice 0 review, likely work separates into:

- additive relocated assessment implementation and fixtures;
- API installed-wheel integration and host logging initialization;
- assessed quarantine qualification;
- cooperative native suspension at safe lifecycle boundaries; and
- API-owned force containment/hard-stop behavior that never claims clean native custody without evidence.

Read-only relocation solves assessment availability only. It does not itself quarantine, suspend, terminate, release capacity, or settle provider custody.

## Exit gate

Stop after the design and provider-free test plan. Implementation requires explicit review approval.
